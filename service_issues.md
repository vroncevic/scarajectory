# Application Service Layer Architectural Audit (`service_issues.md`)

This document tracks architectural compliance, SOLID principles, decomposition requirements, and clean boundary separation for the **Application Service** layer (`scarajectory/core/service/`).

---

## 🏛️ Service Layer Guiding Principles (Source of Truth)

1. **SOLID Principles Compliance & Clean Architecture:** Every service, compiler, coordinator, and factory must strictly adhere to Single Responsibility (SRP), Open/Closed (OCP), Liskov Substitution (LSP), Interface Segregation (ISP), and Dependency Inversion (DIP). Clean Architecture layer boundaries are strictly maintained: `core/model/` <- `core/service/` <- `infrastructure/`.
2. **Factory Hierarchy Rule ("Factory Calls Factory Only"):** A Factory can **ONLY** be called inside another Factory, or inside `main.py` (the top-level composition root / entry point). **A Factory must NEVER be called inside regular classes** (services, compilers, parsers, linters, coordinators, workers, controllers, presenters, GUI widgets). If a class needs to instantiate objects dynamically at runtime, it must receive an abstract factory interface (`@runtime_checkable Protocol`) via constructor dependency injection (e.g. `IWaypointFactory`, `ITrajectoryPlanFactory`, `IInstructionFactory`), or receive pre-built objects created by the parent factory.
3. **Abstract Interfaces Everywhere / Only Factories Work with Created Concrete Instances:** Across the entire application, all class dependencies and method signatures must be typed as abstract interfaces (`@runtime_checkable Protocol`). **Only factory modules instantiate concrete classes and wire up object graphs.** Concrete implementation classes:
   - Must NOT inherit from Protocol classes.
   - Must NOT import Protocol classes.
   - Must NOT use `@override`.
   - Must NOT be imported by peer domain services or adapters.
   All peer collaborations flow strictly through abstract protocols.
4. **No `@staticmethod`, Strict `@classmethod` Everywhere:** Static methods (`@staticmethod`) are strictly forbidden across the codebase. All factory creation methods, class-level helpers, and builders must be declared as `@classmethod(cls, ...)`.
5. **Zero `None` Policy (Absolute Null-Safety & Explicit Typing):** Never use `| None = None` or default `None` values in models, domain entities, or factory creation methods. All parameters must be 100% explicit and non-nullable. If an attribute represents an empty collection, use immutable empty collections (`()`, `{}`), never `None`.
6. **Small Classes with 2+ Methods:** Domain services and collaborators must be small, focused classes with 2+ cohesive public methods. Avoid single-method artificial classes (unless pure strategy) and eliminate monolithic god-classes.
7. **Minimization & Elimination of Private Methods (Zero Private Methods Goal via Decomposition):** Minimize and wherever possible completely eliminate private helper methods (`_method`). Private helper methods indicate hidden responsibilities and multiple reasons to change (violating SRP). Instead of hiding sub-routines in private methods, decompose responsibilities into dedicated collaborating classes with cohesive public interfaces, injected via DI. Methods must remain concise (≤15–25 lines of pure code).
8. **Pure Dependency Injection (DIP) from Parent Modules:** Collaborators and configurations are always injected from parent callers/factories downwards. Services must never instantiate concrete dependencies or use fallback default initializations.
9. **Factories as the Exclusive Instantiation Sites:** The ONLY place where concrete objects are instantiated is in factory modules. No inline `Foo()` calls or default instantiations exist in services, coordinators, or GUI components.
10. **Abstract Interfaces in `core/service/` and `infrastructure/` Only:** All interfaces are defined as `@runtime_checkable Protocol` in `core/service/` (or `infrastructure/`). **Zero interfaces (`Protocol`) are permitted in `core/model/`**.
11. **Models are 100% Pure Data Objects:** Services operate strictly on immutable data models (`@dataclass(frozen=True, slots=True, kw_only=True)`) that have zero methods, zero behavior, and zero mutable state.
12. **Relocation of Stateful Aggregates to Service Layer:** Stateful aggregates managing mutation stacks, history, and observer dispatching (such as `TrajectoryPlan` and `ITrajectoryPlan`) belong strictly in `core/service/trajectory/`.

---

## 📊 Master Status Matrix

| Service / Subsystem | Current State | Audit Status | Violations Identified | Actionable Remediation |
|---|---|---|---|---|
| `dsl/` (Toolchain & Compilers) | Standalone Package | 🟢 RESOLVED (MIGRATED TO SCARALANG) | Extracted to dedicated `scaralang` package (`scaralang.core.service.dsl`); local duplicates removed from `scarajectory` | `scarajectory` is a pure consumer importing from `scaralang` |
| `communication/IBinaryFrameBuilder` | Protocol Interface | 🟢 RESOLVED (MIGRATED TO SCARALANG) | Extracted to `scaralang.core.service.protocol.ibinary_frame_builder`; local duplicate removed from `scarajectory` | Imported directly from `scaralang` |
| `config/IScaraConfigLoader` | Protocol Interface | 🟢 RESOLVED | Relocated to `core/service/config/iscara_config_loader.py` | Clean service protocol placement |
| `Service` (Engine) | Façade (207 lines) | 🟢 RESOLVED | Mandatory pure DI for `dsl_service` without fallback instantiation; 100% protocol dependencies | Require pure DI for `dsl_service` |
| `ServiceFactory` | Domain Factory Service | 🟢 RESOLVED | Created in `core/service/service_factory.py` for assembling Service instances | Clean service factory placement |
| `Service Factories` | Factory Services | 🟢 RESOLVED | Completely decoupled from `infrastructure.config`; use pure domain model factories and optional `IScaraConfigLoader` | Pure DI and domain defaults |
| `kinematics/KinematicsService` | Solvers (225 lines) | 🟢 RESOLVED | Unused/forbidden `IKinematicsService` import removed | Pure mathematical kinematics service with zero protocol coupling |
| `trajectory/TrajectoryValidator` | Validator (200 lines) | 🟢 RESOLVED | Nullable parameters and fallback instantiation removed; pure DI for kinematics; 0 concrete imports | Assembled via `TrajectoryValidatorFactory` |
| `trajectory/PlanHistory` | Domain Service (116 lines) | 🟢 RESOLVED | Relocated from `core/model/` to `core/service/trajectory/plan_history.py` | Clean service placement |
| `trajectory/IPlanHistory` | Protocol Interface | 🟢 RESOLVED | Created in `core/service/trajectory/iplan_history.py` | Granular structural protocol |
| `trajectory/PlanHistoryFactory` | Domain Factory Service | 🟢 RESOLVED | Created in `core/service/trajectory/plan_history_factory.py` | Isolated history creation |
| `trajectory/TrajectoryPlan` | Stateful Observable Aggregate | 🟢 RESOLVED | Relocated to `core/service/trajectory/` with pure DI (`IPlanHistory`) and `TrajectoryPlanFactory` | Clean service aggregate placement |
| `trajectory/ITrajectoryPlan` / `ITrajectory*` | Structural Protocols | 🟢 RESOLVED | Relocated all trajectory protocols to `core/service/trajectory/` | Clean service interfaces |
| `trajectory/TrajectoryPlanFactory` | Domain Factory Service | 🟢 RESOLVED | Created in `core/service/trajectory/trajectory_plan_factory.py` | Injects `IPlanHistory` |
| `trajectory/TrajectoryMetrics` | Domain Service (113 lines) | 🟢 RESOLVED | Relocated from `core/model/` to `core/service/trajectory/trajectory_metrics.py` | Clean service placement |
| `trajectory/ShapeDiscretizer` | Domain Service | 🟢 RESOLVED | Calls `WaypointFactory.create` directly instead of receiving abstract `IWaypointFactory` | Inject `IWaypointFactory` via constructor DI (`SVC-12`) |
| `trajectory/ShapeDiscretizerFactory` | Domain Factory Service | 🟢 RESOLVED | Created `ShapeDiscretizerFactory` in `core/service/trajectory/shape_discretizer_factory.py` | Wire `WaypointFactory` as `IWaypointFactory` |
| `communication/IPacketStrategy` | Structural Protocol | 🟢 RESOLVED | Missing strategy abstraction for formulating ASCII vs Binary wire packets | Define protocol in `core/service/communication/stream/ipacket_strategy.py` |
| `communication/IFlowController` | Structural Protocol | 🟢 RESOLVED | Missing formal protocol interface for dual-protocol flow control contracts | Define protocol in `core/service/communication/stream/iflow_controller.py` |
| `communication/IBinaryFrameDispatcher` | Structural Protocol | 🟢 RESOLVED | Missing event routing interface for firmware response frames (`ACK`, `NACK`, `STATUS`, `MOVE_EVENT`, `FAULT_EVENT`, `DIAGNOSTICS`) | Define protocol in `core/service/communication/event/ibinary_frame_dispatcher.py` |
| `communication/DirectProgramStreaming` | Domain Service Flow | 🟢 RESOLVED | `TrajectoryStreamer` lacks direct execution pathway for pre-compiled `ScaraBinaryProgram` | Add service abstraction for streaming pre-compiled binary steps |
| `service/` Factories | Factory Services | 🟢 RESOLVED | Factories currently accept `| None = None` and fallback defaults; must be 100% explicit without `None` (`SVC-11`) | Refactor all factory signatures (`ConfigFactory`, `KinematicsServiceFactory`, `TrajectoryValidatorFactory`, `ScaraDslServiceFactory`, `TrajectoryPlanFactory`, `SessionFactory`) |
| `service/` Factory Hierarchy | Architecture Rule | 🟢 RESOLVED | Factories called inside regular classes (`ShapeDiscretizer`, `ScaraCompiler`, `ScaraParser`, command parsers) (`SVC-12`) | Factory hierarchy strictly enforced; classes receive abstract factory protocols |
| `service/` Method Signatures | Method Modifiers | 🟢 RESOLVED | ~36 `@staticmethod` decorators across services/factories (`SVC-13`) | All `@staticmethod` converted to `@classmethod(cls, ...)` |
| `communication/IRobotController` | Structural Protocol | 🟢 RESOLVED | Fat interface (10 methods across 4 domains) violated ISP (`SVC-14`) | Decomposed into `IMotionController`, `IJogController`, `IToolController`, `IQueryController` with composite `IRobotController` |
| `communication/ITrajectoryStreamer` | Structural Protocol | 🟢 RESOLVED | Fat interface combining raw I/O, connection, streaming, and observation (`SVC-15`) | Segregated into `IRawChannel`, `IConnection`, `IMotionStreamer`, `IObservable`, and composite facade `ITrajectoryStreamer` |
| `service/` Sub-package Structure | Architecture Packaging | 🟢 RESOLVED | Flat package clutter in `dsl/binary` (13 modules), `dsl/compiler` (20 modules), `trajectory` (26 modules) (`SVC-19`) | Decomposed into focused sub-packages (`command/`, `motion/`, `step/`, `plan/`, `history/`, `validation/`, `discretization/`, `metrics/`, `contract/`) with single-line imports |

