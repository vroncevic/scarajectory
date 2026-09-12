# SCARAjectory Service Layer Architecture & SOLID Audit

This document outlines the architectural analysis of the `scarajectory.core.service` layer, identifying violations of SOLID principles, Clean Architecture guidelines, and responsibilities distribution. It directly complements [`model_issues.md`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/model_issues.md) and [`infrastructure_issues.md`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/infrastructure_issues.md).

---

## Item 1: [RESOLVED] `TrajectoryValidator` – Multiple Mixed Responsibilities & Missing Kinematics Abstraction

* **File:** [`scarajectory/core/service/trajectory_validator.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/service/trajectory_validator.py)
* **Contract:** [`scarajectory/core/service/itrajectory_validator.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/service/itrajectory_validator.py)
* **Kinematics Implementation:** [`scarajectory/core/service/kinematics/kinematics_service.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/service/kinematics/kinematics_service.py)
* **Principles Violated:** Single Responsibility Principle (SRP), Open/Closed Principle (OCP).

### Resolution Summary: 🟢 RESOLVED
Analytical kinematics, forward/inverse kinematic solvers, joint angle boundaries, and annular Cartesian reach calculations ($R_{max}, R_{min}$) were extracted into [`KinematicsService`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/service/kinematics/kinematics_service.py) behind [`IKinematicsService`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/service/kinematics/ikinematics_service.py). `TrajectoryValidator` delegates geometric envelope and kinematic limits to the kinematics service. Comprehensive tests were added in `tests/kinematics_service_test.py`.

---

## Item 2: [RESOLVED] `Service` (Facade) – Domain Mutation & Collaborator Leakage

* **File:** [`scarajectory/core/service/engine.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/service/engine.py)
* **Contract:** [`scarajectory/core/service/iservice.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/service/iservice.py)
* **Principles Violated:** Single Responsibility Principle (SRP), Law of Demeter.

### Resolution Summary: 🟢 RESOLVED
`IService` and `Service` were elevated from an anemic wrapper to a true application use-case facade:
* Added methods: `new_plan()`, `clear_plan()`, `undo()`, `redo()`, `pause_streaming()`, `resume_streaming()`, `validate_plan()`, `save_plan()`, `load_plan()`.
* GUI leaf widgets (`ValidationTab`, `StreamerTab`, `AppMenuBar`) call `self._service` use cases directly rather than reaching deep into internal collaborator graphs.

---

## Item 3: [RESOLVED] `PlanStorageService` vs. `TrajectorySerializer` – Clean Architecture Boundary Violation

* **Files:**
  * [`scarajectory/infrastructure/storage/plan_storage_service.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/infrastructure/storage/plan_storage_service.py)
  * [`scarajectory/core/service/iplan_storage_service.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/service/iplan_storage_service.py)
  * [`scarajectory/core/model/trajectory_serializer.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/model/trajectory_serializer.py)
* **Principles Violated:** Clean Architecture Layers, Single Responsibility Principle (SRP).

### Resolution Summary: 🟢 RESOLVED
`TrajectorySerializer` in `core/model` was stripped of all side-effecting disk I/O and reduced to pure in-memory JSON mapping. The filesystem persistence logic (`save_plan`, `load_plan`, `save_text_file`, `load_text_file`) was implemented in `scarajectory/infrastructure/storage/plan_storage_service.py` satisfying `IPlanStorageService`.

---

## Item 4: [RESOLVED] `ScaraCompiler` – Monolithic Complexity & Overloaded Responsibilities

