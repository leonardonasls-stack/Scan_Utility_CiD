# Scan Utility CiD Constitution

## Core Principles

### I. Desacoplamento Frontend / Backend
A camada de serviços e rede (`backend/`) deve permanecer **100% isolada** da camada visual (`frontend/` em Flet). Toda comunicação entre interface e motor de varredura ocorre por eventos assíncronos e callbacks, sem acoplamento de widgets ou estado de UI no backend.

### II. Assincronismo e Fluidez da Interface
Operações de rede (varredura de sub-redes, sondagem HTTP/FCGI e resolução ARP) devem ser executadas de forma assíncrona (`asyncio`, `httpx.AsyncClient`, `asyncio.Semaphore` com pool de 50 workers), garantindo cancelamento gracioso e evitando qualquer bloqueio da thread principal da UI desktop.

### III. Modelos Imutáveis e Dados Tipados
Os dados coletados e consolidados devem trafegar por dataclasses bem definidas em `backend/models/device.py` (`ControlIdDevice`, `ScanSummary`, `DocumentMetadata`), com normalização consistente entre diferentes linhas de equipamentos Control iD (iDFace, iDClass, iDAccess, iDFlex, iDBlock, etc.).

### IV. Testes com Mock Server e Cobertura por Camadas
Nenhuma alteração crítica no motor de detecção, topologia (`turnstile_linker`) ou geração de relatórios/PDF deve depender exclusivamente de hardware físico. Toda validação automatizada deve utilizar `tests/mock_control_id_server.py` e cobrir testes unitários, de integração e ponta a ponta (`tests/test_backend.py`, `test_scanner.py`, `test_document.py`, `test_e2e.py`).

### V. Simplicidade, Segurança e Empacotamento Windows
A resolução de MAC via Win32 (`iphlpapi.SendARP` via `ctypes`) não deve exigir privilégios de administrador. Hosts não Control iD ou inalcançáveis devem ser descartados silenciosamente. O empacotamento final para distribuição Windows deve seguir o fluxo `build.ps1` (PyInstaller) com assinatura digital Authenticode (LLSystem).

## Stack & Restrições Técnicas

- **Linguagem:** Python 3.10+
- **UI Desktop:** Flet (Flutter Engine, Material Design 3, Dark Mode)
- **Rede / HTTP:** `httpx` assíncrono + Win32 `SendARP`
- **Relatórios:** CSV (`;` com UTF-8 BOM), JSON estruturado e PDF técnico via ReportLab
- **Plataforma Alvo:** Windows (com suporte a execução local e `.exe` empacotado)

## Fluxo de Desenvolvimento e Qualidade

- Especificações de referência do projeto residem em `AGENTS/` (`PRD.md`, `TRD.md`, `API_SPEC.md`, `FRONTEND_SPEC.md`, `TEST_PLAN.md`, `TASKS.md`).
- Novas funcionalidades ou alterações estruturais devem manter compatibilidade com os contratos definidos e passar na suíte `tests/` antes do build.
- Credenciais padrão (`admin` / `admin`) são configuráveis na interface e nunca devem ser hardcoded como segredos de produção.

## Governance

Esta Constitution rege as decisões arquiteturais e de implementação do projeto **Scan Utility CiD**. Alterações nos princípios acima devem ser documentadas e refletidas nas especificações em `.specify/` e `AGENTS/`.

**Version**: 1.0.0 | **Ratified**: 2026-11-23 | **Last Amended**: 2026-11-23