---

## 🔍 Detailed Architectural Findings & Actionable Plans

### Issue SVC-01: `Compiler` Monolithic Responsibilities & Clean Module Naming
- **Status:** 🟢 RESOLVED
- **Affected File:** `scarajectory/core/service/dsl/binary/compiler.py` (decomposed from 269 lines to 154 lines)
- **Violation Category:** Single Responsibility Principle (SRP), Open/Closed Principle (OCP), God-Class Code Smell.
- **Resolution Summary:**
  1. Extracted `IMotionCompiler` / `MotionCompiler` (`motion_compiler.py`) with `MotionCompilerFactory`.
  2. Extracted `ICommandCompiler` / `CommandCompiler` (`command_compiler.py`) with `CommandCompilerFactory`.
  3. `Compiler` now has **zero private methods** and acts as a pure coordinator delegating step compilation to injected sub-compilers.
  4. `CompilerFactory` coordinates explicit DI across child sub-factories.
  5. Eliminated redundant package stuttering (`binary_command_compiler.py` -> `command_compiler.py`, `binary_motion_compiler.py` -> `motion_compiler.py`, `binary_compiler.py` -> `compiler.py`, `ibinary_compiler.py` -> `icompiler.py`, `binary_compiler_factory.py` -> `compiler_factory.py`).
  6. Eliminated redundant `bounds: ScaraBounds | None = None` method parameters from `ICompiler`, `Compiler`, and `ScaraDslService` compiler methods, enforcing SSoT geometry configuration injection via `setup/factory.py` and strict Zero `None` Policy.
- **Actionable Execution Plan:**
  - [x] Define `IMotionCompiler` and implement `MotionCompiler`.
  - [x] Define `ICommandCompiler` and implement `CommandCompiler`.
  - [x] Update `Compiler` to depend strictly on `IMotionCompiler` and `ICommandCompiler`.
  - [x] Update `CompilerFactory` with pure DI for sub-compilers.
  - [x] Eliminate package stuttering in file and class naming (`compiler.py`, `icompiler.py`, `compiler_factory.py`).
  - [x] Purify `ICompiler`, `Compiler`, and `ScaraDslService` compiler signatures by removing redundant `bounds` parameters in compliance with SSoT configuration loading.
  - [x] Update unit tests.

---

### Issue SVC-02: `MotionCommandCompiler` Bloat & Monolithic Private Compilation
- **Status:** 🟢 RESOLVED
- **Affected File:** `scarajectory/core/service/dsl/compiler/motion_command_compiler.py` (decomposed from 250 lines to 179 lines)
- **Violation Category:** Single Responsibility Principle (SRP), High Complexity, Private Method Bloat.
- **Resolution Summary:**
  1. Extracted `CartesianMoveCompiler` (`cartesian_move_compiler.py`) and `CartesianMoveCompilerFactory` handling `MOVE_L` and `MOVE_J`.
  2. Extracted `VerticalMoveCompiler` (`vertical_move_compiler.py`) and `VerticalMoveCompilerFactory` handling `APPROACH` and `RETRACT`.
  3. Extracted `ArcMoveCompiler` (`arc_move_compiler.py`) and `ArcMoveCompilerFactory` handling `ARC_CW` and `ARC_CCW`.
  4. Extracted `MotionCommandCompilerFactory` providing explicit sub-factory dependency injection.
  5. `MotionCommandCompiler` now has **zero private methods** and acts as a pure coordinator delegating directly to injected sub-compilers.
  6. `ScaraCompilerFactory` updated to wire `MotionCommandCompilerFactory`.
- **Actionable Execution Plan:**
  - [x] Extract `CartesianMoveCompiler` and its factory.
  - [x] Extract `VerticalMoveCompiler` and its factory.
  - [x] Extract `ArcMoveCompiler` and its factory.
  - [x] Implement `MotionCommandCompilerFactory`.
  - [x] Remove all private methods from `MotionCommandCompiler`.
  - [x] Wire through `ScaraCompilerFactory` and update unit tests.

---

### Issue SVC-03: Relocation of Domain Services Misplaced in `core/model/trajectory/`
- **Status:** 🟢 RESOLVED
- **Affected Files:**
  - `scarajectory/core/model/trajectory/plan_history.py` -> `scarajectory/core/service/trajectory/plan_history.py`
  - `scarajectory/core/model/trajectory/trajectory_metrics.py` -> `scarajectory/core/service/trajectory/trajectory_metrics.py`
- **Violation Category:** Clean Architecture Layer Separation.
- **Resolution Summary:**
  1. `PlanHistory` relocated to `scarajectory/core/service/trajectory/plan_history.py`.
  2. `TrajectoryMetrics` relocated to `scarajectory/core/service/trajectory/trajectory_metrics.py`.
  3. Imports updated in `TrajectoryPlan`, `TrajectoryValidator`, and GUI editor tabs.
- **Actionable Execution Plan:**
  - [x] Move `PlanHistory` to `core/service/trajectory/plan_history.py`.
  - [x] Move `TrajectoryMetrics` to `core/service/trajectory/trajectory_metrics.py`.
  - [x] Update imports across the codebase and verify all unit tests pass.

---

### Issue SVC-04: Clean Architecture Inversion — `core/service/` Importing Abstractions from `infrastructure/`
- **Status:** 🟢 RESOLVED
- **Affected Files:**
  - `scarajectory/core/service/dsl/binary/binary_motion_compiler.py`
  - `scarajectory/core/service/dsl/binary/binary_command_compiler.py`
  - `scarajectory/core/service/communication/protocol/ibinary_frame_builder.py` (relocated from infrastructure)