* **Package:** `scarajectory/core/service/dsl/`
* **Modules Created:**
  * [`scara_lexer.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/service/dsl/scara_lexer.py) (`ScaraLexer`)
  * [`scara_parser.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/service/dsl/scara_parser.py) (`ScaraParser`)
  * [`scara_compiler_context.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/service/dsl/scara_compiler_context.py) (`ScaraCompilerContext`)
  * Specialized macro expanders (`FrameMacroExpander`, `JumpMacroExpander`, `PalletMacroExpander`, `TangentMacroExpander`).
* **Principles Violated:** Single Responsibility Principle (SRP).

### Resolution Summary: 🟢 RESOLVED
The monolithic 630+ line compiler was decomposed into a modular pipeline where tokenization, AST parsing, compilation context state tracking, macro expansion, and coordinate validation are cleanly isolated.

---

## Item 5: [RESOLVED] `ScaraDslService` – Tight Coupling & Concrete Default Instantiations

* **Files:**
  * [`scarajectory/core/service/dsl/scara_dsl_service.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/service/dsl/scara_dsl_service.py)
  * [`scarajectory/setup/factory.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/setup/factory.py)
* **Principles Violated:** Dependency Inversion Principle (DIP).

### Resolution Summary: 🟢 RESOLVED
`IScaraDslService` is fully registered and wired within `setup/factory.py`. GUI tabs and consumers receive the service via dependency injection rather than ad-hoc instantiations with `new`.

---

## Item 6: [RESOLVED / EVOLUTION - Phase 7] Domain Subpackaging in `core/service`

* **Package:** `scarajectory/core/service`
* **Current Subpackages:**
  * `core/service/kinematics/` (`IKinematicsService`, `KinematicsService`)
  * `core/service/communication/` (`ITrajectoryStreamer`, `IRobotController`, `IStreamObserver`)
  * `core/service/dsl/` (Full DSL compiler subsystem)
* **Target in Phase 7:**
  * `core/service/trajectory/` (`ITrajectoryValidator`, `TrajectoryValidator`, `IPlanStorageService`)

### Execution Plan (Phase 7):
* **Step 7.8:** Create `scarajectory/core/service/trajectory/`.
* **Step 7.9:** Relocate `trajectory_validator.py`, `itrajectory_validator.py`, `iplan_storage_service.py` to `core/service/trajectory/`.
* **Step 7.10:** Re-export in `core/service/__init__.py` for 100% backward compatibility.

---

## Item 7: [RESOLVED] Fat Service Interface & Interface Segregation Violation in `IService`

* **Files:**
  * [`scarajectory/core/service/iservice.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/service/iservice.py)
  * [`scarajectory/core/service/trajectory/iplan_command_service.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/service/trajectory/iplan_command_service.py)
  * [`scarajectory/core/service/trajectory/iplan_persistence_service.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/service/trajectory/iplan_persistence_service.py)
  * [`scarajectory/core/service/trajectory/iplan_validation_service.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/service/trajectory/iplan_validation_service.py)
  * [`scarajectory/core/service/communication/istream_execution_service.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/service/communication/istream_execution_service.py)
  * [`scarajectory/core/service/engine.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/service/engine.py)

### Resolution:
* Created focused role protocols in domain-aligned subpackages (`IPlanCommandService`, `IPlanPersistenceService`, `IPlanValidationService` in `core.service.trajectory`, and `IStreamExecutionService` in `core.service.communication`).
* Composed `IService` from these focused role protocols in `scarajectory.core.service.iservice`.
* Refactored consumers (e.g., `ValidationTab`) to depend strictly on their narrow role interface (`IPlanValidationService`).

---

## Item 8: [RESOLVED] Pipeline Subpackaging & Macro Segregation in `core/service/dsl`

* **Package:** `scarajectory/core/service/dsl/`
* **Original State:** Partial subpackages (`parser/`, `compiler/`, `linter/`) while lexer, parser facade, compiler engine, and 5 macro expanders sat flat in the root.
* **Principles Violated:** Cohesion, Pipeline Boundary Separation.

### Identified Pipeline Subpackages:
1. **Lexer Subpackage (`core/service/dsl/lexer/`):**
   * [`scara_lexer.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/service/dsl/lexer/scara_lexer.py) (`ScaraLexer`)
   * [`iscara_lexer.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/service/dsl/lexer/iscara_lexer.py) (`IScaraLexer`)
2. **Parser Subpackage (`core/service/dsl/parser/`):**
   * [`scara_parser.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/service/dsl/parser/scara_parser.py) (`ScaraParser`) and [`iscara_parser.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/service/dsl/parser/iscara_parser.py) (`IScaraParser`)
   * Unified with 13 command parsers and `icommand_parser.py`, `parameter_extractor.py`.
3. **Macro Subpackage (`core/service/dsl/macro/`):**
   * [`imacro_expander.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/service/dsl/macro/imacro_expander.py) (`IMacroExpander`)
   * [`jump_macro_expander.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/service/dsl/macro/jump_macro_expander.py) (`JumpMacroExpander`)
   * [`tangent_macro_expander.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/service/dsl/macro/tangent_macro_expander.py) (`TangentMacroExpander`)
   * [`frame_macro_expander.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/service/dsl/macro/frame_macro_expander.py) (`FrameMacroExpander`)
   * [`pallet_macro_expander.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/service/dsl/macro/pallet_macro_expander.py) (`PalletMacroExpander`)
