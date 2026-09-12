# SCARAjectory Infrastructure Architecture Audit: GUI, Communication & Domain Packaging

This document outlines the architectural analysis of the `scarajectory.infrastructure` layer, covering both the **GUI presentation layer** and the **Hardware Communication subsystem**, as well as the **Domain Subpackaging Strategy**. It identifies violations of SOLID principles, Clean / Hexagonal Architecture boundary rules, and Law of Demeter. It directly complements [`service_issues.md`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/service_issues.md) and [`model_issues.md`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/model_issues.md).

---

## The Three-Pillar Architecture Status

In Hexagonal / Clean Architecture, **Infrastructure** represents the outermost layer of driving adapters (GUI, CLI) and driven adapters (Hardware Serial/TCP, Filesystem I/O, Preferences):

```
+-----------------------------------------------------------------------------------+
|                           INFRASTRUCTURE LAYER (Adapters)                         |
|  [GUI ISSUES]                                                                     |
|  Item I1: [RESOLVED] GUI bypasses Service facade & breaks Law of Demeter          |
|  Item I2: [RESOLVED] GUI widgets execute direct filesystem I/O                    |
|  Item I3: [RESOLVED] Presentation layer formats ASCII hardware wire commands      |
|  Item I4: [RESOLVED] Hardcoded kinematics & geometry in GUI canvas renderers      |
|  Item I5: [RESOLVED] Presentation models leaked into domain core (M1 mirror)      |
|  Item I6: [RESOLVED] Thread safety risk in Tkinter UI dispatch                    |
|  Item I7: [RESOLVED] Coarse imports standard (100% granular imports achieved)     |
|  Item I8: [RESOLVED] GUI God-Component decomposition (DslTab, StreamerTab, Canvas)|
|  Item I9: [RESOLVED] Remaining CanvasRenderer granular decomposition             |
|  Item I10: [RESOLVED] GUI component domain subpackaging (dsl, canvas, stream)      |
|  Item I11: [RESOLVED] Process Spawning in DslEditorTab (EmulatorLauncher)          |
|  Item I12: [RESOLVED] DRY Violation & Hardcoded Keywords in Highlighter           |
|  Item I13: [RESOLVED] Decompose DslEditorTab (Catalog & File Dialogs)              |
|  Item I14: [RESOLVED] TrajectoryCanvas Event Binding Extraction                   |
|  Item I15: [RESOLVED] StreamerTab Progress Polling Adapter Extraction             |
|  Item I16: [RESOLVED] GUI Subpackaging (menu, toolbar, theme, controls)           |
|                                                                                   |
|  [COMMUNICATION ISSUES]                                                           |
|  Item C1: [RESOLVED] SerialStreamer God Class (decomposed into FlowController)    |
|  Item C2: [RESOLVED] Broken Dependency Inversion (TransportFactory introduced)    |
|  Item C3: [RESOLVED] Primitive Obsession in StreamConfig resolved                 |
|  Item C4: [RESOLVED] CommandFormatter god-mixin decomposed                        |
|  Item C5: [RESOLVED] Duplicated concurrency in Transports (BaseTransport)        |
|  Item C6: [RESOLVED] Missing semantic robot controller interface (IRobotController)|
|  Item C7: [RESOLVED] SerialDevicePreferences decoupled via Repository             |
|  Item C8: [RESOLVED] ISP Segregation in Streamer & Separation of RobotCtrl        |
|  Item C9: [RESOLVED] Decompose TrajectoryStreamer Worker Thread (SRP)             |
|  Item C10: [RESOLVED] TrajectoryStreamer Passthrough Method Elimination           |
|                                                                                   |
|  [PACKAGE STRUCTURAL ISSUES]                                                      |
|  Item P1: [RESOLVED] Final core domain-specific subpackages complete              |
+-----------------------------------------------------------------------------------+
```

---

## SECTION 1: GUI Presentation Layer (Items I1 – I9)

---

### Item I1: [RESOLVED] GUI Architecture & Service Decoupling – GUI Bypasses Application Service Facade and Breaks Law of Demeter

* **Resolution:** `IService` and `Service` were expanded into a full application use-case facade. `ValidationTab`, `StreamerTab`, and `AppMenuBar` call high-level methods (`validate_plan()`, `start_streaming()`, `pause_streaming()`, `clear_plan()`, `undo()`, `redo()`) directly on `self._service`, completely eliminating deep collaborator traversal.

---

### Item I2: [RESOLVED] Direct Filesystem I/O and Ad-Hoc Service Instantiation in GUI Components