- **Violation Category:** Dependency Inversion Principle (DIP), Clean Architecture Layering.
- **Violation Rationale:**
  `binary_motion_compiler.py` and `binary_command_compiler.py` are domain service components located in `core/service/dsl/binary/`. Both import the protocol interface `IBinaryFrameBuilder` from `scarajectory.infrastructure.communication.protocol.binary.ibinary_frame_builder`.
  In Clean Architecture and DIP, high-level core services must not depend on low-level infrastructure modules. Abstractions belong to the calling domain layer, while infrastructure adapters implement those abstractions.
- **Proposed Decoupled Architecture:**
  - Relocate `IBinaryFrameBuilder` to `core/service/communication/protocol/ibinary_frame_builder.py`.
  - Concrete implementation `BinaryFrameBuilder` remains in `infrastructure/communication/protocol/binary/` structurally implementing the protocol.
- **Actionable Execution Plan:**
  - [x] Relocate `IBinaryFrameBuilder` protocol to `core/service/communication/`.
  - [x] Update imports in `binary_motion_compiler.py`, `binary_command_compiler.py`, and `binary_frame_builder.py`.
  - [x] Verify test suite passes without regressions.

---

### Issue SVC-05: Service Factories Directly Coupling to Infrastructure Configuration
- **Status:** 🟢 RESOLVED
- **Affected Files:**
  - `scarajectory/core/service/trajectory/trajectory_validator_factory.py`
  - `scarajectory/core/service/kinematics/kinematics_service_factory.py`
  - `scarajectory/core/service/communication/stream/config_factory.py`
  - `scarajectory/core/service/dsl/scara_dsl_service_factory.py`
  - `scarajectory/core/service/config/iscara_config_loader.py` (relocated from infrastructure)
  - `scarajectory/core/service/kinematics/scara_bounds_factory.py` (NEW)
  - `scarajectory/core/service/kinematics/transmission_parameters_factory.py` (NEW)
- **Violation Category:** Dependency Inversion Principle (DIP), Separation of Concerns.
- **Violation Rationale:**
  Domain service factories in `core/service/` import `ScaraConfigLoaderFactory` directly from `infrastructure/config/` to supply fallback default models if none are provided. Furthermore, the contract `IScaraConfigLoader` lives in `infrastructure/config/`.
- **Proposed Decoupled Architecture:**
  - Relocate the abstract loader protocol `IScaraConfigLoader` to `core/service/config/iscara_config_loader.py`.
  - Service factories should accept domain models (`ScaraBounds`, `StreamConfig`, etc.) explicitly injected, delegating configuration loading to the composition root (`setup/factory.py`).
- **Actionable Execution Plan:**
  - [x] Relocate `IScaraConfigLoader` protocol to `core/service/config/`.
  - [x] Require explicit model injection into service factories or inject `IScaraConfigLoader` abstraction.
  - [x] Update composition root in `setup/factory.py` and test harnesses.

---

### Issue SVC-06: `Service` Facade Fallback Default Dependency Instantiation
- **Status:** 🟢 RESOLVED
- **Affected Files:**
  - `scarajectory/core/service/engine.py`
- **Violation Category:** Dependency Inversion Principle (DIP).
- **Violation Rationale:**
  `Service.__init__` contained conditional fallback instantiation:
  ```python
  self._dsl_service: Final[IScaraDslService] = (
      dsl_service
      if dsl_service is not None
      else ScaraDslServiceFactory.create(validator=validator)
  )
  ```
  Services must receive their collaborators exclusively via pure constructor injection. Factories should be the sole creators of object graphs.
- **Proposed Decoupled Architecture:**
  - Make `dsl_service: IScaraDslService` a required, non-optional parameter in `Service.__init__`.
  - Ensure `SCARAjectoryBundleFactory.create_bundle` always passes the instantiated `dsl_service`.
- **Actionable Execution Plan:**
  - [x] Make `dsl_service` mandatory in `Service.__init__`.
  - [x] Update `setup/factory.py` and service tests.

---

### Issue SVC-07: `KinematicsService` Protocol Import Violation
- **Status:** 🟢 RESOLVED
- **Affected File:** `scarajectory/core/service/kinematics/kinematics_service.py`
- **Violation Category:** Structural Typing & Protocol Implementation Rule.
- **Violation Rationale:**
  `KinematicsService` imported its own interface protocol `IKinematicsService`. Under Python structural subtyping (PEP 544) and project constraints, concrete implementations must never import the protocol interface they satisfy.
- **Resolution Summary:**
  Removed the unused and forbidden `from scarajectory.core.service.kinematics.ikinematics_service import IKinematicsService` from `kinematics_service.py`.
- **Actionable Execution Plan:**
  - [x] Remove `IKinematicsService` import from `kinematics_service.py`.
  - [x] Verify structural subtyping compliance and test suite execution.

---

### Issue SVC-08: Relocation of `TrajectoryPlan` and Trajectory Protocols to Service Layer
- **Status:** 🟢 RESOLVED
- **Affected Files:**
  - `scarajectory/core/model/trajectory/trajectory_plan.py` -> `scarajectory/core/service/trajectory/trajectory_plan.py`
  - `scarajectory/core/model/trajectory/itrajectory_read_only.py` -> `scarajectory/core/service/trajectory/itrajectory_read_only.py`
  - `scarajectory/core/model/trajectory/itrajectory_mutable.py` -> `scarajectory/core/service/trajectory/itrajectory_mutable.py`
  - `scarajectory/core/model/trajectory/itrajectory_history.py` -> `scarajectory/core/service/trajectory/itrajectory_history.py`
  - `scarajectory/core/model/trajectory/itrajectory_plan.py` -> `scarajectory/core/service/trajectory/itrajectory_plan.py`
  - `scarajectory/core/service/trajectory/plan_history.py`
  - `scarajectory/core/service/trajectory/iplan_history.py` (NEW)
  - `scarajectory/core/service/trajectory/plan_history_factory.py` (NEW)
  - `scarajectory/core/service/trajectory/trajectory_plan_factory.py` (NEW)
- **Violation Category:** Clean Architecture Layer Separation, Dependency Inversion Principle (DIP), Model Purity.
- **Violation Rationale:**
  1. **Model Layer Purity:** Domain models in `core/model/` must be 100% pure immutable data objects (`@dataclass(frozen=True, slots=True, kw_only=True)`) with zero methods, zero behavior, and zero mutable state.
  2. **Zero Interfaces in Model Layer:** Abstract interfaces (`@runtime_checkable Protocol`) belong strictly in `core/service/` and `infrastructure/`. Zero protocols are allowed in `core/model/`.
  3. **Misplaced Stateful Aggregate:** `TrajectoryPlan` is an observable, stateful coordinator managing waypoint sequences, undo/redo stacks, selection states, and UI observer dispatches. It does not belong in the domain model layer.
  4. **Direct Instantiation Bypassing Factory:** `TrajectoryPlan.__init__` directly creates `self._history: Final[PlanHistory] = PlanHistory()`, violating the rule that all concrete objects must be created strictly in factory modules.
- **Proposed Decoupled Architecture:**
  - Relocate `TrajectoryPlan` and all 4 trajectory protocols (`ITrajectoryReadOnly`, `ITrajectoryMutable`, `ITrajectoryHistory`, `ITrajectoryPlan`) into `core/service/trajectory/`.
  - Create `IPlanHistory` protocol in `core/service/trajectory/iplan_history.py`.
  - Create `PlanHistoryFactory` in `core/service/trajectory/plan_history_factory.py`.
  - Create `TrajectoryPlanFactory` in `core/service/trajectory/trajectory_plan_factory.py` to instantiate `TrajectoryPlan` with pure constructor DI (`history: IPlanHistory = PlanHistoryFactory.create()`).
  - Enforce pure DI in `TrajectoryPlan.__init__(self, history: IPlanHistory)`.
  - `core/model/` is left with 100% pure data objects (`Waypoint`, `ValidationResult`) and zero protocols or service dependencies.
- **Actionable Execution Plan:**
  - [x] Relocate `itrajectory_read_only.py`, `itrajectory_mutable.py`, `itrajectory_history.py`, `itrajectory_plan.py`, and `trajectory_plan.py` to `core/service/trajectory/`.
  - [x] Create `IPlanHistory` protocol in `core/service/trajectory/iplan_history.py`.
  - [x] Create `PlanHistoryFactory` in `core/service/trajectory/plan_history_factory.py`.
  - [x] Implement `TrajectoryPlanFactory` in `core/service/trajectory/trajectory_plan_factory.py`.
  - [x] Enforce constructor DI in `TrajectoryPlan.__init__(self, history: IPlanHistory)`.
  - [x] Update imports across services, GUI adapters, tests, and composition root.

