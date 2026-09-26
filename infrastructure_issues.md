# Infrastructure Layer Architectural Audit (`infrastructure_issues.md`)

This document tracks architectural compliance, SOLID principles, decomposition requirements, and clean boundary separation for the **Infrastructure / Adapters** layer (`scarajectory/infrastructure/`).

---

## 🏛️ Infrastructure Layer Guiding Principles (Source of Truth)

1. **SOLID Principles Compliance & Clean Architecture:** Infrastructure adapters, storage codecs, communication streamers, and GUI components must strictly adhere to Single Responsibility (SRP), Open/Closed (OCP), Liskov Substitution (LSP), Interface Segregation (ISP), and Dependency Inversion (DIP). Infrastructure adapters depend strictly on service protocols and pure domain models.
2. **Factory Hierarchy Rule ("Factory Calls Factory Only"):** A Factory can **ONLY** be called inside another Factory, or inside `main.py` (the top-level composition root / entry point). **A Factory must NEVER be called inside regular classes** (streamers, workers, controllers, GUI tabs, canvas handlers, widgets, tools). GUI components and adapters must receive pre-assembled dependencies or abstract factory protocols via constructor injection.
3. **Abstract Interfaces Everywhere / Only Factories Work with Created Concrete Instances:** Across infrastructure and presentation, all component dependencies and collaborator types must be typed as abstract interfaces (`@runtime_checkable Protocol`). **Only factory modules instantiate concrete classes and wire up object graphs.** Concrete implementation classes:
   - Must NOT inherit from Protocol classes.
   - Must NOT import Protocol classes.
   - Must NOT use `@override`.
   - Must NOT be imported by peer domain services or adapters.
   All peer collaborations flow strictly through abstract protocols.
4. **No `@staticmethod`, Strict `@classmethod` Everywhere:** Static methods (`@staticmethod`) are strictly forbidden across infrastructure factories and adapters. All class-level factory methods and helpers must be declared as `@classmethod(cls, ...)`.
5. **Zero `None` Policy (Absolute Null-Safety & Explicit Typing):** Never use `| None = None` or default `None` values in adapter constructors or factory creation methods. All parameters must be 100% explicit and non-nullable.
6. **Small Classes with 2+ Methods:** Infrastructure classes should be small, focused, and provide 2+ cohesive public methods. Monolithic god-classes (>250–300 lines) must be decomposed into collaborating components.
7. **Minimization & Elimination of Private Methods (Zero Private Methods Goal via Decomposition):** Minimize and wherever possible completely eliminate private helper methods (`_method`). Private helper methods in infrastructure adapters, streamers, GUI tabs, or workers represent hidden responsibilities. Systematically decompose internal logic into dedicated, injectable collaborating components with cohesive public interfaces. Methods must remain concise (≤15–25 lines of pure code).
8. **Pure Dependency Injection (DIP) from Parent Modules:** Collaborators, hardware transports, and configurations are always injected from parent callers/factories downwards. Classes must never instantiate concrete dependencies or use fallback default initializations.
9. **Factories as the Exclusive Instantiation Sites:** The ONLY place where concrete objects are instantiated is in factory modules. No inline `Foo()` calls or fallback defaults exist in GUI tabs, streamers, workers, or transports.
10. **Clean Presentation Separation:** GUI tabs and widgets must focus solely on rendering and view events, delegating business logic, mathematical discretization, state machines, and background execution to domain services and presenters.
11. **Encapsulation of Wire Codecs & Hardware Isolation:** All binary serialization, struct packing/unpacking, CRC calculations, frame delimiter handling, and hardware I/O live exclusively within infrastructure protocol adapters (`infrastructure/communication/protocol/`) and transports. Domain models remain 100% pure data objects.

---

## 📊 Master Status Matrix

| Component / Submodule | File | Line Count | Audit Status | Violations Identified | Actionable Remediation |
|---|---|---|---|---|---|
| `communication/streamer/` | `trajectory_streamer.py` | 368 lines | 🟢 RESOLVED | Fallback default instantiations removed, 0 private methods | Pure DI enforced with `TrajectoryStreamerFactory` |
| `communication/streamer/` | `stream_state_machine.py` | 111 lines | 🟢 COMPLIANT | None | Manages streaming lifecycle state transitions and active queries |
| `communication/streamer/` | `stream_observer_dispatcher.py` | 136 lines | 🟢 COMPLIANT | None | Dispatches progress and logging callbacks to `IObserver` |
| `communication/streamer/` | `stream_execution_worker.py` | 240 lines | 🟢 RESOLVED | Coupling removed, 0 private methods | Injected `ICommandFormatter` and configurable pacing delays |
| `communication/streamer/` | `flow_controller.py` | 155 lines | 🟢 RESOLVED | Coupling removed | Configurable capacity and injected `IProtocolParser` |
| `communication/protocol/binary/builder/` | `binary_frame_builder.py` | 169 lines | 🟢 RESOLVED | Owns wire framing and packing; uses `BinaryDelimiter` and `BinaryStructFormat` | Subpackaged under `binary/builder/`, injected `Crc16Ccitt` |
| `communication/protocol/binary/parser/` | `binary_frame_parser.py` | 210 lines | 🟢 RESOLVED | Decomposed into pure wire FSM parser and `BinaryPayloadUnpacker` | Subpackaged under `binary/parser/`, uses `ParserState` and `BinaryDelimiter` |
| `communication/protocol/binary/parser/` | `binary_payload_unpacker.py` | 219 lines | 🟢 COMPLIANT | Dedicated payload deserializer for domain events/status | Decoupled payload unpacker with `BinaryStructFormat` constants |
| `communication/protocol/binary/checksum/` | `crc16_ccitt.py` | 94 lines | 🟢 RESOLVED | Encapsulates CRC-16-CCITT calculation | Subpackaged under `binary/checksum/` |
| `communication/controller/` | `base_sub_controller.py` | 132 lines | 🟢 COMPLIANT | Base controller abstracting transport, sequence counter, and framing | Inherited by `MotionController`, `ToolController`, `JogController`, `QueryController` |
| `storage/` | `trajectory_serializer.py` | 154 lines | 🟢 RESOLVED | Relocated from `core/model/` to `infrastructure/storage/` | Clean storage serializer adapter |
| `storage/` | `plan_storage_service.py` | 178 lines | 🟢 RESOLVED | Added `save_binary_program` and `load_binary_file` | Fully supports JSON and binary persistence |
| `gui/dsl/` | `dsl_editor_tab.py` | 290 lines | 🟢 RESOLVED | Fallback removed, 0 private methods | Required DI for `dsl_service`, `DslEditorTabFactory` |
| `gui/stream/` | `streamer_tab.py` | 279 lines | 🟢 RESOLVED | Dynamic `getattr` removed | Uses explicit `get_robot_controller()` or direct DI |
| `gui/stream/` | `jog_tab.py` | 185 lines | 🟢 RESOLVED | Dynamic `getattr` removed | Uses explicit `get_robot_controller()` or direct DI |
| `gui/canvas/` | `canvas_mouse_handler.py` | 280 lines | 🟢 RESOLVED | Raw Waypoint removed, decomposed | Uses `WaypointFactory`, dedicated public methods |
| `gui/canvas/` | `canvas_tool_handler.py` | 178 lines | 🟢 RESOLVED | Extracted shape discretization to domain service (`ShapeDiscretizer`) via `IShapeDiscretizer` & `WaypointFactory` | Clean presentation layer |
| `gui/canvas/` | `canvas_background_renderer.py` | 182 lines | 🟢 RESOLVED | Introspection & hardcoded values removed | Requires `ITrajectoryValidator`, decomposed methods |
| `gui/canvas/` | `canvas.py` | 240 lines | 🟢 RESOLVED | Dead constant `R_MIN_MM` removed | Delegates to dynamic validator bounds |
| `gui/model/` | `viewport_transform.py` | 160 lines | 🟢 RESOLVED | Fallback constant removed | Parameterized `fit_reach` with dynamic `r_max_mm` |
| `gui/toolbar/` | `toolbar.py` | 206 lines | 🟢 RESOLVED | Magic values removed, 0 private methods | Dynamic reach limits from validator, `ToolbarFactory` |
| `gui/editor/` | `preview_tab.py` | 95 lines | 🟢 RESOLVED | 0 private methods, factory assembly | `PreviewTabFactory.create` enforced in controls |
| `setup/` | `factory.py` | 276 lines | 🟢 RESOLVED | Direct instantiation completely eliminated, 0 private methods | Delegated to `TransportFactory`, `TrajectoryStreamerFactory`, `PlanStorageServiceFactory`, `TrajectoryPlanFactory`, `ServiceFactory`, `ScarajectoryGUIFactory`, `CLIBundleFactory` (redundant `CLIFactory` removed) |
| `command/` | `studio_command_definition.py` & `studio_command_executor.py` | 118 / 122 lines | 🟢 RESOLVED | Command flags `--verbose` and `--dead-zone` converted to boolean `store_true` flags; strings removed | Clean CLI command options and executor handling |
| `communication/transport/` | `base_transport.py` | 263 lines | 🟡 MONITOR | 8 private template methods for connection threading | Maintain clean template pattern |
| `communication/streamer/` | `binary_stream_execution_worker.py` | New Component | 🟢 RESOLVED | Missing binary worker capable of streaming packed binary frames and parsing binary responses | Implement `BinaryStreamExecutionWorker` with `BinaryStreamExecutionWorkerFactory` |
| `communication/streamer/` | `binary_packet_strategy.py` | New Strategy | 🟢 RESOLVED | Missing packet strategy implementing `IPacketStrategy` for binary `JointSteps` | Implement `BinaryPacketStrategy` with `BinaryPacketStrategyFactory` |
| `communication/streamer/` | `flow_controller.py` | 191 lines | 🟢 RESOLVED | Dual-mode flow control supporting ASCII and binary queue depth tracking (`MSG_RESP_ACK`, `MSG_RESP_MOVE_EVENT`) | Pure flow controller satisfying `IFlowController` |
| `communication/controller/` | `robot_controller.py` | 125 lines | 🟢 RESOLVED | Sends legacy ASCII commands (`<CMD:...>`); firmware has zero ASCII parser | Add binary command packing (`MSG_CMD_ENABLE`, `MSG_CMD_HOME`, `MSG_CMD_TOOL_PUMP`, `MSG_CMD_ESTOP`) |
| `communication/transport/` | `serial_transport.py` | 110 lines | 🟢 RESOLVED | Line-buffered `readline()` fails on binary wire streams; missing raw byte stream reader | Implement non-blocking `read_bytes` / raw stream iterator for binary frames |
| `gui/stream/` | `streamer_tab.py` & `jog_tab.py` | GUI Tabs | 🟢 RESOLVED | UI assumes ASCII text log and lacks protocol mode selector and binary telemetry displays | Add protocol mode indicator/toggle and binary telemetry HUD |
| `config/` | `scara_geometry.json` & `scheme.json` | Configuration SSoT | 🟢 RESOLVED | Lacks `protocol_mode` configuration attribute in JSON schema | Add `"protocol_mode": "binary"` to config and schema |
| `settings/` | `config_loader.py` & `config_loader_factory.py` | 215 lines | 🟢 RESOLVED | Relocated from `config/` to `settings/`; standard `json` module replaced with ATS `Loader`; 0 `None`, 0 defaults | Pure configuration adapter |
| `gui/` Factory Hierarchy | Architecture Rule | 🟢 RESOLVED | GUI components (`Controls`, `CanvasToolHandler`, `StreamerTab`) calling factories directly (`INF-17`) | Factory hierarchy strictly enforced; classes receive abstract protocols or injected tabs |
| `infrastructure/` Method Modifiers | Method Modifiers | 🟢 RESOLVED | Multiple `@staticmethod` in infrastructure factories (`INF-18`) | Convert all `@staticmethod` to `@classmethod(cls, ...)` |
| `communication/controller/` | Controller Adapters | 🟢 RESOLVED | Monolithic `RobotController` combined 4 distinct control domains (`INF-19`) | Decomposed into `MotionController`, `JogController`, `ToolController`, `QueryController` with companion factories and facade |
| `communication/streamer/` | Connection Manager | 🟢 RESOLVED | `TrajectoryStreamer` burdened with direct transport resolution and raw I/O (`INF-20`) | Extracted `StreamConnectionManager` and `StreamConnectionManagerFactory` owning connection lifecycle and raw byte/command I/O |
| `communication/preferences/` | `connection_repository.py` & `iconnection_repository.py` | 149 / 63 lines | 🟢 RESOLVED | Renamed from `connection_preferences_repository` to avoid package redundancy; class names shortened to `ConnectionRepository` and `IConnectionRepository` | Clean repository and protocol conforming to 1-class-per-module rule |

