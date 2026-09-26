# Domain Model Architectural Audit (`model_issues.md`)

This document tracks architectural compliance, SOLID principles, and clean boundary separation for the **Domain Model** layer (`scarajectory/core/model/`).

---

## 🏛️ Domain Model Guiding Principles (Source of Truth)

In clean domain-driven architecture and consistent with project constraints:
1. **SOLID Principles Compliance & Clean Architecture:** Strictly adhere to Single Responsibility (SRP), Open/Closed (OCP), Liskov Substitution (LSP), Interface Segregation (ISP), and Dependency Inversion (DIP). Clean Architecture layer boundaries are strictly maintained: `core/model/` <- `core/service/` <- `infrastructure/`.
2. **Models are 100% Pure Data Objects:** All domain model classes in `core/model/` must be pure immutable data structures (`@dataclass(frozen=True, slots=True, kw_only=True)`). They contain strictly data fields, zero methods, zero behavior, zero algorithmic logic, and zero mutable state.
3. **Zero `None` Policy (Absolute Null-Safety & Explicit Typing):** Never use `| None = None` or default `None` values in models, domain entities, or factory creation methods. All fields and parameters must be 100% explicit and non-nullable. If an attribute represents an empty collection, use immutable empty collections (`()`, `{}`), never `None`.
4. **Factory Hierarchy Rule ("Factory Calls Factory Only"):** A Factory can **ONLY** be called inside another Factory, or inside `main.py` (the top-level composition root / entry point). **A Factory must NEVER be called inside regular classes** (services, compilers, parsers, linters, coordinators, workers, controllers, presenters, GUI widgets). If a class needs to instantiate objects dynamically at runtime, it must receive an abstract factory interface (`@runtime_checkable Protocol`) via constructor dependency injection (e.g. `IWaypointFactory`, `ITrajectoryPlanFactory`, `IInstructionFactory`), or receive pre-built objects created by the parent factory.
5. **Abstract Interfaces Everywhere / Only Factories Work with Created Concrete Instances:** Zero interfaces (`Protocol`) are permitted in `core/model/`. Across the application, all class dependencies and method signatures must be typed as abstract interfaces (`@runtime_checkable Protocol`). **Only factory modules instantiate concrete classes and wire up object graphs.** Concrete implementation classes:
   - Must NOT inherit from Protocol classes.
   - Must NOT import Protocol classes.
   - Must NOT use `@override`.
   - Must NOT be imported by peer domain services or adapters.
   All peer collaborations flow strictly through abstract protocols.
6. **No `@staticmethod`, Strict `@classmethod` Everywhere:** Static methods (`@staticmethod`) are strictly forbidden across the codebase. All factory creation methods, class-level helpers, and builders must be declared as `@classmethod(cls, ...)`.
7. **Zero Interfaces in `core/model/`:** Abstract interfaces (`@runtime_checkable Protocol`) belong exclusively in the service layer (`core/service/`) and infrastructure layer (`infrastructure/`). Never place interfaces or protocols in `core/model/`.
8. **Zero Reverse Dependencies:** `core/model/` is the innermost core layer and must have **zero imports from `core/service/` or `infrastructure/`**.
9. **Relocation of Stateful Aggregates & Interfaces:** Stateful aggregates managing mutation stacks, history, and observer dispatching (such as `TrajectoryPlan` and `ITrajectoryPlan`) belong strictly in `core/service/trajectory/`. In `core/model/trajectory/`, only pure data objects (`Waypoint`, `ValidationResult`) remain.
10. **Small Classes with 2+ Methods & Zero Private Methods Goal:** Non-model classes must be small, cohesive, and have 2+ public methods. Methods must be concise (≤15–25 lines of pure code). Private methods must be minimized or completely eliminated (0 private methods goal) by decomposing responsibilities into dedicated collaborating components.
11. **Pure Dependency Injection (DIP) from Parent Modules:** Collaborators and configurations are always injected from parent callers/factories downwards. Classes never instantiate concrete dependencies or use fallback default initializations.

---

## 📊 Master Status Matrix