4. **Compiler Subpackage (`core/service/dsl/compiler/`):**
   * [`scara_compiler.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/service/dsl/compiler/scara_compiler.py) (`ScaraCompiler`), [`iscara_compiler.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/service/dsl/compiler/iscara_compiler.py) (`IScaraCompiler`), and [`scara_compiler_context.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/service/dsl/compiler/scara_compiler_context.py) (`ScaraCompilerContext`)
   * Unified with `arc_interpolator.py` and `iarc_interpolator.py`.
5. **Exporter Subpackage (`core/service/dsl/exporter/`):**
   * [`scara_plan_exporter.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/service/dsl/exporter/scara_plan_exporter.py) (`ScaraPlanExporter`)
   * [`iscara_plan_exporter.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/service/dsl/exporter/iscara_plan_exporter.py) (`IScaraPlanExporter`)
6. **Application Service Facade (`core/service/dsl/`):**
   * [`scara_dsl_service.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/service/dsl/scara_dsl_service.py) (`ScaraDslService`)
   * [`iscara_dsl_service.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/service/dsl/iscara_dsl_service.py) (`IScaraDslService`)

### Execution Plan (Phase 9):
* [x] **Step 9.6:** Create `scarajectory/core/service/dsl/lexer/`, `scarajectory/core/service/dsl/macro/`, `scarajectory/core/service/dsl/exporter/` with clean metadata-only `__init__.py` files (0 `__all__`).
* [x] **Step 9.7:** Relocate lexer files to `lexer/`.
* [x] **Step 9.8:** Relocate `scara_parser.py` and `iscara_parser.py` to `parser/`.
* [x] **Step 9.9:** Relocate macro expanders to `macro/`.
* [x] **Step 9.10:** Relocate compiler engine and context to `compiler/`.
* [x] **Step 9.11:** Relocate exporter to `exporter/`.

---

## Item 9: [RESOLVED] Interface Segregation & Dependency Inversion in `IScaraDslService`

* **File:** [`scarajectory/core/service/dsl/iscara_dsl_service.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/service/dsl/iscara_dsl_service.py)
* **Principles Violated:** Interface Segregation Principle (ISP), Law of Demeter.

### Analysis:
1. `export_plan(*, plan: ITrajectoryPlan | TrajectoryPlan) -> str` needlessly demanded the full composite `ITrajectoryPlan` (with mutation and undo/redo methods), whereas plan export only requires a read-only waypoint sequence. It now depends strictly on `ITrajectoryReadOnly`.
2. `IScaraDslService` segregated into focused role protocols:
   * `IScaraDslCompiler` (`compile_script`)
   * `IScaraDslValidator` (`validate_script`, `lint_script`)
   * `IScaraPlanExporterService` (`export_plan`)
   * Composite `IScaraDslService` inheriting the three.

### Execution Plan (Phase 9):
* [x] **Step 9.12:** Update `export_plan` in `IScaraPlanExporter`, `ScaraPlanExporter`, `IScaraDslService`, and `ScaraDslService` to accept `ITrajectoryReadOnly`.
* [x] **Step 9.13:** Decompose `IScaraDslService` into role protocols:
  * `IScaraDslCompiler` (`compile_script`)
  * `IScaraDslValidator` (`validate_script`, `lint_script`)
  * `IScaraPlanExporterService` (`export_plan`)
  * Composite `IScaraDslService` combining all three.

---

## Item 10: [RESOLVED] Monolithic Primitive Handling in `ScaraCompiler`

* **File:** [`scarajectory/core/service/dsl/compiler/scara_compiler.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/service/dsl/compiler/scara_compiler.py)
* **Principles Violated:** Single Responsibility Principle (SRP), Open-Closed Principle (OCP).

### Resolution Summary: 🟢 RESOLVED
`ScaraCompiler` was decomposed from 482 lines into a clean coordinator by extracting 4 specialized sub-compilers implementing `IPrimitiveCompiler`:
1. `MotionCommandCompiler` (`scarajectory/core/service/dsl/compiler/motion_command_compiler.py`): Handles `MOVE_L`, `MOVE_J`, `APPROACH`, `RETRACT`, `ARC_CW`, `ARC_CCW`, encapsulating Cartesian frame translation, tangent heading angle calculation, and circular arc interpolation.
2. `ToolCommandCompiler` (`scarajectory/core/service/dsl/compiler/tool_command_compiler.py`): Handles pneumatic actuation (`PUMP`, `VALVE`).
3. `StateCommandCompiler` (`scarajectory/core/service/dsl/compiler/state_command_compiler.py`): Handles state configuration (`SPEED`, `ACCEL`, `OVERRIDE`, `CONFIG_ELBOW`, `ZONE`).
4. `ControlCommandCompiler` (`scarajectory/core/service/dsl/compiler/control_command_compiler.py`): Handles runtime workflow control (`HOME`, `WAIT_MS`, `HOLD`, `RESUME`, `ESTOP`, `ENABLE`, `DISABLE`).
5. Added comprehensive unit tests in [`tests/scara_compiler_test.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/tests/scara_compiler_test.py).