---

## 🔍 Detailed Architectural Findings & Actionable Plans

### Issue INF-01: `TrajectoryStreamer` Monolithic God-Class
- **Status:** 🟢 RESOLVED
- **Affected File:** `scarajectory/infrastructure/communication/streamer/trajectory_streamer.py`
- **Violation Category:** Single Responsibility Principle (SRP), High Complexity, Monolithic Module.
- **Resolution Summary:**
  1. Extracted `StreamStateMachine` (`stream_state_machine.py`) managing valid lifecycle transitions between `IDLE`, `STREAMING`, `PAUSED`, `STOPPED`, `ERROR`, `COMPLETED`.
  2. Extracted `StreamObserverDispatcher` (`stream_observer_dispatcher.py`) encapsulating observer registration and thread-safe progress / serial logging dispatch.
  3. `TrajectoryStreamer` refactored into a pure workflow coordinator delegating state transitions and observer events to these injected collaborators.
- **Actionable Execution Plan:**
  - [x] Extract `StreamStateMachine` into dedicated module.
  - [x] Extract `StreamObserverDispatcher` into dedicated module.
  - [x] Refactor `TrajectoryStreamer` to inject these components.
  - [x] Add unit tests for `StreamStateMachine` and `StreamObserverDispatcher`.

---

### Issue INF-02: Infrastructure Codec Leaking into Domain Models
- **Status:** 🟢 RESOLVED
- **Affected Files:**
  - `scarajectory/infrastructure/communication/protocol/binary/binary_frame_builder.py`
  - `scarajectory/infrastructure/communication/protocol/binary/binary_frame_parser.py`
  - `scarajectory/core/model/communication/protocol/binary_frame.py`
  - `scarajectory/core/model/communication/protocol/joint_steps.py`
  - `scarajectory/core/model/communication/robot_status.py`
- **Violation Category:** Clean Architecture Boundary Inversion.
- **Resolution Summary:**
  All binary struct packing (`<iiiIIH`), framing delimiters (`SOF1`, `SOF2`, `EOF`), and frame serialization (`pack_frame`) are now owned exclusively by `BinaryFrameBuilder`. All framing parsing, validation, and status/joint struct unpacking (`unpack_robot_status`, `unpack_joint_steps`) are owned exclusively by `BinaryFrameParser`. Domain models are 100% pure frozen dataclasses with zero methods.
- **Actionable Execution Plan:**
  - [x] Add `pack_joint_steps` logic into `BinaryFrameBuilder`.
  - [x] Add `unpack_robot_status` and `unpack_joint_steps` logic into `BinaryFrameParser`.
  - [x] Remove `pack_payload` and `unpack_payload` from domain models.
  - [x] Remove `pack_frame` and delimiter constants from `BinaryFrame`.

---

### Issue INF-03: Relocate `TrajectorySerializer` to Infrastructure Storage
- **Status:** 🟢 RESOLVED
- **Affected File:** `scarajectory/core/model/trajectory/trajectory_serializer.py` -> `scarajectory/infrastructure/storage/trajectory_serializer.py`
- **Violation Category:** Layering & Packaging by Layer.
- **Resolution Summary:**
  `TrajectorySerializer` relocated to `scarajectory/infrastructure/storage/trajectory_serializer.py` alongside `PlanStorageService`. Also expanded with `serialize_waypoint` and `deserialize_waypoint` to allow `Waypoint` to be a 100% pure data model.
- **Actionable Execution Plan:**
  - [x] Move `trajectory_serializer.py` to `infrastructure/storage/`.
  - [x] Implement `serialize_waypoint` and `deserialize_waypoint`.
  - [x] Update import references in services, GUI, and tests.

---

### Issue INF-04: Relieve `ScaraBinaryProgram` of Direct File I/O
- **Status:** 🟢 RESOLVED
- **Affected Files:**
  - `scarajectory/core/model/dsl/binary/scara_binary_program.py`
  - `scarajectory/infrastructure/storage/plan_storage_service.py`
- **Violation Category:** Clean Architecture (I/O in Domain Model).
- **Resolution Summary:**
  `save_to_file` and filesystem imports removed from `ScaraBinaryProgram`. Added `save_binary_program(self, program: ScaraBinaryProgram, filepath: str)` and `load_binary_file(self, filepath: str) -> bytes` to `PlanStorageService`.
- **Actionable Execution Plan:**
  - [x] Add binary file saving and loading methods to `PlanStorageService`.
  - [x] Remove `save_to_file` from `ScaraBinaryProgram`.
  - [x] Verify persistence capabilities with unit tests.

---

### Issue INF-05: `TrajectoryStreamer` Lacks Dedicated Factory & Contains 5 Fallback Instantiations
- **Status:** 🟢 RESOLVED
- **Affected File:** `scarajectory/infrastructure/communication/streamer/trajectory_streamer.py`
- **Violation Category:** Dependency Inversion Principle (DIP), Single Responsibility Principle (SRP).
- **Resolution Summary:**
  `TrajectoryStreamer` refactored to require all collaborators via pure dependency injection, eliminating all 5 fallback default instantiations and achieving 0 private methods. Created `TrajectoryStreamerFactory` in `infrastructure/communication/streamer/trajectory_streamer_factory.py` along with child factories for each collaborator (`StreamStateMachineFactory`, `StreamObserverDispatcherFactory`, `RobotControllerFactory`, `FlowControllerFactory`, `StreamExecutionWorkerFactory`), wiring the complete communication subsystem cleanly.
- **Actionable Execution Plan:**
  - [x] Implement `TrajectoryStreamerFactory` with complete collaborator assembly.
  - [x] Refactor `TrajectoryStreamer.__init__` to require injected collaborators.
  - [x] Update `setup/factory.py` and unit tests.

---

### Issue INF-06: Interface Incomplete & Leaking via `getattr` in `StreamerTab` and `JogTab`
- **Status:** 🟢 RESOLVED
- **Affected Files:**
  - `scarajectory/infrastructure/gui/stream/streamer_tab.py`
  - `scarajectory/infrastructure/gui/stream/jog_tab.py`
  - `scarajectory/core/service/communication/stream/itrajectory_streamer.py`
  - `scarajectory/core/service/communication/controller/irobot_controller.py`
- **Violation Category:** Liskov Substitution Principle (LSP), Interface Segregation Principle (ISP).
- **Resolution Summary:**
  Added `get_robot_controller(self) -> IRobotController` to `ITrajectoryStreamer`. Eliminated dynamic `getattr(streamer, 'get_robot_controller', ...)` lookups in `StreamerTab` and `JogTab`, supporting direct calls and constructor DI.
- **Actionable Execution Plan:**
  - [x] Provide explicit `IRobotController` injection into `StreamerTab` and `JogTab`.
  - [x] Eliminate dynamic `getattr` lookups.

---

### Issue INF-07: `CanvasMouseHandler` Tool Mode OCP Violation & Raw Waypoint Construction
- **Status:** 🟢 RESOLVED
- **Affected Files:**
  - `scarajectory/infrastructure/gui/canvas/canvas_mouse_handler.py`
  - `scarajectory/infrastructure/gui/canvas/canvas.py`
- **Violation Category:** Open/Closed Principle (OCP), Don't Repeat Yourself (DRY).
- **Resolution Summary:**
  1. Replaced all raw `Waypoint(...)` constructions in `CanvasMouseHandler` with `WaypointFactory.create(...)`.
  2. Extracted tool operations into dedicated public methods (`commit_point`, `commit_line`, `commit_circle`, `commit_rectangle`, `handle_drag_select`, `handle_drag_freehand`).
  3. Removed dead `R_MIN_MM: ClassVar[float] = 86.1` constant from `TrajectoryCanvas`.