| Submodule | Class / Entity | Current State | Audit Status | Violations Identified | Actionable Remediation |
|---|---|---|---|---|---|
| `kinematics/` | `ScaraBounds` | Pure Dataclass | 🟢 RESOLVED | Hardcoded defaults removed; loaded from JSON SSoT via `ScaraConfigLoader` | Pure frozen dataclass with slots, no hardcoded defaults |
| `kinematics/` | `TransmissionParameters` | Pure Dataclass | 🟢 RESOLVED | Kinematic calculation methods and hardcoded defaults removed; loaded from JSON SSoT | Pure frozen dataclass with slots, no hardcoded defaults |
| `communication/protocol/` | `MessageId`, `ErrorCode`, `BinaryFrame`, `JointSteps`, `ToolId` | Protocol Models | 🟢 RESOLVED (MIGRATED TO SCARALANG) | Extracted to `scaralang.core.model.protocol`; duplicate files removed from `scarajectory` | Imported directly from `scaralang` |
| `communication/protocol/` | `ProtocolMode` | StrEnum | 🟢 RESOLVED | Defined in `core/model/communication/protocol/protocol_mode.py` (`ASCII`, `BINARY`) | Pure StrEnum wire protocol mode |
| `communication/protocol/` | `ScaraResponse` | Pure Dataclass | 🟢 RESOLVED | Defined in `core/model/communication/protocol/scara_response.py`; 0 defaults, 0 `None` | Pure frozen dataclass with slots, 0 defaults |
| `communication/event/` | `MoveEvent` | Pure Dataclass | 🟢 RESOLVED | Defined in `core/model/communication/event/move_event.py` for firmware `MSG_RESP_MOVE_EVENT (0x85)` | Pure frozen dataclass with slots, 0 defaults |
| `communication/event/` | `FaultEvent` | Pure Dataclass | 🟢 RESOLVED | Defined in `core/model/communication/event/fault_event.py` for firmware `MSG_RESP_FAULT_EVENT (0x89)` | Pure frozen dataclass with slots, 0 defaults |
| `communication/telemetry/` | `ScaraStatus` | Pure Dataclass | 🟢 RESOLVED | Defined in `core/model/communication/telemetry/scara_status.py`; unpacking in `BinaryFrameParser` | Pure frozen dataclass with slots, 0 defaults |
| `communication/telemetry/` | `DiagnosticsSnapshot` | Pure Dataclass | 🟢 RESOLVED | Defined in `core/model/communication/telemetry/diagnostics_snapshot.py` for `MSG_RESP_DIAGNOSTICS` | Pure frozen dataclass with slots, 0 defaults |
| `communication/telemetry/` | `DiagnosticsBundle` | Pure Dataclass | 🟢 RESOLVED | Defined in `core/model/communication/telemetry/diagnostics_bundle.py` bundling 17 telemetry parameters | Pure frozen dataclass with slots, 0 defaults |
| `communication/stream/` | `StreamConfig` | Pure Dataclass | 🟢 RESOLVED | Defined in `core/model/communication/stream/stream_config.py` with required `protocol_mode` | Pure frozen dataclass with slots, 0 defaults |
| `communication/stream/` | `StreamSession` | Pure Dataclass | 🟢 RESOLVED | Defined in `core/model/communication/stream/stream_session.py`; lifecycle in `StreamSessionFactory` | Pure dataclass with slots, 0 defaults |
| `communication/stream/` | `StreamProgress` | Pure Dataclass | 🟢 RESOLVED | Defined in `core/model/communication/stream/stream_progress.py`; dispatched by `StreamObserverDispatcher` | Pure frozen dataclass with slots, 0 defaults |
| `communication/stream/` | `StreamState` | StrEnum | 🟢 RESOLVED | Defined in `core/model/communication/stream/stream_state.py` | Pure StrEnum streaming lifecycle state |
| `communication/preferences/` | `ConnectionPreference` | Pure Dataclass | 🟢 RESOLVED | Defined in `core/model/communication/preferences/connection_preference.py`; 0 methods, 0 `None` | Pure frozen dataclass with slots, constructed via `ConnectionPreferenceFactory` |
| `communication/` Factories | Domain Factory Services | Architecture Standard | 🟢 RESOLVED | `StreamConfigFactory`, `StreamSessionFactory`, `MoveEventFactory`, `FaultEventFactory`, `DiagnosticsSnapshotFactory`, `ConnectionPreferenceFactory` in `core/service/communication/` | Clean domain service factories |
| `trajectory/` | `ValidationResult` | Pure Dataclass | 🟢 RESOLVED | Default `error_index` removed; pure validation outcome DTO | Pure frozen dataclass with slots, 0 defaults |
| `trajectory/` | `Waypoint` | Pure Dataclass | 🟢 RESOLVED | Distance calculations, dict serialization, and all defaults removed; instantiation defaults moved to `WaypointFactory` | Pure frozen dataclass with slots, 0 methods, 0 defaults |
| `trajectory/` | `WaypointFactory` | Domain Factory Service | 🟢 RESOLVED | Created in `core/service/trajectory/waypoint_factory.py` to isolate waypoint instantiation defaults | Clean service factory placement |
| `trajectory/` | `TrajectoryPlan` | Stateful Observable Aggregate | 🟢 RESOLVED | Relocated to `core/service/trajectory/` with `TrajectoryPlanFactory` and pure DI (`IPlanHistory`); `core/model/` is 100% pure data objects | Relocate to `core/service/trajectory/` with `TrajectoryPlanFactory`; leave `core/model/` 100% pure data objects |
| `trajectory/` | `ITrajectoryPlan` / `ITrajectory*` | Structural Protocols | 🟢 RESOLVED | Relocated all trajectory protocols to `core/service/trajectory/`; 0 interfaces in `core/model/` | Relocate all trajectory protocols to `core/service/trajectory/` |
| `trajectory/` | `PlanHistory` | Domain Service | 🟢 RESOLVED | Relocated to `core/service/trajectory/plan_history.py` | Clean service placement |
| `trajectory/` | `TrajectoryMetrics` | Domain Service | 🟢 RESOLVED | Relocated to `core/service/trajectory/trajectory_metrics.py` | Clean service placement |
| `trajectory/` | `TrajectorySerializer` | Storage Codec | 🟢 RESOLVED | Relocated to `infrastructure/storage/trajectory_serializer.py` | Clean infrastructure placement |
| `dsl/` | All AST, Token, Diagnostic, and Binary Models | Standalone Toolchain | 🟢 RESOLVED (MIGRATED TO SCARALANG) | Extracted to `scaralang.core.model.dsl`; duplicate files removed from `scarajectory` | `scarajectory` is now a pure consumer importing from `scaralang` |


---

## 🔍 Detailed Architectural Findings & Actionable Plans