---

### Issue SVC-09: Extraction of Shape Discretization Domain Service from GUI Layer
- **Status:** 🟢 RESOLVED
- **Affected Files:**
  - `scarajectory/infrastructure/gui/canvas/canvas_tool_handler.py`
  - `scarajectory/core/service/trajectory/shape_discretizer.py` (NEW)
  - `scarajectory/core/service/trajectory/shape_discretizer_factory.py` (NEW)
  - `scarajectory/core/service/trajectory/ishape_discretizer.py` (NEW)
- **Violation Category:** Single Responsibility Principle (SRP), Separation of Concerns, Clean Architecture.
- **Violation Rationale:**
  1. Mathematical discretization of lines, circles, and rectangles into waypoint sequences (`discretize_line`, `discretize_circle`, `discretize_rectangle`) is core domain trajectory generation logic, yet it is currently located inside `CanvasToolHandler` in `infrastructure/gui/canvas/`.
  2. Canvas tool handler directly instantiates raw `Waypoint(...)` instances on 8 separate occasions instead of using `WaypointFactory.create(...)`.
  3. Embedding domain algorithms in GUI modules prevents CLI tools, automated batch scripts, and DSL services from generating geometric paths without coupling to Tkinter/GUI components.
- **Proposed Decoupled Architecture:**
  - Create abstract protocol `IShapeDiscretizer` in `core/service/trajectory/ishape_discretizer.py`.
  - Implement `ShapeDiscretizer` in `core/service/trajectory/shape_discretizer.py` delegating waypoint creation to `WaypointFactory.create(...)`.
  - Create `ShapeDiscretizerFactory` in `core/service/trajectory/shape_discretizer_factory.py`.
  - Inject `IShapeDiscretizer` into `CanvasToolHandler`.
- **Actionable Execution Plan:**
  - [x] Create `IShapeDiscretizer` protocol in `core/service/trajectory/ishape_discretizer.py`.
  - [x] Implement `ShapeDiscretizer` in `core/service/trajectory/shape_discretizer.py` using `WaypointFactory`.
  - [x] Implement `ShapeDiscretizerFactory` in `core/service/trajectory/shape_discretizer_factory.py`.
  - [x] Inject `IShapeDiscretizer` into `CanvasToolHandler` and remove internal discretization methods.

---

### Issue SVC-10: Binary Streaming Strategy, Flow Control Protocol & Event Dispatching
- **Status:** 🟢 RESOLVED
- **Affected Files:**
  - `scarajectory/core/service/communication/stream/ipacket_strategy.py` (NEW)
  - `scarajectory/core/service/communication/stream/iflow_controller.py` (NEW)
  - `scarajectory/core/service/communication/event/ibinary_frame_dispatcher.py` (NEW)
  - `scarajectory/core/service/communication/event/binary_frame_dispatcher.py` (NEW)
  - `scarajectory/core/service/communication/event/binary_frame_dispatcher_factory.py` (NEW)
  - `scarajectory/core/service/communication/stream/itrajectory_streamer.py`
  - `scarajectory/core/service/communication/event/move_event_factory.py` (NEW)
  - `scarajectory/core/service/communication/event/fault_event_factory.py` (NEW)
  - `scarajectory/core/service/communication/telemetry/idiagnostics_snapshot_factory.py` (NEW)
  - `scarajectory/core/service/communication/telemetry/diagnostics_snapshot_factory.py` (NEW)
- **Violation Category:** Strategy Pattern, Interface Segregation Principle (ISP), Dependency Inversion Principle (DIP).
- **Violation Rationale:**
  1. **Tight Coupling to Text Protocol in Streaming Service Contracts:** `ITrajectoryStreamer` and `TrajectoryStreamer` are currently locked to Cartesian waypoint lists (`TrajectoryPlan`). When a user compiles a DSL program to `ScaraBinaryProgram` (which contains pre-calculated `JointSteps`), there is no service contract allowing direct streaming of `ScaraBinaryProgram` or `tuple[JointSteps, ...]`.
  2. **Lack of Abstract Flow Control Protocol:** `FlowController` in infrastructure is currently concrete without an abstract `@runtime_checkable Protocol` in `core/service/communication/`. Furthermore, flow control in ASCII mode depends on text `<RESP:ACK#QUEUE=3>` strings, whereas binary mode flow control is governed by `MSG_RESP_ACK` free buffer slot counts and segment completion notifications (`MSG_RESP_MOVE_EVENT` with `MOVE_EVT_DONE`).
  3. **Absence of Unified Packet Formatting Strategy:** Outgoing packet formulation is split awkwardly between ASCII text line formatting and binary struct packing. An `IPacketStrategy` interface is needed so `StreamExecutionWorker` can stream either ASCII or binary packets via strategy injection without `if/else` protocol branching.
  4. **Missing Asynchronous Event Dispatching Protocol:** The firmware pushes asynchronous wire notifications (`MOVE_EVENT`, `FAULT_EVENT`, `DIAGNOSTICS`). An `IBinaryFrameDispatcher` protocol must be established in the service layer to decouple the byte-level frame receiver from domain state machines, progress monitors, and UI observers.
- **Proposed Decoupled Architecture:**
  - Define `IPacketStrategy` in `core/service/communication/stream/ipacket_strategy.py` with methods to encode waypoints / steps into wire payloads.
  - Define `IFlowController` in `core/service/communication/stream/iflow_controller.py` covering both line-based and frame-based windowing mechanisms.
  - Define `IBinaryFrameDispatcher` in `core/service/communication/event/ibinary_frame_dispatcher.py` with registration and dispatch methods for `MessageId` frame types.
  - Implement `BinaryFrameDispatcher` in `core/service/communication/event/binary_frame_dispatcher.py` with dedicated factory `BinaryFrameDispatcherFactory`.
  - Extend `ITrajectoryStreamer` to declare `stream_binary_program(session: StreamSession, program: ScaraBinaryProgram) -> None` or accept an iterable of `JointSteps`.
- **Actionable Execution Plan:**
  - [x] Define `IPacketStrategy` protocol in `core/service/communication/stream/ipacket_strategy.py`.
  - [x] Define `IFlowController` protocol in `core/service/communication/stream/iflow_controller.py`.
  - [x] Define `IBinaryFrameDispatcher` protocol in `core/service/communication/event/ibinary_frame_dispatcher.py`.
  - [x] Implement `BinaryFrameDispatcher` and `BinaryFrameDispatcherFactory` in `core/service/communication/`.
  - [x] Add `stream_binary_program` method to `ITrajectoryStreamer` contract.
  - [x] Update `TrajectoryStreamer` to support streaming pre-compiled binary steps directly.
  - [x] Write unit tests for new service protocols and dispatcher.

---

### Issue SVC-11: Complete Elimination of Nullable/Optional Parameters and Fallback Defaults in Service Factories and APIs
- **Status:** 🟢 RESOLVED
- **Affected Files:**
  - `scarajectory/core/service/dsl/ast/instruction_factory.py` (🟢 RESOLVED - 0 `None`, 0 defaults)
  - `scarajectory/core/service/dsl/ast/program_factory.py` (🟢 RESOLVED - 0 `None`, 0 defaults)
  - `scarajectory/core/service/config/iscara_config_loader.py` (🟢 RESOLVED - 0 `None`, 0 defaults, explicit port & options)
  - `scarajectory/infrastructure/settings/config_loader.py` (🟢 RESOLVED - 0 `None`, 0 defaults, relocated to `settings/`)
  - `scarajectory/core/service/communication/stream/config_factory.py`
  - `scarajectory/core/service/communication/stream/session_factory.py`
  - `scarajectory/core/service/kinematics/kinematics_service_factory.py` (🟢 RESOLVED - 0 `None`, pure DI with `*, bounds: ScaraBounds`)
  - `scarajectory/core/service/trajectory/trajectory_validator_factory.py`
  - `scarajectory/core/service/trajectory/trajectory_plan_factory.py`
  - `scarajectory/core/service/dsl/scara_dsl_service_factory.py`
  - `scarajectory/core/service/dsl/binary/compiler_factory.py`
  - `scarajectory/core/service/dsl/linter/scara_linter_factory.py`
  - `scarajectory/core/service/dsl/linter/scara_lint_context.py`
  - `scarajectory/core/service/dsl/parser/scara_parser_factory.py`
