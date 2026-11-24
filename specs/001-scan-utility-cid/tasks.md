# Tasks: Scan Utility CiD

**Input**: Design documents from `specs/001-scan-utility-cid/` (`spec.md`, `plan.md`)  
**Prerequisites**: `constitution.md`, `spec.md`, `plan.md`

## Phase 1: Setup & Ambiente (Shared Infrastructure)

- [x] T001 Estruturar projeto desacoplado em `backend/`, `frontend/`, `tests/` e `reports/`
- [x] T002 Definir dependências em `requirements.txt` (`flet==1.0.4`, `flet-desktop==1.0.4`, `httpx`, `reportlab`, `pyinstaller`)
- [x] T003 Criar ambiente virtual `.venv` e instalar dependências de `requirements.txt` para execução local e testes

---

## Phase 2: Foundational (Modelos e Utilitários de Rede)

- [x] T004 [P] Implementar dataclasses `ControlIdDevice`, `ScanSummary` e `DocumentMetadata` em `backend/models/device.py`
- [x] T005 [P] Implementar detecção de IP local e cálculo/validação CIDR em `backend/core/network_utils.py`
- [x] T006 [P] Implementar resolução de MAC via Win32 `SendARP` sem privilégios de admin em `backend/core/arp_helper.py`

---

## Phase 3: User Story 1 - Varredura Sob Demanda e Detecção de Rede (Priority: P1)

- [x] T007 [US1] Implementar orquestrador assíncrono `NetworkScanner` com `asyncio.Semaphore(50)` e cancelamento gracioso em `backend/core/scanner.py`
- [x] T008 [US1] Implementar controles de sub-rede (AUTO/MANUAL), credenciais e botões Iniciar/Cancelar em `frontend/components/controls.py`
- [x] T009 [US1] Integrar eventos assíncronos, barra de progresso e KPIs em tempo real em `frontend/app.py` e `frontend/components/kpi_cards.py`

---

## Phase 4: User Story 2 - Identificação de Modelos e Topologia de Catracas (Priority: P1)

- [x] T010 [US2] Implementar sondagem em cascata e autenticação (`/login.fcgi` / `/logout.fcgi`) em `backend/core/detector.py`
- [x] T011 [US2] Implementar agrupamento hierárquico de catracas e leitores (`Entrada`/`Saída`) em `backend/services/turnstile_linker.py`
- [x] T012 [US2] Exibir tabela hierárquica com recuo e badges `[Entrada]`/`[Saída]` em `frontend/components/device_table.py`

---

## Phase 5: User Story 3 - Exportação de Relatórios e Documento Técnico PDF (Priority: P2)

- [x] T013 [US3] Implementar exportação CSV (UTF-8 BOM) e JSON + atalho para pasta `reports/` em `backend/services/report_service.py`
- [x] T014 [US3] Implementar geração do Documento Técnico PDF (ReportLab) em `backend/services/document_service.py`
- [x] T015 [US3] Implementar formulário de metadados do cliente/técnico em `frontend/components/client_form.py`

---

## Phase 6: Verificação, Testes e Empacotamento Windows

- [x] T016 [P] Implementar servidor mock e suíte de testes (`tests/mock_control_id_server.py`, `test_backend.py`, `test_scanner.py`, `test_document.py`, `test_e2e.py`)
- [x] T017 Configurar empacotamento PyInstaller e assinatura Authenticode em `build.ps1`
- [x] T018 Executar a suíte completa de testes em `tests/` no ambiente `.venv` e validar 100% de aprovação