### Issue MOD-01: Kinematic Calculations Embedded Inside `TransmissionParameters`
- **Status:** 🟢 RESOLVED
- **Affected File:** `scarajectory/core/model/kinematics/transmission_parameters.py`
- **Violation Category:** Single Responsibility Principle (SRP), Domain Model Purity.
- **Resolution Summary:**
  `TransmissionParameters` converted into a pure `@dataclass(frozen=True, slots=True, kw_only=True)` with zero methods, containing exclusively domain configuration attributes. Step scaling and angle-to-step conversions (`_steps_per_rad`, `_steps_per_mm_z`, `angles_to_steps`) relocated directly into `StepDiscretizer` in the domain service layer.
- **Actionable Execution Plan:**
  - [x] Remove `steps_per_rad`, `steps_per_mm_z`, and `angles_to_steps` from `TransmissionParameters`.
  - [x] Implement `angles_to_steps` and scale factor calculations directly inside `StepDiscretizer`.
  - [x] Update all references and unit tests.

---

### Issue MOD-02: Binary Protocol Serialization & Codecs Embedded in Value Objects
- **Status:** 🟢 RESOLVED
- **Affected Files:**
  - `scarajectory/core/model/communication/protocol/binary_frame.py`
  - `scarajectory/core/model/communication/protocol/joint_steps.py`
  - `scarajectory/core/model/communication/scara_status.py`
- **Violation Category:** Separation of Concerns, Clean Architecture Boundary Leak.
- **Resolution Summary:**
  `BinaryFrame`, `JointSteps`, and `ScaraStatus` (renamed from `RobotStatus`) converted into pure frozen dataclasses with slots and zero methods. All binary frame packing (`pack_frame`), struct packing (`<iiiIIH`), and wire delimiters (`SOF1`, `SOF2`, `EOF`) relocated to `BinaryFrameBuilder`. All binary unpacking (`unpack_scara_status`, `unpack_joint_steps`) relocated to `BinaryFrameParser`.
- **Actionable Execution Plan:**
  - [x] Remove `pack_payload` and `unpack_payload` from `JointSteps`.
  - [x] Remove `unpack_payload`, `is_idle`, and `get_steps` from `ScaraStatus`.
  - [x] Remove `pack_frame` and delimiter constants from `BinaryFrame`.
  - [x] Move payload packing to `BinaryFrameBuilder` and payload unpacking to `BinaryFrameParser`.

---

### Issue MOD-03: File I/O Inside `ScaraBinaryProgram`
- **Status:** 🟢 RESOLVED
- **Affected File:** `scarajectory/core/model/dsl/binary/scara_binary_program.py`
- **Violation Category:** Clean Architecture (I/O in Domain Model).
- **Resolution Summary:**
  `save_to_file` and all OS/filesystem imports (`os.path.dirname`, `os.makedirs`, `open`) completely removed from `ScaraBinaryProgram`. Model is now a 100% pure dataclass holding compiled step tuples, raw bytes, and metrics. Persistence relocated to `PlanStorageService.save_binary_program`.
- **Actionable Execution Plan:**
  - [x] Remove `save_to_file` and file I/O imports from `ScaraBinaryProgram`.
  - [x] Add `save_binary_program` and `load_binary_file` to `PlanStorageService`.

---

### Issue MOD-04: Algorithmic Logic and Serialization Inside `Waypoint`
- **Status:** 🟢 RESOLVED
- **Affected File:** `scarajectory/core/model/trajectory/waypoint.py`
- **Violation Category:** Single Responsibility Principle (SRP), Domain Model Purity.
- **Resolution Summary:**
  1. `Waypoint` converted into a pure `@dataclass(frozen=True, slots=True, kw_only=True)` with zero methods and zero behavior.
  2. Planar radial distance and 3D Euclidean distance calculations extracted into `TrajectoryMetrics.distance_between` and `TrajectoryMetrics.radial_distance`.
  3. Single waypoint dictionary serialization and deserialization extracted into `TrajectorySerializer.serialize_waypoint` and `TrajectorySerializer.deserialize_waypoint`.
- **Actionable Execution Plan:**
  - [x] Move `radial_distance` and `distance_to` calculations to `TrajectoryMetrics`.
  - [x] Move `to_dict` and `from_dict` mapping logic into `TrajectorySerializer`.
  - [x] Reduce `Waypoint` to a pure data model matching `ScaraBounds`.
  - [x] Update GUI callers (`table.py`) to compute radial distance via `hypot`.

---

### Issue MOD-05: Misplaced Services in `core/model/trajectory/`
- **Status:** 🟢 RESOLVED
- **Affected Files:**
  - `scarajectory/core/model/trajectory/plan_history.py` -> `scarajectory/core/service/trajectory/plan_history.py`
  - `scarajectory/core/model/trajectory/trajectory_metrics.py` -> `scarajectory/core/service/trajectory/trajectory_metrics.py`
  - `scarajectory/core/model/trajectory/trajectory_serializer.py` -> `scarajectory/infrastructure/storage/trajectory_serializer.py`
- **Violation Category:** Packaging by Layer & Clean Architecture.
- **Resolution Summary:**
  All misplaced services have been relocated to their proper clean architecture layers:
  1. `PlanHistory` moved to `scarajectory/core/service/trajectory/plan_history.py`.
  2. `TrajectoryMetrics` moved to `scarajectory/core/service/trajectory/trajectory_metrics.py`.
  3. `TrajectorySerializer` moved to `scarajectory/infrastructure/storage/trajectory_serializer.py`.
- **Actionable Execution Plan:**
  - [x] Relocate `PlanHistory` to `core/service/trajectory/`.
  - [x] Relocate `TrajectoryMetrics` to `core/service/trajectory/`.
  - [x] Relocate `TrajectorySerializer` to `infrastructure/storage/`.
  - [x] Clean up package imports across services, GUI, and unit tests.