### Execution Plan (Phase 10):
* [x] **Step 10.1:** Define `IPrimitiveCompiler` protocol for primitive instruction processing.
* [x] **Step 10.2:** Extract motion generation into `MotionCommandCompiler` (integrating with `IArcInterpolator`).
* [x] **Step 10.3:** Extract pneumatic, state, and control configuration logic into dedicated helper compilers (`ToolCommandCompiler`, `StateCommandCompiler`, `ControlCommandCompiler`).
* [x] **Step 10.4:** Refactor `ScaraCompiler` to delegate all primitive execution to the specialized compilers.
* [x] **Step 10.5:** Verify all compiler unit tests pass without behavioral divergence.

---

## Item 11: [RESOLVED] Monolithic Lint Rules in `ScaraLinter` (Rule Strategy Pattern)

* **File:** [`scarajectory/core/service/dsl/linter/scara_linter.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/service/dsl/linter/scara_linter.py)
* **Principles Violated:** Single Responsibility Principle (SRP), Open-Closed Principle (OCP).

### Resolution Summary: 🟢 RESOLVED
`ScaraLinter` was decomposed from 337 lines into a thin coordinator (~125 lines) by introducing a Rule Strategy Pattern under `scarajectory/core/service/dsl/linter/rules/`:
1. `ScaraLintContext` (`scarajectory/core/service/dsl/linter/scara_lint_context.py`): Defined as `@dataclass(slots=True)` carrying simulation state.
2. `IScaraLintRule` (`scarajectory/core/service/dsl/linter/rules/iscara_lint_rule.py`): Structural protocol defining `check(*, instruction, context, diagnostics)`.
3. Dedicated rule components:
   * `StateLintRule`: Tracks `HOME` calibration and `ZONE` blend configuration.
   * `MotionLintRule`: Validates `UNCALIBRATED_MOTION` and `DUPLICATE_MOTION`.
   * `PneumaticLintRule`: Validates `PNEUMATIC_CONFLICT`, `REDUNDANT_TOOL_CMD`, and `TOOL_IN_FLYBY`.
   * `TimingLintRule`: Validates `DEAD_WAIT` and `TOOL_IN_FLYBY` during dwell delay.
4. `ScaraLinter` accepts injected rules and evaluates them during AST traversal.
5. Added unit tests for custom rule injection in [`tests/scara_linter_test.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/tests/scara_linter_test.py).

### Execution Plan (Phase 10):
* [x] **Step 10.6:** Create `scarajectory/core/service/dsl/linter/rules/` package with metadata-only `__init__.py`.
* [x] **Step 10.7:** Define `IScaraLintRule` protocol and `ScaraLintContext` state tracker.
* [x] **Step 10.8:** Implement discrete rule classes (`StateLintRule`, `PneumaticLintRule`, `MotionLintRule`, `TimingLintRule`).
* [x] **Step 10.9:** Refactor `ScaraLinter` to evaluate rules via dependency injection / composition.
* [x] **Step 10.10:** Verify all linter unit tests pass without behavioral regression.

---

## Item 12: [RESOLVED] Domain Subpackaging of Command Parsers in `core/service/dsl/parser`

* **Package:** [`scarajectory/core/service/dsl/parser/`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/service/dsl/parser)
* **Principles Violated:** Package Cohesion, Common Closure Principle (CCP), Single Responsibility Principle (SRP).

