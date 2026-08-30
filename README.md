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
- [📊 Code coverage](#-code-coverage)
- [🛠 Usage](#-usage)
    - [CLI Command Options](#cli-command-options)
    - [Interactive Motion Planning Workflow](#interactive-motion-planning-workflow)
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
         │   │   │   ├── __init__.py
         │   │   │   ├── protocol_parser.py
         │   │   │   └── robot_response_dto.py
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

     15 directories, 100 files
```
</details>

#### 🏗 Architecture & SOLID Principles

```
                  ┌──────────────────────────────┐
                  │       ScarajectoryGUI        │ (Presenter / Controller)
                  └──────────────┬───────────────┘
                                 │ Uses DTOs (StreamConfigDTO, CanvasSettingsDTO)
         ┌───────────────────────┼───────────────────────┐
         │                       │                       │
         ▼                       ▼                       ▼
┌──────────────────┐    ┌─────────────────┐    ┌──────────────────┐
│ TrajectoryCanvas │    │ TrajectoryTable │    │  TrajectoryPlan  │ (Domain Model)
└──────────────────┘    └─────────────────┘    └────────┬─────────┘
   (Vector CAD)           (Data Grid)                   │
         ▲                       ▲                      │
         └───────────┬───────────┘                      │
                     │ (itrajectory_observer.py)        │
                     └──────────────────────────────────┤
                                                        ▼
                                             ┌────────────────────────┐
                    (Interface Segregation)  │ itrajectory_validator  │
                                             └──────────┬─────────────┘
                                                        │ Uses PointDTO
                                                        ▼
                                             ┌────────────────────────┐
                                             │  trajectory_validator  │ (Reachability Engine)
                                             └────────────────────────┘
```

#### ✨ Features

* **Interactive Vector CAD Editor**: Real-time vector drafting with dedicated Point, Line, Rectangle, Circle, and Freehand tools with live vertex dragging and viewport zoom/pan.
* **Kinematic Reachability & Deadzone Enforcement**: Annular geometric validation ensuring trajectories stay within reachable workspace boundaries ($R_{min} = |L_1 - L_2|$, $R_{max} = L_1 + L_2$).
* **Undo / Redo Transaction Stack**: Non-destructive history management for waypoint additions, modifications, insertions, and deletions (`Ctrl+Z`, `Ctrl+Y`).
* **ASCII Protocol Generation**: Generates micro-command streaming packets for RP2040 firmware (`<pt#X#Y#Z#PHI#SPEED#end>`).
* **Sliding Window Hardware Streaming**: Multi-threaded USB serial (`/dev/ttyACM0`) and TCP socket streaming with dynamic ACK tracking, auto-pause on buffer full, and progress monitoring.
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
| `scarajectory/core/model/itrajectory_plan.py` | 31 | 0 | 100%|
| `scarajectory/core/model/plan_history.py` | 34 | 1 | 97%|
| `scarajectory/core/model/point_dto.py` | 18 | 0 | 100%|
| `scarajectory/core/model/scara_bounds.py` | 18 | 0 | 100%|
| `scarajectory/core/model/stream_config_dto.py` | 15 | 0 | 100%|
| `scarajectory/core/model/stream_progress.py` | 25 | 3 | 88%|
| `scarajectory/core/model/stream_state.py` | 17 | 0 | 100%|
| `scarajectory/core/model/trajectory_metrics.py` | 37 | 7 | 81%|
| `scarajectory/core/model/trajectory_plan.py` | 100 | 14 | 86%|
| `scarajectory/core/model/trajectory_serializer.py` | 29 | 0 | 100%|
| `scarajectory/core/model/validation_result_dto.py` | 15 | 0 | 100%|
| `scarajectory/core/model/viewport_transform.py` | 48 | 0 | 100%|
| `scarajectory/core/model/waypoint.py` | 42 | 4 | 90%|
| `scarajectory/core/service/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/engine.py` | 45 | 3 | 93%|
| `scarajectory/core/service/iplan_storage_service.py` | 16 | 0 | 100%|
| `scarajectory/core/service/iservice.py` | 26 | 0 | 100%|
| `scarajectory/core/service/istream_observer.py` | 15 | 0 | 100%|
| `scarajectory/core/service/itrajectory_observer.py` | 14 | 0 | 100%|
| `scarajectory/core/service/itrajectory_streamer.py` | 25 | 0 | 100%|
| `scarajectory/core/service/itrajectory_validator.py` | 18 | 0 | 100%|
| `scarajectory/core/service/plan_storage_service.py` | 17 | 0 | 100%|
| `scarajectory/core/service/trajectory_validator.py` | 69 | 9 | 87%|
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
| `scarajectory/infrastructure/communication/protocol/command_formatter.py` | 58 | 9 | 84%|
| `scarajectory/infrastructure/communication/protocol/command_templates.py` | 35 | 2 | 94%|
| `scarajectory/infrastructure/communication/protocol/protocol_parser.py` | 64 | 17 | 73%|
| `scarajectory/infrastructure/communication/protocol/robot_response_dto.py` | 17 | 0 | 100%|
| `scarajectory/infrastructure/communication/serial_port_scanner.py` | 36 | 5 | 86%|
| `scarajectory/infrastructure/communication/serial_streamer.py` | 150 | 83 | 45%|
| `scarajectory/infrastructure/communication/stream_session.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/communication/transport/__init__.py` | 8 | 0 | 100%|
| `scarajectory/infrastructure/communication/transport/itransport.py` | 19 | 0 | 100%|
| `scarajectory/infrastructure/communication/transport/serial_transport.py` | 104 | 63 | 39%|
| `scarajectory/infrastructure/communication/transport/tcp_transport.py` | 120 | 80 | 33%|
| `scarajectory/infrastructure/gui/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas.py` | 170 | 92 | 46%|
| `scarajectory/infrastructure/gui/components/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/components/canvas_renderer.py` | 79 | 23 | 71%|
| `scarajectory/infrastructure/gui/components/canvas_tool_handler.py` | 42 | 0 | 100%|
| `scarajectory/infrastructure/gui/components/jog_tab.py` | 67 | 8 | 88%|
| `scarajectory/infrastructure/gui/components/menu_bar.py` | 75 | 14 | 81%|
| `scarajectory/infrastructure/gui/components/preview_tab.py` | 32 | 4 | 88%|
| `scarajectory/infrastructure/gui/components/serial_console.py` | 34 | 6 | 82%|
| `scarajectory/infrastructure/gui/components/stream_status_bar.py` | 29 | 4 | 86%|
| `scarajectory/infrastructure/gui/components/streamer_tab.py` | 96 | 31 | 68%|
| `scarajectory/infrastructure/gui/components/toolbar.py` | 73 | 9 | 88%|
| `scarajectory/infrastructure/gui/components/validation_tab.py` | 35 | 5 | 86%|
| `scarajectory/infrastructure/gui/components/waypoint_editor.py` | 71 | 17 | 76%|
| `scarajectory/infrastructure/gui/controls.py` | 44 | 3 | 93%|
| `scarajectory/infrastructure/gui/engine.py` | 98 | 19 | 81%|
| `scarajectory/infrastructure/gui/icanvas.py` | 20 | 0 | 100%|
| `scarajectory/infrastructure/gui/icontrols.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/gui/igui.py` | 17 | 0 | 100%|
| `scarajectory/infrastructure/gui/itable.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/gui/table.py` | 77 | 29 | 62%|
| `scarajectory/infrastructure/gui/theme.py` | 58 | 0 | 100%|
| `scarajectory/setup/__init__.py` | 9 | 0 | 100%|
| `scarajectory/setup/bundle.py` | 25 | 1 | 96%|
| `scarajectory/setup/dep_validator.py` | 36 | 5 | 86%|
| `scarajectory/setup/dependencies.py` | 21 | 0 | 100%|
| `scarajectory/setup/factory.py` | 84 | 4 | 95%|
| `scarajectory/setup/keys.py` | 37 | 0 | 100%|
| `scarajectory/setup/opt_validator.py` | 36 | 5 | 86%|
| `scarajectory/setup/options.py` | 20 | 0 | 100%|
| `scarajectory/setup/registry.py` | 34 | 1 | 97%|
| `scarajectory/setup/validator.py` | 53 | 5 | 91%|
| **Total** | 3455 | 656 | 81% |

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