- **Violation Category:** Strict Null-Safety (Axiomatic Constraint), Explicit Dependency Injection, API Transparency.
- **Violation Rationale:**
  1. **Harmful Impact of `None` on System Architecture:** Allowing `| None = None` in factory methods and domain APIs creates insidious hidden defaults, obscures true dependency graphs, forces downstream consumers to perform defensive `None` checks, and invites runtime `AttributeError` or `TypeError` crashes.
  2. **Core Architectural Constraint:** In Clean Architecture and idiomatic type-safe Python, factory methods must be 100% explicit: every required collaborator, model, or configuration value must be a mandatory parameter without fallback default instantiations or nullable defaults.
  3. **Empty Collections Over `None`:** For empty collections, callers must pass explicit immutable empty collections (`parameters={}`, `instructions=()`, `waypoints=()`), never `None`.
- **Proposed Decoupled Architecture:**
  - Refactor all domain factories to eliminate `| None = None` from their signatures.
  - Require explicit arguments for every collaborator, model, or configuration item.
  - Update all caller sites across tests, setup, and GUI to supply explicit arguments.
- **Actionable Execution Plan:**
  - [x] Refactor `InstructionFactory.create` to require explicit `parameters: Mapping[str, Any]` without `None`.
  - [x] Refactor `ProgramFactory.create` to require explicit `instructions: Sequence[Instruction]` without `None`.
  - [x] Refactor `StreamConfigFactory.create` to require explicit configuration values or loaded domain models without `| None = None`.
  - [x] Refactor `StreamSessionFactory.create` to require explicit `waypoints: Sequence[Waypoint]` without `| None = None`.
  - [x] Refactor `KinematicsServiceFactory.create` to require explicit `bounds: ScaraBounds` without `| None = None`.
  - [x] Refactor `TrajectoryValidatorFactory.create` to require explicit `bounds: ScaraBounds` and `kinematics: IKinematicsService` without `| None = None`.
  - [x] Refactor `TrajectoryPlanFactory.create` to require explicit `history: IPlanHistory` without `| None = None`.
  - [x] Refactor `ScaraDslServiceFactory.create` and `CompilerFactory.create` to require explicit collaborator arguments without `| None = None`.
  - [x] Refactor `ScaraLinterFactory.create` and `ScaraLintContext` to eliminate nullable parameters and sentinel `None` values.
  - [x] Refactor `ScaraParserFactory.create` to eliminate nullable parameters and sentinel `None` values.
  - [x] Update all factory caller sites across tests, setup, and GUI.

---

### Issue SVC-12: Strict Enforcement of Factory Hierarchy ("Factory Calls Factory Only") and Abstract Interface Dependencies
- **Status:** 🟢 RESOLVED
- **Affected Submodules & Files:**
  - `scarajectory/core/service/trajectory/shape_discretizer.py` (calls `WaypointFactory.create(...)` directly)
  - `scarajectory/core/service/dsl/compiler/scara_compiler.py` (calls `TrajectoryPlanFactory.create()` and `TrajectoryValidatorFactory.create(...)` directly)
  - `scarajectory/core/service/dsl/parser/scara_parser.py` (calls `ScaraProgramFactory.create(...)` directly)
  - `scarajectory/core/service/dsl/parser/commands/motion_command_parser.py` (calls `ScaraInstructionFactory.create(...)` directly)
  - `scarajectory/core/service/dsl/parser/commands/frame_command_parser.py` (calls `ScaraInstructionFactory.create(...)` directly)
  - `scarajectory/core/service/dsl/parser/commands/flow_command_parser.py` (calls `ScaraInstructionFactory.create(...)` directly)
  - `scarajectory/core/service/trajectory/trajectory_plan_factory.py` (has inline fallback calling `PlanHistoryFactory.create()`)
  - `scarajectory/core/service/trajectory/iwaypoint_factory.py` (NEW Protocol needed)
  - `scarajectory/core/service/trajectory/itrajectory_plan_factory.py` (NEW Protocol needed)
  - `scarajectory/core/service/dsl/ast/iinstruction_factory.py` (NEW Protocol needed)
  - `scarajectory/core/service/dsl/ast/iprogram_factory.py` (NEW Protocol needed)
- **Violation Category:** Dependency Inversion Principle (DIP), Clean Architecture, Factory Encapsulation, Law of Demeter.
- **Violation Rationale:**
  1. **Core Architectural Axiom ("Factory Calls Factory Only"):** A Factory may ONLY be called inside another Factory, or inside `main.py` (the composition root). Regular runtime classes (services, compilers, parsers, discretizers) must **never** call concrete factories directly.
  2. **Abstract Interfaces Everywhere / Only Factories Work with Created Concrete Instances:** Across the application, all class dependencies and method signatures must be typed as abstract interfaces (`@runtime_checkable Protocol`). Concrete implementation classes must never be imported or coupled to by peer classes.
  3. **Runtime Instantiation via Injected Factory Interfaces:** When a domain class requires dynamic object creation at runtime (such as `ShapeDiscretizer` producing `Waypoint`s, `ScaraParser` producing `Instruction`s / `Program`s, or `ScaraCompiler` generating `TrajectoryPlan`s), it must receive an abstract factory interface via constructor dependency injection. Only factories instantiate and assemble concrete implementations.
- **Proposed Decoupled Architecture:**
  - Define structural factory protocols in `core/service/`:
    - `IWaypointFactory` in `core/service/trajectory/iwaypoint_factory.py`.
    - `ITrajectoryPlanFactory` in `core/service/trajectory/itrajectory_plan_factory.py`.
    - `IInstructionFactory` in `core/service/dsl/ast/iinstruction_factory.py`.
    - `IProgramFactory` in `core/service/dsl/ast/iprogram_factory.py`.
  - Refactor `ShapeDiscretizer` to accept `IWaypointFactory` in its constructor, wired via `ShapeDiscretizerFactory`.
  - Refactor `ScaraCompiler` to accept `ITrajectoryPlanFactory` and `ITrajectoryValidator` in its constructor, eliminating calls to `TrajectoryPlanFactory` and `TrajectoryValidatorFactory`.
  - Refactor `ScaraParser` and command parser handlers to receive `IInstructionFactory` and `IProgramFactory`, wired via `ScaraParserFactory`.
- **Actionable Execution Plan:**
  - [x] Define `IWaypointFactory` protocol in `core/service/trajectory/iwaypoint_factory.py`.
  - [x] Define `ITrajectoryPlanFactory` protocol in `core/service/trajectory/itrajectory_plan_factory.py`.
  - [x] Define `IInstructionFactory` protocol in `core/service/dsl/ast/iinstruction_factory.py`.
  - [x] Define `IProgramFactory` protocol in `core/service/dsl/ast/iprogram_factory.py`.
  - [x] Refactor `ShapeDiscretizer` to accept `IWaypointFactory` in constructor and call `self._waypoint_factory.create(...)`.
  - [x] Refactor `ScaraCompiler` to accept `ITrajectoryPlanFactory` and `ITrajectoryValidatorFactory` in constructor and remove direct calls to `TrajectoryPlanFactory` and `TrajectoryValidatorFactory`.
  - [x] Refactor `ScaraParser` and command parser handlers to receive `IInstructionFactory` and `IProgramFactory` via constructor DI.
  - [x] Update parent factories (`ShapeDiscretizerFactory`, `ScaraCompilerFactory`, `ScaraParserFactory`) to wire up concrete factories satisfying the protocols.
  - [x] Verify test suite passes without regressions.

---

### Issue SVC-13: System-Wide Elimination of `@staticmethod` in Favor of `@classmethod`
- **Status:** 🟢 RESOLVED
- **Affected Submodules & Files:**
  - `core/service/trajectory/trajectory_metrics.py`
  - `core/service/trajectory/shape_discretizer_factory.py`
  - `core/service/trajectory/plan_history_factory.py`
  - `core/service/trajectory/trajectory_plan_factory.py`
  - `core/service/trajectory/trajectory_validator_factory.py`
  - `core/service/kinematics/kinematics_service_factory.py`
  - `core/service/kinematics/scara_bounds_factory.py`
  - `core/service/kinematics/transmission_parameters_factory.py`
  - `core/service/communication/stream/config_factory.py`
  - `core/service/communication/stream/session_factory.py`
  - `core/service/dsl/scara_dsl_service_factory.py`
  - `core/service/dsl/lexer/scara_lexer_factory.py`
  - `core/service/dsl/parser/scara_parser_factory.py`
  - `core/service/dsl/compiler/scara_compiler_factory.py`
  - `core/service/dsl/linter/scara_linter_factory.py`
  - `core/service/dsl/binary/scara_binary_compiler_factory.py`
  - `core/service/service_factory.py`
