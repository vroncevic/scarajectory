# SCARAjectory Domain Model Architecture & SOLID Audit

This document outlines the architectural analysis of the `scarajectory.core.model` layer, identifying violations of SOLID principles, Clean Architecture boundary rules, and responsibilities distribution. It directly complements [`service_issues.md`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/service_issues.md) and [`infrastructure_issues.md`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/infrastructure_issues.md).

---

## Relationship Across Models, Services, and Infrastructure

In Clean / Hexagonal Architecture, domain models represent core entities and invariants, application services orchestrate use cases, and infrastructure adapts presentation, communication, and storage:

```
+-----------------------------------------------------------------------------------+
|                        INFRASTRUCTURE ISSUES (Adapters)                           |
|  Item I1: [RESOLVED] GUI bypasses Service facade & breaks Law of Demeter          |
|  Item I2: [RESOLVED] GUI widgets perform direct disk I/O & instantiate services   |
|  Item I3: [RESOLVED] Presentation layer formats ASCII hardware commands           |
|  Item I4: [RESOLVED] Hardcoded kinematics & geometry in GUI canvas renderers      |
|  Item I5: [RESOLVED] Presentation models leaked into domain core (M1 mirror)      |
|  Item I6: [RESOLVED] Thread safety risk: background threads mutate Tkinter UI     |
|  Item I7: [RESOLVED] Coarse imports & missing contracts across GUI components     |
|  Item I8: [RESOLVED] God-Component decomposition (DslTab, StreamerTab, Canvas)    |
|  Item I9: [RESOLVED] CanvasRenderer granular decomposition                         |
|  Item I10-I12: [RESOLVED] GUI subpackaging, EmulatorLauncher, Highlighter DRY      |
|  Item I13: [RESOLVED] Decompose DslEditorTab (Catalog & Dialogs)                   |
|  Item C1-C7: [RESOLVED] Communication subsystem refactored (Transports, Formatter)|
|  Item C8: [RESOLVED] ISP & Separation of RobotController from Streamer             |
|  Item C9: [RESOLVED] Decompose TrajectoryStreamer Worker Thread (SRP)             |
+-----------------------------------------------------------------------------------+
                                    ▲
                                    │ (Drives / Observes)
                                    ▼
+-----------------------------------------------------------------------------------+
|                          APPLICATION SERVICE ISSUES                               |
|  Item 1: [RESOLVED] TrajectoryValidator mixes IK math, bounds & metrics reporting |
|  Item 2: [RESOLVED] Service facade leaks collaborators & mutates plan             |
|  Item 3: [RESOLVED] PlanStorageService is an empty pass-through                   |
|  Item 4: [RESOLVED] ScaraCompiler is modularized                                  |
|  Item 5: [RESOLVED] ScaraDslService has decoupled collaborator interfaces         |
|  Item 6: [RESOLVED] Service subpackaging (kinematics, communication, dsl)        |
|  Item 7: [RESOLVED] Fat Service Interface & ISP Segregation in IService           |
|  Item 8-9: [RESOLVED] DSL pipeline subpackages & ISP in IScaraDslService           |
|  Item 10: [RESOLVED] Decompose ScaraCompiler into Command Handlers             |
|  Item 11: [RESOLVED] Decompose ScaraLinter into Rule Strategy Pattern          |
+-----------------------------------------------------------------------------------+
                                    ▲
                                    │ (Orchestrates)
                                    ▼
+-----------------------------------------------------------------------------------+
|                            DOMAIN MODEL ISSUES                                    |
|  Item M1: [RESOLVED] GUI / Canvas models leaked into core/model                   |
|  Item M2: [RESOLVED] Disk I/O inside TrajectorySerializer                         |
|  Item M3: [RESOLVED] Firmware ASCII protocol leaked into Waypoint & Metrics       |
|  Item M4: [RESOLVED] Point vs Waypoint Canonical Consolidation                    |
|  Item M5: [RESOLVED] UI selection & undo/redo mixed into TrajectoryPlan           |
|  Item M6: [RESOLVED] Physical link geometry bundled with operational limits       |
|  Item M7: [RESOLVED] Core Domain Subpackaging (kinematics, trajectory)            |
|  Item M8: [RESOLVED] Interface Segregation for ITrajectoryPlan                     |
|  Item M9: [RESOLVED] DSL Model Subpackaging (token, ast, diagnostic)              |
+-----------------------------------------------------------------------------------+
```

---

## Item M1: [RESOLVED] GUI / Presentation Models Leaked into Domain Layer (`core/model`)