- **Actionable Execution Plan:**
  - [x] Replace `Waypoint` raw instantiation in `CanvasMouseHandler` with `WaypointFactory.create(...)`.
  - [x] Remove `R_MIN_MM` class attribute from `TrajectoryCanvas`.
  - [x] Refactor tool handling into tool strategy components.

---

### Issue INF-08: `DslEditorTab` Buggy Fallback Instantiation & High Line Count
- **Status:** 🟢 RESOLVED
- **Affected File:** `scarajectory/infrastructure/gui/dsl/dsl_editor_tab.py`
- **Violation Category:** Dependency Inversion Principle (DIP), Single Responsibility Principle (SRP).
- **Resolution Summary:**
  Refactored `DslEditorTab` constructor to require `dsl_service: IScaraDslService` via pure dependency injection, eliminating the broken `ScaraDslService(validator=validator)` fallback instantiation and removing concrete service imports. Created `DslEditorTabFactory` to handle assembly cleanly. Converted internal callbacks to public methods achieving 0 private methods in `DslEditorTab`.
- **Actionable Execution Plan:**
  - [x] Require mandatory injected `dsl_service` in `DslEditorTab`.
  - [x] Remove erroneous fallback instantiation.
  - [x] Create `DslEditorTabFactory` and enforce assembly via factory.

---

### Issue INF-09: `StreamExecutionWorker` Hardcoded Coupling to ASCII `CommandFormatter` (DIP/OCP)
- **Status:** 🟢 RESOLVED
- **Affected File:** `scarajectory/infrastructure/communication/streamer/stream_execution_worker.py`
- **Violation Category:** Dependency Inversion Principle (DIP), Open/Closed Principle (OCP).
- **Resolution Summary:**
  Defined `ICommandFormatter` protocol in `core/service/communication/protocol/icommand_formatter.py` and factory `CommandFormatterFactory`. Refactored `StreamExecutionWorker` to inject `ICommandFormatter` and parameterized pacing delays (`send_delay`, `throttle_delay`, `poll_delay`). Made `run_loop` public, achieving 0 private methods in worker. Implemented `StreamExecutionWorkerFactory`.
- **Actionable Execution Plan:**
  - [x] Define abstract command/packet formatter interface.
  - [x] Inject formatter strategy into `StreamExecutionWorker`.
  - [x] Extract hardcoded sleep durations into `StreamConfig` timing parameters.

---

### Issue INF-10: `FlowController` Hardcoded Ring Buffer Capacity & Static Coupling to `ProtocolParser` (DIP/OCP)
- **Status:** 🟢 RESOLVED
- **Affected File:** `scarajectory/infrastructure/communication/streamer/flow_controller.py`
- **Violation Category:** Single Source of Truth (SSoT), Dependency Inversion Principle (DIP).
- **Resolution Summary:**
  Created `ScaraResponse` (formerly `RobotResponseDTO`) pure data model and `IProtocolParser` protocol interface. Created `ProtocolParserFactory`. Refactored `FlowController` to inject `IProtocolParser` and queue capacity, eliminating all static calls to `ProtocolParser`. Added `queue_capacity` to `scara_geometry.json`, `scheme.json`, `StreamConfig`, and `ConfigFactory`. Implemented `FlowControllerFactory`.
- **Actionable Execution Plan:**
  - [x] Add queue capacity parameter to `StreamConfig` and `scara_geometry.json`.
  - [x] Define `IProtocolParser` protocol interface.
  - [x] Inject `IProtocolParser` into `FlowController`.

---

### Issue INF-11: `CanvasBackgroundRenderer` Hardcoded Robot Geometry & Duck-Typing Introspection (DIP/LSP)
- **Status:** 🟢 RESOLVED
- **Affected File:** `scarajectory/infrastructure/gui/canvas/canvas_background_renderer.py`
- **Violation Category:** Liskov Substitution Principle (LSP), Single Source of Truth (SSoT).
- **Resolution Summary:**
  `CanvasBackgroundRenderer.draw_background` strictly types `validator: ITrajectoryValidator` as a required parameter, eliminating the `float | ITrajectoryValidator` union, `hasattr` duck typing, and hardcoded physical robot link fallback constants. Decomposed the renderer into 4 focused public classmethods (`draw_polar_grid`, `draw_boundary_circles`, `draw_j1_limit_crescent`, `draw_annotations`).
- **Actionable Execution Plan:**
  - [x] Require `bounds: ScaraBounds` or `validator: ITrajectoryValidator` in `CanvasBackgroundRenderer.draw_background`.
  - [x] Remove `float | ITrajectoryValidator` union and hardcoded geometry fallback.

---

### Issue INF-12: `ViewportTransform` & `Toolbar` Hardcoded Workspace Reach Limits and Settings
- **Status:** 🟢 RESOLVED
- **Affected Files:**
  - `scarajectory/infrastructure/gui/model/viewport_transform.py`
  - `scarajectory/infrastructure/gui/toolbar/toolbar.py`
  - `scarajectory/infrastructure/gui/engine.py`
- **Violation Category:** Single Source of Truth (SSoT), Don't Repeat Yourself (DRY).
- **Resolution Summary:**
  1. Removed `R_MAX_MM: ClassVar[float] = 270.0` from `ViewportTransform` and parameterized `fit_reach` with dynamic `r_max_mm`.
  2. Dynamically formatted Toolbar reach limit text (`f'Enforce Reach Limits ({r_min:.0f}-{r_max:.0f}mm)'`) using injected kinematic reach values.
  3. Bound spinbox default speed and z parameters dynamically from configuration / bounds settings. Created `ToolbarFactory` for clean GUI assembly with zero private methods in `Toolbar`.
- **Actionable Execution Plan:**
  - [x] Inject `bounds` into `Toolbar` to dynamically display reach limits.
  - [x] Remove magic constants from `ViewportTransform` and `Toolbar`.
  - [x] Load default canvas settings from configuration.

---

### Issue INF-13: `CanvasToolHandler` Direct `Waypoint` Construction & Geometry Generation Misplaced in GUI (SRP/DRY)
- **Status:** 🟢 RESOLVED
- **Affected File:** `scarajectory/infrastructure/gui/canvas/canvas_tool_handler.py`
- **Violation Category:** Single Responsibility Principle (SRP), Don't Repeat Yourself (DRY).
- **Violation Rationale:**
  1. `discretize_line`, `discretize_circle`, and `discretize_rectangle` directly construct `Waypoint(...)` passing 7 raw arguments (`x`, `y`, `z`, `phi`, `speed`, `name`, `command`) on 8 separate occasions instead of delegating to `WaypointFactory.create(...)`.
  2. Mathematical discretization of lines, circles, and rectangles into trajectory point sequences is domain trajectory generation logic. Placing it inside GUI canvas helpers prevents headless CLI and DSL services from generating shapes without importing GUI modules.
- **Proposed Decoupled Architecture:**
  - Delegate all `Waypoint` creation to `WaypointFactory.create(...)`.
  - Extract shape discretization into a domain service (`ShapeDiscretizer` in `core/service/trajectory/`).
- **Actionable Execution Plan:**
  - [x] Replace raw `Waypoint` instantiation in `CanvasToolHandler` with `WaypointFactory.create(...)`.
  - [x] Move shape discretization logic to `core/service/trajectory/shape_discretizer.py`.

---

### Issue INF-14: `SCARAjectoryBundleFactory` Direct Instantiation of Concrete Adapters (DIP)
- **Status:** 🟢 RESOLVED
- **Affected File:** `scarajectory/setup/factory.py`
- **Violation Category:** Dependency Inversion Principle (DIP).
- **Resolution Summary:**
  Delegated component creation entirely to dedicated factory modules (`TransportFactory`, `TrajectoryStreamerFactory`, `PlanStorageServiceFactory`, `TrajectoryPlanFactory`, `ScaraConfigLoaderFactory`, `KinematicsServiceFactory`, `TrajectoryValidatorFactory`, `ScaraDslServiceFactory`). Converted `_resolve_bounds` into a public classmethod `resolve_bounds`, achieving zero private methods.
- **Actionable Execution Plan:**
  - [x] Use `TransportFactory` in `SCARAjectoryBundleFactory`.
  - [x] Use `TrajectoryStreamerFactory` once implemented.
  - [x] Use `PlanStorageServiceFactory` in `SCARAjectoryBundleFactory`.
  - [x] Make `resolve_bounds` public to maintain zero private methods.

---

### Issue INF-15: Binary Execution Worker, Dual-Protocol Streamer & Controller Adapter
- **Status:** 🟢 RESOLVED
- **Affected Files:**
  - `scarajectory/infrastructure/communication/streamer/binary_stream_execution_worker.py` (NEW)
  - `scarajectory/infrastructure/communication/streamer/binary_stream_execution_worker_factory.py` (NEW)
  - `scarajectory/infrastructure/communication/streamer/binary_packet_strategy.py` (NEW)
  - `scarajectory/infrastructure/communication/streamer/flow_controller.py`
  - `scarajectory/infrastructure/communication/controller/robot_controller.py`
  - `scarajectory/infrastructure/communication/transport/serial_transport.py`
  - `scarajectory/infrastructure/communication/transport/itransport.py`
  - `scarajectory/infrastructure/communication/protocol/binary/binary_frame_builder.py`
  - `scarajectory/infrastructure/communication/protocol/binary/binary_frame_parser.py`
  - `scarajectory/infrastructure/gui/stream/streamer_tab.py`
  - `scarajectory/infrastructure/gui/stream/jog_tab.py`
  - `scarajectory/infrastructure/config/scara_geometry.json`
  - `scarajectory/infrastructure/config/scheme.json`