---

### Issue MOD-06: Hardcoded Model Defaults & Split-Brain Configuration
- **Status:** 🟢 RESOLVED
- **Affected Files:**
  - `scarajectory/core/model/kinematics/scara_bounds.py`
  - `scarajectory/core/model/kinematics/transmission_parameters.py`
  - `scarajectory/core/model/trajectory/waypoint.py`
  - `scarajectory/core/model/communication/protocol/binary_frame.py`
  - `scarajectory/infrastructure/config/scara_geometry.json`
  - `scarajectory/infrastructure/config/scheme.json`
  - `scarajectory/infrastructure/settings/config_loader.py`
  - `scarajectory/infrastructure/settings/config_loader_factory.py`
  - `scarajectory/core/service/config/iscara_config_loader.py`
- **Violation Category:** Single Source of Truth (SSoT), Model Purity, Configuration Decoupling.
- **Resolution Summary:**
  1. Pure Data Models: Hardcoded default numbers and magic coordinates removed from domain model definitions (`ScaraBounds`, `TransmissionParameters`, `Waypoint`, `BinaryFrame`). Operational fields like `z` and `speed` in `Waypoint` and `payload` and `crc16` in `BinaryFrame` are now mandatory arguments.
  2. Single Source of Truth: All physical geometry (`l1`, `l2`, limits, speeds, accelerations) and transmission ratios (`steps_per_rev`, `microstepping`, `gear_ratio_j1`, `gear_ratio_j2`, `gear_ratio_j4`, `leadscrew_pitch_z`) centralized in `scara_geometry.json` and validated by `scheme.json`.
  3. Decoupled Loader Adapter: Created `ScaraConfigLoader` (conforming to `IScaraConfigLoader` protocol) and `ScaraConfigLoaderFactory` in `infrastructure/settings/`, handling ATS loader ingestion.
  4. Dependency Injection: Factories (`TrajectoryValidatorFactory`, `KinematicsServiceFactory`, `ScaraDslServiceFactory`, `setup/factory.py`) now load configuration models via `ScaraConfigLoaderFactory` instead of hardcoding empty model instantiations.
- **Actionable Execution Plan:**
  - [x] Remove default value assignments from `BinaryFrame` (`payload`, `crc16`).
  - [x] Remove ALL default value assignments from `Waypoint` (`z`, `speed`, `phi`, `name`, `command`), achieving 100% pure domain model.
  - [x] Implement `WaypointFactory` in `core/service/trajectory/waypoint_factory.py` to isolate waypoint instantiation defaults.
  - [x] Remove default value assignments from `ScaraBounds` and `TransmissionParameters`.
  - [x] Extend `scara_geometry.json` and `scheme.json` to cover all transmission and deadzone parameters.
  - [x] Implement `IScaraConfigLoader`, `ScaraConfigLoader`, and `ScaraConfigLoaderFactory`.
  - [x] Refactor `setup/factory.py` `_resolve_bounds` to delegate to `ScaraConfigLoaderFactory`.
  - [x] Inject loader-provided models into service factories when defaults are requested.
  - [x] Add comprehensive test suite in `tests/scara_config_loader_test.py`.

---

### Issue MOD-07: Communication, Validation, and DSL Models Hardcoded Defaults
- **Status:** 🟢 RESOLVED
- **Affected Files:**
  - `scarajectory/core/model/communication/protocol/joint_steps.py`
  - `scarajectory/core/model/communication/stream/stream_config.py`
  - `scarajectory/core/model/communication/stream/stream_progress.py`
  - `scarajectory/core/model/communication/stream/stream_session.py`
  - `scarajectory/core/model/trajectory/validation_result.py`
  - `scarajectory/core/model/dsl/binary/scara_binary_step.py`
  - `scarajectory/core/model/dsl/binary/scara_binary_program.py`
  - `scarajectory/core/model/dsl/diagnostic/scara_diagnostic.py`
  - `scarajectory/core/model/dsl/ast/scara_program.py`
  - `scarajectory/infrastructure/config/scara_geometry.json`
  - `scarajectory/infrastructure/config/scheme.json`
  - `scarajectory/core/service/communication/stream/session_factory.py`
  - `scarajectory/core/service/communication/stream/config_factory.py`
- **Violation Category:** Single Source of Truth (SSoT), Model Purity, Separation of Concerns.
- **Resolution Summary:**
  1. Communication Models Purified:
     - `JointSteps`: Hardcoded `feedrate_scale: int = 100` removed; `default_feedrate_scale` centralized in `scara_geometry.json`.
     - `StreamConfig`: Hardcoded `baudrate: int = 115200` and `timeout: float = 0.1` removed; parameters centralized in `scara_geometry.json` and loaded via `ScaraConfigLoader.load_stream_config` and `ConfigFactory`.
     - `StreamProgress`: Snapshot default values (`failed_waypoints`, `current_line`, `error_message`, `elapsed_seconds`, `percentage`) removed; `StreamObserverDispatcher` provides full snapshot.
     - `StreamSession`: State defaults removed; session initialization encapsulated cleanly in `SessionFactory.create()`.
  2. Validation & DSL Models Purified:
     - `ValidationResult`: Default `error_index: int = -1` removed; explicit in validator outcomes.
     - `ScaraBinaryStep`: Default values (`target_steps`, `description`, `line_number`) removed.
     - `ScaraBinaryProgram`: Default `step_counts` removed.
     - `ScaraDiagnostic`: Defaults `line` and `command` removed.
     - `ScaraProgram`: Default empty instructions removed.