* **Resolution:** Raw `open(...)` operations were eliminated from `menu_bar.py`. All trajectory plan and DSL file operations are routed through `PlanStorageService` and `ScaraDslService`. Dependency injection via `setup/factory.py` ensures services are injected rather than instantiated on the fly.

---

### Item I3: [RESOLVED] Presentation Layer Formats Hardware ASCII Wire Commands & Protocol Packets

* **Resolution:** Semantic robot control methods on [`ITrajectoryStreamer`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/service/communication/itrajectory_streamer.py) and [`IRobotController`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/service/communication/irobot_controller.py) (`home()`, `set_feedrate_override()`, `set_vacuum_pump()`, `pulse_purge_valve()`) are called by UI panels (`RobotOverridePanel`, `JogTab`). No GUI component imports `CommandFormatter` or constructs ASCII wire strings.

---

### Item I4: [RESOLVED] Hardcoded Kinematics and Geometry in GUI Canvas Renderers

* **Resolution:** Static literals ($270\,\text{mm}, 86.1\,\text{mm}$) were eliminated. `TrajectoryCanvas` and `CanvasRenderer` dynamically derive $R_{max}, R_{min}$, and link geometry from the active kinematics service and validation bounds loaded from configuration.

---

### Item I5: [RESOLVED] GUI State Models Belong in Infrastructure/GUI, Not Domain Core

* **Resolution:** `CanvasSettings`, `CanvasToolMode`, `CanvasInteractionState`, and `ViewportTransform` were moved from `core/model` to `scarajectory/infrastructure/gui/model/`.

---

### Item I6: [RESOLVED] Thread Safety & Direct Non-Main-Thread Tkinter UI Mutations