- **Violation Category:** Architectural Coding Standard, Uniform Class-Method Semantics.
- **Violation Rationale:**
  Static methods (`@staticmethod`) detach methods from class hierarchies and polymorphic introspection. The project standard strictly mandates that all class-level operations, utility methods, and factory builders must be declared with `@classmethod(cls, ...)`.
- **Actionable Execution Plan:**
  - [x] Audit and convert all `@staticmethod` occurrences in `core/service/` to `@classmethod(cls, ...)`.
  - [x] Ensure `cls` is utilized as the first parameter.
  - [x] Verify that tests and callers execute identically.

---

## 🚀 Master Architectural Remediation Roadmap & Execution Plan

This section coordinates the master remediation plan across all layers, focusing on execution steps and contracts within the Application Service layer.

### 🗺️ High-Level 4-Phase Execution Roadmap

| Phase | Focus Areas | Key Issues | Target Architecture |
|---|---|---|---|
| **Phase 1** | Pure Data Models & Clean Architecture Boundaries | `MOD-09`, `SVC-04`, `SVC-05`, `SVC-06`, `SVC-08` | Relocate `IBinaryFrameBuilder` and `IScaraConfigLoader` to `core/service/`; relocate `TrajectoryPlan` and all `ITrajectory*` protocols to `core/service/trajectory/`; enforce mandatory `dsl_service` in `Service`; pure DI across all service factories. |
| **Phase 2** | Communication & Streaming Podsystem | `INF-05`, `INF-06`, `INF-09`, `INF-10` | Define and implement service protocols `IProtocolParser` and `ICommandFormatter`; streamline `TrajectoryStreamer` through dedicated factory. |
| **Phase 3** | GUI, Canvas, CAD Tools & Setup Assembly | `INF-07`, `INF-08`, `INF-11`, `INF-12`, `INF-13`, `INF-14`, `SVC-09` | Extract `IShapeDiscretizer` and `ShapeDiscretizer` into `core/service/trajectory/`; eliminate raw `Waypoint` instantiation via `WaypointFactory.create(...)`; pure factory assembly in `SCARAjectoryBundleFactory`. |
| **Phase 4** | Full Hardware & Firmware Alignment (`scara_base` RP2040) | `MOD-10`, `SVC-10`, `INF-15` | Define `IStreamPacketStrategy`, `IFlowController`, and `IBinaryFrameDispatcher` protocols; implement `BinaryFrameDispatcher`; enable direct execution of `ScaraBinaryProgram`. |

---

### 📋 Phase 1 Execution Detail for Service Layer (`SVC-04`, `SVC-05`, `SVC-06`, `SVC-08`)
- **Step 1 (SVC-04):** Create `scarajectory/core/service/communication/protocol/ibinary_frame_builder.py` (`@runtime_checkable Protocol`). Update imports in `binary_motion_compiler.py`, `binary_command_compiler.py`, and compiler factories. Delete `infrastructure/communication/protocol/binary/ibinary_frame_builder.py`.
- **Step 2 (SVC-05):** Relocate `IScaraConfigLoader` protocol to `scarajectory/core/service/config/iscara_config_loader.py`. Decouple service factories (`TrajectoryValidatorFactory`, `KinematicsServiceFactory`, `StreamConfigFactory`, `ScaraDslServiceFactory`) from `ScaraConfigLoaderFactory` by requiring injected domain models / loaders.
- **Step 3 (SVC-06):** In `scarajectory/core/service/engine.py` (`Service.__init__`), make `dsl_service: IScaraDslService` a mandatory argument without fallback defaults.
- **Step 4 (SVC-08):** Move `TrajectoryPlan`, `itrajectory_read_only.py`, `itrajectory_mutable.py`, `itrajectory_history.py`, `itrajectory_plan.py` to `core/service/trajectory/`. Create `IPlanHistory` protocol and `PlanHistoryFactory`. Implement `TrajectoryPlanFactory` injecting `history: IPlanHistory`.
- **Step 5:** Run full test suite (`python3 -m unittest discover -s tests -p "*_test.py"`).

---

### 📋 Phase 3 Execution Detail for Service Layer (`SVC-09`)
- **Step 1:** Create `IShapeDiscretizer` protocol in `scarajectory/core/service/trajectory/ishape_discretizer.py`.
- **Step 2:** Implement `ShapeDiscretizer` in `scarajectory/core/service/trajectory/shape_discretizer.py` using `WaypointFactory.create(...)`.
- **Step 3:** Implement `ShapeDiscretizerFactory` in `scarajectory/core/service/trajectory/shape_discretizer_factory.py`.
- **Step 4:** Inject `IShapeDiscretizer` into `CanvasToolHandler` in GUI infrastructure layer.

---

### 📋 Phase 4 Execution Detail for Service Layer (`SVC-10`)
- **Step 1:** Define `IPacketStrategy` in `scarajectory/core/service/communication/stream/ipacket_strategy.py`.
- **Step 2:** Define `IFlowController` in `scarajectory/core/service/communication/stream/iflow_controller.py`.
- **Step 3:** Define `IBinaryFrameDispatcher` in `scarajectory/core/service/communication/event/ibinary_frame_dispatcher.py`.
- **Step 4:** Implement `BinaryFrameDispatcher` and `BinaryFrameDispatcherFactory` in `scarajectory/core/service/communication/`.
- **Step 5:** Extend `ITrajectoryStreamer` in `scarajectory/core/service/communication/stream/itrajectory_streamer.py` to declare `stream_binary_program(self, session: StreamSession, program: ScaraBinaryProgram) -> None`.
- **Step 6:** Update unit test suite in `tests/service_test.py`.

---

### 🧪 Acceptance Criteria for Service Layer
- [x] High-level services depend strictly on `@runtime_checkable Protocol` abstractions.
- [x] Zero imports from `infrastructure/` inside `core/service/` (Clean Architecture boundary preserved).
- [x] 100% of concrete service instantiations take place in dedicated `*_factory.py` modules.
- [x] Factory modules call child factory modules and inject dependencies into child factories.
- [x] Zero fallback default instantiations in service constructors.
- [x] Zero or strictly minimized private methods across service classes (systematic decomposition into dedicated collaborating components).
- [x] Full test suite execution passes (190/190 tests passing).
- [x] Structural protocols `IPacketStrategy`, `IFlowController`, and `IBinaryFrameDispatcher` defined in `core/service/communication/`.
- [x] `BinaryFrameDispatcher` implemented with zero private methods and assembled via factory.
- [x] `ITrajectoryStreamer` supports direct binary program streaming.
---

### Issue SVC-14: Interface Segregation Principle (ISP) Decomposition of Robot Controller
- **Status:** 🟢 RESOLVED
- **Affected Interfaces & Adapters:**
  - `core/service/communication/controller/imotion_controller.py` (`IMotionController`: `home`, `enable`, `disable`, `clear_fault`)
  - `core/service/communication/controller/ijog_controller.py` (`IJogController`: `jog`, `set_feedrate_override`)
  - `core/service/communication/controller/itool_controller.py` (`IToolController`: `set_vacuum_pump`, `pulse_purge_valve`, `set_valve`)
  - `core/service/communication/controller/iquery_controller.py` (`IQueryController`: `query_status`, `query_position`)
  - `core/service/communication/controller/irobot_controller.py` (`IRobotController`: composite protocol inheriting all 4 granular protocols)
  - `infrastructure/communication/controller/motion_controller.py` & `motion_controller_factory.py`
  - `infrastructure/communication/controller/jog_controller.py` & `jog_controller_factory.py`
  - `infrastructure/communication/controller/tool_controller.py` & `tool_controller_factory.py`
  - `infrastructure/communication/controller/query_controller.py` & `query_controller_factory.py`
  - `infrastructure/communication/controller/robot_controller.py` & `robot_controller_factory.py`
- **Violation Category:** Interface Segregation Principle (ISP), Single Responsibility Principle (SRP).
- **Violation Rationale:**
  `IRobotController` previously combined 10 methods spanning 4 distinct functional domains (power/homing, jogging, pneumatic tooling, and telemetry queries) into a single fat interface. Clients requiring only manual jog controls (like `JogTab`) were forced to depend on methods for vacuum pump actuation and telemetry queries.