- **Violation Category:** Single Responsibility Principle (SRP), Strategy Pattern, Hardware Integration Alignment.
- **Violation Rationale:**
  1. **Firmware Mismatch (Critical Operational Gap):** The new RP2040 firmware completely eliminated ASCII parsing (`main.c` executes a pure binary frame state machine). However, `StreamExecutionWorker`, `RobotController`, `FlowController`, and the GUI tabs in `scarajectory` are still hardcoded to ASCII command strings (`<pt#...>`, `<CMD:ENABLE>`, `<CMD:HOME>`, `<RESP:ACK#QUEUE=3>`). Attempting to connect `scarajectory` to the physical robot currently causes 100% frame rejection because the firmware rejects ASCII as invalid framing bytes (expecting `0xAA 0x55`).
  2. **Streaming Execution Worker Line Coupling:** `StreamExecutionWorker` writes newline-terminated strings (`transport.write_line(cmd)`) and reads responses via `transport.read_line()`. In binary protocol, frames are packed bytes (`BinaryFrameBuilder.pack_frame(...)`) and responses are binary frames decoded via `BinaryFrameParser.feed_byte()`.
  3. **Flow Control Logic Divergence:** In ASCII mode, the host decrements buffer occupancy when it sees `<RESP:ACK#QUEUE=N>`. In the firmware's binary protocol:
     - `MSG_RESP_ACK` carries `queue_free_slots` (the MCU ring buffer free space).
     - Execution progress and completion are signaled asynchronously by `MSG_RESP_MOVE_EVENT` with `MOVE_EVT_DONE` and `segment_id`.
     - Buffer management must handle this dual flow control model cleanly without spaghetti logic.
  4. **Controller Command Dispatch:** `RobotController` sends manual jog and tool commands as ASCII. It must be adapted (via `ProtocolMode` or strategy) to pack binary frames:
     - `MSG_CMD_ENABLE (0x03)`
     - `MSG_CMD_DISABLE (0x04)`
     - `MSG_CMD_ESTOP (0x05)`
     - `MSG_CMD_HOME (0x06)`
     - `MSG_CMD_TOOL_PUMP (0x0B)`
     - `MSG_CMD_TOOL_VALVE (0x0C)`
     - `MSG_CMD_QUERY_STATUS (0x09)`
     - `MSG_CMD_CLEAR_FAULT (0x0D)`
     - `MSG_CMD_BOOTLOADER (0x30)`
  5. **Serial Transport Raw Byte Stream Support:** `ITransport` and `SerialTransport` must provide raw non-blocking byte reads (`read_bytes(size: int) -> bytes`) or a byte stream iterator to feed `BinaryFrameParser` cleanly without blocking on newlines.
  6. **Configuration & GUI Alignment:** `scara_geometry.json` and its JSON schema `scheme.json` must be updated with `"protocol_mode": "binary"`. `StreamerTab` and `JogTab` must be updated to display active protocol mode and display real-time status telemetry (joint step positions, homed flags, and buffer depth).
- **Proposed Decoupled Architecture:**
  - Implement `BinaryPacketStrategy` satisfying `IPacketStrategy`.
  - Implement `BinaryStreamExecutionWorker` with `BinaryStreamExecutionWorkerFactory`.
  - Update `FlowController` to implement `IFlowController` with methods for binary ACK free slot updates and move event completion.
  - Update `RobotController` to support binary frame generation based on `StreamConfig.protocol_mode`.
  - Add `read_bytes` to `ITransport` and implement in `SerialTransport` and `VirtualSerialTransport`.
  - Add `"protocol_mode"` to `scara_geometry.json` and `scheme.json`.
  - Wire binary streaming and controller support in `SCARAjectoryBundleFactory` and `TrajectoryStreamerFactory`.
- **Actionable Execution Plan:**
  - [x] Add `"protocol_mode"` (`"binary"` / `"ascii"`) to `scara_geometry.json` and `scheme.json`.
  - [x] Add `read_bytes` method to `ITransport` and implement in `SerialTransport` and `VirtualSerialTransport`.
  - [x] Implement `BinaryPacketStrategy` in `scarajectory/infrastructure/communication/streamer/binary_packet_strategy.py`.
  - [x] Implement `BinaryStreamExecutionWorker` with `BinaryStreamExecutionWorkerFactory`.
  - [x] Update `FlowController` to handle binary `queue_free_slots` and `MoveEvent` notifications.
  - [x] Refactor `RobotController` to pack binary command frames when `protocol_mode == ProtocolMode.BINARY`.
  - [x] Update `TrajectoryStreamerFactory` and `SCARAjectoryBundleFactory` to wire binary streaming components.
  - [x] Update `StreamerTab` and `JogTab` to display protocol mode and binary telemetry.
  - [x] Add integration and unit tests for binary streaming, transport raw reads, and controller binary dispatch.

---

### Issue INF-16: Enforcement of Strict Null-Safety and Explicit Dependency Injection across Adapters and GUI Components
- **Status:** 🟢 RESOLVED
- **Affected Submodules:**
  - `infrastructure/communication/streamer/trajectory_streamer.py` (🟢 RESOLVED - 6 mandatory collaborators, 0 fallback defaults)
  - `infrastructure/gui/dsl/dsl_editor_tab.py` (🟢 RESOLVED - `dsl_service` mandatory, 0 fallback defaults)
  - `infrastructure/gui/canvas/canvas_background_renderer.py` (🟢 RESOLVED - required validator, 0 None)
  - `infrastructure/gui/toolbar/toolbar.py` (🟢 RESOLVED - dynamic bounds required, 0 None)
  - `infrastructure/setup/factory.py` (assemble via dedicated factories, pure explicit DI)
- **Violation Category:** Strict Null-Safety (Axiomatic Constraint), Explicit Dependency Injection, Elimination of Hidden Defaults.
- **Violation Rationale:**
  1. **Zero Tolerance for `None` Defaults:** In infrastructure components, accepting `| None = None` in constructors or factory methods encourages hidden fallback instantiations, circular dependencies, and fragile runtime states.
  2. **Explicit Dependency Injection:** Every hardware transport, protocol parser, command formatter, validator, and service must be explicitly passed into adapter constructors without fallback defaults.
- **Actionable Execution Plan:**
  - [x] Eliminate fallback defaults in `TrajectoryStreamer.__init__`.
  - [x] Eliminate fallback defaults in `DslEditorTab.__init__`.
  - [x] Eliminate duck-typing and None fallbacks in `CanvasBackgroundRenderer`.
  - [x] Audit remaining infrastructure components to guarantee zero optional `| None = None` collaborators.

---

### Issue INF-17: Strict Enforcement of Factory Hierarchy ("Factory Calls Factory Only") in Infrastructure and GUI Layers
- **Status:** 🟢 RESOLVED
- **Affected Submodules & Files:**
  - `scarajectory/infrastructure/gui/editor/controls.py` (directly calls `PreviewTabFactory.create(...)`)
  - `scarajectory/infrastructure/gui/canvas/canvas_tool_handler.py` (directly calls `WaypointFactory.create(...)`)
  - `scarajectory/infrastructure/gui/stream/streamer_tab.py` (receives or attempts to build internal components)
  - `scarajectory/infrastructure/gui/main_window.py`
  - `scarajectory/infrastructure/gui/gui_factory.py`
  - `scarajectory/infrastructure/gui/editor/preview_tab_factory.py`
  - `scarajectory/infrastructure/setup/factory.py` (composition root)
- **Violation Category:** Dependency Inversion Principle (DIP), Clean Presentation Separation, Factory Hierarchy.
- **Violation Rationale:**
  1. **Core Architectural Axiom ("Factory Calls Factory Only"):** A Factory can **ONLY** be called inside another Factory, or inside `main.py` (the top-level composition root). Presentation classes, GUI tabs, canvas handlers, and controls must never invoke concrete factories directly.
  2. **Abstract Interfaces Everywhere / Only Factories Work with Created Concrete Instances:** GUI components must only depend on abstract protocols (`@runtime_checkable Protocol`). They must not instantiate collaborators or invoke concrete factories.
  3. **Parent Factory Composition:** All GUI tabs (PreviewTab, DslEditorTab, StreamerTab, JogTab, Canvas) must be pre-assembled by dedicated GUI factories (e.g. `PreviewTabFactory`, `DslEditorTabFactory`, `StreamerTabFactory`, `ControlsFactory`, `ScarajectoryGUIFactory`) and injected into parent containers via constructor injection.
- **Proposed Decoupled Architecture:**
  - Refactor `Controls` so it does not invoke `PreviewTabFactory.create(...)`. Instead, `PreviewTab` is created by `ControlsFactory` or `ScarajectoryGUIFactory` and injected as `IPreviewTab` into `Controls`.
  - Refactor `CanvasToolHandler` to inject `IWaypointFactory` or use `IShapeDiscretizer` exclusively, eliminating direct calls to `WaypointFactory`.
  - Ensure all GUI factories wire child factories hierarchically, leaving GUI view classes as pure rendering/interaction layers with zero factory calls.
- **Actionable Execution Plan:**
  - [x] Refactor `Controls` to accept tabs via constructor or `ControlsPanelFactory`.
  - [x] Refactor `ControlsPanelFactory` to call `PreviewTabFactory.create(...)` and `DslEditorTabFactory.create(...)` and inject the resulting tabs into `Controls`.
  - [x] Refactor `CanvasToolHandler` to remove direct calls to `ShapeDiscretizerFactory.create(...)`.
  - [x] Refactor `CanvasMouseHandler` to inject `IWaypointFactory` and `IShapeDiscretizer`, eliminating `WaypointFactory.create(...)`.
  - [x] Refactor `StreamerTab` to inject `IConfigFactory`, eliminating `ConfigFactory.create(...)`.
  - [x] Audit GUI classes for any other direct concrete factory invocations (verified 0).
  - [x] Verify test suite passes without regressions (194/194 OK).

---

### Issue INF-18: System-Wide Elimination of `@staticmethod` in Infrastructure Factories
- **Status:** 🟢 RESOLVED
- **Affected Submodules & Files:**
  - `infrastructure/communication/streamer/trajectory_streamer_factory.py`
  - `infrastructure/communication/transport/transport_factory.py`
  - `infrastructure/storage/plan_storage_service_factory.py`
  - `infrastructure/gui/gui_factory.py`
  - `infrastructure/gui/toolbar/toolbar_factory.py`
  - `infrastructure/gui/dsl/dsl_editor_tab_factory.py`
  - `infrastructure/gui/editor/preview_tab_factory.py`
  - `infrastructure/setup/factory.py`
  - `infrastructure/cli/cli_factory.py`