* **Resolution:** In `ScarajectoryGUI` ([`engine.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/infrastructure/gui/engine.py)), callbacks from background communication threads (`on_serial_log`, `on_stream_progress`) are wrapped with `self._root.after(0, ...)`, ensuring all widget modifications run strictly on the Tkinter main event loop thread.

---

### Item I7: [RESOLVED] Granular Imports & Missing Component Abstraction Contracts

* **Resolution:** Enforced 100% granular imports across the entire codebase (`0` whole-module imports). Key interfaces (`ICanvas`, `ITable`, `IControls`, `IGUI`) are defined as structural protocols.

---

### Item I8: [RESOLVED] God-Component Anti-Pattern in GUI Modules (Phase 5.3 Decomposition)

* **Resolution:** Monolithic components were broken into focused SRP modules:
  1. **`DslEditorTab` (497 lines):** Decomposed into [`dsl_editor_toolbar.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/infrastructure/gui/components/dsl_editor_toolbar.py), [`dsl_code_editor.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/infrastructure/gui/components/dsl_code_editor.py), [`dsl_console_view.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/infrastructure/gui/components/dsl_console_view.py), and slim [`dsl_editor_tab.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/infrastructure/gui/components/dsl_editor_tab.py).
  2. **`StreamerTab` (334 lines):** Decomposed into [`port_connection_panel.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/infrastructure/gui/components/port_connection_panel.py), [`stream_control_panel.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/infrastructure/gui/components/stream_control_panel.py), [`robot_override_panel.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/infrastructure/gui/components/robot_override_panel.py), and slim [`streamer_tab.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/infrastructure/gui/components/streamer_tab.py).
  3. **`TrajectoryCanvas` (374 lines):** Decomposed by extracting mouse click and drag processing into [`canvas_mouse_handler.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/infrastructure/gui/components/canvas_mouse_handler.py).
  4. **`GuiEventMediator`:** Added [`gui_event_mediator.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/infrastructure/gui/gui_event_mediator.py) to decouple UI selection and observer dispatching.

---

### Item I9: [RESOLVED] Granular Decomposition of `CanvasRenderer`

* **Files:**
  * [`scarajectory/infrastructure/gui/components/canvas_background_renderer.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/infrastructure/gui/components/canvas_background_renderer.py)
  * [`scarajectory/infrastructure/gui/components/canvas_trajectory_renderer.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/infrastructure/gui/components/canvas_trajectory_renderer.py)
  * [`scarajectory/infrastructure/gui/components/canvas_preview_renderer.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/infrastructure/gui/components/canvas_preview_renderer.py)
  * [`scarajectory/infrastructure/gui/components/canvas_renderer.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/infrastructure/gui/components/canvas_renderer.py)

#### Resolution:
* Extracted background geometry (polar rays, concentric circles, Cartesian axes, reach boundary, deadzone crescent) to [`CanvasBackgroundRenderer`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/infrastructure/gui/components/canvas_background_renderer.py).
* Extracted trajectory drawing (waypoint nodes, coordinates/labels, path polylines, selection rings) to [`CanvasTrajectoryRenderer`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/infrastructure/gui/components/canvas_trajectory_renderer.py).
* Extracted interactive CAD mouse drag previews (circle, rectangle, line) to [`CanvasPreviewRenderer`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/infrastructure/gui/components/canvas_preview_renderer.py).
* Refactored [`CanvasRenderer`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/infrastructure/gui/components/canvas_renderer.py) into a clean, lightweight facade coordinating all 3 renderers.
* Each renderer resides in its own dedicated module file with 100% granular imports and zero `__all__` re-exports.

---

### Item I10: [RESOLVED] Elimination of Generic `gui/components/` in Favor of Domain Subpackages

* **Target:** Remove generic "junk-drawer" package [`scarajectory/infrastructure/gui/components/`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/infrastructure/gui/components/) entirely.
* **Principles Violated:** Cohesion and Module Organization (Avoid generic "components/utils" anti-pattern).

#### Proposed Architecture:
Extract components directly into domain subpackages under `scarajectory/infrastructure/gui/`:
1. **DSL Domain Subpackage (`infrastructure/gui/dsl/`):**
   * `dsl_editor_tab.py`
   * `dsl_code_editor.py`
   * `dsl_editor_toolbar.py`
   * `dsl_syntax_highlighter.py`
   * `dsl_console_view.py`
2. **Canvas Domain Subpackage (`infrastructure/gui/canvas/`):**
   * `canvas.py` (`TrajectoryCanvas`), `icanvas.py` (`ICanvas`)
   * `canvas_renderer.py` (facade)
   * `canvas_background_renderer.py`
   * `canvas_trajectory_renderer.py`
   * `canvas_preview_renderer.py`
   * `canvas_mouse_handler.py`
   * `canvas_tool_handler.py`
3. **Streaming / Hardware Domain Subpackage (`infrastructure/gui/stream/`):**
   * `streamer_tab.py`
   * `stream_control_panel.py`
   * `robot_override_panel.py`
   * `port_connection_panel.py`
   * `jog_tab.py`
4. **Trajectory Editor Domain Subpackage (`infrastructure/gui/editor/`):**
#### Execution Plan (Phase 9):
* [x] **Step 9.14:** Create domain subpackages (`gui/dsl/`, `gui/canvas/`, `gui/stream/`, `gui/editor/`) with clean metadata-only `__init__.py` files (0 `__all__`).
* [x] **Step 9.15:** Relocate DSL GUI components into `gui/dsl/`.
* [x] **Step 9.16:** Relocate Canvas GUI components into `gui/canvas/`.
* [x] **Step 9.17:** Relocate Streaming GUI components into `gui/stream/`.
* [x] **Step 9.18:** Relocate Editor GUI components into `gui/editor/`.
* [x] **Step 9.19:** Completely remove empty `scarajectory/infrastructure/gui/components/` directory.
* [x] **Step 9.20:** Update all consumer imports, tests, and Sphinx docs.

---

### Item I11: [RESOLVED] Process Spawning & External Subprocess in `DslEditorTab`

* **File:** [`scarajectory/infrastructure/gui/dsl/dsl_editor_tab.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/infrastructure/gui/dsl/dsl_editor_tab.py)
* **Launcher Adapter:** [`scarajectory/infrastructure/gui/dsl/emulator_launcher.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/infrastructure/gui/dsl/emulator_launcher.py)
* **Contract:** [`scarajectory/infrastructure/gui/dsl/iemulator_launcher.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/infrastructure/gui/dsl/iemulator_launcher.py)
* **Principles Violated:** Separation of Concerns, Clean Architecture (Infrastructure adapter concerns leaking into UI widget).

#### Analysis:
`DslEditorTab.preview_in_scaraemu()` directly imported `Popen`, created `NamedTemporaryFile`, inspected the filesystem for `SCARAEmu`, and executed a background subprocess manipulating `sys.executable` and `os.environ['PYTHONPATH']`. UI widgets must not manage OS processes or temporary files directly.

#### Resolution:
* Defined `IEmulatorLauncher(Protocol)` in `scarajectory/infrastructure/gui/dsl/iemulator_launcher.py`.
* Implemented concrete `EmulatorLauncher` in `scarajectory/infrastructure/gui/dsl/emulator_launcher.py`.
* Injected `launcher: IEmulatorLauncher | None = None` into `DslEditorTab`, delegating preview launching cleanly without leaking subprocesses or temporary files into UI presentation code.
* Added comprehensive unit tests in `tests/emulator_launcher_test.py`.

#### Execution Plan (Phase 9):
* [x] **Step 9.19:** Define `IEmulatorLauncher(Protocol)` in `infrastructure/gui/dsl/iemulator_launcher.py`.
* [x] **Step 9.20:** Implement concrete `EmulatorLauncher` in `infrastructure/gui/dsl/emulator_launcher.py`.
* [x] **Step 9.21:** Inject launcher into `DslEditorTab` and delegate preview.

---

### Item I12: [RESOLVED] DRY Violation & Keyword Duplication in `DslSyntaxHighlighter`

* **File:** [`scarajectory/infrastructure/gui/dsl/dsl_syntax_highlighter.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/infrastructure/gui/dsl/dsl_syntax_highlighter.py)
* **Principles Violated:** Single Source of Truth (SSOT), Don't Repeat Yourself (DRY).

#### Analysis:
`DslSyntaxHighlighter._commands` hardcoded a 30+ string `frozenset` duplicating command definitions from `ScaraCommandType` / `ScaraTokenType`. Adding or renaming any DSL command required manual edits in two separate packages.

#### Resolution:
* Refactored `DslSyntaxHighlighter` to dynamically derive recognized command keywords directly from `ScaraCommandType` as the Single Source of Truth.

#### Execution Plan (Phase 9):
* [x] **Step 9.22:** Refactor `DslSyntaxHighlighter` to dynamically derive recognized command keywords from `ScaraCommandType` and `ScaraTokenType`.

---

### Item I13: [RESOLVED] Embedded Demonstration Scripts & File Dialog Mixing in `DslEditorTab`

* **Files:**
  * [`scarajectory/infrastructure/gui/dsl/dsl_editor_tab.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/infrastructure/gui/dsl/dsl_editor_tab.py)
  * [`scarajectory/infrastructure/gui/dsl/dsl_example_catalog.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/infrastructure/gui/dsl/dsl_example_catalog.py)
  * [`scarajectory/infrastructure/gui/dsl/dsl_document_manager.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/infrastructure/gui/dsl/dsl_document_manager.py)
* **Principles Violated:** Single Responsibility Principle (SRP), Separation of Concerns.

#### Resolution Summary: 🟢 RESOLVED
1. Extracted hardcoded demonstration scripts and example file discovery into dedicated [`DslExampleCatalog`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/infrastructure/gui/dsl/dsl_example_catalog.py).
2. Extracted modal file dialog orchestration (`askopenfilename`, `asksaveasfilename`) and error handling into dedicated [`DslDocumentManager`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/infrastructure/gui/dsl/dsl_document_manager.py).
3. Refactored `DslEditorTab` to delegate example retrieval and file persistence, reducing file size from 368 lines to ~198 lines focused purely on Tkinter widget layout.
4. Added comprehensive unit tests in [`tests/dsl_document_manager_test.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/tests/dsl_document_manager_test.py).

#### Execution Plan (Phase 10):
* [x] **Step 10.11:** Extract `_EXAMPLE_SCRIPT` into dedicated `DslExampleCatalog`.
* [x] **Step 10.12:** Extract file dialog interactions into `DslDocumentManager`.
* [x] **Step 10.13:** Refactor `DslEditorTab` to delegate example retrieval and file persistence.

---

### Item I14: [RESOLVED] Event Binding & Canvas Lifecycle in `TrajectoryCanvas`

* **File:** [`scarajectory/infrastructure/gui/canvas/canvas.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/infrastructure/gui/canvas/canvas.py)
* **Extracted Class:** [`CanvasEventBinder`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/infrastructure/gui/canvas/canvas_event_binder.py)
* **Principles Violated:** Single Responsibility Principle (SRP), Cohesion.

#### Resolution Summary: 🟢 RESOLVED
Extracted canvas event binding orchestration, canvas resize triggers, and mouse cursor updates into dedicated [`CanvasEventBinder`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/infrastructure/gui/canvas/canvas_event_binder.py). Reduced `TrajectoryCanvas` method count to 13 methods, satisfying the SRP quality gate limit (<= 15 methods).

---

### Item I15: [RESOLVED] Progress Polling & Connection Lifecycle in `StreamerTab`

* **File:** [`scarajectory/infrastructure/gui/stream/streamer_tab.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/infrastructure/gui/stream/streamer_tab.py)
* **Extracted Class:** [`StreamProgressAdapter`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/infrastructure/gui/stream/stream_progress_adapter.py)
* **Principles Violated:** Single Responsibility Principle (SRP).

#### Resolution Summary: 🟢 RESOLVED
Extracted streaming progress status bar updates, connection state toggling, and disconnection detection log parsing into dedicated [`StreamProgressAdapter`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/infrastructure/gui/stream/stream_progress_adapter.py).

---

### Item I16: [RESOLVED] Domain Subpackaging of Core GUI Components (`menu/`, `toolbar/`, `theme/`, `controls/`)

* **Package:** [`scarajectory/infrastructure/gui/`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/infrastructure/gui)
* **Principles Violated:** Package Cohesion, Single Responsibility Principle (Package Level), Clean Architecture.

#### Resolution Summary: 🟢 RESOLVED
Decomposed root GUI components into four dedicated domain subpackages under `scarajectory/infrastructure/gui/`:
* `scarajectory/infrastructure/gui/menu/` ([`menu_bar.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/infrastructure/gui/menu/menu_bar.py), [`iapp_menu_bar.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/infrastructure/gui/menu/iapp_menu_bar.py))
* `scarajectory/infrastructure/gui/toolbar/` ([`toolbar.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/infrastructure/gui/toolbar/toolbar.py), [`itoolbar.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/infrastructure/gui/toolbar/itoolbar.py))
* `scarajectory/infrastructure/gui/theme/` ([`theme.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/infrastructure/gui/theme/theme.py))
* `scarajectory/infrastructure/gui/controls/` ([`controls.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/infrastructure/gui/controls/controls.py), [`icontrols_panel.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/infrastructure/gui/controls/icontrols_panel.py))