* **Original Files:**
  * `scarajectory/core/model/canvas_settings.py`
  * `scarajectory/core/model/canvas_tool_mode.py`
  * `scarajectory/core/model/canvas_interaction_state.py`
  * `scarajectory/core/model/viewport_transform.py`
* **Destination:** [`scarajectory/infrastructure/gui/model/`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/infrastructure/gui/model/)
* **Principles Violated:** Clean Architecture Boundary Rule, Separation of Concerns.

### Resolution Summary: 🟢 RESOLVED
All 4 presentation classes were completely relocated to `scarajectory/infrastructure/gui/model/` and purged from `core/model/`. GUI consumers import strictly from the GUI model package. Unit tests were migrated to `tests/canvas_interaction_state_test.py` and `tests/viewport_transform_test.py`.

---

## Item M2: [RESOLVED] Disk Filesystem I/O within Domain Model (`TrajectorySerializer`)

* **File:** [`scarajectory/core/model/trajectory_serializer.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/model/trajectory_serializer.py)
* **Storage Adapter:** [`scarajectory/infrastructure/storage/plan_storage_service.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/infrastructure/storage/plan_storage_service.py)
* **Principles Violated:** Clean Architecture Layers, Single Responsibility Principle (SRP).

### Resolution Summary: 🟢 RESOLVED
`TrajectorySerializer` was refactored into a pure in-memory JSON serializer (`to_json(waypoints) -> str` and `from_json(json_str) -> list[Waypoint]`). All side-effecting disk I/O, file reading/writing, and error handling were moved to `PlanStorageService` in the infrastructure storage adapter.

---

## Item M3: [RESOLVED] Firmware Protocol Formatting Leaked into Domain Entities

* **Files:**
  * [`scarajectory/core/model/waypoint.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/model/waypoint.py)
  * [`scarajectory/core/model/trajectory_metrics.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/model/trajectory_metrics.py)