- **Violation Category:** Architectural Coding Standard, Uniform Class-Method Semantics.
- **Violation Rationale:**
  Static methods (`@staticmethod`) detach methods from class hierarchies and polymorphic introspection. The project standard strictly mandates that all class-level operations, utility methods, and factory builders must be declared with `@classmethod(cls, ...)`.
- **Actionable Execution Plan:**
  - [x] Audit and convert all `@staticmethod` occurrences in `infrastructure/` to `@classmethod(cls, ...)`.
  - [x] Ensure `cls` is utilized as the first parameter.
  - [x] Verify that tests and callers execute identically.

---

### Issue INF-19: Decomposition of RobotController God-Adapter into Focused Sub-Controllers
- **Status:** 🟢 RESOLVED
- **Affected Submodules & Files:**
  - `infrastructure/communication/controller/motion_controller.py` & `motion_controller_factory.py`
  - `infrastructure/communication/controller/jog_controller.py` & `jog_controller_factory.py`
  - `infrastructure/communication/controller/tool_controller.py` & `tool_controller_factory.py`
  - `infrastructure/communication/controller/query_controller.py` & `query_controller_factory.py`
  - `infrastructure/communication/controller/robot_controller.py` & `robot_controller_factory.py`
- **Violation Category:** Single Responsibility Principle (SRP), Separation of Concerns (SoC).
- **Violation Rationale:**
  The previous `RobotController` was a monolithic adapter class handling homing/power management, manual relative jogging, vacuum and pneumatic valve actuation, and status/position polling in one module.
- **Proposed Decoupled Architecture:**
  - Decompose into 4 focused controllers (`MotionController`, `JogController`, `ToolController`, `QueryController`), each with its own dedicated factory.
  - Sub-controllers depend only on `IRawChannel` (or `IBinaryFrameBuilder`), eliminating unnecessary coupling with `TrajectoryStreamer`.
  - Provide a composite `RobotController` facade that coordinates the sub-controllers and presents a unified hardware control surface.
- **Actionable Execution Plan:**
  - [x] Implement `MotionController` and `MotionControllerFactory`.
  - [x] Implement `JogController` and `JogControllerFactory`.
  - [x] Implement `ToolController` and `ToolControllerFactory`.
  - [x] Implement `QueryController` and `QueryControllerFactory`.
  - [x] Refactor `RobotController` to delegate to sub-controllers.
  - [x] Provide `RobotControllerFactory` wiring sub-controller factories.

---

### Issue INF-20: TrajectoryStreamer God-Class Decomposition and Extraction of StreamConnectionManager
- **Status:** 🟢 RESOLVED
- **Affected Submodules & Files:**
  - `infrastructure/communication/streamer/stream_connection_manager.py`
  - `infrastructure/communication/streamer/stream_connection_manager_factory.py`
  - `infrastructure/communication/streamer/trajectory_streamer.py`
  - `infrastructure/communication/streamer/trajectory_streamer_factory.py`
- **Violation Category:** Single Responsibility Principle (SRP), God-Class Code Smell.
- **Violation Rationale:**
  `TrajectoryStreamer` was overburdened with low-level transport resolution (serial vs TCP), connection lifecycle management, listener callback registration, and raw transmission in addition to high-level trajectory worker orchestration, flow control, and observer dispatching.
- **Proposed Decoupled Architecture:**
  - Extract `StreamConnectionManager` to own transport resolution, connection opening with `StreamConfig`, disconnection, listener registration, and raw transmission.
  - Provide `StreamConnectionManagerFactory` for isolated factory creation.
  - Refactor `TrajectoryStreamer` to delegate all transport and connection lifecycle tasks directly to `StreamConnectionManager`.
- **Actionable Execution Plan:**
  - [x] Create `StreamConnectionManager` in `infrastructure/communication/streamer/stream_connection_manager.py`.
  - [x] Create `StreamConnectionManagerFactory` in `infrastructure/communication/streamer/stream_connection_manager_factory.py`.
  - [x] Refactor `TrajectoryStreamer` to inject and delegate to `StreamConnectionManager`.
  - [x] Update `TrajectoryStreamerFactory` to instantiate `StreamConnectionManager` via its factory.
  - [x] Verify all unit tests pass with zero regressions.

---

## 🚀 Master Architectural Remediation Roadmap & Execution Plan

This section coordinates the master remediation plan across all layers, focusing on execution steps and adapters within the Infrastructure / Presentation layer.

### 🗺️ High-Level 4-Phase Execution Roadmap

| Phase | Focus Areas | Key Issues | Target Architecture |
|---|---|---|---|
| **Phase 1** | Pure Data Models & Clean Architecture Boundaries | `MOD-09`, `SVC-04`, `SVC-05`, `SVC-06`, `SVC-08` | Relocate `IBinaryFrameBuilder` and `IScaraConfigLoader` to `core/service/`; relocate `TrajectoryPlan` to `core/service/trajectory/`; clean architecture boundary inversion eliminated. |
| **Phase 2** | Communication & Streaming Podsystem | `INF-05`, `INF-06`, `INF-09`, `INF-10` | Enforce explicit `IRobotController` injection without `getattr`; parameterize flow buffer capacity; inject `IProtocolParser` and `ICommandFormatter` strategies; create `TrajectoryStreamerFactory`. |
| **Phase 3** | GUI, Canvas, CAD Tools & Setup Assembly | `INF-07`, `INF-08`, `INF-11`, `INF-12`, `INF-13`, `INF-14`, `SVC-09` | Mandatory DI in `DslEditorTab`; extract domain `ShapeDiscretizer`; eliminate raw `Waypoint` instantiation via `WaypointFactory.create(...)`; dynamic workspace reach limits; assemble object graph via factories in `SCARAjectoryBundleFactory`. |
| **Phase 4** | Full Hardware & Firmware Alignment (`scara_base` RP2040) | `MOD-10`, `SVC-10`, `INF-15` | Implement `BinaryStreamExecutionWorker`, `BinaryPacketStrategy`, raw byte serial transport, binary `RobotController` command dispatch, and dual-mode UI telemetry. |

---

### 📋 Phase 2 Execution Detail for Infrastructure Layer (`INF-05`, `INF-06`, `INF-09`, `INF-10`)
- **Step 1 (INF-06):** In `ITrajectoryStreamer` (`core/service/communication/stream/itrajectory_streamer.py`), declare `get_robot_controller(self) -> IRobotController`. In `StreamerTab` and `JogTab`, eliminate `getattr` reflection and call `streamer.get_robot_controller()` or accept injected `robot_controller`.
- **Step 2 (INF-10):** Define `IProtocolParser` in `core/service/communication/protocol/iprotocol_parser.py`. Make buffer capacity configurable from `StreamConfig`. Inject `IProtocolParser` into `FlowController`. Create `FlowControllerFactory`.
- **Step 3 (INF-09):** Define `ICommandFormatter` in `core/service/communication/protocol/icommand_formatter.py`. Make `CommandFormatter` satisfy it. Inject `ICommandFormatter` into `StreamExecutionWorker`. Create `StreamExecutionWorkerFactory`.
- **Step 4 (INF-05):** In `TrajectoryStreamer.__init__`, require all 6 collaborators explicitly (`transport`, `state_machine`, `dispatcher`, `flow_controller`, `worker`, `robot_controller`) with zero fallback defaults. Implement `TrajectoryStreamerFactory` in `infrastructure/communication/streamer/trajectory_streamer_factory.py`.
- **Step 5:** Run full test suite (`python3 -m unittest discover -s tests -p "*_test.py"`).

---

### 📋 Phase 3 Execution Detail for Infrastructure Layer (`INF-07`, `INF-08`, `INF-11`, `INF-12`, `INF-13`, `INF-14`)
- **Step 1 (INF-08):** In `DslEditorTab.__init__`, require `dsl_service: IScaraDslService` via pure DI and remove invalid `ScaraDslService(validator=validator)` fallback.
- **Step 2 (INF-13 & INF-07):** In `CanvasToolHandler`, delegate shape discretization to injected `IShapeDiscretizer`. In `CanvasMouseHandler`, replace all 4 raw `Waypoint(...)` calls with `WaypointFactory.create(...)`. Remove dead `R_MIN_MM: ClassVar[float] = 86.1` from `TrajectoryCanvas`. Consolidate duplicate canvas constants into `canvas_settings.py`.
- **Step 3 (INF-11 & INF-12):** In `CanvasBackgroundRenderer.draw_background`, require `bounds: ScaraBounds` (or `validator: ITrajectoryValidator`), eliminating duck typing `hasattr` and hardcoded link dimensions (`150`, `120`). In `ViewportTransform`, eliminate hardcoded `270.0`. In `Toolbar`, dynamically display reach limits `({bounds.r_min:.0f}-{bounds.r_max:.0f}mm)`.
- **Step 4 (INF-14):** In `SCARAjectoryBundleFactory.create_bundle` (`setup/factory.py`), assemble all components via their dedicated factories: `TransportFactory`, `TrajectoryStreamerFactory`, `PlanStorageServiceFactory`, `TrajectoryPlanFactory`.
- **Step 5:** Run full test suite (`python3 -m unittest discover -s tests -p "*_test.py"`).

---