#### Action Points & Execution Checklist (Phase 11):
* [x] **Step 11.10:** Create `scarajectory/infrastructure/gui/toolbar/` with metadata-only `__init__.py` and relocate `toolbar.py` (extracting `IToolbar` protocol).
* [x] **Step 11.11:** Create `scarajectory/infrastructure/gui/menu/` with metadata-only `__init__.py` and relocate `menu_bar.py` (extracting `IAppMenuBar` protocol).
* [x] **Step 11.12:** Create `scarajectory/infrastructure/gui/theme/` with metadata-only `__init__.py` and relocate `theme.py`.
* [x] **Step 11.13:** Create `scarajectory/infrastructure/gui/controls/` with metadata-only `__init__.py` and relocate `controls.py`, `icontrols_panel.py`.
* [x] **Step 11.14:** Update import statements in `engine.py`, `factory.py`, and test files.
* [x] **Step 11.15:** Rebuild Sphinx API docs (`sphinx-apidoc`) with 0 warnings.

---

## SECTION 2: Communication Subsystem (Items C1 – C8)

---

### Item C1: [RESOLVED] `SerialStreamer` is a "God Class" with 7 Mixed Responsibilities

* **Resolution:** Flow control, queue capacity tracking, and barrier event synchronization were extracted to [`FlowController`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/infrastructure/communication/streamer/flow_controller.py).