- **Actionable Execution Plan:**
  - [x] Remove defaults from `JointSteps` and add `default_feedrate_scale` to `scara_geometry.json`.
  - [x] Remove defaults from `StreamConfig` and add `baudrate` and `timeout` to `scara_geometry.json`.
  - [x] Implement `load_stream_config` in `IScaraConfigLoader` and `ScaraConfigLoader`.
  - [x] Create `ConfigFactory` in `core/service/communication/stream/config_factory.py`.
  - [x] Remove defaults from `StreamProgress` and update `StreamObserverDispatcher`.
  - [x] Remove defaults from `StreamSession` and create `SessionFactory`.
  - [x] Remove defaults from `ValidationResult`, `ScaraBinaryStep`, `ScaraBinaryProgram`, `ScaraDiagnostic`, and `ScaraProgram`.
  - [x] Update all production callers and unit tests.

---

### Issue MOD-08: DSL AST and Diagnostic Model Purity & Protocol Elimination
- **Status:** 🟢 RESOLVED
- **Affected Files:**
  - `scarajectory/core/model/dsl/ast/scara_instruction.py`
  - `scarajectory/core/model/dsl/ast/scara_program.py`
  - `scarajectory/core/model/dsl/diagnostic/scara_diagnostic.py`
  - `scarajectory/core/model/dsl/ast/iscara_instruction.py` (DELETED)
  - `scarajectory/core/model/dsl/ast/iscara_program.py` (DELETED)
  - `scarajectory/core/service/dsl/ast/instruction_factory.py` (NEW)
  - `scarajectory/core/service/dsl/ast/program_factory.py` (NEW)
  - `scarajectory/core/service/dsl/ast/scara_instruction_factory.py` (DELETED)
  - `scarajectory/core/service/dsl/ast/scara_program_factory.py` (DELETED)
  - `scarajectory/core/service/dsl/ast/scara_program_serializer.py` (NEW)
  - `scarajectory/core/service/dsl/ast/scara_source_generator.py` (NEW)
  - `scarajectory/core/service/dsl/diagnostic/scara_diagnostic_formatter.py` (NEW)
- **Violation Category:** Single Responsibility Principle (SRP), Domain Model Purity, Protocol Bloat.
- **Resolution Summary:**
  1. AST & Diagnostic Models Purified:
     - `ScaraInstruction`: Stripped hardcoded parameter and raw_text defaults; stripped serialization method `to_dict()`; parameters encapsulated with defensive `MappingProxyType`.
     - `ScaraProgram`: Stripped convenience classmethod `from_instructions()`; stripped serialization method `to_dict()` and unparsing method `to_text()`; typed `instructions: tuple[ScaraInstruction, ...]`.
     - `ScaraDiagnostic`: Stripped presentation formatting method `format_report()`, converted to pure value object.
  2. Redundant Protocols Eliminated:
     - Deleted `IScaraInstruction` and `IScaraProgram` which violated the rule against interfaces in model packages and caused unnecessary protocol overhead for pure AST data structures.
  3. Single-Responsibility Collaborators Created:
     - `InstructionFactory`: Handles default parameters and safe construction of `Instruction` (with alias `scara_instruction_factory.py` safely deleted).
     - `ProgramFactory`: Handles instruction sequence conversion to tuple for `Program` (with alias `scara_program_factory.py` safely deleted).
     - `ScaraProgramSerializer`: Isolated dictionary serialization for instructions and programs.
     - `ScaraSourceGenerator`: Isolated DSL text unparsing and code generation from AST trees.
     - `ScaraDiagnosticFormatter`: Standardized human-readable report formatting with emoji severity tags.
  4. Consumers & Tests Updated:
     - All 23+ parsers, compilers, macro expanders, linter rules, and facade services updated to use concrete purified models and new domain services.
     - Comprehensive unit test suites added in `tests/`, achieving 100% test pass rate across 170 unit tests.
- **Actionable Execution Plan:**
  - [x] Create `InstructionFactory`, `ProgramFactory`, `ScaraProgramSerializer`, `ScaraSourceGenerator`, and `ScaraDiagnosticFormatter`.
  - [x] Purify `ScaraInstruction`, `ScaraProgram`, and `ScaraDiagnostic`.
  - [x] Delete `iscara_instruction.py` and `iscara_program.py`.
  - [x] Refactor all parsers, compilers, macro expanders, linter rules, and facades.
  - [x] Write dedicated unit tests for all new domain services and purified models.
  - [x] Verify full project test suite (170/170 passing).
  - [x] Migrate all consumers across services, parsers, compilers, and tests from legacy `scara_*.py` aliases to canonical models (`instruction.py`, `program.py`, `command_type.py`, `binary_program.py`, `binary_step.py`, `diagnostic.py`, `diagnostic_severity.py`, `token.py`, `token_type.py`).
  - [x] Permanently delete the 9 legacy alias files (`scara_command_type.py`, `scara_instruction.py`, `scara_program.py`, `scara_binary_program.py`, `scara_binary_step.py`, `scara_diagnostic_severity.py`, `scara_diagnostic.py`, `scara_token_type.py`, `scara_token.py`).
  - [x] Permanently delete legacy alias factory files `scara_instruction_factory.py` and `scara_program_factory.py` after redirecting all parsers, factories, and tests to canonical `instruction_factory.py` and `program_factory.py`.

---