### 📋 Phase 4 Execution Detail for Infrastructure Layer (`INF-15`)
- **Step 1:** Add `"protocol_mode": "binary"` to `scara_geometry.json` and validate against `scheme.json`.
- **Step 2:** Add `read_bytes(self, size: int) -> bytes` to `ITransport` in `infrastructure/communication/transport/itransport.py` and implement non-blocking raw read in `SerialTransport` and `VirtualSerialTransport`.
- **Step 3:** Implement `BinaryPacketStrategy` in `infrastructure/communication/streamer/binary_packet_strategy.py` utilizing `BinaryFrameBuilder`.
- **Step 4:** Implement `BinaryStreamExecutionWorker` in `infrastructure/communication/streamer/binary_stream_execution_worker.py` utilizing `BinaryFrameParser.feed_byte()` to decode inbound frames.
- **Step 5:** Enhance `FlowController` in `infrastructure/communication/streamer/flow_controller.py` to handle binary free slot updates from `MSG_RESP_ACK` and completion from `MSG_RESP_MOVE_EVENT`.
- **Step 6:** Refactor `RobotController` in `infrastructure/communication/controller/robot_controller.py` to pack binary command frames when `protocol_mode == ProtocolMode.BINARY`.
- **Step 7:** Update `TrajectoryStreamerFactory` and `SCARAjectoryBundleFactory` to wire dual-protocol components based on configuration.
- **Step 8:** Update `StreamerTab` and `JogTab` to display active protocol mode and real-time status telemetry.
- **Step 9:** Run full test suite to guarantee 100% test pass rate.

---

### 🧪 Acceptance Criteria for Infrastructure Layer
- [x] Zero fallback default instantiations in streamers, controllers, workers, and GUI tabs.
- [x] 100% of concrete infrastructure instantiations take place in dedicated `*_factory.py` modules.
- [x] Presentation layer (GUI) focuses strictly on rendering and events, zero business logic.
- [x] Zero dynamic reflection hacks (`getattr`, `hasattr`) to infer interfaces or capabilities.
- [x] Zero or strictly minimized private methods across infrastructure and GUI classes (systematic decomposition into dedicated collaborating components).
- [x] Full test suite execution passes (190/190 tests passing).
- [x] `BinaryStreamExecutionWorker` and `BinaryPacketStrategy` implemented with dedicated factories.
- [x] `SerialTransport` supports non-blocking raw byte streaming via `read_bytes`.
- [x] `RobotController` supports packing binary command frames for firmware hardware control.
- [x] `scara_geometry.json` and `scheme.json` include validated `"protocol_mode"` configuration.

---

### Issue INF-09: Factory Domain Boundary & Pure Dependency Injection Compliance
- **Status:** 🟢 RESOLVED
- **Guiding Architectural Pattern:** Every infrastructure factory receives only external dependencies via DI and internally constructs all collaborating adapters belonging to its domain.
- **Affected Infrastructure Factories:**
  - `TrajectoryStreamerFactory`: requires `transport: ITransport` (external hardware DI), removes 8 `| None = None` internal arguments.
  - `BinaryPacketStrategyFactory`: requires `kinematics: IKinematicsService` and `transmission: TransmissionParameters` (external DI), constructs `BinaryFrameBuilder` internally.
  - `BinaryStreamExecutionWorkerFactory`: constructs `BinaryFrameParser` internally via `BinaryFrameParserFactory`.
  - `FlowControllerFactory`: constructs `ProtocolParser` internally via `ProtocolParserFactory`.
  - `ScarajectoryGUIFactory`: clean `create(service)` and `create_with_root(service, root)` methods.
- **Actionable Execution Plan:**
  - [x] Refactor `FlowControllerFactory.create` to eliminate `parser | None = None`.
  - [x] Refactor `BinaryPacketStrategyFactory.create` to eliminate `frame_builder | None = None`.
  - [x] Refactor `BinaryStreamExecutionWorkerFactory.create` to eliminate `frame_parser | None = None`.
  - [x] Refactor `TrajectoryStreamerFactory.create` to require `transport: ITransport` and eliminate 8 `| None = None` arguments.
  - [x] Refactor `ScarajectoryGUIFactory.create` to eliminate `root | None = None`.
  - [x] Update all callers across tests and setup.
  - [x] Run test suite to verify 100% pass rate.

---

### Issue INF-10: Systematic Zero-None Policy Enforcement Across Infrastructure & GUI Factories
- **Status:** 🟢 RESOLVED
- **Affected Factories:**
  - `StreamExecutionWorkerFactory`: removed `formatter: ICommandFormatter | None = None`; added `create(...)` (default formatter) and `create_with_formatter(...)` (explicit DI).
  - `StreamObserverDispatcherFactory`: removed `observer: IObserver | None = None`; added `create()` (empty dispatcher) and `create_with_observer(observer)` (explicit DI).
  - `PlanStorageServiceFactory`: removed `context_bundle: ContextBundle | None = None`; added `create()` (default ContextBundle) and `create_with_context(context_bundle)` (explicit DI).
  - `DslEditorTabFactory`: removed `| None = None` on storage, launcher, catalog, document_manager; added `create(...)` and `create_with_collaborators(...)`.
  - `ControlsPanelFactory`: removed ambiguous branching `if dsl_service is not None ... elif service is not None ...`; requires all parameters explicitly.
  - `ToolbarFactory`: removed `| None = None` on `r_min`, `r_max`, and `settings`; removed unused `ScaraBounds` import.
  - `CLIBundleFactory`: eliminated `| None` typed lookups; safely extracts validated keys directly from options mapping.
  - `SCARAjectoryBundleFactory`: separated into `create_bundle()` and `create_bundle_with_options(options)` and `resolve_bounds()` and `resolve_bounds_with_options(options)`, completely eliminating `options | None = None`.
  - `BinaryStreamExecutionWorkerFactory` & `BinaryStreamExecutionWorker`: eliminated dummy module-level callback functions (`_default_on_diagnostics`, `_default_on_status`) and unnecessary constructor callback parameters, logging telemetries directly through `_notify_log` with exact symmetry to `StreamExecutionWorker`.

---

### Issue INF-21: Elimination of Static `SerialDevicePreferences` Proxy and Pure DI for `ConnectionRepository`
- **Status:** 🟢 RESOLVED
- **Affected Files:**
  - `scarajectory/infrastructure/communication/preferences/connection_repository.py`
  - `scarajectory/infrastructure/communication/preferences/connection_repository_factory.py`
  - `scarajectory/infrastructure/communication/preferences/iconnection_repository.py`
  - `scarajectory/infrastructure/communication/serial_device_preferences.py` (DELETED)
  - `scarajectory/setup/factory.py`
  - `scarajectory/infrastructure/gui/gui_factory.py`
  - `scarajectory/infrastructure/gui/engine.py`
  - `scarajectory/infrastructure/gui/controls/controls_panel_factory.py`
  - `scarajectory/infrastructure/gui/stream/streamer_tab.py`
  - `scarajectory/infrastructure/gui/stream/port_connection_panel.py`
- **Violation Category:** Global Mutable State Anti-Pattern, Hidden Dependencies, Nullable Optional Parameters.
- **Resolution Summary:**
  1. `SerialDevicePreferences` was a static class proxy holding `_repository: ClassVar[IConnectionRepository | None] = None`, creating global mutable state and allowing components to bypass dependency injection.
  2. Deleted `serial_device_preferences.py` completely.
  3. `ConnectionRepository` constructor simplified to require strictly `context_bundle: ContextBundle` (the central ATS context bundle from `base_bundle.context_bundle`). Removed optional `config_file` from constructor since user configuration path is always standard `~/.config/scara/serial_device.json`.
  4. Created `ConnectionRepositoryFactory` with `@classmethod create(cls, context_bundle: ContextBundle) -> ConnectionRepository`.
  5. Wired `IConnectionRepository` down the entire GUI composition chain via strict dependency injection:
     - `SCARAjectoryBundleFactory` creates `connection_repo` via `ConnectionRepositoryFactory.create(context_bundle=base_bundle.context_bundle)`
     - Passed to `ScarajectoryGUIFactory.create(service=service, connection_repository=connection_repo)`
     - Passed to `ScarajectoryGUI(service=service, connection_repository=connection_repository)`
     - Passed to `ControlsPanelFactory.create(..., connection_repository=self._connection_repository)`
     - Passed to `StreamerTab(..., connection_repository=connection_repository)`
     - Passed to `PortConnectionPanel(..., connection_repository=connection_repository)`
- **Actionable Execution Plan:**
  - [x] Simplify `ConnectionRepository.__init__` to strictly `(context_bundle: ContextBundle)`.
  - [x] Create `ConnectionRepositoryFactory`.
  - [x] Delete `serial_device_preferences.py` and its `.rst` docs.
  - [x] Inject `IConnectionRepository` through `PortConnectionPanel`, `StreamerTab`, `ControlsPanelFactory`, `ScarajectoryGUI`, and `ScarajectoryGUIFactory`.
  - [x] Wire in `SCARAjectoryBundleFactory`.
  - [x] Update tests in `tests/transport_test.py`.
  - [x] Update Sphinx documentation and coverage tables.

---

### Issue INF-22: Elimination of Nullable Tuple in `ConnectionRepository` in Favor of `ConnectionPreference`
- **Status:** 🟢 RESOLVED
- **Affected Files:**
  - `scarajectory/core/model/communication/preferences/connection_preference.py`
  - `scarajectory/core/service/communication/preferences/connection_preference_factory.py`
  - `scarajectory/infrastructure/communication/preferences/iconnection_repository.py`
  - `scarajectory/infrastructure/communication/preferences/connection_repository.py`
  - `scarajectory/infrastructure/gui/stream/port_connection_panel.py`
  - `tests/connection_preference_test.py`
  - `tests/transport_test.py`
- **Violation Category:** Primitive Obsession, Double Nullable Return Type (`tuple[str | None, int | None]`), Violation of Zero-`None` Policy.
- **Resolution Summary:**
  1. `load_preference()` previously returned `tuple[str | None, int | None]`, which allowed invalid intermediate states, forced callers to unpack tuples, and violated Zero-`None`.
  2. Created pure domain model `ConnectionPreference(port: str, baud: int)` with 0 methods, frozen dataclass with slots.
  3. Created `ConnectionPreferenceFactory` with `@classmethod create(cls, *, port: str, baud: int)` and `@classmethod create_default(cls)`.
  4. Added `has_preference(self) -> bool` to `IConnectionRepository` and `ConnectionRepository` to check for configuration existence.
  5. Refactored `load_preference(self) -> ConnectionPreference` to always return a valid `ConnectionPreference` (defaulting when absent).
  6. Refactored `save_preference(self, preference: ConnectionPreference) -> bool` to accept strongly typed preference.
  7. Refactored `PortConnectionPanel` to use `ConnectionPreference` without any tuple unpacking or `None` checks.