- **Proposed Decoupled Architecture:**
  - Decompose `IRobotController` into 4 granular, focused structural protocols (`IMotionController`, `IJogController`, `IToolController`, `IQueryController`) each in its own dedicated module.
  - Define `IRobotController` as a composite `@runtime_checkable Protocol` combining all 4 interfaces.
  - Decompose concrete `RobotController` into 4 dedicated controller classes with individual factories in `infrastructure/communication/controller/`.
  - Assemble `RobotController` as a composite facade delegating to the 4 specialized controllers.
- **Actionable Execution Plan:**
  - [x] Create `IMotionController`, `IJogController`, `IToolController`, `IQueryController` protocols.
  - [x] Update `IRobotController` as a composite protocol.
  - [x] Create `MotionController`, `JogController`, `ToolController`, `QueryController` adapters and factories.
  - [x] Re-implement `RobotController` as a facade delegating to sub-controllers.
  - [x] Implement unit tests in `tests/controller_test.py`.

---

### Issue SVC-15: Interface Segregation Principle (ISP) Decomposition of Trajectory Streamer Protocol
- **Status:** 🟢 RESOLVED
- **Affected Interfaces:**
  - `core/service/communication/stream/iraw_channel.py` (`IRawChannel`: `is_connected`, `send_raw_command`, `send_raw_bytes`)
  - `core/service/communication/stream/iconnection.py` (`IConnection`: `connect_with_config`, `disconnect`, `is_connected`)
  - `core/service/communication/stream/imotion_streamer.py` (`IMotionStreamer`: `start_streaming`, `stream_binary_program`, `pause_streaming`, `resume_streaming`, `stop_streaming`)
  - `core/service/communication/stream/iobservable.py` (`IObservable`: `set_observer`)
  - `core/service/communication/stream/itrajectory_streamer.py` (`ITrajectoryStreamer`: composite protocol combining `IConnection`, `IRawChannel`, `IMotionStreamer`, `IObservable`, and declaring `get_robot_controller`)
- **Violation Category:** Interface Segregation Principle (ISP).
- **Violation Rationale:**
  `ITrajectoryStreamer` formerly bundled raw low-level transport communications, connection management, waypoint and binary program streaming execution, progress observer registration, and controller access into a single monolithic protocol. Controllers and consumers requiring only basic raw channel access (`send_raw_command`, `send_raw_bytes`) or connection control were unnecessarily forced to depend on trajectory streaming and observer management methods.
- **Proposed Decoupled Architecture:**
  - Segregate `ITrajectoryStreamer` into 4 cohesive, fine-grained structural protocols (`IRawChannel`, `IConnection`, `IMotionStreamer`, `IObservable`), each defined in its own dedicated module.
  - Compose `ITrajectoryStreamer` via structural protocol inheritance.
  - Decouple `MotionController`, `JogController`, `ToolController`, and `QueryController` to depend strictly on `IRawChannel` instead of the fat streamer interface.
- **Actionable Execution Plan:**
  - [x] Define `IRawChannel` in `core/service/communication/stream/iraw_channel.py`.
  - [x] Define `IConnection` in `core/service/communication/stream/iconnection.py`.
  - [x] Define `IMotionStreamer` in `core/service/communication/stream/imotion_streamer.py`.
  - [x] Define `IObservable` in `core/service/communication/stream/iobservable.py`.
  - [x] Refactor `ITrajectoryStreamer` as a composite `@runtime_checkable Protocol`.
  - [x] Update controllers and factories to depend on `IRawChannel`.
  - [x] Verify complete test suite execution.
### Issue SVC-16: Strict Factory Domain Boundary & Pure Dependency Injection Pattern
- **Status:** 🟢 RESOLVED
- **Guiding Architectural Pattern:** Every factory class must strictly adhere to the domain boundary principle:
  1. A factory receives via DI **ONLY** parameters that come from OUTSIDE its domain (external collaborators, external models, configurations).
  2. A factory internally constructs ALL instances and collaborators that belong to ITS OWN DOMAIN, using appropriate domain factories.
  3. No `| None = None` nullable defaults, no fallback chains, no inline `Foo()` instantiation in signature default values.
- **Affected Domain Factories:**
  - `TrajectoryValidatorFactory`: requires `kinematics: IKinematicsService` (external DI), removes `bounds` and `loader` fallback logic.
  - `TrajectoryPlanFactory`: takes zero args (no `history | None = None`), creates `PlanHistoryFactory.create()` internally.
  - `ShapeDiscretizerFactory`: removes `waypoint_factory: IWaypointFactory = WaypointFactory()`, creates `WaypointFactory()` internally.
  - `ScaraCompilerFactory`: requires `validator: ITrajectoryValidator` (external DI), removes 5 `| None = None` internal arguments and constructs them internally.
  - Sub-compiler factories (`MotionCommandCompilerFactory`, `CartesianMoveCompilerFactory`, `ArcMoveCompilerFactory`, `VerticalMoveCompilerFactory`): standardize on `@classmethod create(cls)`.
- **Actionable Execution Plan:**
  - [x] Refactor `TrajectoryValidatorFactory.create` to require `kinematics: IKinematicsService`.
  - [x] Refactor `TrajectoryPlanFactory.create` to require zero arguments and wire `PlanHistoryFactory.create()`.
  - [x] Refactor `ShapeDiscretizerFactory.create` to require zero arguments and wire `WaypointFactory()`.
  - [x] Refactor `ScaraCompilerFactory.create` to require `validator: ITrajectoryValidator` and wire internal expanders, linter, sub-compilers.
  - [x] Standardize move sub-compiler factories to `@classmethod create(cls)`.
  - [x] Update all caller sites across tests and setup.
  - [x] Run test suite to verify 100% pass rate.

---

### Issue SVC-17: Elimination of Redundant Domain Dataclass Factories & Zero-None Standardization
- **Status:** 🟢 RESOLVED
- **Affected Factories & Tests:**
  - `TransmissionParametersFactory` (deleted - was redundant wrapper around immutable `@dataclass` duplicating `scara_geometry.json`).
  - `ScaraBoundsFactory` (deleted - was redundant wrapper around immutable `@dataclass` duplicating `scara_geometry.json`).
  - Test suites migrated to `ScaraConfigLoaderFactory.create().load_bounds()` and `load_transmission()` or direct dataclass instantiation:
    - `tests/scara_dsl_service_test.py`
    - `tests/binary_streamer_test.py`
    - `tests/service_engine_test.py`
    - `tests/service_factory_test.py`
    - `tests/scara_compiler_test.py`
- **Violation Category:** DRY violation, Single Source of Truth violation, redundant boilerplate.
- **Violation Rationale:**
  `TransmissionParameters` and `ScaraBounds` are pure immutable value objects (`@dataclass(frozen=True, slots=True, kw_only=True)`). Hardcoding default numerical parameters inside dedicated factory classes duplicated the single source of truth (`scara_geometry.json`), and permitted undefined behavior with extensive `| None = None` parameter fallbacks. In production, configurations are consistently loaded via `IScaraConfigLoader` (`ScaraConfigLoaderFactory.create()`), and custom configurations can instantiate the pure dataclass directly without a factory wrapper.
- **Actionable Execution Plan:**
  - [x] Migrate test call sites to `ScaraConfigLoaderFactory.create().load_*()` or direct dataclass creation.
  - [x] Delete `scara_bounds_factory.py` and its test `tests/scara_bounds_factory_test.py`.
  - [x] Delete `transmission_parameters_factory.py` and its test `tests/transmission_parameters_factory_test.py`.
  - [x] Enforce absolute Zero-`None` parameter signatures across all remaining domain and infrastructure factories.
  - [x] Verify complete test suite execution with 100% pass rate.

---