---

### Item C2: [RESOLVED] Broken Dependency Inversion in `SerialStreamer`

* **Resolution:** Transport instantiation was extracted to [`TransportFactory`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/infrastructure/communication/transport/transport_factory.py). Streamers depend purely on [`ITransport`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/infrastructure/communication/transport/itransport.py).

---

### Item C3: [RESOLVED] Primitive Obsession in `StreamConfig` & Naming Misnomer

* **Resolution:** Renamed to `TrajectoryStreamer`. `StreamConfig` cleanly encapsulates host/port/baudrate parameters for both Serial and TCP channels.

---

### Item C4: [RESOLVED] `CommandFormatter` Multiple-Inheritance God-Mixin

* **Resolution:** Granular, single-responsibility formatters established: `MotionCommandFormatter`, `ConfigCommandFormatter`, and `ToolCommandFormatter`.

---

### Item C5: [RESOLVED] Duplicated Concurrency & Thread Lifecycle in Transports

* **Resolution:** Concurrency, transmission locks, and background reader worker threads were centralized in [`BaseTransport`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/infrastructure/communication/transport/base_transport.py).

---

### Item C6: [RESOLVED] Missing Semantic Robot Controller Interface (`IRobotController`)

* **Resolution:** [`IRobotController`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/service/communication/irobot_controller.py) was defined and implemented, exposing semantic actuation methods.