### Issue MOD-09: Relocate Stateful Trajectory Interfaces and Plan to Service Layer
- **Status:** 🟢 RESOLVED
- **Affected Files:**
  - `scarajectory/core/model/trajectory/trajectory_plan.py` -> `scarajectory/core/service/trajectory/trajectory_plan.py`
  - `scarajectory/core/model/trajectory/itrajectory_read_only.py` -> `scarajectory/core/service/trajectory/itrajectory_read_only.py`
  - `scarajectory/core/model/trajectory/itrajectory_mutable.py` -> `scarajectory/core/service/trajectory/itrajectory_mutable.py`
  - `scarajectory/core/model/trajectory/itrajectory_history.py` -> `scarajectory/core/service/trajectory/itrajectory_history.py`
  - `scarajectory/core/model/trajectory/itrajectory_plan.py` -> `scarajectory/core/service/trajectory/itrajectory_plan.py`
  - `scarajectory/core/service/trajectory/plan_history.py`
  - `scarajectory/core/service/trajectory/itrajectory_observer.py`
- **Violation Category:** Domain Model Purity, Clean Architecture Layer Separation, DIP.
- **Violation Rationale:**
  1. **Model Layer Purity Rule:** Domain models in `core/model/` must be 100% pure immutable data objects (`@dataclass(frozen=True, slots=True, kw_only=True)`) with zero methods, zero behavior, and zero state mutation. Furthermore, **zero interfaces (`Protocol`) are permitted in `core/model/`**; all interfaces belong exclusively in `core/service/` and `infrastructure/`.
  2. **Misplaced Aggregates & Interfaces in Model:** `TrajectoryPlan` is a stateful mutable aggregate coordinating waypoints, selection index, undo/redo stacks, and UI observers. Its contracts (`ITrajectoryReadOnly`, `ITrajectoryMutable`, `ITrajectoryHistory`, `ITrajectoryPlan`) are currently in `core/model/trajectory/`, causing reverse imports into `core/service/` (`plan_history.py` and `itrajectory_observer.py`).
  3. **Direct Instantiation Bypassing Factory:** `TrajectoryPlan.__init__` directly instantiates `self._history: Final[PlanHistory] = PlanHistory()`, violating the rule that objects must only be created by factory modules.
- **Proposed Decoupled Architecture:**
  - Relocate all trajectory interfaces (`ITrajectoryReadOnly`, `ITrajectoryMutable`, `ITrajectoryHistory`, `ITrajectoryPlan`) and `TrajectoryPlan` to `core/service/trajectory/`.
  - Create `TrajectoryPlanFactory` in `core/service/trajectory/trajectory_plan_factory.py` to instantiate `TrajectoryPlan` with pure constructor DI (`history: IPlanHistory = PlanHistoryFactory.create()`).
  - Create `IPlanHistory` protocol in `core/service/trajectory/iplan_history.py` and `PlanHistoryFactory` in `core/service/trajectory/plan_history_factory.py`.
  - Leave `core/model/trajectory/` with **only pure frozen data objects** (`Waypoint`, `ValidationResult`).
  - `core/model/` becomes 100% free of interfaces and 100% free of any imports from `core/service/` or `infrastructure/`.
- **Actionable Execution Plan:**
  - [x] Relocate `itrajectory_read_only.py`, `itrajectory_mutable.py`, `itrajectory_history.py`, `itrajectory_plan.py`, and `trajectory_plan.py` to `core/service/trajectory/`.
  - [x] Create `IPlanHistory` protocol in `core/service/trajectory/iplan_history.py`.
  - [x] Create `PlanHistoryFactory` in `core/service/trajectory/plan_history_factory.py`.
  - [x] Implement `TrajectoryPlanFactory` in `core/service/trajectory/trajectory_plan_factory.py` injecting `history: IPlanHistory`.
  - [x] Enforce pure constructor DI in `TrajectoryPlan.__init__(self, history: IPlanHistory)`.
  - [x] Update imports across services, GUI adapters, tests, and `setup/factory.py`.

---

### Issue MOD-10: Missing Domain Models for Firmware Wire Event & Protocol Mode Alignment
- **Status:** 🟢 RESOLVED
- **Affected Files:**
  - `scarajectory/core/model/communication/protocol/protocol_mode.py` (NEW)
  - `scarajectory/core/model/communication/event/move_event.py` (NEW)
  - `scarajectory/core/model/communication/stream/stream_config.py`
  - `scarajectory/core/service/communication/stream/config_factory.py`
  - `scarajectory/core/service/communication/event/move_event_factory.py` (NEW)
  - `scarajectory/core/service/communication/event/fault_event_factory.py` (NEW)
  - `scarajectory/core/service/communication/telemetry/diagnostics_snapshot_factory.py` (NEW)
