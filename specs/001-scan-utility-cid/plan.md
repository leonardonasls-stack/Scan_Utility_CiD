# Implementation Plan: Scan Utility CiD

**Branch**: `001-scan-utility-cid` | **Date**: 2026-11-23 | **Spec**: [spec.md](file:///d:/projetos/Scan_Utility_CiD/specs/001-scan-utility-cid/spec.md)  
**Input**: Arquitetura real do código-fonte atual, `requirements.txt`, `build.ps1` e `AGENTS/TRD.md` (atualizado para refletir as evoluções implementadas).

## Summary

O **Scan Utility CiD** é uma aplicação desktop Windows em Python 3.10+ com arquitetura desacoplada em duas camadas: **Backend** assíncrono (`httpx` + `asyncio` + Win32 `SendARP` + ReportLab) e **Frontend** reativo em **Flet** (`flet==1.0.4`, `flet-desktop==1.0.4`, Dark Mode). Em relação ao `AGENTS/TRD.md` original, o projeto evoluiu para incluir o serviço `turnstile_linker.py` (hierarquia de catracas e direção Entrada/Saída), `document_service.py` (PDF técnico via ReportLab), `client_form.py` na UI e empacotamento standalone via `build.ps1` com assinatura Authenticode (LLSystem).

## Technical Context

**Language/Version**: Python 3.10+  
**Primary Dependencies**: `flet==1.0.4`, `flet-desktop==1.0.4`, `httpx>=0.27.0,<1.0.0`, `reportlab>=5.0.1,<6.0.0`, `pyinstaller>=6.5.0,<7.0.0`  
**Storage**: Arquivos locais em `reports/` (CSV UTF-8 BOM, JSON, PDF)  
**Testing**: `unittest` / `pytest` com `tests/mock_control_id_server.py` (`test_backend.py`, `test_scanner.py`, `test_document.py`, `test_e2e.py`)  
**Target Platform**: Windows Desktop (execução local e `.exe` PyInstaller assinado)  
**Project Type**: Desktop application (Backend + Flet UI)  
**Performance Goals**: Varredura de bloco `/24` (254 hosts) em < 20s com pool de 50 workers assíncronos; UI fluida sem congelamento.  
**Constraints**: Sem exigência de privilégios de administrador para `SendARP`; descarte silencioso de hosts não Control iD.

## Constitution Check

*GATE: Verificado contra [constitution.md](file:///d:/projetos/Scan_Utility_CiD/.specify/memory/constitution.md).*

- **I. Desacoplamento Frontend / Backend**: PASS — `backend/` não importa `flet` nem módulos de `frontend/`.
- **II. Assincronismo e Fluidez**: PASS — `NetworkScanner` usa `asyncio.Semaphore(50)` e `httpx.AsyncClient`.
- **III. Modelos Tipados**: PASS — `ControlIdDevice`, `ScanSummary` e `DocumentMetadata` em `backend/models/device.py`.
- **IV. Testes com Mock Server**: PASS (estrutural) — suíte em `tests/` pronta; pendente apenas criação de `.venv` e instalação de `requirements.txt` no ambiente local.
- **V. Empacotamento Windows**: PASS — `build.ps1` e certificado `LLSystem-CodeSigning.cer` configurados.

## Project Structure

### Documentation (this feature)

```text
specs/001-scan-utility-cid/
├── spec.md              # Especificação baseline alinhada ao código atual
└── plan.md              # Este plano técnico atualizado
```

### Source Code (repository root)

```text
backend/
├── core/
│   ├── arp_helper.py        # Resolução de MAC via Win32 SendARP (ctypes)
│   ├── detector.py          # Sonda em cascata, login/logout e parser Control iD
│   ├── network_utils.py     # Detecção de IP local e validação/cálculo CIDR
│   └── scanner.py           # Orquestrador assíncrono (NetworkScanner, 50 workers)
├── models/
│   └── device.py            # Dataclasses ControlIdDevice, ScanSummary, DocumentMetadata
└── services/
    ├── document_service.py  # Geração de PDF técnico (ReportLab)
    ├── report_service.py    # Exportação CSV (UTF-8 BOM) e JSON + abrir pasta
    └── turnstile_linker.py  # Agrupamento hierárquico catraca/leitores e direção

frontend/
├── app.py                   # Controlador principal Flet e ciclo de eventos
├── components/
│   ├── client_form.py       # Formulário de metadados do cliente/técnico
│   ├── controls.py          # CIDR (AUTO/MANUAL), credenciais e Iniciar/Cancelar
│   ├── device_table.py      # Tabela hierárquica com badges Entrada/Saída
│   ├── header.py            # Topbar do Scan Utility CiD
│   └── kpi_cards.py         # Cards de KPI em tempo real
└── styles/
    └── theme.py             # Tokens de design Dark Mode

tests/
├── mock_control_id_server.py
├── test_backend.py
├── test_document.py
├── test_e2e.py
└── test_scanner.py
```

## Complexity Tracking

Nenhuma violação da Constitution identificada.
