import asyncio
import logging
import time
from typing import Callable, List, Optional

import httpx

from backend.core.detector import probe_control_id
from backend.core.network_utils import get_hosts_in_cidr, validate_cidr
from backend.models.device import ControlIdDevice, ScanSummary

logger = logging.getLogger(__name__)


class NetworkScanner:
    """
    Orquestrador assíncrono de varredura de rede com controle
    de concorrência, suporte a credenciais de autenticação e emissão de callbacks.
    """

    def __init__(
        self,
        cidr: str,
        concurrency: int = 50,
        port: int = 80,
        timeout_sec: float = 1.5,
        username: str = "admin",
        password: str = "admin",
        on_progress: Optional[Callable[[int, int, str], None]] = None,
        on_device_found: Optional[Callable[[ControlIdDevice], None]] = None,
    ):
        self.cidr = cidr.strip()
        self.concurrency = concurrency
        self.port = port
        self.timeout_sec = timeout_sec
        self.username = username
        self.password = password
        self.on_progress = on_progress
        self.on_device_found = on_device_found

        self._cancelled = False
        self._is_running = False
        self._workers: list[asyncio.Task] = []

    @property
    def is_running(self) -> bool:
        return self._is_running

    def cancel(self) -> None:
        """Sinaliza interrupção imediata da varredura e cancela workers ativos."""
        self._cancelled = True
        for worker in self._workers:
            if not worker.done():
                worker.cancel()

    async def scan(self) -> ScanSummary:
        """
        Executa a varredura completa da sub-rede especificada.
        Retorna o ScanSummary consolidado.
        """
        if not validate_cidr(self.cidr):
            raise ValueError(f"Formato de CIDR inválido: {self.cidr}")

        hosts = get_hosts_in_cidr(self.cidr)
        total_hosts = len(hosts)
        found_devices: List[ControlIdDevice] = []
        scanned_count = 0
        self._cancelled = False
        self._is_running = True

        start_time = time.perf_counter()

        limits = httpx.Limits(
            max_connections=self.concurrency,
            max_keepalive_connections=self.concurrency
        )
        timeout = httpx.Timeout(self.timeout_sec, connect=self.timeout_sec)

        queue: asyncio.Queue[str] = asyncio.Queue()
        for ip in hosts:
            queue.put_nowait(ip)

        async with httpx.AsyncClient(limits=limits, timeout=timeout) as client:
            async def scan_single_host(ip: str):
                nonlocal scanned_count
                if self._cancelled:
                    return

                device = await probe_control_id(
                    client=client,
                    ip=ip,
                    port=self.port,
                    timeout_sec=self.timeout_sec,
                    username=self.username,
                    password=self.password
                )

                scanned_count += 1
                if device:
                    found_devices.append(device)
                    if self.on_device_found:
                        try:
                            res = self.on_device_found(device)
                            if asyncio.iscoroutine(res):
                                await res
                        except Exception as exc:
                            logger.warning("Erro no callback on_device_found para %s: %s", ip, exc, exc_info=True)

                if self.on_progress:
                    try:
                        res = self.on_progress(scanned_count, total_hosts, ip)
                        if asyncio.iscoroutine(res):
                            await res
                    except Exception as exc:
                        logger.warning("Erro no callback on_progress para %s: %s", ip, exc, exc_info=True)

            async def worker():
                while not self._cancelled:
                    try:
                        ip = queue.get_nowait()
                    except asyncio.QueueEmpty:
                        break
                    try:
                        await scan_single_host(ip)
                    finally:
                        queue.task_done()

            num_workers = min(self.concurrency, len(hosts)) if hosts else 0
            self._workers = [asyncio.create_task(worker()) for _ in range(num_workers)]

            try:
                if self._workers:
                    await asyncio.gather(*self._workers, return_exceptions=True)
            finally:
                self._workers = []
                self._is_running = False

        duration = time.perf_counter() - start_time

        return ScanSummary(
            network_target=self.cidr,
            total_scanned=scanned_count,
            total_found=len(found_devices),
            duration_seconds=duration,
            devices=found_devices
        )