- **Actionable Execution Plan:**
  - [x] Define `ConnectionPreference` pure data model in `core/model/communication/preferences/`.
  - [x] Define `ConnectionPreferenceFactory` domain factory in `core/service/communication/preferences/`.
  - [x] Update `IConnectionRepository` and `ConnectionRepository` methods.
  - [x] Update `PortConnectionPanel` to consume `ConnectionPreference`.
  - [x] Add unit tests in `tests/connection_preference_test.py` and update `tests/transport_test.py`.
  - [x] Run `./run_coverage.sh` and Sphinx build.

---

### Issue INF-23: Decomposition of Monolithic `MotionCommandFormatter` into Specialized ASCII Command Formatters
- **Status:** 🟢 RESOLVED
- **Affected Files:**
  - `scarajectory/infrastructure/communication/protocol/ascii/motion_command_formatter.py`
  - `scarajectory/infrastructure/communication/protocol/ascii/jog_command_formatter.py`
  - `scarajectory/infrastructure/communication/protocol/ascii/query_command_formatter.py`
  - `scarajectory/infrastructure/communication/protocol/ascii/system_command_formatter.py`
  - `scarajectory/infrastructure/communication/protocol/ascii/command_formatter.py`
  - `tests/protocol_test.py`
- **Violation Category:** Single Responsibility Principle (SRP), God-Class Anti-Pattern, Mixed Concerns, Nullable Default Parameters (`total_distance: float | None = None`).
- **Resolution Summary:**
  1. `MotionCommandFormatter` previously accumulated 14 methods spanning trajectory motion, manual jogging, telemetry/kinematics queries, and robot system lifecycle (enable/disable/estop/pause/resume), violating SRP and creating a bloated multi-concern class.
  2. Decomposed `MotionCommandFormatter` into 4 dedicated, focused formatters strictly following the 1-class-per-module rule:
     - `JogCommandFormatter`: manual axis jogging (`format_jog`).
     - `QueryCommandFormatter`: position and kinematics mode queries (`format_getpos`, `format_get_elbow`, `format_set_elbow`).
     - `SystemCommandFormatter`: safety, power lifecycle, and stream control (`format_enable`, `format_disable`, `format_estop`, `format_status`, `format_pause`, `format_resume`).
     - `MotionCommandFormatter`: strictly trajectory motion and packet formatting (`format_home`, `format_move`, `format_waypoint_packet`, `format_program`).
  3. Enforced Zero-`None` parameter policy on `format_program`: changed `total_distance: float | None = None` to `total_distance: float = 0.0`.
  4. Unified all formatters in `CommandFormatter` via multiple inheritance facade (`MotionCommandFormatter`, `JogCommandFormatter`, `QueryCommandFormatter`, `SystemCommandFormatter`, `ConfigCommandFormatter`, `ToolCommandFormatter`), ensuring 100% backward compatibility for all callers (`MotionController`, `JogController`, `QueryController`, `StreamExecutionWorker`, etc.) with zero regressions.
  5. Added comprehensive unit tests in `tests/protocol_test.py` validating each formatter independently and through the unified `CommandFormatter` facade.
  6. Re-generated coverage metrics and Sphinx documentation via automated tooling (`./run_coverage.sh` and `sphinx_doc`).
- **Actionable Execution Plan:**
  - [x] Create dedicated `JogCommandFormatter` with `format_jog`.
  - [x] Create dedicated `QueryCommandFormatter` with `format_getpos`, `format_get_elbow`, `format_set_elbow`.
  - [x] Create dedicated `SystemCommandFormatter` with `format_enable`, `format_disable`, `format_estop`, `format_status`, `format_pause`, `format_resume`.
  - [x] Refactor `MotionCommandFormatter` to focus purely on trajectory motion methods and eliminate `None` default on `total_distance`.
  - [x] Update `CommandFormatter` to inherit from all 6 specialized formatters.
  - [x] Add unit tests in `tests/protocol_test.py` covering all new formatters directly and via facade.
  - [x] Run `./run_coverage.sh` and `sphinx_doc` to update Sphinx docs, coverage tables, and directory trees.

---

### Issue INF-24: Subpackage Modularization of ASCII Communication Protocol (`formatter` & `parser`)
- **Status:** 🟢 RESOLVED
- **Affected Packages:**
  - `scarajectory/infrastructure/communication/protocol/ascii/formatter/`
  - `scarajectory/infrastructure/communication/protocol/ascii/parser/`
  - All calling controllers, streamers, workers, and unit tests
- **Violation Category:** Package Bloat, Mixed Responsibilities (Encoding vs Parsing Flat Organization).
- **Resolution Summary:**
  1. Reorganized the previously flat 12-module `scarajectory.infrastructure.communication.protocol.ascii` namespace into two dedicated, cohesive subpackages:
     - `formatter/`: Encapsulates all ASCII packet encoding logic, command templates registry, specialized command formatters (`MotionCommandFormatter`, `JogCommandFormatter`, `QueryCommandFormatter`, `SystemCommandFormatter`, `ConfigCommandFormatter`, `ToolCommandFormatter`), the composite `CommandFormatter` facade, and `CommandFormatterFactory`.
     - `parser/`: Encapsulates all ASCII response decoding and packet classification logic (`ProtocolParser`, `ProtocolParserFactory`).
  2. Created metadata-only `__init__.py` files for both new subpackages without `__all__` and without symbol re-exports, strictly conforming to the project architecture rule.
  3. Updated all internal and external callers across `communication/controller/`, `communication/streamer/`, `gui/editor/`, and `tests/` to use explicit, granular subpackage import paths.
  4. Removed obsolete root-level ASCII `.rst` files and regenerated documentation structure via `sphinx_doc ../scarajectory`.
  5. Ran `./run_coverage.sh` confirming all 209 unit tests pass and rebuilding coverage tables and README/index architecture trees.
- **Actionable Execution Plan:**
  - [x] Create `formatter/` and `parser/` subpackage directories with metadata-only `__init__.py`.
  - [x] Migrate formatters and `command_templates.py` into `formatter/`.
  - [x] Migrate `protocol_parser.py` and factory into `parser/`.
  - [x] Update internal imports within `formatter/` and `parser/`.
  - [x] Run `./run_coverage.sh` and verify all unit tests pass with zero regressions.

---

### Issue INF-25: Decomposition of `ProtocolParser` into `ResponseParser` and `ProtocolStatusClassifier` with Pattern Matching
- **Status:** 🟢 RESOLVED
- **Affected Files:**
  - `scarajectory/infrastructure/communication/protocol/ascii/parser/response_parser.py`
  - `scarajectory/infrastructure/communication/protocol/ascii/parser/protocol_status_classifier.py`
  - `scarajectory/infrastructure/communication/protocol/ascii/parser/protocol_parser.py`
  - `tests/protocol_test.py`
- **Violation Category:** Single Responsibility Principle (SRP), Repetitive Code Blocks, Long Waterfall If-Elif Conditionals.
- **Resolution Summary:**
  1. `ProtocolParser` previously combined two distinct concerns: raw text response parsing / regex extraction (`parse_response`, `parse_queue_depth`) and domain safety/state classification (`is_*` methods). Furthermore, `parse_response` contained a 14-branch `if-elif` conditional with 10 repetitions of packet bracket stripping.
  2. Decomposed into two specialized modules:
     - `ResponseParser`: Encapsulates raw ASCII string decoding via Python `match case` with tuple prefix matching and zero redundant string slicing, plus queue depth extraction.
     - `ProtocolStatusClassifier`: Encapsulates semantic status, completion, and safety predicates (`is_buffer_full`, `is_move_done`, `is_move_failed`, `is_action_done`, `is_complete`, `is_homed_success`, `is_homing_failed`, `is_telemetry`, `is_error`).
  3. `ProtocolParser` inherits from both `ResponseParser` and `ProtocolStatusClassifier` to maintain 100% `IProtocolParser` compatibility, and defines concrete methods `get_version() -> str` and `is_valid_packet(line: str) -> bool` (syntactic frame validation).
  4. Added comprehensive unit tests in `tests/protocol_test.py` verifying `ResponseParser`, `ProtocolStatusClassifier`, and the new facade methods on `ProtocolParser`.
  5. Ran test coverage script (`./run_coverage.sh`), achieving 210/210 passed tests and 89% total coverage.
  6. Rebuilt Sphinx documentation (`sphinx_doc ../scarajectory && make html`).
- **Actionable Execution Plan:**
  - [x] Create `ResponseParser` using `match case` pattern matching and zero redundant slicing.
  - [x] Create `ProtocolStatusClassifier` implementing domain status and safety predicates.
  - [x] Refactor `ProtocolParser` as a non-empty composite facade implementing `get_version` and `is_valid_packet`.
  - [x] Add unit tests in `tests/protocol_test.py` for direct and facade methods.
  - [x] Run `./run_coverage.sh` and Sphinx build to verify 100% success and updated docs.

---

### Issue INF-26: Subpackage Modularization of Binary Communication Protocol (`builder`, `parser`, `checksum`) & DIP Compliance
- **Status:** 🟢 RESOLVED
- **Affected Packages:**
  - `scarajectory/core/service/communication/protocol/`
  - `scarajectory/infrastructure/communication/protocol/binary/builder/`
  - `scarajectory/infrastructure/communication/protocol/binary/parser/`
  - `scarajectory/infrastructure/communication/protocol/binary/checksum/`
  - All calling controllers, streamers, workers, and unit tests