- **Violation Category:** Clean Architecture / Firmware Specification Alignment / Domain Model Completeness.
- **Violation Rationale:**
  1. **Protocol Mode Representation:** The newly upgraded `scara_base` RP2040 firmware operates strictly on the binary wire protocol (`0xAA 0x55` framing, CRC16-CCITT). `scarajectory` currently lacks a domain model representing the wire protocol mode (`ProtocolMode.ASCII` vs `ProtocolMode.BINARY`), preventing configuration validation, negotiation, and multi-protocol streaming in higher layers.
  2. **Missing Wire Event Models:** The firmware dispatches asynchronous wire response frames:
     - `MSG_RESP_MOVE_EVENT (0x85)`: indicates step segment state transitions (`MOVE_EVT_STARTED = 1`, `MOVE_EVT_DONE = 2`, `MOVE_EVT_FAILED = 3`) for specific `segment_id`s. Currently there is no domain model `MoveEvent` in `core/model/communication/`.
     - `MSG_RESP_FAULT_EVENT (0x89)`: indicates hardware fault trips (`severity`, `fault_code: ErrorCode`, `extra_info`). There is no domain model `FaultEvent`.
     - `MSG_RESP_DIAGNOSTICS (0x88)`: periodic or on-demand telemetry (`rx_frames`, `tx_frames`, `crc_errors`, `queue_watermark`, `min_free_blocks`, `following_error_j1`, `following_error_j2`, `stall_flags`). There is no domain model `DiagnosticsSnapshot`.
  3. **Model Purity & Null-Safety Constraints:** These models must adhere strictly to the project's Core Constraints:
     - Pure frozen dataclasses (`@dataclass(frozen=True, slots=True, kw_only=True)`).
     - Zero methods, zero algorithmic logic, zero mutable fields, 0 `None` attributes, 0 defaults.
     - Zero interfaces in `core/model/`.
     - Instantiation strictly through dedicated factory modules in `core/service/communication/`.
- **Proposed Decoupled Architecture:**
  - Create `ProtocolMode` enum in `core/model/communication/protocol/protocol_mode.py` (`ASCII = 'ascii'`, `BINARY = 'binary'`).
  - Add `protocol_mode: ProtocolMode` to `StreamConfig`. Update `ConfigFactory` to resolve `protocol_mode` from the SSoT JSON configuration (`scara_geometry.json`).
  - Create `MoveEvent` in `core/model/communication/event/move_event.py` (`event_type: int`, `segment_id: int`) and `MoveEventFactory` in `core/service/communication/event/move_event_factory.py`.
  - Create `FaultEvent` in `core/model/communication/event/fault_event.py` (`severity: int`, `fault_code: ErrorCode`, `extra_info: int`) and `FaultEventFactory` in `core/service/communication/event/fault_event_factory.py`.
  - Create `DiagnosticsSnapshot` in `core/model/communication/telemetry/diagnostics_snapshot.py` and `DiagnosticsSnapshotFactory` in `core/service/communication/telemetry/diagnostics_snapshot_factory.py`.
- **Actionable Execution Plan:**
  - [x] Create `ProtocolMode` enum in `scarajectory/core/model/communication/protocol/protocol_mode.py`.
  - [x] Add required `protocol_mode: ProtocolMode` attribute to `StreamConfig` without default values.
  - [x] Update `ConfigFactory` to parse and supply `protocol_mode` from configuration loader.
  - [x] Create `MoveEvent` pure dataclass and `MoveEventFactory`.
  - [x] Create `FaultEvent` pure dataclass and `FaultEventFactory`.
  - [x] Create `DiagnosticsSnapshot` pure dataclass and `DiagnosticsSnapshotFactory`.
  - [x] Update unit tests in `tests/model_test.py` and `tests/communication_events_test.py`.

---

### Issue MOD-11: Complete Elimination of Optional/Nullable Fields in Domain Models
- **Status:** 🟢 RESOLVED
- **Affected Submodules:**
  - `core/model/dsl/ast/instruction.py` (`Instruction` - `parameters: Mapping[str, Any]`, 0 `None`, empty mapping for parameterless commands)
  - `core/model/dsl/ast/program.py` (`Program` - `instructions: tuple[Instruction, ...]`, 0 `None`, empty tuple for empty programs)
  - `core/model/communication/protocol/scara_response.py` (`ScaraResponse` - `queue_depth` removed into parser, 0 `None`)
  - `core/model/communication/protocol/joint_steps.py` (`JointSteps` - all 6 fields non-nullable, 0 `None`)
  - `core/model/communication/protocol/binary_frame.py` (`BinaryFrame` - all 4 fields non-nullable, 0 `None`)
  - `core/model/trajectory/waypoint.py` (`Waypoint` - all 7 fields non-nullable, 0 `None`)
  - `core/model/trajectory/validation_result.py` (`ValidationResult` - all 3 fields non-nullable, 0 `None`)
  - `core/model/kinematics/transmission_parameters.py` (`TransmissionParameters` - all fields non-nullable, 0 `None`)
  - `core/model/kinematics/scara_bounds.py` (`ScaraBounds` - all fields non-nullable, 0 `None`)
- **Violation Category:** Axiomatic Null-Safety Constraint, Model Purity, Deterministic Typing.
- **Violation Rationale:**
  1. **Harmful Impact of `None` in Domain Data Models:** In domain-driven architecture, models represent known, immutable state facts. Allowing nullable attributes (`foo: Bar | None = None`) causes ambiguity, invites `NullPointerException` / `AttributeError` runtime crashes, and forces all consumers to litter business logic with defensive `if model.foo is not None:` branches.
  2. **Strict Null-Safety Rule:** Every single field in `core/model/` must be strictly typed, required, and non-nullable. Where an entity can be empty, domain-appropriate empty representations must be used (`()` for tuples, `{}` for mappings, `''` for strings), NEVER `None`.
  3. **Zero Defaults:** Models define pure slots without inline defaults.
- **Actionable Execution Plan:**
  - [x] Audit all domain model classes in `core/model/` for `| None` attributes (100% clean, 0 `None` found).
  - [x] Verify `Instruction.parameters` is non-nullable `Mapping[str, Any]`.
  - [x] Verify `Program.instructions` is non-nullable `tuple[Instruction, ...]`.
  - [x] Verify `ScaraResponse` has zero `None` attributes.
  - [x] Maintain strict zero-tolerance for `None` in future domain models (`ProtocolMode`, `MoveEvent`, `FaultEvent`, `DiagnosticsSnapshot`).

