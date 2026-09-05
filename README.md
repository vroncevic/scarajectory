# SCARA Motion Trajectory Studio & Streamer

<img align="right" src="https://raw.githubusercontent.com/vroncevic/scarajectory/dev/docs/scarajectory_logo.png" width="25%">

**scarajectory** is a standalone CAD/CAM motion planning, kinematic validation, and real-time trajectory streaming software for SCARA robotic manipulators.

Developed in **[python](https://www.python.org/)** code.

The README is used to introduce the modules and provide instructions on
how to install the modules, any machine dependencies it may have and any
other information that should be provided before the modules are installed.

[![scarajectory python checker](https://github.com/vroncevic/scarajectory/actions/workflows/scarajectory_python_checker.yml/badge.svg)](https://github.com/vroncevic/scarajectory/actions/workflows/scarajectory_python_checker.yml) [![scarajectory package checker](https://github.com/vroncevic/scarajectory/actions/workflows/scarajectory_package_checker.yml/badge.svg)](https://github.com/vroncevic/scarajectory/actions/workflows/scarajectory_package_checker.yml) [![scarajectory interface checker](https://github.com/vroncevic/scarajectory/actions/workflows/scarajectory_interface_checker.yml/badge.svg)](https://github.com/vroncevic/scarajectory/actions/workflows/scarajectory_interface_checker.yml) [![scarajectory isp checker](https://github.com/vroncevic/scarajectory/actions/workflows/scarajectory_isp_checker.yml/badge.svg)](https://github.com/vroncevic/scarajectory/actions/workflows/scarajectory_isp_checker.yml) [![scarajectory srp checker](https://github.com/vroncevic/scarajectory/actions/workflows/scarajectory_srp_checker.yml/badge.svg)](https://github.com/vroncevic/scarajectory/actions/workflows/scarajectory_srp_checker.yml) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0) [![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/) [![GitHub issues open](https://img.shields.io/github/issues/vroncevic/scarajectory.svg)](https://github.com/vroncevic/scarajectory/issues) [![GitHub contributors](https://img.shields.io/github/contributors/vroncevic/scarajectory.svg)](https://github.com/vroncevic/scarajectory/graphs/contributors)

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**

- [🚀 Installation](#-installation)
    - [Install using pip](#install-using-pip)
    - [Install using build](#install-using-build)
    - [Install using py setup](#install-using-py-setup)
    - [Install using docker](#install-using-docker)
- [📦 Dependencies](#-dependencies)
- [📁 Tool structure](#-tool-structure)
  - [🏗 Architecture & SOLID Principles](#-architecture--solid-principles)
  - [✨ Features](#-features)
  - [📐 SCARA Kinematic & Geometric Configuration](#-scara-kinematic--geometric-configuration)
  - [📜 SCARA Domain-Specific Language (DSL) & `.scara` Programs](#-scara-domain-specific-language-dsl---scara-programs)
  - [📡 Unified Serial ASCII Communication Protocol](#-unified-serial-ascii-communication-protocol)
- [📊 Code coverage](#-code-coverage)
- [🛠 Usage](#-usage)
    - [CLI Command Options](#cli-command-options)
    - [Interactive Motion Planning Workflow](#interactive-motion-planning-workflow)
    - [🤖 Digital Twin Integration with SCARAEmu](#-digital-twin-integration-with-scaraemu)
        - [Mode 1: One-Click Simulation from DSL Editor](#mode-1-one-click-simulation-from-dsl-editor)
        - [Mode 2: Real-Time Closed-Loop TCP Streaming](#mode-2-real-time-closed-loop-tcp-streaming)
        - [Mode 3: Direct File Loading in SCARAEmu](#mode-3-direct-file-loading-in-scaraemu)
- [📚 Docs](#-docs)
- [👥 Contributing](#-contributing)
- [📄 Copyright and licence](#-copyright-and-licence)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

### 🚀 Installation

Used next development environment

![debian linux os](https://raw.githubusercontent.com/vroncevic/scarajectory/dev/docs/debtux.png)

[![scarajectory python3 build](https://github.com/vroncevic/scarajectory/actions/workflows/scarajectory_python3_build.yml/badge.svg)](https://github.com/vroncevic/scarajectory/actions/workflows/scarajectory_python3_build.yml)

Currently there are three ways to install package
* Install process based on using pip mechanism
* Install process based on build mechanism
* Install process based on setup.py mechanism
* Install process based on docker mechanism

##### Install using pip

**scarajectory** is located at **[pypi.org](https://pypi.org/project/scarajectory/)**.

You can install by using pip

```bash
# python3
pip3 install scarajectory
```

##### Install using build

Navigate to release **[page](https://github.com/vroncevic/scarajectory/releases/)** download and extract release archive.

To install **scarajectory** type the following

```bash
tar xvzf scarajectory-x.y.z.tar.gz
cd scarajectory-x.y.z/
# python3
wget https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py 
python3 -m pip install --upgrade setuptools
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade build
pip3 install -r requirements.txt
python3 -m build --no-isolation --wheel
pip3 install ./dist/scarajectory-*-py3-none-any.whl
rm -f get-pip.py
chmod 755 /usr/local/lib/python3.10/dist-packages/usr/local/bin/scarajectory_run.py
ln -s /usr/local/lib/python3.10/dist-packages/usr/local/bin/scarajectory_run.py /usr/local/bin/scarajectory_run.py
```

##### Install using py setup

Navigate to **[release page](https://github.com/vroncevic/scarajectory/releases)** download and extract release archive.

To install **scarajectory** locate and run setup.py with arguments

```bash
tar xvzf scarajectory-x.y.z.tar.gz
cd scarajectory-x.y.z
# python3
pip3 install -r requirements.txt
python3 setup.py install_lib
python3 setup.py install_egg_info
```

##### Install using docker

You can use Dockerfile to create image/container.

### 📦 Dependencies

**scarajectory** requires next modules and libraries

* [ats-utilities - Python App/Tool/Script Utilities](https://pypi.org/project/ats-utilities/) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
* [pyserial - Python Serial Port Extension](https://pypi.org/project/pyserial/) [![License: BSD](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

### 📁 Tool structure

**scarajectory** is based on OOP and Clean Architecture.

Tool structure

<details>
<summary><b>Click to expand framework structure</b></summary>

```bash
    scarajectory/
         ├── core/
         │   ├── __init__.py
         │   ├── model/
         │   │   ├── canvas_interaction_state.py
         │   │   ├── canvas_settings_dto.py
         │   │   ├── canvas_tool_mode.py
         │   │   ├── dsl/
         │   │   │   ├── __init__.py
         │   │   │   ├── iscara_instruction.py
         │   │   │   ├── iscara_program.py
         │   │   │   ├── scara_command_type.py
         │   │   │   ├── scara_diagnostic.py
         │   │   │   ├── scara_diagnostic_severity.py
         │   │   │   ├── scara_instruction.py
         │   │   │   ├── scara_program.py
         │   │   │   ├── scara_token.py
         │   │   │   └── scara_token_type.py
         │   │   ├── __init__.py
         │   │   ├── itrajectory_plan.py
         │   │   ├── plan_history.py
         │   │   ├── point_dto.py
         │   │   ├── scara_bounds.py
         │   │   ├── stream_config_dto.py
         │   │   ├── stream_progress.py
         │   │   ├── stream_state.py
         │   │   ├── trajectory_metrics.py
         │   │   ├── trajectory_plan.py
         │   │   ├── trajectory_serializer.py
         │   │   ├── validation_result_dto.py
         │   │   ├── viewport_transform.py
         │   │   └── waypoint.py
         │   └── service/
         │       ├── dsl/
         │       │   ├── compiler/
         │       │   │   ├── arc_interpolator.py
         │       │   │   ├── iarc_interpolator.py
         │       │   │   └── __init__.py
         │       │   ├── frame_macro_expander.py
         │       │   ├── imacro_expander.py
         │       │   ├── __init__.py
         │       │   ├── iscara_compiler.py
         │       │   ├── iscara_dsl_service.py
         │       │   ├── iscara_lexer.py
         │       │   ├── iscara_parser.py
         │       │   ├── iscara_plan_exporter.py
         │       │   ├── jump_macro_expander.py
         │       │   ├── linter/
         │       │   │   ├── __init__.py
         │       │   │   ├── iscara_linter.py
         │       │   │   └── scara_linter.py
         │       │   ├── pallet_macro_expander.py
         │       │   ├── parser/
         │       │   │   ├── approach_retract_parser.py
         │       │   │   ├── arc_command_parser.py
         │       │   │   ├── config_command_parser.py
         │       │   │   ├── flow_command_parser.py
         │       │   │   ├── frame_command_parser.py
         │       │   │   ├── icommand_parser.py
         │       │   │   ├── __init__.py
         │       │   │   ├── jog_command_parser.py
         │       │   │   ├── jump_command_parser.py
         │       │   │   ├── motion_command_parser.py
         │       │   │   ├── pallet_command_parser.py
         │       │   │   ├── parameter_extractor.py
         │       │   │   ├── probe_command_parser.py
         │       │   │   ├── tool_command_parser.py
         │       │   │   ├── tool_orient_command_parser.py
         │       │   │   └── zone_command_parser.py
         │       │   ├── scara_compiler.py
         │       │   ├── scara_compiler_context.py
         │       │   ├── scara_dsl_service.py
         │       │   ├── scara_lexer.py
         │       │   ├── scara_parser.py
         │       │   ├── scara_plan_exporter.py
         │       │   └── tangent_macro_expander.py
         │       ├── engine.py
         │       ├── __init__.py
         │       ├── iplan_storage_service.py
         │       ├── iservice.py
         │       ├── istream_observer.py
         │       ├── itrajectory_observer.py
         │       ├── itrajectory_streamer.py
         │       ├── itrajectory_validator.py
         │       ├── plan_storage_service.py
         │       └── trajectory_validator.py
         ├── engine.py
         ├── infrastructure/
         │   ├── cli/
         │   │   ├── engine.py
         │   │   ├── icli.py
         │   │   ├── __init__.py
         │   │   └── setup/
         │   │       ├── bundle.py
         │   │       ├── dep_validator.py
         │   │       ├── dependencies.py
         │   │       ├── factory.py
         │   │       ├── __init__.py
         │   │       ├── keys.py
         │   │       ├── opt_validator.py
         │   │       ├── options.py
         │   │       ├── registry.py
         │   │       └── validator.py
         │   ├── command/
         │   │   ├── command.py
         │   │   ├── icommand_definition.py
         │   │   ├── icommand_executor.py
         │   │   ├── __init__.py
         │   │   ├── studio_command_definition.py
         │   │   └── studio_command_executor.py
         │   ├── communication/
         │   │   ├── __init__.py
         │   │   ├── protocol/
         │   │   │   ├── command_formatter.py
         │   │   │   ├── command_templates.py
         │   │   │   ├── config_command_formatter.py
         │   │   │   ├── __init__.py
         │   │   │   ├── motion_command_formatter.py
         │   │   │   ├── protocol_parser.py
         │   │   │   ├── robot_response_dto.py
         │   │   │   └── tool_command_formatter.py
         │   │   ├── serial_device_preferences.py
         │   │   ├── serial_port_scanner.py
         │   │   ├── serial_streamer.py
         │   │   ├── stream_session.py
         │   │   └── transport/
         │   │       ├── __init__.py
         │   │       ├── itransport.py
         │   │       ├── serial_transport.py
         │   │       └── tcp_transport.py
         │   ├── config/
         │   │   ├── scara_geometry.json
         │   │   ├── scarajectory.cfg
         │   │   ├── scarajectory.logo
         │   │   └── scheme.json
         │   ├── gui/
         │   │   ├── canvas.py
         │   │   ├── components/
         │   │   │   ├── canvas_renderer.py
         │   │   │   ├── canvas_tool_handler.py
         │   │   │   ├── dsl_editor_tab.py
         │   │   │   ├── dsl_syntax_highlighter.py
         │   │   │   ├── __init__.py
         │   │   │   ├── jog_tab.py
         │   │   │   ├── menu_bar.py
         │   │   │   ├── preview_tab.py
         │   │   │   ├── serial_console.py
         │   │   │   ├── stream_status_bar.py
         │   │   │   ├── streamer_tab.py
         │   │   │   ├── toolbar.py
         │   │   │   ├── validation_tab.py
         │   │   │   └── waypoint_editor.py
         │   │   ├── controls.py
         │   │   ├── engine.py
         │   │   ├── icanvas.py
         │   │   ├── icontrols.py
         │   │   ├── igui.py
         │   │   ├── __init__.py
         │   │   ├── itable.py
         │   │   ├── table.py
         │   │   └── theme.py
         │   └── __init__.py
         ├── __init__.py
         ├── py.typed
         └── setup/
             ├── bundle.py
             ├── dep_validator.py
             ├── dependencies.py
             ├── factory.py
             ├── __init__.py
             ├── keys.py
             ├── opt_validator.py
             ├── options.py
             ├── registry.py
             └── validator.py

     20 directories, 155 files
```
</details>

#### 🏗 Architecture & SOLID Principles

**scarajectory** is built on a strictly decoupled, **Layered Clean Architecture** where presentation, domain logic, AST compilation, and hardware communication are segregated through pure Python protocols:

```
                  ┌─────────────────────────────────────────────────────────┐
                  │                     ScarajectoryGUI                     │ (Presenter / Main Window)
                  └────────────────────────────┬────────────────────────────┘
                                               │ Orchestrates UI Components via DTOs
         ┌─────────────────────────┬───────────┴─────────────┬──────────────────────────┐
         ▼                         ▼                         ▼                          ▼
┌──────────────────┐      ┌─────────────────┐      ┌───────────────────┐      ┌──────────────────┐
│ TrajectoryCanvas │      │ TrajectoryTable │      │   DslEditorTab    │      │   StreamerTab    │
│   (Vector CAD)   │      │   (Data Grid)   │      │(Syntax Highlighter│      │ (Live Feedrate & │
└────────┬─────────┘      └────────┬────────┘      └─────────┬─────────┘      │  Device Control) │
         │                         │                         │                └────────┬─────────┘
         │                         │                         │                         │
         └────────────┬────────────┴─────────────────────────┘                         │
                      │ Observes / Modifies TrajectoryPlan                             │
                      ▼                                                                │
         ┌──────────────────────────┐                                                  │
         │      TrajectoryPlan      │ (Domain Model)                                   │
         └────────────┬─────────────┘                                                  │
                      │                                                                │
         ┌────────────┴────────────┬────────────────────────┐                          │ Uses ITransport &
         ▼                         ▼                        ▼                          │ IProtocolParser
┌──────────────────┐      ┌──────────────────┐     ┌─────────────────┐                 ▼
│TrajectoryValidat.│      │  ScaraDslService │     │ ScaraPlanExport │        ┌──────────────────┐
│(Workspace Bounds)│      │  (DSL Compiler)  │     │  (Plan to DSL)  │        │  SerialStreamer  │
└──────────────────┘      └────────┬─────────┘     └─────────────────┘        └────────┬─────────┘
                                   │                                                   │
              ┌────────────────────┼────────────────────┐                              ▼
              ▼                    ▼                    ▼                     ┌──────────────────┐
     ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐            │  ProtocolParser  │
     │   ScaraLexer    │  │   ScaraParser   │  │  ScaraCompiler  │            └──────────────────┘
     │  (Token Stream) │  │(ICommandParser) │  │(IMacroExpander) │
     └─────────────────┘  └─────────────────┘  └─────────────────┘
```

##### SOLID Principles Compliance

* **S — Single Responsibility Principle (SRP)**:
  * Every module and class has exactly one clearly bounded reason to change.
  * Parser and compiler logic is decomposed into dedicated handlers (`MotionCommandParser`, `ArcCommandParser`, `JumpMacroExpander`, etc.) rather than a monolithic interpreter.
  * Enforced by automated gate: strict limit of $\le 15$ methods per class across the entire codebase.
* **O — Open/Closed Principle (OCP)**:
  * The DSL parser and compiler are open for extension without modifying existing code.
  * New DSL keywords and high-level macros plug into `ICommandParser` and `IMacroExpander` registries dynamically.
* **L — Liskov Substitution Principle (LSP)**:
  * Pure structural subtyping via Python `@runtime_checkable Protocol` definitions. Concrete classes never inherit concrete logic, ensuring complete interchangeability.
* **I — Interface Segregation Principle (ISP)**:
  * Clients depend only on the minimal interfaces they require (`ITrajectoryValidator`, `IScaraLexer`, `IScaraParser`, `IScaraCompiler`, `ISerialStreamer`, `ITransport`).
* **D — Dependency Inversion Principle (DIP)**:
  * Core domain entities and compilers have zero dependencies on lower-level infrastructure (serial drivers, formatters, UI widgets). All dependencies are injected via protocols.

##### Automated Quality Gates (`run_quality_gates.sh`)

Every build is validated against 4 strict automated quality gates:
1. **Structural Protocols Gate**: Verifies 100% compliance with `@runtime_checkable Protocol` structural typing.
2. **Interface Segregation Gate (ISP)**: Verifies that no bloated or unused interfaces exist.
3. **Module Limits Gate**: Enforces file length and line length limits ($\le 100$ characters).
4. **Single Responsibility Gate (SRP)**: Strictly enforces $\le 15$ methods per class.

#### ✨ Features

* **Interactive Vector CAD Editor**: Real-time vector drafting with dedicated Point, Line, Rectangle, Circle, and Freehand tools with live vertex dragging and viewport zoom/pan.
* **Integrated `.scara` DSL Editor & AST Compiler**: Full-featured code editor with real-time syntax highlighting for industrial SCARA scripts (`.scara`), AST compilation, and instant bidirectional visual canvas synchronization.
* **Kinematic Reachability & Deadzone Enforcement**: Annular geometric validation ensuring trajectories stay within reachable workspace boundaries ($R_{min} = |L_1 - L_2|$, $R_{max} = L_1 + L_2$).
* **Undo / Redo Transaction Stack**: Non-destructive history management for waypoint additions, modifications, insertions, and deletions (`Ctrl+Z`, `Ctrl+Y`).
* **ASCII Protocol Generation**: Generates micro-command streaming packets for RP2040 firmware (`<pt#X#Y#Z#PHI#SPEED#end>`).
* **Sliding Window Hardware Streaming**: Multi-threaded USB serial (`/dev/ttyACM0`) and TCP socket streaming with dynamic ACK tracking, auto-pause on buffer full, progress monitoring, and live Feedrate Override (10% - 200%).
* **Manual Jogging & Diagnostics**: Interactive jog grid (X, Y, Z, Phi), vacuum pump and release valve toggles, homing, status queries, and raw serial command console.
* **Configurable Kinematics & Dimensions**: Dynamic robot link lengths ($L_1, L_2$), stroke limits ($Z_{min}, Z_{max}$), and speed bounds configurable via CLI options and JSON schema.
* **Strict Quality & SOLID Standards**: 100% protocol conformity, zero ISP/SRP violations, 81% test coverage, and 10.00 / 10.00 Pylint score.

#### 📐 SCARA Kinematic & Geometric Configuration

The robot dimensions and physical boundaries can be customized in [`scara_geometry.json`](scarajectory/infrastructure/config/scara_geometry.json) or injected programmatically:

| Parameter | Default Value | Description |
|---|:---:|---|
| **`l1`** | `150.0 mm` | Primary arm link length (shoulder to elbow). |
| **`l2`** | `120.0 mm` | Secondary arm link length (elbow to wrist). |
| **`r_min`** | `30.0 mm` | Inner singular deadzone radius ($|L_1 - L_2|$). |
| **`r_max`** | `270.0 mm` | Maximum horizontal reach boundary ($L_1 + L_2$). |
| **`z_min`** | `0.0 mm` | Minimum vertical height limit (bed level). |
| **`z_max`** | `100.0 mm` | Maximum vertical stroke limit. |
| **`min_speed`** | `1.0 mm/s` | Minimum allowable feedrate speed. |
| **`max_speed`** | `100.0 mm/s` | Maximum allowable safe feedrate speed. |

#### 📜 SCARA Domain-Specific Language (DSL) & `.scara` Programs

**scarajectory** includes a dedicated, industrial-grade Domain-Specific Language designed specifically for SCARA robotic manipulators. Programs are written in plain text files with the `.scara` extension and compiled into validated Cartesian trajectories via a clean AST pipeline:

```
                    ┌─────────────────────────┐
                    │     .scara Source       │
                    └────────────┬────────────┘
                                 │ ScaraLexer
                                 ▼
                    ┌─────────────────────────┐
                    │      Token Stream       │
                    └────────────┬────────────┘
                                 │ ScaraParser
                                 ▼
                    ┌─────────────────────────┐
                    │      Abstract AST       │
                    └────────────┬────────────┘
                                 │ ScaraCompiler (Macros + Kinematics)
                                 ▼
                    ┌─────────────────────────┐
                    │     TrajectoryPlan      │ (Waypoints & Protocols)
                    └─────────────────────────┘
```

##### SCARA DSL Instruction Reference

| Category | Instruction & Syntax | Parameters | Description |
|---|---|---|---|
| **Motion** | `MOVE_J X <x> Y <y> Z <z> [P <phi>]` | `X, Y, Z` (mm), `P` (deg) | Rapid Cartesian point-to-point motion. |
| | `MOVE_L X <x> Y <y> Z <z> [P <phi>]` | `X, Y, Z` (mm), `P` (deg) | Linear interpolated Cartesian path. |
| | `ARC_CW X <x> Y <y> I <i> J <j> [Z <z>]` | `X, Y` target, `I, J` center offset | Clockwise circular arc interpolation. |
| | `ARC_CCW X <x> Y <y> I <i> J <j> [Z <z>]` | `X, Y` target, `I, J` center offset | Counter-clockwise circular arc interpolation. |
| | `APPROACH DIST <d>` | `DIST` (mm) | Vertical descent towards workpiece along Z. |
| | `RETRACT DIST <d>` | `DIST` (mm) | Vertical clearance ascent along Z. |
| **Macros** | `JUMP X <x> Y <y> Z <z> [ARCH <h>]` | `X, Y, Z`, `ARCH` apex clearance | Smooth 3D parabolic pick-and-place arch motion. |
| | `PALLET ROWS <r> COLS <c> DX <dx> DY <dy>` | Grid dimensions & spacing | Generates structured 2D Cartesian pallet matrix. |
| | `TANGENT_ARC RADIUS <r> ANGLE <a>` | `RADIUS` (mm), `ANGLE` (deg) | Smooth tangential curve blending into path. |
| **Actuators** | `PUMP <ON\|OFF>` | `ON` or `OFF` | Actuates end-effector vacuum pump. |
| | `VALVE <ON\|OFF>` | `ON` or `OFF` | Opens or closes pneumatic release blow-off valve. |
| | `WAIT <ms>` | `ms` (milliseconds) | Dwells execution for specified hardware duration. |
| | `HOME` | None | Triggers complete multi-axis homing routine. |
| **Dynamics** | `SPEED <RAPID\|WORK> <val>` | `RAPID` or `WORK`, feedrate (mm/s)| Configures travel or working linear feedrate. |
| | `ACCEL <val>` | `val` (mm/s²) | Configures linear path acceleration limit. |
| | `OVERRIDE <percent>` | `percent` (10% - 200%) | Scales path execution velocity dynamically. |
| | `ZONE <OFF\|FINE\|Z1..Z50>` | Corner rounding tolerance | Corner tolerance zone for trajectory smoothing. |
| **Config** | `CONFIG ELBOW <LEFT\|RIGHT>` | `LEFT` or `RIGHT` | Sets arm kinematic inverse solution branch. |
| | `FRAME X <x> Y <y> Z <z> [PHI <p>]` | Cartesian offset coordinates | Defines user workpiece reference coordinate frame. |
| | `PROBE AXIS <Z> FEED <f>` | Axis identifier, search feedrate | Probes touch switch / surface sensor. |

##### Example `.scara` Program: Industrial Pick & Place

```scara
# ----------------------------------------------------
# Industrial Pick-and-Place Cycle with Pneumatic Grip
# ----------------------------------------------------
CONFIG ELBOW LEFT
SPEED RAPID 180.0
SPEED WORK 60.0
ACCEL 400.0
OVERRIDE 100

# Home robot to reference position
HOME

# Rapid move above pick feeder station
MOVE_J X 140.0 Y -30.0 Z 35.0
APPROACH DIST 30.0

# Engage suction cup and pause for vacuum seal
PUMP ON
WAIT 200

# Retract with part
RETRACT DIST 30.0

# Smooth 3D parabolic arch transfer to drop location
JUMP X 180.0 Y 30.0 Z 5.0 ARCH 40.0

# Release part with air pulse
PUMP OFF
VALVE ON
WAIT 100
VALVE OFF

# Retract to safe transit altitude
RETRACT DIST 30.0
HOME
```

#### 📡 Unified Serial ASCII Communication Protocol

All communication between **scarajectory**, the physical **`scara_base`** firmware, and the **`scaraemu`** digital twin is governed by a packetized ASCII streaming protocol:

##### Command Packets (PC $\to$ Robot)

| Command Packet | Description | Response Handshake |
|---|---|---|
| `<pt#X#Y#Z#PHI#SPEED#end>` | Push Cartesian trajectory point to FIFO motion buffer | `<RESP:ACK#QUEUE=n>` then `<RESP:MOVE_DONE#...>` |
| `<CMD:JOG#axis#step>` | Incremental manual jog (`X`, `Y`, `Z`, `P`) by `step` mm/deg | `<RESP:ACK#JOG_QUEUED#QUEUE=n>` |
| `<CMD:OVERRIDE#percent>` | Real-time feedrate override scaling (`10` to `200` %) | `<RESP:ACK#OVERRIDE=percent>` |
| `<CMD:WAIT#ms>` | Synchronous dwell delay pause on motion controller | `<RESP:ACK#WAIT_DONE#MS=ms>` |
| `<CMD:PUMP#1>` / `<CMD:PUMP#0>` | Energize / de-energize vacuum pump actuator | `<RESP:ACK#PUMP_ON>` / `<RESP:ACK#PUMP_OFF>` |
| `<CMD:VALVE#1>` / `<CMD:VALVE#0>`| Open / close pneumatic air release valve | `<RESP:ACK#VALVE_ON>` / `<RESP:ACK#VALVE_OFF>` |
| `<CMD:HOME>` | Execute multi-axis homing and calibrate zero | `<RESP:ACK#HOMING_STARTED>` then `<RESP:HOMED_SUCCESS#...>` |
| `<CMD:ENABLE>` / `<CMD:DISABLE>`| Energize / de-energize stepper driver stages | `<RESP:ACK#MOTORS_ENABLED>` / `<RESP:ACK#MOTORS_DISABLED>` |
| `<CMD:ESTOP>` | Instant emergency stop and motion queue abort | `<RESP:ACK#ESTOP_TRIGGERED>` |
| `<CMD:HOLD>` / `<CMD:RESUME>` | Decelerate to feed hold / resume paused trajectory | `<RESP:ACK#FEED_HOLD_ACTIVE>` / `<RESP:ACK#MOTION_RESUMED>` |
| `<CMD:STATUS>` | Query operational machine state and endstop flags | `<RESP:STATUS#STATE=...#ENDSTOPS=...>` |
| `<CMD:GETPOS>` | Read active Cartesian tool coordinates and orientation | `<RESP:POS#X=...#Y=...#Z=...#PHI=...>` |
| `<CMD:SET_ELBOW#LEFT\|RIGHT>` | Select inverse kinematic arm solution branch | `<RESP:ACK#ELBOW=LEFT\|RIGHT>` |
| `<CMD:GET_ELBOW>` | Query active elbow configuration branch | `<RESP:ELBOW#CONFIG=LEFT\|RIGHT>` |
| `<CMD:GET_CONFIG>` | Read persisted geometry, dynamics, and stroke bounds | `<RESP:CONFIG#L1=...#L2=...#MIN_SPD=...>` |
| `<CMD:SET_CONFIG#...>` | Update robot link lengths, stroke, and speed bounds | `<RESP:ACK#CONFIG_STORED...>` |
| `<CMD:SAVE_CONFIG>` | Commit active configuration to RP2040 Flash (CRC32) | `<RESP:ACK#CONFIG_SAVED>` |
| `<CMD:RESET_CONFIG>` | Restore factory default geometry and kinematic bounds | `<RESP:ACK#CONFIG_RESET>` |

##### Microcontroller Response Packets (Robot $\to$ PC)

| Response Packet | Category | Streamer Meaning |
|---|:---:|---|
| `<RESP:ACK#QUEUE=n>` | Acknowledgment | Waypoint accepted into ring buffer; `n` slots remaining. |
| `<RESP:MOVE_DONE#X=..#Y=..#Z=..#PHI=..>` | Move Complete | Physical execution of waypoint completed. Advances done counter. |
| `<RESP:ACK#WAIT_DONE#...>` | Action Complete | Hardware dwell delay elapsed. Advances streamer progress. |
| `<RESP:ACK#PUMP_ON\|OFF>` | Action Complete | Tool actuation complete. Advances streamer progress. |
| `<RESP:ACK#VALVE_ON\|OFF>` | Action Complete | Valve actuation complete. Advances streamer progress. |
| `<RESP:HOMED_SUCCESS#...>` | Homing Complete | Machine homed and zero-reference established. |
| `<RESP:NACK_BUFFER_FULL>` | Flow Control | Microcontroller queue full; streamer enters auto-pause. |
| `<RESP:NACK_ESTOP_ACTIVE>` | Error / Safety | E-Stop asserted; all motions rejected until reset. |
| `<RESP:NACK_OUT_OF_REACH>` | Kinematic Rejection | Target coordinate outside reachable arm envelope ($R_{max}$). |
| `<RESP:NACK_SINGULARITY_LIMIT>` | Kinematic Rejection | Target inside inner deadzone ($R_{min} = \|L_1 - L_2\|$). |

### 📊 Code coverage

<details>
<summary><b>Click to expand code coverage</b></summary>

| Name | Stmts | Miss | Cover |
|------|-------|------|-------|
| `scarajectory/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/model/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/model/canvas_interaction_state.py` | 26 | 0 | 100%|
| `scarajectory/core/model/canvas_settings_dto.py` | 15 | 0 | 100%|
| `scarajectory/core/model/canvas_tool_mode.py` | 17 | 0 | 100%|
| `scarajectory/core/model/dsl/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/model/dsl/iscara_instruction.py` | 28 | 5 | 82%|
| `scarajectory/core/model/dsl/iscara_program.py` | 24 | 4 | 83%|
| `scarajectory/core/model/dsl/scara_command_type.py` | 44 | 0 | 100%|
| `scarajectory/core/model/dsl/scara_diagnostic.py` | 22 | 0 | 100%|
| `scarajectory/core/model/dsl/scara_diagnostic_severity.py` | 15 | 0 | 100%|
| `scarajectory/core/model/dsl/scara_instruction.py` | 25 | 1 | 96%|
| `scarajectory/core/model/dsl/scara_program.py` | 32 | 9 | 72%|
| `scarajectory/core/model/dsl/scara_token.py` | 17 | 0 | 100%|
| `scarajectory/core/model/dsl/scara_token_type.py` | 23 | 0 | 100%|
| `scarajectory/core/model/itrajectory_plan.py` | 31 | 0 | 100%|
| `scarajectory/core/model/plan_history.py` | 34 | 1 | 97%|
| `scarajectory/core/model/point_dto.py` | 18 | 0 | 100%|
| `scarajectory/core/model/scara_bounds.py` | 29 | 0 | 100%|
| `scarajectory/core/model/stream_config_dto.py` | 15 | 0 | 100%|
| `scarajectory/core/model/stream_progress.py` | 26 | 3 | 88%|
| `scarajectory/core/model/stream_state.py` | 17 | 0 | 100%|
| `scarajectory/core/model/trajectory_metrics.py` | 37 | 5 | 86%|
| `scarajectory/core/model/trajectory_plan.py` | 100 | 14 | 86%|
| `scarajectory/core/model/trajectory_serializer.py` | 29 | 0 | 100%|
| `scarajectory/core/model/validation_result_dto.py` | 15 | 0 | 100%|
| `scarajectory/core/model/viewport_transform.py` | 48 | 0 | 100%|
| `scarajectory/core/model/waypoint.py` | 45 | 2 | 96%|
| `scarajectory/core/service/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/dsl/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/dsl/compiler/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/dsl/compiler/arc_interpolator.py` | 37 | 25 | 32%|
| `scarajectory/core/service/dsl/compiler/iarc_interpolator.py` | 13 | 0 | 100%|
| `scarajectory/core/service/dsl/frame_macro_expander.py` | 27 | 10 | 63%|
| `scarajectory/core/service/dsl/imacro_expander.py` | 18 | 2 | 89%|
| `scarajectory/core/service/dsl/iscara_compiler.py` | 19 | 1 | 95%|
| `scarajectory/core/service/dsl/iscara_dsl_service.py` | 20 | 0 | 100%|
| `scarajectory/core/service/dsl/iscara_lexer.py` | 15 | 1 | 93%|
| `scarajectory/core/service/dsl/iscara_parser.py` | 19 | 2 | 89%|
| `scarajectory/core/service/dsl/iscara_plan_exporter.py` | 14 | 0 | 100%|
| `scarajectory/core/service/dsl/jump_macro_expander.py` | 34 | 17 | 50%|
| `scarajectory/core/service/dsl/linter/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/dsl/linter/iscara_linter.py` | 15 | 0 | 100%|
| `scarajectory/core/service/dsl/linter/scara_linter.py` | 93 | 6 | 94%|
| `scarajectory/core/service/dsl/pallet_macro_expander.py` | 42 | 24 | 43%|
| `scarajectory/core/service/dsl/parser/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/dsl/parser/approach_retract_parser.py` | 22 | 4 | 82%|
| `scarajectory/core/service/dsl/parser/arc_command_parser.py` | 22 | 4 | 82%|
| `scarajectory/core/service/dsl/parser/config_command_parser.py` | 43 | 12 | 72%|
| `scarajectory/core/service/dsl/parser/flow_command_parser.py` | 36 | 6 | 83%|
| `scarajectory/core/service/dsl/parser/frame_command_parser.py` | 23 | 5 | 78%|
| `scarajectory/core/service/dsl/parser/icommand_parser.py` | 18 | 2 | 89%|
| `scarajectory/core/service/dsl/parser/jog_command_parser.py` | 27 | 10 | 63%|
| `scarajectory/core/service/dsl/parser/jump_command_parser.py` | 20 | 2 | 90%|
| `scarajectory/core/service/dsl/parser/motion_command_parser.py` | 24 | 0 | 100%|
| `scarajectory/core/service/dsl/parser/pallet_command_parser.py` | 26 | 8 | 69%|
| `scarajectory/core/service/dsl/parser/parameter_extractor.py` | 40 | 8 | 80%|
| `scarajectory/core/service/dsl/parser/probe_command_parser.py` | 20 | 2 | 90%|
| `scarajectory/core/service/dsl/parser/tool_command_parser.py` | 32 | 3 | 91%|
| `scarajectory/core/service/dsl/parser/tool_orient_command_parser.py` | 27 | 9 | 67%|
| `scarajectory/core/service/dsl/parser/zone_command_parser.py` | 27 | 1 | 96%|
| `scarajectory/core/service/dsl/scara_compiler.py` | 159 | 49 | 69%|
| `scarajectory/core/service/dsl/scara_compiler_context.py` | 40 | 7 | 82%|
| `scarajectory/core/service/dsl/scara_dsl_service.py` | 61 | 3 | 95%|
| `scarajectory/core/service/dsl/scara_lexer.py` | 51 | 5 | 90%|
| `scarajectory/core/service/dsl/scara_parser.py` | 63 | 5 | 92%|
| `scarajectory/core/service/dsl/scara_plan_exporter.py` | 25 | 1 | 96%|
| `scarajectory/core/service/dsl/tangent_macro_expander.py` | 30 | 12 | 60%|
| `scarajectory/core/service/engine.py` | 45 | 3 | 93%|
| `scarajectory/core/service/iplan_storage_service.py` | 16 | 0 | 100%|
| `scarajectory/core/service/iservice.py` | 26 | 0 | 100%|
| `scarajectory/core/service/istream_observer.py` | 15 | 0 | 100%|
| `scarajectory/core/service/itrajectory_observer.py` | 14 | 0 | 100%|
| `scarajectory/core/service/itrajectory_streamer.py` | 25 | 0 | 100%|
| `scarajectory/core/service/itrajectory_validator.py` | 18 | 0 | 100%|
| `scarajectory/core/service/plan_storage_service.py` | 17 | 0 | 100%|
| `scarajectory/core/service/trajectory_validator.py` | 100 | 17 | 83%|
| `scarajectory/engine.py` | 64 | 30 | 53%|
| `scarajectory/infrastructure/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/cli/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/cli/engine.py` | 39 | 7 | 82%|
| `scarajectory/infrastructure/cli/icli.py` | 15 | 0 | 100%|
| `scarajectory/infrastructure/cli/setup/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/cli/setup/bundle.py` | 22 | 1 | 95%|
| `scarajectory/infrastructure/cli/setup/dep_validator.py` | 36 | 5 | 86%|
| `scarajectory/infrastructure/cli/setup/dependencies.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/cli/setup/factory.py` | 37 | 1 | 97%|
| `scarajectory/infrastructure/cli/setup/keys.py` | 28 | 0 | 100%|
| `scarajectory/infrastructure/cli/setup/opt_validator.py` | 36 | 5 | 86%|
| `scarajectory/infrastructure/cli/setup/options.py` | 17 | 0 | 100%|
| `scarajectory/infrastructure/cli/setup/registry.py` | 24 | 1 | 96%|
| `scarajectory/infrastructure/cli/setup/validator.py` | 43 | 5 | 88%|
| `scarajectory/infrastructure/command/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/command/command.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/command/icommand_definition.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/command/icommand_executor.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/command/studio_command_definition.py` | 24 | 1 | 96%|
| `scarajectory/infrastructure/command/studio_command_executor.py` | 38 | 15 | 61%|
| `scarajectory/infrastructure/communication/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/communication/protocol/__init__.py` | 8 | 0 | 100%|
| `scarajectory/infrastructure/communication/protocol/command_formatter.py` | 13 | 0 | 100%|
| `scarajectory/infrastructure/communication/protocol/command_templates.py` | 46 | 2 | 96%|
| `scarajectory/infrastructure/communication/protocol/config_command_formatter.py` | 22 | 4 | 82%|
| `scarajectory/infrastructure/communication/protocol/motion_command_formatter.py` | 51 | 7 | 86%|
| `scarajectory/infrastructure/communication/protocol/protocol_parser.py` | 108 | 30 | 72%|
| `scarajectory/infrastructure/communication/protocol/robot_response_dto.py` | 17 | 0 | 100%|
| `scarajectory/infrastructure/communication/protocol/tool_command_formatter.py` | 25 | 0 | 100%|
| `scarajectory/infrastructure/communication/serial_device_preferences.py` | 40 | 11 | 72%|
| `scarajectory/infrastructure/communication/serial_port_scanner.py` | 36 | 5 | 86%|
| `scarajectory/infrastructure/communication/serial_streamer.py` | 200 | 129 | 36%|
| `scarajectory/infrastructure/communication/stream_session.py` | 19 | 0 | 100%|
| `scarajectory/infrastructure/communication/transport/__init__.py` | 8 | 0 | 100%|
| `scarajectory/infrastructure/communication/transport/itransport.py` | 19 | 0 | 100%|
| `scarajectory/infrastructure/communication/transport/serial_transport.py` | 104 | 63 | 39%|
| `scarajectory/infrastructure/communication/transport/tcp_transport.py` | 120 | 80 | 33%|
| `scarajectory/infrastructure/gui/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas.py` | 170 | 92 | 46%|
| `scarajectory/infrastructure/gui/components/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/components/canvas_renderer.py` | 117 | 23 | 80%|
| `scarajectory/infrastructure/gui/components/canvas_tool_handler.py` | 42 | 0 | 100%|
| `scarajectory/infrastructure/gui/components/dsl_editor_tab.py` | 188 | 80 | 57%|
| `scarajectory/infrastructure/gui/components/dsl_syntax_highlighter.py` | 54 | 0 | 100%|
| `scarajectory/infrastructure/gui/components/jog_tab.py` | 67 | 8 | 88%|
| `scarajectory/infrastructure/gui/components/menu_bar.py` | 103 | 36 | 65%|
| `scarajectory/infrastructure/gui/components/preview_tab.py` | 32 | 4 | 88%|
| `scarajectory/infrastructure/gui/components/serial_console.py` | 51 | 17 | 67%|
| `scarajectory/infrastructure/gui/components/stream_status_bar.py` | 30 | 5 | 83%|
| `scarajectory/infrastructure/gui/components/streamer_tab.py` | 152 | 58 | 62%|
| `scarajectory/infrastructure/gui/components/toolbar.py` | 73 | 9 | 88%|
| `scarajectory/infrastructure/gui/components/validation_tab.py` | 35 | 5 | 86%|
| `scarajectory/infrastructure/gui/components/waypoint_editor.py` | 71 | 17 | 76%|
| `scarajectory/infrastructure/gui/controls.py` | 51 | 4 | 92%|
| `scarajectory/infrastructure/gui/engine.py` | 98 | 19 | 81%|
| `scarajectory/infrastructure/gui/icanvas.py` | 20 | 0 | 100%|
| `scarajectory/infrastructure/gui/icontrols.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/gui/igui.py` | 17 | 0 | 100%|
| `scarajectory/infrastructure/gui/itable.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/gui/table.py` | 77 | 29 | 62%|
| `scarajectory/infrastructure/gui/theme.py` | 57 | 0 | 100%|
| `scarajectory/setup/__init__.py` | 9 | 0 | 100%|
| `scarajectory/setup/bundle.py` | 25 | 1 | 96%|
| `scarajectory/setup/dep_validator.py` | 36 | 5 | 86%|
| `scarajectory/setup/dependencies.py` | 21 | 0 | 100%|
| `scarajectory/setup/factory.py` | 98 | 4 | 96%|
| `scarajectory/setup/keys.py` | 37 | 0 | 100%|
| `scarajectory/setup/opt_validator.py` | 36 | 5 | 86%|
| `scarajectory/setup/options.py` | 20 | 0 | 100%|
| `scarajectory/setup/registry.py` | 34 | 1 | 97%|
| `scarajectory/setup/validator.py` | 53 | 5 | 91%|
| **Total** | 5579 | 1139 | 80% |

</details>

### 🛠 Usage

Install package

```bash
pip3 install scarajectory
```

Prepare main entry point by downloading [main.py](https://raw.githubusercontent.com/vroncevic/scarajectory/main/main.py) or create your own.

```bash
wget -O main.py https://raw.githubusercontent.com/vroncevic/scarajectory/main/main.py
```

##### CLI Command Options

Launch the graphical studio with default configuration:

```bash
python3 main.py studio
```

Launch with initial trajectory plan file and disabled deadzone restriction:

```bash
python3 main.py studio --file ./trajectories/rectangle_demo.json --dead-zone disable --verbose enable
```

| Option | Type | Choices | Description |
|---|:---:|:---:|---|
| **`--file`** | `str` | *File path* | Path to initial trajectory JSON plan file to load on startup. |
| **`--dead-zone`** | `str` | `enable`, `disable` | Enable or disable inner deadzone geometric validation ($R_{min}$). |
| **`--verbose`** | `str` | `enable`, `disable` | Enable or disable verbose ATS operational logging. |

##### Interactive Motion Planning Workflow

1. **Design Trajectory & Geometry**:
   * Use **Point**, **Line**, **Rectangle**, **Circle**, or **Freehand** tools directly on the interactive vector canvas.
   * Fine-tune Cartesian parameters ($X, Y, Z, \phi, \text{speed}$) using the Waypoint Data Table or interactive vertex drag.
2. **Kinematic Validation**:
   * Open the **Plan Validation** tab and run validation against reachability limits ($L_1 = 150\text{ mm}, L_2 = 120\text{ mm}$).
   * Verify total path length and estimated execution time.
3. **ASCII Program Preview**:
   * Inspect the formatted ASCII micro-command stream (`<pt#...#end>`) under the **Program Preview** tab.
4. **Hardware Streaming & Execution**:
   * Connect to `/dev/ttyACM0` (or TCP host) under the **Hardware Streamer** tab.
   * Trigger streaming to execute real-time motion on the physical SCARA robot.
5. **Manual Jogging & Diagnostics**:
   * Use the **Manual Jog** tab for directional jog movements, vacuum pump activation, release valve triggers, and homing.

##### 🤖 Digital Twin Integration with SCARAEmu

**scarajectory** seamlessly integrates with **[scaraemu](https://github.com/vroncevic/scaraemu)** as a software-in-the-loop (SITL) Digital Twin. This allows you to visually simulate, animate, and validate trajectories and `.scara` DSL programs in 2D/3D before deploying to physical hardware.

###### Mode 1: One-Click Simulation from DSL Editor
1. In **scarajectory**, open the **SCARA DSL Editor** tab.
2. Write or load any `.scara` program (or select from bundled examples in `examples/`).
3. Click the **🚀 Preview in SCARAEmu** button located at the bottom toolbar.
4. **scarajectory** automatically launches **scaraemu** in a background subprocess, passing the active trajectory file via `--file`.
5. The 2D Planar and 3D Z-Tower canvases immediately render the robot arm executing the trajectory.

###### Mode 2: Real-Time Closed-Loop TCP Streaming
1. Launch **scaraemu**:
   ```bash
   python3 main.py emulator
   ```
2. Activate the Virtual Robot Server:
   * Click the **🌐 Virtual Server: OFF** toggle button on the top status bar.
   * The button turns green and displays **🌐 Virtual Server: 8888**, listening on `127.0.0.1:8888`.
3. Launch **scarajectory**:
   ```bash
   python3 main.py studio
   ```
4. Compile DSL code to trajectory:
   * In the **SCARA DSL Editor** tab, load or write your `.scara` script.
   * Click **`⚡ Compile to Plan`**. The AST compiler compiles Cartesian paths, macros, and action commands into the active trajectory plan.
5. Navigate to the **Hardware Streamer** tab.
6. In the **Port** dropdown, select **`127.0.0.1:8888 (Digital Twin)`**.
7. Click **Connect**. The status bar updates to `Streamer: Connected to 127.0.0.1:8888`.
8. Click **Stream Trajectory** (or use the **Manual Jog** controls):
   * Trajectory waypoints (`<pt#X#Y#Z#PHI#SPEED#end>`) stream live over the loopback TCP socket.
   * **scaraemu** smoothly animates the dual-link arm and carriage along the path.
   * Closed-loop protocol acknowledgments (`<RESP:ACK#QUEUE=1>`, `<RESP:MOVE_DONE#...>`) flow back to **scarajectory**, dynamically driving the streaming progress bar.

###### Mode 3: Direct File Loading in SCARAEmu
* Open **scaraemu** and navigate to the **Trajectories** tab.
* In the **SCARA DSL Script** dropdown, select any of the 12 bundled programs (e.g. `pick_and_place.scara`, `engrave_spiral.scara`, `pallet_matrix.scara`).
* Or click **📂 Load** to load any custom `.scara` script or exported `plan.json` file.

### 📚 Docs

[![Documentation Status](https://readthedocs.org/projects/scarajectory/badge/?version=latest)](https://scarajectory.readthedocs.io/en/latest/?badge=latest)

More documentation and info at

* [scarajectory.readthedocs.io](https://scarajectory.readthedocs.io)
* [www.python.org](https://www.python.org/)

### 👥 Contributing

[Contributing to scarajectory](CONTRIBUTING.md)

### 📄 Copyright and licence

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Copyright (C) 2026 by [vroncevic.github.io/scarajectory](https://vroncevic.github.io/scarajectory)

**scarajectory** is free software; you can redistribute it and/or modify
it under the same terms as Python itself, either Python version 3.x or,
at your option, any later version of Python 3 you may have available.

Special thanks to **Google** and the Google developer ecosystem for their tremendous support and innovative tools from the Google bundle that empowered the development and realization of this project. *Google, you make this world a better place!* 🌍✨

Lets help and support PSF.

[![Python Software Foundation](https://raw.githubusercontent.com/vroncevic/scarajectory/dev/docs/psf-logo-alpha.png)](https://www.python.org/psf/)

[![Donate](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.python.org/psf/donations/)