* **Protocol Formatter:** [`scarajectory/infrastructure/communication/protocol/motion_command_formatter.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/infrastructure/communication/protocol/motion_command_formatter.py)
* **Principles Violated:** Single Responsibility Principle (SRP), Separation of Concerns.

### Resolution Summary: 🟢 RESOLVED
`Waypoint.to_ascii_packet()` and `TrajectoryMetrics.to_ascii_program()` were removed from domain models. Wire ASCII packet generation (`<pt#...#end>`, `<CMD:ENABLE>`) is strictly encapsulated in `MotionCommandFormatter`.

---

## Item M4: [RESOLVED] Redundant Duplicate Entities (`Point` vs. `Waypoint`)

* **Files:**
  * [`scarajectory/core/model/waypoint.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/model/waypoint.py)
  * [`scarajectory/core/service/itrajectory_validator.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/service/itrajectory_validator.py)
  * [`scarajectory/core/service/trajectory_validator.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/service/trajectory_validator.py)
* **Principles Violated:** DRY (Don't Repeat Yourself), Interface Segregation, Unnecessary Allocation Overhead.

### Resolution Summary: 🟢 RESOLVED
1. `Point` entity was completely eliminated from `scarajectory/core/model/point.py`.
2. `Waypoint` is the sole canonical domain entity representing 4-DOF motion targets throughout the entire codebase.
3. `to_dto()` and `from_dto()` methods were removed from `Waypoint`.
4. `TrajectoryValidator.validate_point` and `ITrajectoryValidator.validate_point` strictly accept `point: Waypoint`.
5. All test suites and Sphinx documentation were updated with zero warnings.

---

## Item M5: [RESOLVED] UI Selection, Observers, and Undo/Redo Mixed into Domain Aggregate (`TrajectoryPlan`)

* **Files:**
  * [`scarajectory/core/model/trajectory_plan.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/model/trajectory_plan.py)
  * [`scarajectory/core/model/itrajectory_plan.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/model/itrajectory_plan.py)
  * [`scarajectory/infrastructure/gui/gui_event_mediator.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/infrastructure/gui/gui_event_mediator.py)
* **Principles Violated:** Single Responsibility Principle (SRP), Separation of Concerns.

### Resolution Summary: 🟢 RESOLVED
Presentation state (selected waypoint index) and UI observer dispatching (`ITrajectoryObserver` notifications to `TrajectoryCanvas` and `WaypointEditor`) were decoupled from `TrajectoryPlan` and transferred to [`GuiEventMediator`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/infrastructure/gui/gui_event_mediator.py). `TrajectoryPlan` maintains pure domain collection semantics and undo/redo snapshots.

---

## Item M6: [RESOLVED] Physical Geometry Bundled with Operational Limits (`ScaraBounds`)

* **Files:**
  * [`scarajectory/core/model/scara_bounds.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/model/scara_bounds.py)
  * [`scarajectory/core/service/kinematics/kinematics_service.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/service/kinematics/kinematics_service.py)
* **Principles Violated:** Separation of Concerns.

### Resolution Summary: 🟢 RESOLVED
Kinematics math, forward/inverse geometry solvers, and workspace reach calculations were extracted to `KinematicsService`. `ScaraBounds` acts as the configuration parameter model loaded from `scara_geometry.json`.

---

## Item M7: [RESOLVED] Domain Subpackaging in `core/model` and `core/service`

* **Packages:** `scarajectory/core/model`, `scarajectory/core/service`
* **Hierarchy:**
  * `core/model/kinematics/`: `scara_bounds.py`
  * `core/model/trajectory/`: `waypoint.py`, `trajectory_plan.py`, `itrajectory_plan.py`, `trajectory_metrics.py`, `trajectory_serializer.py`, `plan_history.py`, `validation_result.py`
  * `core/service/trajectory/`: `trajectory_validator.py`, `itrajectory_validator.py`, `iplan_storage_service.py`, `itrajectory_observer.py`

### Resolution Summary: 🟢 RESOLVED
1. Subpackages created with clean metadata-only `__init__.py` (zero `__all__` or re-exports).
2. All 50 consuming files across models, services, infrastructure adapters, and tests updated to granular import paths.
3. Sphinx documentation structure updated and rebuilt with 0 warnings.
4. Rule explicitly added to global agent guidelines prohibiting `__all__` and re-exports in package `__init__.py`.

---

## Item M8: [RESOLVED] Interface Segregation Violation in `ITrajectoryPlan`

* **Files:**
  * [`scarajectory/core/model/trajectory/itrajectory_read_only.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/model/trajectory/itrajectory_read_only.py)
  * [`scarajectory/core/model/trajectory/itrajectory_mutable.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/model/trajectory/itrajectory_mutable.py)
  * [`scarajectory/core/model/trajectory/itrajectory_history.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/model/trajectory/itrajectory_history.py)
  * [`scarajectory/core/model/trajectory/itrajectory_plan.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/model/trajectory/itrajectory_plan.py)

### Resolution Summary: 🟢 RESOLVED
* Segregated `ITrajectoryPlan` into 4 dedicated, focused role interfaces across separate module files:
  1. `ITrajectoryReadOnly`: Read-only sequence view (`waypoints: Sequence[Waypoint]`, `count: int`).
  2. `ITrajectoryMutable`: Authoring mutation methods (`add_point`, `insert_point`, `remove_point`, `clear`, `set_waypoints`, `update_point`).
  3. `ITrajectoryHistory`: Undo and redo operations (`undo`, `redo`).
  4. `ITrajectoryPlan`: Clean composite protocol inheriting the 3 role protocols.
* Strictly satisfies "one interface per module file" with 100% granular imports and zero `__all__` in `__init__.py`.

---

## Item M9: [RESOLVED] Domain Subpackaging in `core/model/dsl`

* **Package:** `scarajectory/core/model/dsl/`
* **Original Structure:** 9 files flat in `core/model/dsl/` mixing tokens, AST nodes, and diagnostic models.
* **Principles Violated:** Cohesion & Single Responsibility Principle at the package level.

### Identified Subdomains:
1. **Token Domain (`core/model/dsl/token/`):**
   * [`scara_token.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/model/dsl/token/scara_token.py) (`ScaraToken`)
   * [`scara_token_type.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/model/dsl/token/scara_token_type.py) (`ScaraTokenType`)
2. **AST & Instruction Domain (`core/model/dsl/ast/`):**
   * [`scara_command_type.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/model/dsl/ast/scara_command_type.py) (`ScaraCommandType`)
   * [`scara_instruction.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/model/dsl/ast/scara_instruction.py) (`ScaraInstruction`)
   * [`iscara_instruction.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/model/dsl/ast/iscara_instruction.py) (`IScaraInstruction`)
   * [`scara_program.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/model/dsl/ast/scara_program.py) (`ScaraProgram`)
   * [`iscara_program.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/model/dsl/ast/iscara_program.py) (`IScaraProgram`)
3. **Diagnostic Domain (`core/model/dsl/diagnostic/`):**
   * [`scara_diagnostic.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/model/dsl/diagnostic/scara_diagnostic.py) (`ScaraDiagnostic`)
   * [`scara_diagnostic_severity.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/model/dsl/diagnostic/scara_diagnostic_severity.py) (`ScaraDiagnosticSeverity`)

### Execution Plan (Phase 9):
* [x] **Step 9.1:** Create `scarajectory/core/model/dsl/token/`, `scarajectory/core/model/dsl/ast/`, and `scarajectory/core/model/dsl/diagnostic/` with clean metadata-only `__init__.py` files (0 `__all__`).
* [x] **Step 9.2:** Relocate token models (`scara_token.py`, `scara_token_type.py`) to `token/`.
* [x] **Step 9.3:** Relocate AST models (`scara_command_type.py`, `scara_instruction.py`, `iscara_instruction.py`, `scara_program.py`, `iscara_program.py`) to `ast/`.
* [x] **Step 9.4:** Relocate diagnostic models (`scara_diagnostic.py`, `scara_diagnostic_severity.py`) to `diagnostic/`.
* [x] **Step 9.5:** Update all consuming imports across compiler, parsers, linters, services, GUI, and tests.

---

### Item M10: [RESOLVED] TrajectoryPlan Redundant Method Elimination & SRP Hardening

* **Files:**
  * [`scarajectory/core/model/trajectory/trajectory_plan.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/model/trajectory/trajectory_plan.py)
  * [`scarajectory/core/model/trajectory/itrajectory_plan.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/model/trajectory/itrajectory_plan.py)
* **Principles Violated:** Single Responsibility Principle (SRP), Don't Repeat Yourself (DRY).

#### Resolution Summary: 🟢 RESOLVED
Eliminated duplicate alias method `select_point(self, index: int)` from `TrajectoryPlan` and `ITrajectoryPlan` in favor of canonical `set_selected_index(self, index: int)`. Reduced `TrajectoryPlan` method count from 16 to exactly 15 methods, bringing the domain entity into full compliance with the automated SRP quality gate (`srp_checker.py`).

---

## Master Roadmap Matrix (Phases 1 – 11)

| Phase | Service Issues | Model Issues | Infrastructure Issues | Scope & Deliverables | Status |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **Phase 1** | **Item 1** (`TrajectoryValidator`) | **Item M6** (`ScaraGeometry`) | **Item I4** (Canvas reach) | Kinematics abstraction & dynamic canvas | 🟢 **DONE** |
| **Phase 2** | **Item 3** (`PlanStorageService`) | **Item M2** (Disk I/O from serializer) | **Item I2** (Remove `open()` from UI) | In-memory serializer & storage adapter | 🟢 **DONE** |
| **Phase 3** | **Item 2** (`Service` facade) | **Item M3** (ASCII protocol from domain) | **Items C1–C7, I3** (Hardware comms) | Full communication refactor & semantic robot API | 🟢 **DONE** |
| **Phase 4** | — | **Item M1** (Move Canvas models) | **Item I5** (Create GUI model package) | Presentation models relocated to `gui/model` | 🟢 **DONE** |
| **Phase 5** | **Item 2** (`Service` facade) | **Item M5** (Plan UI decoupling) | **Items I1, I6, I8** (Demeter, thread safety) | Thread safety, `GuiEventMediator`, GUI decomposition | 🟢 **DONE** |
| **Phase 6** | **Item 4, Item 5** (DSL compiler) | — | **Item I2** (DSL injection) | DSL pipeline modularization & macro expanders | 🟢 **DONE** |
| **Phase 7** | — | **Items M4, M7** (Point vs Waypoint & Subpackages) | **Item I7** (Imports polish) | **Canonical Entity Consolidation & Subpackaging** | 🟢 **DONE** |
| **Phase 8** | **Item 7** (ISP on `IService`) | **Item M8** (ISP on `ITrajectoryPlan`) | **Items C8, I9** (Split Streamer & CanvasRenderer) | **Interface Segregation (ISP) & Component Separation** | 🟢 **DONE** |
| **Phase 9** | **Items 8, 9** (DSL Pipeline Subpackages & ISP) | **Item M9** (DSL Model Subpackages) | **Items I10–I12** (GUI Subpackaging, Launcher, DRY) | **DSL Subsystem Deep Modularization & Architecture Hardening** | 🟢 **DONE** |
| **Phase 10** | **Items 10, 11** (`ScaraCompiler`, `ScaraLinter`) | — | **Items I13, C9** (`DslEditorTab`, `StreamerWorker`) | **Granular Decomposition of God-Modules into Collaborators** | 🟢 **100% DONE** |
| **Phase 11** | **Item 12** (`ParserCommands`) | **Item M10** (`TrajectoryPlan` SRP) | **Items C10, I14–I16** (`StreamerISP`, `Canvas`, `Progress`, `GuiPackages`) | **Parser & GUI Subpackaging, Passthrough Elimination, Quality Gates Hardening** | 🟢 **100% DONE** |