### Analysis:
The `scarajectory.core.service.dsl.parser` package currently contains **17 files** in a single flat directory:
* **Parser Core & Contracts (4 files):**
  * [`scara_parser.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/service/dsl/parser/scara_parser.py) (`ScaraParser` facade/aggregator)
  * [`iscara_parser.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/service/dsl/parser/iscara_parser.py) (`IScaraParser` contract)
  * [`icommand_parser.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/service/dsl/parser/icommand_parser.py) (`ICommandParser` contract)
  * [`parameter_extractor.py`](file:///data/dev/python/3_tools/scarajectory/github/scarajectory/scarajectory/core/service/dsl/parser/parameter_extractor.py) (`ParameterExtractor` token utility)
* **Concrete Command Parsers (13 files):**
  * Motion/Trajectory: `motion_command_parser.py`, `arc_command_parser.py`, `approach_retract_parser.py`, `jump_command_parser.py`, `jog_command_parser.py`
  * Actuation/Tool: `tool_command_parser.py`, `tool_orient_command_parser.py`, `probe_command_parser.py`
  * Config/Calibration: `config_command_parser.py`, `zone_command_parser.py`, `frame_command_parser.py`, `pallet_command_parser.py`
  * Flow/Control: `flow_command_parser.py`

This flat layout obscures the primary architectural contracts (`IScaraParser`, `ScaraParser`) and clutters the package namespace. It departs from the clean subpackaging pattern successfully established in `core/service/dsl/linter/rules/` and `core/service/dsl/compiler/`.

### Proposed Architecture:
Isolate all individual statement parsers into a dedicated subpackage `scarajectory/core/service/dsl/parser/commands/`:
```
scarajectory/core/service/dsl/parser/
├── __init__.py                     # Metadata-only (0 __all__)
├── iscara_parser.py                # Public AST parser protocol
├── scara_parser.py                 # Top-level orchestrator & dispatcher
├── icommand_parser.py              # Single command parser protocol
├── parameter_extractor.py          # Shared token extraction utility
└── commands/                       # Isolated statement parsers
    ├── __init__.py                 # Metadata-only (0 __all__)
    ├── approach_retract_parser.py
    ├── arc_command_parser.py
    ├── config_command_parser.py
    ├── flow_command_parser.py
    ├── frame_command_parser.py
    ├── jog_command_parser.py
    ├── jump_command_parser.py
    ├── motion_command_parser.py
    ├── pallet_command_parser.py
    ├── probe_command_parser.py
    ├── tool_command_parser.py
    ├── tool_orient_command_parser.py
    └── zone_command_parser.py
```

### Action Points & Execution Checklist (Phase 11):
* [x] **Step 11.4:** Create `scarajectory/core/service/dsl/parser/commands/` with metadata-only `__init__.py` (strictly adhering to no `__all__` and no re-exports).
* [x] **Step 11.5:** Relocate the 13 command parser modules into `scarajectory/core/service/dsl/parser/commands/`.
* [x] **Step 11.6:** Update internal import paths in `commands/*.py` to import `ICommandParser` and `ParameterExtractor` from `scarajectory.core.service.dsl.parser.*`.
* [x] **Step 11.7:** Update `scara_parser.py` registration imports to load concrete parsers from `scarajectory.core.service.dsl.parser.commands.*`.
* [x] **Step 11.8:** Update unit test imports (`tests/scara_parser_test.py` and any command-specific parser tests).
* [x] **Step 11.9:** Rebuild Sphinx API docs (`sphinx-apidoc`) and verify 0 warnings with `-W --keep-going`.

---

## Master Roadmap Status

| Phase | Focus Areas | Status |
| :---: | :--- | :---: |
| **Phase 1** | Kinematics abstraction & dynamic canvas | 🟢 **100% DONE** |
| **Phase 2** | In-memory serializer & storage adapter | 🟢 **100% DONE** |
| **Phase 3** | Hardware communication & semantic robot API | 🟢 **100% DONE** |
| **Phase 4** | GUI presentation models relocation | 🟢 **100% DONE** |
| **Phase 5** | Application Facade, Thread Safety & GUI Decomposition | 🟢 **100% DONE** |
| **Phase 6** | DSL compiler pipeline modularization | 🟢 **100% DONE** |
| **Phase 7** | **Domain Entity Consolidation (`Point` vs `Waypoint`) & Trajectory Subpackaging** | 🟢 **100% DONE** |
| **Phase 8** | **Interface Segregation (ISP) on `IService`, `ITrajectoryPlan`, and Streamer** | 🟢 **100% DONE** |
| **Phase 9** | **DSL Pipeline Subpackages, ISP & Hardening** | 🟢 **100% DONE** |
| **Phase 10** | **Granular Decomposition of God-Modules into Collaborators** | 🟢 **100% DONE** |
| **Phase 11** | **Parser & GUI Subpackaging, Passthrough Elimination, Quality Gates Hardening** | 🟢 **100% DONE** |