- **Violation Category:** Clean Architecture Dependency Inversion Principle (DIP) violation & Flat Package Organization.
- **Resolution Summary:**
  1. Identified that `ibinary_frame_parser.py` was mistakenly located in `infrastructure/communication/protocol/binary/` rather than in the application service layer `core/service/communication/protocol/` alongside its peer interfaces `ibinary_frame_builder.py`, `icommand_formatter.py`, and `iprotocol_parser.py`.
  2. Relocated `ibinary_frame_parser.py` to `scarajectory/core/service/communication/protocol/ibinary_frame_parser.py` establishing strict Clean Architecture DIP compliance.
  3. Reorganized the flat `scarajectory.infrastructure.communication.protocol.binary` package into three dedicated, cohesive subpackages mirroring the architectural pattern of `protocol/ascii/`:
     - `builder/`: Encapsulates binary frame composition, wire serializing, and factory (`BinaryFrameBuilder`, `BinaryFrameBuilderFactory`).
     - `parser/`: Encapsulates streaming binary frame parsing, telemetry extraction, and factory (`BinaryFrameParser`, `BinaryFrameParserFactory`).
     - `checksum/`: Encapsulates CRC-16-CCITT packet validation algorithm (`Crc16Ccitt`).
  4. Created metadata-only `__init__.py` files for each subpackage (`builder/`, `parser/`, `checksum/`, and root `binary/`) without `__all__` and without symbol re-exports, strictly conforming to the project architecture rule.
  5. Updated all internal imports and external consumers across `core/service/dsl/`, `infrastructure/communication/controller/`, `infrastructure/communication/streamer/`, and `tests/` (`binary_compiler_test.py`, `binary_streamer_test.py`, `controller_test.py`).
  6. Refined `BinaryFrameBuilder` to eliminate all magic struct format strings by extracting `TOOL_CMD_FORMAT = '<BB'`, `HEADER_FORMAT = '<BBB'`, and `TRAILER_FORMAT = '<HB'` alongside `JOINT_STEPS_FORMAT`, ensuring full symmetry between CRC header calculation and wire frame serialization.
  7. Verified that all 211 unit tests pass with zero regressions.
  8. Regenerated Sphinx documentation (`sphinx_doc scarajectory && make html`) and ran `./run_coverage.sh` (89% total coverage).
- **Actionable Execution Plan:**
  - [x] Relocate `ibinary_frame_parser.py` to `core/service/communication/protocol/ibinary_frame_parser.py`.
  - [x] Create `builder/`, `parser/`, and `checksum/` subdirectories with metadata-only `__init__.py`.
  - [x] Move concrete classes into their respective subpackages.
  - [x] Update internal imports within `builder/`, `parser/`, and external callers.
  - [x] Extract `TOOL_CMD_FORMAT`, `HEADER_FORMAT`, `TRAILER_FORMAT` class-level struct constants in `BinaryFrameBuilder`.
  - [x] Run unit tests and `./run_coverage.sh` (all 211 tests passing).
  - [x] Rebuild Sphinx documentation.

---

### Issue INF-27: Comprehensive SRP Decomposition and De-duplication of Binary Protocol and Sub-Controllers
- **Status:** 🟢 RESOLVED
- **Affected Components:**
  - `scarajectory/core/model/communication/protocol/tool_id.py` (new)
  - `scarajectory/infrastructure/communication/protocol/binary/binary_delimiter.py` (new)
  - `scarajectory/infrastructure/communication/protocol/binary/binary_struct_format.py` (new)
  - `scarajectory/infrastructure/communication/protocol/binary/parser/parser_state.py` (new)
  - `scarajectory/infrastructure/communication/protocol/binary/parser/binary_payload_unpacker.py` (new)
  - `scarajectory/infrastructure/communication/protocol/binary/parser/binary_frame_parser.py`
  - `scarajectory/infrastructure/communication/protocol/binary/builder/binary_frame_builder.py`
  - `scarajectory/infrastructure/communication/controller/base_sub_controller.py` (new)
  - `scarajectory/infrastructure/communication/controller/motion_controller.py`
  - `scarajectory/infrastructure/communication/controller/tool_controller.py`
  - `scarajectory/infrastructure/communication/controller/jog_controller.py`
  - `scarajectory/infrastructure/communication/controller/query_controller.py`
  - All calling streamers and unit tests
- **Violation Category:** Single Responsibility Principle (SRP), DRY Violations, Magic Struct Formats, Boilerplate Duplication Across Controllers.
- **Problem Analysis:**
  1. `BinaryFrameParser` (307 lines) conflated wire streaming FSM parsing (`feed_byte`, `feed_bytes`, `reset`) with 7 domain payload struct deserializers (`unpack_scara_status`, `unpack_joint_steps`, `unpack_move_event`, `unpack_fault_event`, `unpack_ack`, `unpack_nack`, `unpack_diagnostics`).
  2. Struct format strings and delimiters (`SOF1`, `SOF2`, `EOF`, `JOINT_STEPS_FORMAT`, `'<BB'`, `'<BI'`, `'<BBI'`, `'<IIIIBBIIIIiiiiBBI'`) were duplicated or hardcoded across builder, parser, and controllers.
  3. FSM states were represented by raw magic integers (`0..8`).
  4. Sub-controllers (`MotionController`, `ToolController`, `JogController`, `QueryController`) duplicated identical connection checking, packet sequence counting (`_next_seq`), string command transmission (`_send_command`), binary frame transmission (`_send_frame`), and protocol mode dispatching (`set_protocol_mode`).
- **Resolution Summary:**
  1. **SSoT Enums Established:**
     - Created `ToolId(IntEnum)` in `scarajectory/core/model/communication/protocol/tool_id.py` defining `PUMP = 0`, `VALVE = 1`.
     - Created `BinaryDelimiter(IntEnum)` in `scarajectory/infrastructure/communication/protocol/binary/binary_delimiter.py` defining `SOF1 = 0xAA`, `SOF2 = 0x55`, `EOF = 0x0D`, `MAX_PAYLOAD_LEN = 64`.
     - Created `BinaryStructFormat(StrEnum)` in `scarajectory/infrastructure/communication/protocol/binary/binary_struct_format.py` declaring all struct pack/unpack format strings.
     - Created `ParserState(IntEnum)` in `scarajectory/infrastructure/communication/protocol/binary/parser/parser_state.py` defining explicit FSM states `SEARCH_SOF1` through `READ_EOF`.
  2. **Parser Decomposition (SRP):**
     - Extracted `BinaryPayloadUnpacker` in `parser/binary_payload_unpacker.py` providing all domain payload deserializers (`unpack_scara_status`, `unpack_robot_status`, `unpack_joint_steps`, `unpack_move_event`, `unpack_fault_event`, `unpack_ack`, `unpack_nack`, `unpack_diagnostics`, `unpack_tool_cmd`).
     - Refactored `BinaryFrameParser` to inherit from `BinaryPayloadUnpacker` (preserving full backwards compatibility), reduced line count from 307 to 210 lines, removed all private helper methods (`_handle_sof`, `_handle_header`, `_handle_tail`), and converted the state machine to a clean Python `match-case` over `ParserState`.
  3. **Builder Refactoring:**
     - Refactored `BinaryFrameBuilder` to source framing delimiters from `BinaryDelimiter` and struct formats from `BinaryStructFormat`.
  4. **Sub-Controller De-duplication:**
     - Created `BaseSubController` in `infrastructure/communication/controller/base_sub_controller.py`, encapsulating shared transport connection checking (`is_connected`), monotonic sequence counting (`_next_seq`), ASCII transmission (`_send_command`), binary frame packing/transmission (`_send_frame`), and protocol mode switching (`set_protocol_mode`).
     - Subclassed `MotionController`, `ToolController`, `JogController`, and `QueryController` from `BaseSubController`, eliminating over 200 lines of redundant boilerplate across the controller layer.
     - Converted magic integer tool IDs in `ToolController` to `ToolId.PUMP` and `ToolId.VALVE`.
  5. **Verification & Quality:**
     - Added comprehensive unit tests in `tests/binary_protocol_test.py` covering enums, unpacker methods, frame parser FSM transitions/resets, and `BaseSubController`.
     - Executed full test suite: 219/219 tests passed with 0 failures.
     - Ran `./run_coverage.sh`: achieved 89% total project test coverage.
     - Rebuilt Sphinx documentation without errors (`make -C docs html`).
- **Actionable Execution Plan:**
  - [x] **Step 1: Domain & Protocol Enums (SSoT)**
    - [x] Create `ToolId(IntEnum)` in `core/model/communication/protocol/tool_id.py` (`PUMP = 0`, `VALVE = 1`).
    - [x] Create `BinaryDelimiter(IntEnum)` in `infrastructure/communication/protocol/binary/binary_delimiter.py` (`SOF1 = 0xAA`, `SOF2 = 0x55`, `EOF = 0x0D`, `MAX_PAYLOAD_LEN = 64`).
    - [x] Create `BinaryStructFormat(StrEnum)` in `infrastructure/communication/protocol/binary/binary_struct_format.py` (all struct format strings).
    - [x] Create `ParserState(IntEnum)` in `infrastructure/communication/protocol/binary/parser/parser_state.py` (FSM states 0..8).
  - [x] **Step 2: Binary Parser Decomposition (SRP)**
    - [x] Create `BinaryPayloadUnpacker` in `parser/binary_payload_unpacker.py` encapsulating all payload deserialization methods with full docstrings and `BinaryStructFormat` constants.
    - [x] Refactor `BinaryFrameParser` to inherit from `BinaryPayloadUnpacker`, use `ParserState`, `BinaryDelimiter`, and `BinaryStructFormat`.
  - [x] **Step 3: Binary Frame Builder Refactoring**
    - [x] Update `BinaryFrameBuilder` to use `BinaryDelimiter`, `BinaryStructFormat`, and `ToolId`.
  - [x] **Step 4: Sub-Controller De-duplication**
    - [x] Create `BaseSubController` in `infrastructure/communication/controller/base_sub_controller.py` defining common state, sequence management, and transmission helpers.
    - [x] Refactor `MotionController`, `ToolController`, `JogController`, and `QueryController` to inherit from `BaseSubController`.
    - [x] Use `ToolId` in `ToolController` in place of magic numbers `0` and `1`.
  - [x] **Step 5: Verification & Documentation**
    - [x] Run full test suite (`python3 -m unittest discover tests "*_test.py"`).
    - [x] Run `./run_coverage.sh` (ensure ≥89% coverage and all tests passing).
    - [x] Rebuild Sphinx docs (`sphinx_doc scarajectory && make html`).
    - [x] Mark Issue INF-27 🟢 RESOLVED in `infrastructure_issues.md`.