---

### Item C7: [RESOLVED] `SerialDevicePreferences` Hardcoded Paths & Lacks Abstraction

* **Resolution:** Abstracted via [`IConnectionPreferencesRepository`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/infrastructure/communication/preferences/iconnection_preferences_repository.py) and [`ConnectionPreferencesRepository`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/infrastructure/communication/preferences/connection_preferences_repository.py) with configurable file paths.

---

### Item C8: [RESOLVED] Interface Segregation in Communication Subsystem & Separation of `TrajectoryStreamer` and `RobotController`

* **Files:**
  * [`scarajectory/infrastructure/communication/streamer/robot_controller.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/infrastructure/communication/streamer/robot_controller.py)
  * [`scarajectory/infrastructure/communication/streamer/trajectory_streamer.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/infrastructure/communication/streamer/trajectory_streamer.py)
* **Contracts:**
  * [`ITrajectoryStreamer`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/core/service/communication/itrajectory_streamer.py)
  * [`IRobotController`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/core/service/communication/irobot_controller.py)

#### Resolution:
* Extracted manual semantic actuation methods (`home`, `enable`, `disable`, `set_feedrate_override`, `set_vacuum_pump`, `pulse_purge_valve`, `set_valve`, `jog`, `query_status`, `query_position`) into dedicated class [`RobotController`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/infrastructure/communication/streamer/robot_controller.py).
* `TrajectoryStreamer` delegates actuation calls to internal `RobotController` instance and exposes `get_robot_controller()`.

---

### Item C9: [RESOLVED] Mixed Responsibilities in `TrajectoryStreamer` (Extracting `StreamExecutionWorker`)

* **Files:**
  * [`scarajectory/infrastructure/communication/streamer/trajectory_streamer.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/infrastructure/communication/streamer/trajectory_streamer.py)
  * [`scarajectory/infrastructure/communication/streamer/stream_execution_worker.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/infrastructure/communication/streamer/stream_execution_worker.py)
* **Principles Violated:** Single Responsibility Principle (SRP).

#### Resolution Summary: 🟢 RESOLVED
1. Extracted low-level background thread execution, packet queue transmission loop, sleep intervals, and line-by-line ack parsing into dedicated [`StreamExecutionWorker`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/infrastructure/communication/streamer/stream_execution_worker.py).
2. Refactored `TrajectoryStreamer` to act as a lightweight facade coordinating `ITransport`, `StreamSession`, `RobotController`, and `StreamExecutionWorker`.
3. Added comprehensive unit tests in [`tests/stream_execution_worker_test.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/tests/stream_execution_worker_test.py).

#### Execution Plan (Phase 10):
* [x] **Step 10.14:** Implement `StreamExecutionWorker` to encapsulate background thread execution, queue transmission, and ack parsing.
* [x] **Step 10.15:** Refactor `TrajectoryStreamer` to delegate thread management to `StreamExecutionWorker`.
* [x] **Step 10.16:** Verify all communication and streaming unit tests pass.

---

### Item C10: [RESOLVED] Elimination of Passthrough Methods in `TrajectoryStreamer` (Strict ISP)

* **File:** [`scarajectory/infrastructure/communication/streamer/trajectory_streamer.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/infrastructure/communication/streamer/trajectory_streamer.py)
* **Principles Violated:** Interface Segregation Principle (ISP), Don't Repeat Yourself (DRY).

#### Resolution Summary: 🟢 RESOLVED
1. Removed the 10 redundant passthrough forwarding methods (`home`, `enable`, `disable`, `set_feedrate_override`, `set_vacuum_pump`, `pulse_purge_valve`, `set_valve`, `jog`, `query_status`, `query_position`) from `TrajectoryStreamer`.
2. Enforced direct usage of `IRobotController` (obtained via `streamer.get_robot_controller()`) in `JogTab`, `StreamerTab`, and unit tests.
3. Streamlined event callback wiring directly to `_worker.handle_incoming_line`, reducing `TrajectoryStreamer` method count to 14 methods (satisfying the SRP quality gate limit of <= 15 methods).

---

## SECTION 3: Storage & Configuration Subsystems

---

### Item S1: [RESOLVED] Direct Disk I/O Moved Out of Domain & Presentation

* **Resolution:** Centralized in [`PlanStorageService`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/infrastructure/storage/plan_storage_service.py).

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