---

## 🚀 Master Architectural Remediation Roadmap & Execution Plan

This section coordinates the master remediation plan across all layers, highlighting Phase 1 impacts on the Domain Model layer and Phase 4 firmware alignment.

### 🗺️ High-Level 4-Phase Execution Roadmap

| Phase | Focus Areas | Key Issues | Target Architecture |
|---|---|---|---|
| **Phase 1** | Pure Data Models & Clean Architecture Boundaries | `MOD-09`, `SVC-04`, `SVC-05`, `SVC-06` | Relocate `IBinaryFrameBuilder` and `IScaraConfigLoader` to core service; purify `core/model/` by relocating `TrajectoryPlan` and all `ITrajectory*` protocols to `core/service/trajectory/`; enforce 0 interfaces and 0 service imports in `core/model/`. |
| **Phase 2** | Communication & Streaming Podsystem | `INF-05`, `INF-06`, `INF-09`, `INF-10` | Enforce explicit `IRobotController` injection; parameterize flow buffer capacity; inject `IProtocolParser` and `ICommandFormatter` strategies; create `TrajectoryStreamerFactory`. |
| **Phase 3** | GUI, Canvas, CAD Tools & Setup Assembly | `INF-07`, `INF-08`, `INF-11`, `INF-12`, `INF-13`, `INF-14` | Mandatory DI in `DslEditorTab`; extract domain `ShapeDiscretizer`; eliminate raw `Waypoint` instantiation via `WaypointFactory.create(...)`; dynamic workspace reach limits; assemble object graph via factories in `SCARAjectoryBundleFactory`. |
| **Phase 4** | Full Hardware & Firmware Alignment (`scara_base` RP2040) | `MOD-10`, `SVC-10`, `INF-15` | Add `ProtocolMode`, `MoveEvent`, `FaultEvent`, `DiagnosticsSnapshot`; define streaming strategy and flow control protocols in `core/service/communication/`; implement `BinaryStreamExecutionWorker`, raw byte stream transport, binary controller, and dual-mode GUI. |

---

### 📋 Phase 1 Execution Detail for Model Layer (`MOD-09`)
- **Step 1:** Relocate `itrajectory_read_only.py`, `itrajectory_mutable.py`, `itrajectory_history.py`, `itrajectory_plan.py`, and `trajectory_plan.py` from `scarajectory/core/model/trajectory/` to `scarajectory/core/service/trajectory/`.
- **Step 2:** Create `IPlanHistory` protocol in `scarajectory/core/service/trajectory/iplan_history.py` declaring undo, redo, snapshot, can_undo, can_redo methods.
- **Step 3:** Implement `PlanHistoryFactory` in `scarajectory/core/service/trajectory/plan_history_factory.py`.
- **Step 4:** Implement `TrajectoryPlanFactory` in `scarajectory/core/service/trajectory/trajectory_plan_factory.py` injecting `history: IPlanHistory = PlanHistoryFactory.create()`.
- **Step 5:** Enforce constructor injection in `TrajectoryPlan.__init__(self, history: IPlanHistory)` (no inline `PlanHistory()` instantiation).
- **Step 6:** Update all imports in GUI (`controls_panel.py`, `table.py`, `waypoint_editor.py`), storage (`plan_storage_service.py`), bundle factory (`setup/factory.py`), and test suites.
- **Step 7:** Run `python3 -m unittest discover -s tests -p "*_test.py"` to ensure 100% test pass rate.

---

### 📋 Phase 4 Execution Detail for Model Layer (`MOD-10`)
- **Step 1:** Create `ProtocolMode` enum in `scarajectory/core/model/communication/protocol/protocol_mode.py` (`ASCII = 'ascii'`, `BINARY = 'binary'`).
- **Step 2:** Add `protocol_mode: ProtocolMode` attribute to `StreamConfig` (`core/model/communication/stream/stream_config.py`).
- **Step 3:** Update `ConfigFactory` (`core/service/communication/stream/config_factory.py`) to parse `protocol_mode` from the SSoT JSON configuration with strict validation.
- **Step 4:** Create pure frozen dataclasses `MoveEvent`, `FaultEvent`, and `DiagnosticsSnapshot` in `core/model/communication/` (0 methods, 0 defaults, 0 `None` attributes).
- **Step 5:** Create dedicated factories `MoveEventFactory`, `FaultEventFactory`, and `DiagnosticsSnapshotFactory` in `core/service/communication/`.
- **Step 6:** Update and execute unit tests in `tests/model_test.py` and `tests/stream_config_test.py`.

---

### 🧪 Acceptance Criteria for Model Layer
- [x] 100% of classes in `core/model/` are pure `@dataclass(frozen=True, slots=True, kw_only=True)`.
- [x] 0 methods, 0 properties, 0 algorithmic logic, 0 mutable fields in `core/model/`.
- [x] 0 protocols / interfaces in `core/model/`.
- [x] 0 imports from `core/service/` or `infrastructure/` in `core/model/`.
- [x] Full test suite execution passes (190/190 tests passing).
- [x] `ProtocolMode` enum created and wired into `StreamConfig` via `ConfigFactory`.
- [x] Pure wire event models (`MoveEvent`, `FaultEvent`, `DiagnosticsSnapshot`) implemented with 0 defaults and dedicated factories.
- [x] Pure domain models `TransmissionParameters` and `ScaraBounds` remain 100% pure frozen dataclasses loaded via `ScaraConfigLoader` (SSoT `scara_geometry.json`); redundant numerical wrapper factories eliminated.