### Issue SVC-18: Strict SOLID & DIP Alignment for Factory Interfaces & Dead Protocol Removal
- **Status:** 🟢 RESOLVED
- **Affected Files:**
  - `scarajectory/core/service/dsl/compiler/scara_compiler.py` (DIP fix: returns `ITrajectoryPlan`, removed concrete `TrajectoryPlan` import).
  - `scarajectory/core/service/dsl/binary/icompiler.py` (DIP fix: accepts `ITrajectoryPlan` in `compile_plan`).
  - `scarajectory/core/service/dsl/binary/compiler.py` (DIP fix: accepts `ITrajectoryPlan` in `compile_plan`).
  - `tests/communication_events_test.py` (removed unused factory interface imports).
  - Deleted Dead Factory Protocols (YAGNI & ISP cleanup - zero active consumers):
    - `scarajectory/core/service/communication/telemetry/idiagnostics_snapshot_factory.py`
    - `scarajectory/core/service/communication/stream/isession_factory.py`
    - `scarajectory/core/service/communication/event/ifault_event_factory.py`
    - `scarajectory/core/service/communication/event/imove_event_factory.py`
    - `scarajectory/core/service/trajectory/itrajectory_validator_factory.py`
- **Violation Category:** Dependency Inversion Principle (DIP), Interface Segregation Principle (ISP), YAGNI.
- **Violation Rationale:**
  1. **Partial Inversion in `ScaraCompiler`:** Although `ScaraCompiler` received `ITrajectoryPlanFactory`, it still directly imported `TrajectoryPlan` and annotated `compile(...) -> TrajectoryPlan`, violating DIP and creating unnecessary coupling to the concrete aggregate.
  2. **Dead Factory Protocols:** Several `I*Factory` protocols were created speculatively without any consumers in the application, cluttering the interface layer and violating ISP ("clients should not depend on interfaces they do not use, nor should unused interfaces exist without clients").
- **Actionable Execution Plan:**
  - [x] Update `ScaraCompiler.compile` signature and docstring to return `ITrajectoryPlan`.
  - [x] Remove concrete `TrajectoryPlan` import from `ScaraCompiler`.
  - [x] Update `ICompiler.compile_plan` and `Compiler.compile_plan` to accept `ITrajectoryPlan`.
  - [x] Delete all 5 dead factory protocol files.
  - [x] Remove unused imports from `communication_events_test.py`.
  - [x] Confirm all 5 remaining factory protocols (`ITrajectoryPlanFactory`, `IWaypointFactory`, `IProgramFactory`, `IInstructionFactory`, `IConfigFactory`) have active consumers.
  - [x] Verify complete test suite execution with 100% pass rate (203/203 OK).

---

### Issue SVC-19: Package Modularization & Sub-package Decomposition for Service Layer
- **Status:** 🟢 RESOLVED
- **Problem Statement:**
  The service layer contains several packages suffering from flat-package clutter where 13–26 modules are dumped into single directories without sub-packages:
  1. `scarajectory.core.service.dsl.binary` (13 modules in flat directory).
  2. `scarajectory.core.service.dsl.compiler` (20 modules in flat directory).
  3. `scarajectory.core.service.trajectory` (26 modules in flat directory).
  This flat structure reduces cohesion, makes discovery difficult, and violates Clean Architecture packaging principles.
- **Target Sub-package Architecture:**

  #### Phase 1: `scarajectory.core.service.dsl.binary` (13 modules -> 4 sub-packages)
  * `core/service/dsl/binary/` (Binary compiler orchestrator & root contracts):
    - `compiler.py`
    - `compiler_factory.py`
    - `icompiler.py`
  * `core/service/dsl/binary/command/` (Binary command packet compilation):
    - `command_compiler.py`
    - `command_compiler_factory.py`
    - `icommand_compiler.py`
  * `core/service/dsl/binary/motion/` (Binary motion trajectory compilation):
    - `motion_compiler.py`
    - `motion_compiler_factory.py`
    - `imotion_compiler.py`
  * `core/service/dsl/binary/step/` (Time-sliced joint step discretization):
    - `step_discretizer.py`
    - `step_discretizer_factory.py`
    - `istep_discretizer.py`

  #### Phase 2: `scarajectory.core.service.dsl.compiler` (20 modules -> 3 sub-packages)
  * `core/service/dsl/compiler/` (DSL compiler coordinator & compilation context):
    - `scara_compiler.py`
    - `scara_compiler_factory.py`
    - `iscara_compiler.py`
    - `scara_compiler_context.py`
  * `core/service/dsl/compiler/motion/` (Motion sub-compilers, arc interpolator):
    - `motion_command_compiler.py`, `motion_command_compiler_factory.py`
    - `cartesian_move_compiler.py`, `cartesian_move_compiler_factory.py`
    - `vertical_move_compiler.py`, `vertical_move_compiler_factory.py`
    - `arc_move_compiler.py`, `arc_move_compiler_factory.py`
    - `arc_interpolator.py`, `iarc_interpolator.py`
  * `core/service/dsl/compiler/primitive/` (Discrete non-motion primitive compilers):
    - `control_command_compiler.py`
    - `state_command_compiler.py`
    - `tool_command_compiler.py`
    - `iprimitive_compiler.py`

  #### Phase 3: `scarajectory.core.service.trajectory` (26 modules -> 6 sub-packages)
  * `core/service/trajectory/plan/` (Trajectory plan aggregate and mutation/observation contracts):
    - `trajectory_plan.py`, `trajectory_plan_factory.py`
    - `itrajectory_plan.py`, `itrajectory_plan_factory.py`
    - `itrajectory_read_only.py`, `itrajectory_mutable.py`, `itrajectory_observer.py`, `itrajectory_history.py`
  * `core/service/trajectory/history/` (Plan mutation history and undo/redo service):
    - `plan_history.py`, `plan_history_factory.py`, `iplan_history.py`
  * `core/service/trajectory/validation/` (Kinematic reachability and plan validation):
    - `trajectory_validator.py`, `trajectory_validator_factory.py`, `itrajectory_validator.py`
  * `core/service/trajectory/discretization/` (Geometric shape discretization and waypoint creation):
    - `shape_discretizer.py`, `shape_discretizer_factory.py`, `ishape_discretizer.py`
    - `waypoint_factory.py`, `iwaypoint_factory.py`
  * `core/service/trajectory/metrics/` (Path metrics and calculation services):
    - `trajectory_metrics.py`
  * `core/service/trajectory/contract/` (Composite facade role interfaces for engine):
    - `iplan_command_service.py`, `iplan_persistence_service.py`, `iplan_storage_service.py`, `iplan_validation_service.py`

- **Actionable Execution Plan:**
  - **Phase 1: `scarajectory.core.service.dsl.binary`:**
    - [x] Create sub-packages `command/`, `motion/`, `step/` under `scarajectory/core/service/dsl/binary/` with metadata-only `__init__.py`.
    - [x] Move command compiler modules (`command_compiler.py`, `command_compiler_factory.py`, `icommand_compiler.py`) to `command/`.
    - [x] Move motion compiler modules (`motion_compiler.py`, `motion_compiler_factory.py`, `imotion_compiler.py`) to `motion/`.
    - [x] Move step discretizer modules (`step_discretizer.py`, `step_discretizer_factory.py`, `istep_discretizer.py`) to `step/`.
    - [x] Update all import paths across `scarajectory` and `tests/` with single-line imports.
    - [x] Verify test suite pass rate (203/203 OK).
  - **Phase 2: `scarajectory.core.service.dsl.compiler`:**
    - [x] Create sub-packages `motion/` and `primitive/` under `scarajectory/core/service/dsl/compiler/` with metadata-only `__init__.py`.
    - [x] Move motion compiler modules (`motion_command_compiler*`, `cartesian_move_compiler*`, `vertical_move_compiler*`, `arc_move_compiler*`, `arc_interpolator*`, `iarc_interpolator.py`) to `motion/`.
    - [x] Move primitive compiler modules (`control_command_compiler.py`, `state_command_compiler.py`, `tool_command_compiler.py`, `iprimitive_compiler.py`) to `primitive/`.
    - [x] Update all import paths across `scarajectory` and `tests/` with single-line imports.
    - [x] Verify test suite pass rate (203/203 OK).
  - **Phase 3: `scarajectory.core.service.trajectory`:**
    - [x] Create sub-packages `plan/`, `history/`, `validation/`, `discretization/`, `metrics/`, `contract/` under `scarajectory/core/service/trajectory/` with metadata-only `__init__.py`.
    - [x] Move plan aggregate modules to `plan/`.
    - [x] Move history modules to `history/`.
    - [x] Move validation modules to `validation/`.
    - [x] Move shape discretization and waypoint factory modules to `discretization/`.
    - [x] Move trajectory metrics to `metrics/`.
    - [x] Move plan facade interfaces to `contract/`.
    - [x] Update all import paths across `scarajectory` and `tests/` with single-line imports.
    - [x] Verify test suite pass rate (203/203 OK).



