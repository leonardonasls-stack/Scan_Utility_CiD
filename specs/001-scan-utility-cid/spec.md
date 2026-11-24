# Feature Specification: Scan Utility CiD

**Feature Branch**: `001-scan-utility-cid`  
**Created**: 2026-11-23  
**Status**: Baseline (Atualizado conforme código atual)  
**Input**: Baseado no código atual do projeto e nos documentos de referência em `AGENTS/` (`PRD.md` e `TRD.md`).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Varredura Sob Demanda e Detecção de Rede (Priority: P1)
O técnico de campo abre o aplicativo desktop e inicia uma varredura sob demanda na rede local (detectando automaticamente o IP/CIDR da interface ativa ou informando uma faixa manualmente) para descobrir equipamentos Control iD sem bloquear a interface.

**Why this priority**: É a função central do utilitário; sem ela não há inventário nem geração de relatórios.

**Independent Test**: Pode ser testado executando `NetworkScanner` contra `tests/mock_control_id_server.py` e validando detecção, cancelamento gracioso e métricas em `ScanSummary`.

**Acceptance Scenarios**:
1. **Given** uma sub-rede válida (modo AUTO ou MANUAL), **When** o usuário inicia a varredura, **Then** o sistema varre os hosts com pool assíncrono (50 workers) e atualiza a tabela e os KPIs em tempo real.
2. **Given** uma varredura em andamento, **When** o usuário aciona cancelar, **Then** todas as tarefas pendentes são interrompidas graciosamente sem travar a UI.

---

### User Story 2 - Identificação de Modelos, Autenticação e Topologia de Catracas (Priority: P1)
O sistema sonda endpoints embarcados Control iD em cascata, autentica quando necessário, resolve o MAC via Win32 `SendARP` e agrupa leitores escravos às respectivas catracas mestres com direção (`Entrada` / `Saída`) e áreas limpas.

**Why this priority**: Garante inventário técnico preciso para implantação e suporte em campo.

**Independent Test**: Testado via `tests/test_scanner.py` e `tests/test_backend.py` contra o servidor mock e casos de `turnstile_linker`.

**Acceptance Scenarios**:
1. **Given** um equipamento Control iD na rede (iDFace, iDClass, iDAccess, iDFlex, iDBlock, iDBlock PNE, etc.), **When** a sonda executa em cascata (`/system_information.fcgi`, `/api/system/information`, `/login.fcgi`, `/`), **Then** extrai IP, MAC, serial, modelo, firmware e latência, descartando silenciosamente hosts não Control iD.
2. **Given** leitores faciais vinculados a uma catraca mestre no iDSecure, **When** `turnstile_linker` processa os dispositivos, **Then** agrupa hierarquicamente os leitores sob a catraca com badges `[Entrada]` / `[Saída]` e remove áreas genéricas órfãs.

---

### User Story 3 - Exportação de Relatórios (CSV, JSON) e Documento Técnico PDF (Priority: P2)
O usuário preenche os dados do cliente/técnico (`client_form.py`) e exporta o inventário em CSV (`;` UTF-8 BOM), JSON estruturado ou Documento Técnico em PDF (ReportLab) com hierarquia, KPIs e atalho para abrir a pasta `reports/`.

**Why this priority**: Entrega o artefato final exigido pelo cliente e pela equipe técnica.

**Independent Test**: Validado via `tests/test_document.py` e `tests/test_backend.py` verificando geração de arquivos em `reports/`.

**Acceptance Scenarios**:
1. **Given** uma varredura concluída e metadados preenchidos, **When** o usuário exporta CSV, JSON ou PDF, **Then** os arquivos são salvos em `reports/` preservando a hierarquia de catracas e leitores.

## Requirements *(mandatory)*

### Functional Requirements
- **FR-001**: Detectar automaticamente IP local e sub-rede CIDR ativa (`backend/core/network_utils.py`) e permitir edição manual.
- **FR-002**: Executar varredura assíncrona sob demanda com pool de 50 workers (`backend/core/scanner.py`) e cancelamento gracioso.
- **FR-003**: Sondar equipamentos Control iD em cascata com autenticação automática configurável (`backend/core/detector.py`).
- **FR-004**: Resolver endereços MAC via Win32 `iphlpapi.SendARP` sem exigir privilégios de administrador (`backend/core/arp_helper.py`).
- **FR-005**: Agrupar catracas e leitores subordinados com direção e filtragem de áreas (`backend/services/turnstile_linker.py`).
- **FR-006**: Exportar inventário em CSV, JSON (`backend/services/report_service.py`) e PDF técnico (`backend/services/document_service.py`).
- **FR-007**: Exibir interface desktop Dark Mode em Flet (`frontend/app.py`) com KPIs, tabela hierárquica, progresso em tempo real e formulário de cliente.

### Key Entities
- `ControlIdDevice` (`backend/models/device.py`): Representa cada equipamento identificado (IP, MAC, serial, modelo, firmware, latência, área, direção, vínculo).
- `ScanSummary` (`backend/models/device.py`): Consolida totais da varredura, tempo decorrido e lista de dispositivos.
- `DocumentMetadata` (`backend/models/device.py`): Metadados do cliente, técnico e local para o PDF.
