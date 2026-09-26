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
    - [SOLID Principles Compliance](#solid-principles-compliance)
    - [Automated Quality Gates (`run_quality_gates.sh`)](#automated-quality-gates-run_quality_gatessh)
  - [✨ Features](#-features)
  - [📐 SCARA Kinematic & Geometric Configuration](#-scara-kinematic--geometric-configuration)
  - [📜 SCARA Domain-Specific Language (DSL) & `.scara` Programs](#-scara-domain-specific-language-dsl--scara-programs)
    - [SCARA DSL Instruction Reference](#scara-dsl-instruction-reference)
    - [Example `.scara` Program: Industrial Pick & Place](#example-scara-program-industrial-pick--place)
  - [📡 Unified Serial ASCII Communication Protocol](#-unified-serial-ascii-communication-protocol)
    - [Command Packets (PC $\to$ Robot)](#command-packets-pc-%5Cto-robot)
    - [Microcontroller Response Packets (Robot $\to$ PC)](#microcontroller-response-packets-robot-%5Cto-pc)
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
         │   │   ├── communication/
         │   │   │   ├── event/
         │   │   │   │   ├── fault_event.py
         │   │   │   │   ├── __init__.py
         │   │   │   │   └── move_event.py
         │   │   │   ├── __init__.py
         │   │   │   ├── preferences/
         │   │   │   │   ├── connection_preference.py
         │   │   │   │   └── __init__.py
         │   │   │   ├── protocol/
         │   │   │   │   ├── __init__.py
         │   │   │   │   ├── protocol_mode.py
         │   │   │   │   └── scara_response.py
         │   │   │   ├── stream/
         │   │   │   │   ├── __init__.py
         │   │   │   │   ├── stream_config.py
         │   │   │   │   ├── stream_progress.py
         │   │   │   │   ├── stream_session.py
         │   │   │   │   └── stream_state.py
         │   │   │   └── telemetry/
         │   │   │       ├── diagnostics_bundle.py
         │   │   │       ├── diagnostics_snapshot.py
         │   │   │       ├── __init__.py
         │   │   │       └── scara_status.py
         │   │   ├── dsl/
         │   │   │   ├── ast/
         │   │   │   ├── binary/
         │   │   │   ├── diagnostic/
         │   │   │   └── token/
         │   │   ├── __init__.py
         │   │   ├── kinematics/
         │   │   │   ├── __init__.py
         │   │   │   ├── scara_bounds.py
         │   │   │   └── transmission_parameters.py
         │   │   └── trajectory/
         │   │       ├── __init__.py
         │   │       ├── validation_result.py
         │   │       └── waypoint.py
         │   └── service/
         │       ├── communication/
         │       │   ├── controller/
         │       │   │   ├── ijog_controller.py
         │       │   │   ├── imotion_controller.py
         │       │   │   ├── __init__.py
         │       │   │   ├── iquery_controller.py
         │       │   │   ├── irobot_controller.py
         │       │   │   └── itool_controller.py
         │       │   ├── event/
         │       │   │   ├── binary_frame_dispatcher.py
         │       │   │   ├── binary_frame_dispatcher_factory.py
         │       │   │   ├── fault_event_factory.py
         │       │   │   ├── ibinary_frame_dispatcher.py
         │       │   │   ├── __init__.py
         │       │   │   └── move_event_factory.py
         │       │   ├── __init__.py
         │       │   ├── preferences/
         │       │   │   ├── connection_preference_factory.py
         │       │   │   └── __init__.py
         │       │   ├── protocol/
         │       │   │   ├── icommand_formatter.py
         │       │   │   ├── __init__.py
         │       │   │   └── iprotocol_parser.py
         │       │   ├── stream/
         │       │   │   ├── config_factory.py
         │       │   │   ├── iconfig_factory.py
         │       │   │   ├── iconnection.py
         │       │   │   ├── iexecution_service.py
         │       │   │   ├── iexecution_worker.py
         │       │   │   ├── iflow_controller.py
         │       │   │   ├── imotion_streamer.py
         │       │   │   ├── __init__.py
         │       │   │   ├── iobservable.py
         │       │   │   ├── iobserver.py
         │       │   │   ├── ipacket_strategy.py
         │       │   │   ├── iraw_channel.py
         │       │   │   ├── itrajectory_streamer.py
         │       │   │   └── session_factory.py
         │       │   └── telemetry/
         │       │       ├── diagnostics_snapshot_factory.py
         │       │       └── __init__.py
         │       ├── config/
         │       │   ├── __init__.py
         │       │   └── iscara_config_loader.py
         │       ├── dsl/
         │       │   ├── ast/
         │       │   ├── binary/
         │       │   │   ├── command/
         │       │   │   ├── motion/
         │       │   │   └── step/
         │       │   ├── compiler/
         │       │   │   ├── motion/
         │       │   │   └── primitive/
         │       │   ├── diagnostic/
         │       │   ├── exporter/
         │       │   ├── lexer/
         │       │   ├── linter/
         │       │   │   └── rules/
         │       │   ├── macro/
         │       │   └── parser/
         │       │       └── commands/
         │       ├── engine.py
         │       ├── __init__.py
         │       ├── iservice.py
         │       ├── kinematics/
         │       │   ├── ikinematics_service.py
         │       │   ├── __init__.py
         │       │   ├── kinematics_service.py
         │       │   └── kinematics_service_factory.py
         │       ├── service_factory.py
         │       └── trajectory/
         │           ├── contract/
         │           │   ├── __init__.py
         │           │   ├── iplan_command_service.py
         │           │   ├── iplan_persistence_service.py
         │           │   ├── iplan_storage_service.py
         │           │   └── iplan_validation_service.py
         │           ├── discretization/
         │           │   ├── __init__.py
         │           │   ├── ishape_discretizer.py
         │           │   ├── iwaypoint_factory.py
         │           │   ├── shape_discretizer.py
         │           │   ├── shape_discretizer_factory.py
         │           │   └── waypoint_factory.py
         │           ├── history/
         │           │   ├── __init__.py
         │           │   ├── iplan_history.py
         │           │   ├── plan_history.py
         │           │   └── plan_history_factory.py
         │           ├── __init__.py
         │           ├── metrics/
         │           │   ├── __init__.py
         │           │   └── trajectory_metrics.py
         │           ├── plan/
         │           │   ├── __init__.py
         │           │   ├── itrajectory_history.py
         │           │   ├── itrajectory_mutable.py
         │           │   ├── itrajectory_observer.py
         │           │   ├── itrajectory_plan.py
         │           │   ├── itrajectory_plan_factory.py
         │           │   ├── itrajectory_read_only.py
         │           │   ├── trajectory_plan.py
         │           │   └── trajectory_plan_factory.py
         │           └── validation/
         │               ├── __init__.py
         │               ├── itrajectory_validator.py
         │               ├── trajectory_validator.py
         │               └── trajectory_validator_factory.py
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
         │   │   ├── controller/
         │   │   │   ├── base_sub_controller.py
         │   │   │   ├── __init__.py
         │   │   │   ├── jog_controller.py
         │   │   │   ├── jog_controller_factory.py
         │   │   │   ├── motion_controller.py
         │   │   │   ├── motion_controller_factory.py
         │   │   │   ├── query_controller.py
         │   │   │   ├── query_controller_factory.py
         │   │   │   ├── robot_controller.py
         │   │   │   ├── robot_controller_factory.py
         │   │   │   ├── tool_controller.py
         │   │   │   └── tool_controller_factory.py
         │   │   ├── __init__.py
         │   │   ├── preferences/
         │   │   │   ├── connection_repository.py
         │   │   │   ├── connection_repository_factory.py
         │   │   │   ├── iconnection_repository.py
         │   │   │   └── __init__.py
         │   │   ├── protocol/
         │   │   │   ├── ascii/
         │   │   │   │   ├── formatter/
         │   │   │   │   │   ├── command_formatter.py
         │   │   │   │   │   ├── command_formatter_factory.py
         │   │   │   │   │   ├── command_templates.py
         │   │   │   │   │   ├── config_command_formatter.py
         │   │   │   │   │   ├── __init__.py
         │   │   │   │   │   ├── jog_command_formatter.py
         │   │   │   │   │   ├── motion_command_formatter.py
         │   │   │   │   │   ├── query_command_formatter.py
         │   │   │   │   │   ├── system_command_formatter.py
         │   │   │   │   │   └── tool_command_formatter.py
         │   │   │   │   ├── __init__.py
         │   │   │   │   └── parser/
         │   │   │   │       ├── __init__.py
         │   │   │   │       ├── protocol_parser.py
         │   │   │   │       ├── protocol_parser_factory.py
         │   │   │   │       ├── protocol_status_classifier.py
         │   │   │   │       └── response_parser.py
         │   │   │   ├── binary/
         │   │   │   │   ├── builder/
         │   │   │   │   ├── checksum/
         │   │   │   │   └── parser/
         │   │   │   └── __init__.py
         │   │   ├── serial_port_scanner.py
         │   │   ├── streamer/
         │   │   │   ├── binary_packet_strategy.py
         │   │   │   ├── binary_packet_strategy_factory.py
         │   │   │   ├── binary_stream_execution_worker.py
         │   │   │   ├── binary_stream_execution_worker_factory.py
         │   │   │   ├── flow_controller.py
         │   │   │   ├── flow_controller_factory.py
         │   │   │   ├── __init__.py
         │   │   │   ├── stream_connection_manager.py
         │   │   │   ├── stream_connection_manager_factory.py
         │   │   │   ├── stream_execution_worker.py
         │   │   │   ├── stream_execution_worker_factory.py
         │   │   │   ├── stream_observer_dispatcher.py
         │   │   │   ├── stream_observer_dispatcher_factory.py
         │   │   │   ├── stream_state_machine.py
         │   │   │   ├── stream_state_machine_factory.py
         │   │   │   ├── trajectory_streamer.py
         │   │   │   └── trajectory_streamer_factory.py
         │   │   └── transport/
         │   │       ├── base_transport.py
         │   │       ├── __init__.py
         │   │       ├── itransport.py
         │   │       ├── serial_transport.py
         │   │       ├── tcp_transport.py
         │   │       └── transport_factory.py
         │   ├── config/
         │   │   ├── scara_geometry.json
         │   │   ├── scarajectory.cfg
         │   │   ├── scarajectory.logo
         │   │   └── scheme.json
         │   ├── gui/
         │   │   ├── canvas/
         │   │   │   ├── canvas.py
         │   │   │   ├── canvas_background_renderer.py
         │   │   │   ├── canvas_event_binder.py
         │   │   │   ├── canvas_mouse_handler.py
         │   │   │   ├── canvas_preview_renderer.py
         │   │   │   ├── canvas_renderer.py
         │   │   │   ├── canvas_tool_handler.py
         │   │   │   ├── canvas_trajectory_renderer.py
         │   │   │   ├── icanvas.py
         │   │   │   └── __init__.py
         │   │   ├── controls/
         │   │   │   ├── controls.py
         │   │   │   ├── controls_panel_factory.py
         │   │   │   ├── icontrols_panel.py
         │   │   │   └── __init__.py
         │   │   ├── dsl/
         │   │   │   ├── dsl_code_editor.py
         │   │   │   ├── dsl_console_view.py
         │   │   │   ├── dsl_document_manager.py
         │   │   │   ├── dsl_editor_tab.py
         │   │   │   ├── dsl_editor_tab_factory.py
         │   │   │   ├── dsl_editor_toolbar.py
         │   │   │   ├── dsl_example_catalog.py
         │   │   │   ├── dsl_syntax_highlighter.py
         │   │   │   ├── emulator_launcher.py
         │   │   │   ├── iemulator_launcher.py
         │   │   │   └── __init__.py
         │   │   ├── editor/
         │   │   │   ├── __init__.py
         │   │   │   ├── itable.py
         │   │   │   ├── preview_tab.py
         │   │   │   ├── preview_tab_factory.py
         │   │   │   ├── table.py
         │   │   │   ├── validation_tab.py
         │   │   │   └── waypoint_editor.py
         │   │   ├── engine.py
         │   │   ├── gui_event_mediator.py
         │   │   ├── gui_factory.py
         │   │   ├── igui.py
         │   │   ├── __init__.py
         │   │   ├── menu/
         │   │   │   ├── iapp_menu_bar.py
         │   │   │   ├── __init__.py
         │   │   │   └── menu_bar.py
         │   │   ├── model/
         │   │   │   ├── canvas_interaction_state.py
         │   │   │   ├── canvas_settings.py
         │   │   │   ├── canvas_tool_mode.py
         │   │   │   ├── __init__.py
         │   │   │   └── viewport_transform.py
         │   │   ├── stream/
         │   │   │   ├── __init__.py
         │   │   │   ├── jog_tab.py
         │   │   │   ├── port_connection_panel.py
         │   │   │   ├── robot_override_panel.py
         │   │   │   ├── serial_console.py
         │   │   │   ├── stream_control_panel.py
         │   │   │   ├── stream_progress_adapter.py
         │   │   │   ├── stream_status_bar.py
         │   │   │   └── streamer_tab.py
         │   │   ├── theme/
         │   │   │   ├── __init__.py
         │   │   │   └── theme.py
         │   │   └── toolbar/
         │   │       ├── __init__.py
         │   │       ├── itoolbar.py
         │   │       ├── toolbar.py
         │   │       └── toolbar_factory.py
         │   ├── __init__.py
         │   ├── settings/
         │   │   ├── config_loader.py
         │   │   ├── config_loader_factory.py
         │   │   └── __init__.py
         │   └── storage/
         │       ├── __init__.py
         │       ├── plan_storage_service.py
         │       ├── plan_storage_service_factory.py
         │       └── trajectory_serializer.py
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

     81 directories, 263 files
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
| `scarajectory/core/model/communication/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/model/communication/event/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/model/communication/event/fault_event.py` | 15 | 0 | 100%|
| `scarajectory/core/model/communication/event/move_event.py` | 14 | 0 | 100%|
| `scarajectory/core/model/communication/preferences/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/model/communication/preferences/connection_preference.py` | 14 | 0 | 100%|
| `scarajectory/core/model/communication/protocol/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/model/communication/protocol/protocol_mode.py` | 14 | 0 | 100%|
| `scarajectory/core/model/communication/protocol/scara_response.py` | 16 | 0 | 100%|
| `scarajectory/core/model/communication/stream/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/model/communication/stream/stream_config.py` | 18 | 0 | 100%|
| `scarajectory/core/model/communication/stream/stream_progress.py` | 22 | 0 | 100%|
| `scarajectory/core/model/communication/stream/stream_session.py` | 19 | 0 | 100%|
| `scarajectory/core/model/communication/stream/stream_state.py` | 17 | 0 | 100%|
| `scarajectory/core/model/communication/telemetry/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/model/communication/telemetry/diagnostics_bundle.py` | 29 | 0 | 100%|
| `scarajectory/core/model/communication/telemetry/diagnostics_snapshot.py` | 29 | 0 | 100%|
| `scarajectory/core/model/communication/telemetry/scara_status.py` | 19 | 0 | 100%|
| `scarajectory/core/model/kinematics/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/model/kinematics/scara_bounds.py` | 29 | 0 | 100%|
| `scarajectory/core/model/kinematics/transmission_parameters.py` | 18 | 0 | 100%|
| `scarajectory/core/model/trajectory/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/model/trajectory/validation_result.py` | 15 | 0 | 100%|
| `scarajectory/core/model/trajectory/waypoint.py` | 19 | 0 | 100%|
| `scarajectory/core/service/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/communication/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/communication/controller/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/communication/controller/ijog_controller.py` | 14 | 0 | 100%|
| `scarajectory/core/service/communication/controller/imotion_controller.py` | 16 | 0 | 100%|
| `scarajectory/core/service/communication/controller/iquery_controller.py` | 14 | 0 | 100%|
| `scarajectory/core/service/communication/controller/irobot_controller.py` | 22 | 0 | 100%|
| `scarajectory/core/service/communication/controller/itool_controller.py` | 15 | 0 | 100%|
| `scarajectory/core/service/communication/event/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/communication/event/binary_frame_dispatcher.py` | 29 | 0 | 100%|
| `scarajectory/core/service/communication/event/binary_frame_dispatcher_factory.py` | 17 | 1 | 94%|
| `scarajectory/core/service/communication/event/fault_event_factory.py` | 17 | 1 | 94%|
| `scarajectory/core/service/communication/event/ibinary_frame_dispatcher.py` | 15 | 15 | 0%|
| `scarajectory/core/service/communication/event/move_event_factory.py` | 17 | 1 | 94%|
| `scarajectory/core/service/communication/preferences/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/communication/preferences/connection_preference_factory.py` | 23 | 0 | 100%|
| `scarajectory/core/service/communication/protocol/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/communication/protocol/icommand_formatter.py` | 14 | 0 | 100%|
| `scarajectory/core/service/communication/protocol/iprotocol_parser.py` | 24 | 0 | 100%|
| `scarajectory/core/service/communication/stream/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/communication/stream/config_factory.py` | 18 | 1 | 94%|
| `scarajectory/core/service/communication/stream/iconfig_factory.py` | 15 | 0 | 100%|
| `scarajectory/core/service/communication/stream/iconnection.py` | 16 | 0 | 100%|
| `scarajectory/core/service/communication/stream/iexecution_service.py` | 16 | 16 | 0%|
| `scarajectory/core/service/communication/stream/iexecution_worker.py` | 18 | 0 | 100%|
| `scarajectory/core/service/communication/stream/iflow_controller.py` | 22 | 22 | 0%|
| `scarajectory/core/service/communication/stream/imotion_streamer.py` | 20 | 0 | 100%|
| `scarajectory/core/service/communication/stream/iobservable.py` | 14 | 0 | 100%|
| `scarajectory/core/service/communication/stream/iobserver.py` | 15 | 0 | 100%|
| `scarajectory/core/service/communication/stream/ipacket_strategy.py` | 14 | 14 | 0%|
| `scarajectory/core/service/communication/stream/iraw_channel.py` | 15 | 0 | 100%|
| `scarajectory/core/service/communication/stream/itrajectory_streamer.py` | 18 | 0 | 100%|
| `scarajectory/core/service/communication/stream/session_factory.py` | 16 | 0 | 100%|
| `scarajectory/core/service/communication/telemetry/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/communication/telemetry/diagnostics_snapshot_factory.py` | 18 | 1 | 94%|
| `scarajectory/core/service/config/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/config/iscara_config_loader.py` | 23 | 0 | 100%|
| `scarajectory/core/service/engine.py` | 53 | 1 | 98%|
| `scarajectory/core/service/iservice.py` | 26 | 0 | 100%|
| `scarajectory/core/service/kinematics/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/kinematics/ikinematics_service.py` | 23 | 0 | 100%|
| `scarajectory/core/service/kinematics/kinematics_service.py` | 84 | 4 | 95%|
| `scarajectory/core/service/kinematics/kinematics_service_factory.py` | 19 | 1 | 95%|
| `scarajectory/core/service/service_factory.py` | 19 | 0 | 100%|
| `scarajectory/core/service/trajectory/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/trajectory/contract/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/trajectory/contract/iplan_command_service.py` | 16 | 0 | 100%|
| `scarajectory/core/service/trajectory/contract/iplan_persistence_service.py` | 14 | 0 | 100%|
| `scarajectory/core/service/trajectory/contract/iplan_storage_service.py` | 18 | 0 | 100%|
| `scarajectory/core/service/trajectory/contract/iplan_validation_service.py` | 13 | 0 | 100%|
| `scarajectory/core/service/trajectory/discretization/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/trajectory/discretization/ishape_discretizer.py` | 16 | 0 | 100%|
| `scarajectory/core/service/trajectory/discretization/iwaypoint_factory.py` | 15 | 1 | 93%|
| `scarajectory/core/service/trajectory/discretization/shape_discretizer.py` | 20 | 0 | 100%|
| `scarajectory/core/service/trajectory/discretization/shape_discretizer_factory.py` | 22 | 2 | 91%|
| `scarajectory/core/service/trajectory/discretization/waypoint_factory.py` | 14 | 0 | 100%|
| `scarajectory/core/service/trajectory/history/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/trajectory/history/iplan_history.py` | 17 | 0 | 100%|
| `scarajectory/core/service/trajectory/history/plan_history.py` | 34 | 1 | 97%|
| `scarajectory/core/service/trajectory/history/plan_history_factory.py` | 14 | 0 | 100%|
| `scarajectory/core/service/trajectory/metrics/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/trajectory/metrics/trajectory_metrics.py` | 40 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/itrajectory_history.py` | 14 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/itrajectory_mutable.py` | 21 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/itrajectory_observer.py` | 14 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/itrajectory_plan.py` | 19 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/itrajectory_plan_factory.py` | 14 | 14 | 0%|
| `scarajectory/core/service/trajectory/plan/itrajectory_read_only.py` | 18 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/trajectory_plan.py` | 96 | 10 | 90%|
| `scarajectory/core/service/trajectory/plan/trajectory_plan_factory.py` | 19 | 0 | 100%|
| `scarajectory/core/service/trajectory/validation/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/trajectory/validation/itrajectory_validator.py` | 28 | 0 | 100%|
| `scarajectory/core/service/trajectory/validation/trajectory_validator.py` | 75 | 11 | 85%|
| `scarajectory/core/service/trajectory/validation/trajectory_validator_factory.py` | 19 | 1 | 95%|
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
| `scarajectory/infrastructure/command/studio_command_executor.py` | 37 | 14 | 62%|
| `scarajectory/infrastructure/communication/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/communication/controller/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/communication/controller/base_sub_controller.py` | 41 | 0 | 100%|
| `scarajectory/infrastructure/communication/controller/jog_controller.py` | 34 | 0 | 100%|
| `scarajectory/infrastructure/communication/controller/jog_controller_factory.py` | 20 | 1 | 95%|
| `scarajectory/infrastructure/communication/controller/motion_controller.py` | 39 | 0 | 100%|
| `scarajectory/infrastructure/communication/controller/motion_controller_factory.py` | 20 | 1 | 95%|
| `scarajectory/infrastructure/communication/controller/query_controller.py` | 29 | 0 | 100%|
| `scarajectory/infrastructure/communication/controller/query_controller_factory.py` | 20 | 1 | 95%|
| `scarajectory/infrastructure/communication/controller/robot_controller.py` | 81 | 14 | 83%|
| `scarajectory/infrastructure/communication/controller/robot_controller_factory.py` | 34 | 1 | 97%|
| `scarajectory/infrastructure/communication/controller/tool_controller.py` | 41 | 6 | 85%|
| `scarajectory/infrastructure/communication/controller/tool_controller_factory.py` | 20 | 1 | 95%|
| `scarajectory/infrastructure/communication/preferences/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/communication/preferences/connection_repository.py` | 56 | 6 | 89%|
| `scarajectory/infrastructure/communication/preferences/connection_repository_factory.py` | 15 | 0 | 100%|
| `scarajectory/infrastructure/communication/preferences/iconnection_repository.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/communication/protocol/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/communication/protocol/ascii/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/communication/protocol/ascii/formatter/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/communication/protocol/ascii/formatter/command_formatter.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/communication/protocol/ascii/formatter/command_formatter_factory.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/communication/protocol/ascii/formatter/command_templates.py` | 46 | 2 | 96%|
| `scarajectory/infrastructure/communication/protocol/ascii/formatter/config_command_formatter.py` | 22 | 4 | 82%|
| `scarajectory/infrastructure/communication/protocol/ascii/formatter/jog_command_formatter.py` | 15 | 0 | 100%|
| `scarajectory/infrastructure/communication/protocol/ascii/formatter/motion_command_formatter.py` | 38 | 0 | 100%|
| `scarajectory/infrastructure/communication/protocol/ascii/formatter/query_command_formatter.py` | 21 | 0 | 100%|
| `scarajectory/infrastructure/communication/protocol/ascii/formatter/system_command_formatter.py` | 29 | 0 | 100%|
| `scarajectory/infrastructure/communication/protocol/ascii/formatter/tool_command_formatter.py` | 25 | 0 | 100%|
| `scarajectory/infrastructure/communication/protocol/ascii/parser/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/communication/protocol/ascii/parser/protocol_parser.py` | 19 | 0 | 100%|
| `scarajectory/infrastructure/communication/protocol/ascii/parser/protocol_parser_factory.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/communication/protocol/ascii/parser/protocol_status_classifier.py` | 47 | 0 | 100%|
| `scarajectory/infrastructure/communication/protocol/ascii/parser/response_parser.py` | 68 | 7 | 90%|
| `scarajectory/infrastructure/communication/serial_port_scanner.py` | 36 | 5 | 86%|
| `scarajectory/infrastructure/communication/streamer/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/communication/streamer/binary_packet_strategy.py` | 42 | 0 | 100%|
| `scarajectory/infrastructure/communication/streamer/binary_packet_strategy_factory.py` | 24 | 2 | 92%|
| `scarajectory/infrastructure/communication/streamer/binary_stream_execution_worker.py` | 149 | 26 | 83%|
| `scarajectory/infrastructure/communication/streamer/binary_stream_execution_worker_factory.py` | 26 | 2 | 92%|
| `scarajectory/infrastructure/communication/streamer/flow_controller.py` | 77 | 19 | 75%|
| `scarajectory/infrastructure/communication/streamer/flow_controller_factory.py` | 22 | 2 | 91%|
| `scarajectory/infrastructure/communication/streamer/stream_connection_manager.py` | 61 | 19 | 69%|
| `scarajectory/infrastructure/communication/streamer/stream_connection_manager_factory.py` | 19 | 1 | 95%|
| `scarajectory/infrastructure/communication/streamer/stream_execution_worker.py` | 110 | 15 | 86%|
| `scarajectory/infrastructure/communication/streamer/stream_execution_worker_factory.py` | 23 | 1 | 96%|
| `scarajectory/infrastructure/communication/streamer/stream_observer_dispatcher.py` | 34 | 0 | 100%|
| `scarajectory/infrastructure/communication/streamer/stream_observer_dispatcher_factory.py` | 18 | 1 | 94%|
| `scarajectory/infrastructure/communication/streamer/stream_state_machine.py` | 28 | 1 | 96%|
| `scarajectory/infrastructure/communication/streamer/stream_state_machine_factory.py` | 15 | 0 | 100%|
| `scarajectory/infrastructure/communication/streamer/trajectory_streamer.py` | 176 | 85 | 52%|
| `scarajectory/infrastructure/communication/streamer/trajectory_streamer_factory.py` | 65 | 3 | 95%|
| `scarajectory/infrastructure/communication/transport/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/communication/transport/base_transport.py` | 137 | 86 | 37%|
| `scarajectory/infrastructure/communication/transport/itransport.py` | 21 | 0 | 100%|
| `scarajectory/infrastructure/communication/transport/serial_transport.py` | 40 | 14 | 65%|
| `scarajectory/infrastructure/communication/transport/tcp_transport.py` | 61 | 35 | 43%|
| `scarajectory/infrastructure/communication/transport/transport_factory.py` | 21 | 0 | 100%|
| `scarajectory/infrastructure/gui/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/canvas.py` | 89 | 21 | 76%|
| `scarajectory/infrastructure/gui/canvas/canvas_background_renderer.py` | 92 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/canvas_event_binder.py` | 49 | 14 | 71%|
| `scarajectory/infrastructure/gui/canvas/canvas_mouse_handler.py` | 121 | 38 | 69%|
| `scarajectory/infrastructure/gui/canvas/canvas_preview_renderer.py` | 29 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/canvas_renderer.py` | 27 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/canvas_tool_handler.py` | 37 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/canvas_trajectory_renderer.py` | 40 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/icanvas.py` | 20 | 0 | 100%|
| `scarajectory/infrastructure/gui/controls/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/controls/controls.py` | 54 | 7 | 87%|
| `scarajectory/infrastructure/gui/controls/controls_panel_factory.py` | 40 | 1 | 98%|
| `scarajectory/infrastructure/gui/controls/icontrols_panel.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/dsl_code_editor.py` | 37 | 4 | 89%|
| `scarajectory/infrastructure/gui/dsl/dsl_console_view.py` | 27 | 3 | 89%|
| `scarajectory/infrastructure/gui/dsl/dsl_document_manager.py` | 42 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/dsl_editor_tab.py` | 109 | 40 | 63%|
| `scarajectory/infrastructure/gui/dsl/dsl_editor_tab_factory.py` | 24 | 1 | 96%|
| `scarajectory/infrastructure/gui/dsl/dsl_editor_toolbar.py` | 48 | 3 | 94%|
| `scarajectory/infrastructure/gui/dsl/dsl_example_catalog.py` | 36 | 4 | 89%|
| `scarajectory/infrastructure/gui/dsl/dsl_syntax_highlighter.py` | 55 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/emulator_launcher.py` | 34 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/iemulator_launcher.py` | 13 | 0 | 100%|
| `scarajectory/infrastructure/gui/editor/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/editor/itable.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/gui/editor/preview_tab.py` | 32 | 4 | 88%|
| `scarajectory/infrastructure/gui/editor/preview_tab_factory.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/gui/editor/table.py` | 78 | 29 | 63%|
| `scarajectory/infrastructure/gui/editor/validation_tab.py` | 42 | 9 | 79%|
| `scarajectory/infrastructure/gui/editor/waypoint_editor.py` | 72 | 17 | 76%|
| `scarajectory/infrastructure/gui/engine.py` | 104 | 19 | 82%|
| `scarajectory/infrastructure/gui/gui_event_mediator.py` | 40 | 0 | 100%|
| `scarajectory/infrastructure/gui/gui_factory.py` | 23 | 1 | 96%|
| `scarajectory/infrastructure/gui/igui.py` | 17 | 0 | 100%|
| `scarajectory/infrastructure/gui/menu/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/menu/iapp_menu_bar.py` | 16 | 16 | 0%|
| `scarajectory/infrastructure/gui/menu/menu_bar.py` | 97 | 32 | 67%|
| `scarajectory/infrastructure/gui/model/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/model/canvas_interaction_state.py` | 26 | 0 | 100%|
| `scarajectory/infrastructure/gui/model/canvas_settings.py` | 15 | 0 | 100%|
| `scarajectory/infrastructure/gui/model/canvas_tool_mode.py` | 17 | 0 | 100%|
| `scarajectory/infrastructure/gui/model/viewport_transform.py` | 47 | 0 | 100%|
| `scarajectory/infrastructure/gui/stream/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/stream/jog_tab.py` | 69 | 8 | 88%|
| `scarajectory/infrastructure/gui/stream/port_connection_panel.py` | 65 | 18 | 72%|
| `scarajectory/infrastructure/gui/stream/robot_override_panel.py` | 40 | 4 | 90%|
| `scarajectory/infrastructure/gui/stream/serial_console.py` | 51 | 17 | 67%|
| `scarajectory/infrastructure/gui/stream/stream_control_panel.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/gui/stream/stream_progress_adapter.py` | 36 | 13 | 64%|
| `scarajectory/infrastructure/gui/stream/stream_status_bar.py` | 30 | 5 | 83%|
| `scarajectory/infrastructure/gui/stream/streamer_tab.py` | 116 | 43 | 63%|
| `scarajectory/infrastructure/gui/theme/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/theme/theme.py` | 58 | 0 | 100%|
| `scarajectory/infrastructure/gui/toolbar/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/toolbar/itoolbar.py` | 15 | 15 | 0%|
| `scarajectory/infrastructure/gui/toolbar/toolbar.py` | 81 | 9 | 89%|
| `scarajectory/infrastructure/gui/toolbar/toolbar_factory.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/settings/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/settings/config_loader.py` | 83 | 1 | 99%|
| `scarajectory/infrastructure/settings/config_loader_factory.py` | 18 | 1 | 94%|
| `scarajectory/infrastructure/storage/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/storage/plan_storage_service.py` | 58 | 7 | 88%|
| `scarajectory/infrastructure/storage/plan_storage_service_factory.py` | 19 | 0 | 100%|
| `scarajectory/infrastructure/storage/trajectory_serializer.py` | 39 | 0 | 100%|
| `scarajectory/setup/__init__.py` | 9 | 0 | 100%|
| `scarajectory/setup/bundle.py` | 25 | 1 | 96%|
| `scarajectory/setup/dep_validator.py` | 36 | 5 | 86%|
| `scarajectory/setup/dependencies.py` | 21 | 0 | 100%|
| `scarajectory/setup/factory.py` | 122 | 4 | 97%|
| `scarajectory/setup/keys.py` | 37 | 0 | 100%|
| `scarajectory/setup/opt_validator.py` | 36 | 5 | 86%|
| `scarajectory/setup/options.py` | 20 | 0 | 100%|
| `scarajectory/setup/registry.py` | 34 | 1 | 97%|
| `scarajectory/setup/validator.py` | 53 | 5 | 91%|
| **Total** | 7524 | 974 | 87% |

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

Launch with initial trajectory plan file, deadzone restriction, and verbose output:

```bash
python3 main.py studio --file ./trajectories/rectangle_demo.json --dead-zone --verbose
```

| Option | Type | Choices | Description |
|---|:---:|:---:|---|
| **`--file`** | `str` | *File path* | Path to initial trajectory JSON plan file to load on startup. |
| **`--dead-zone`** | `bool` | *Flag* | Enable kinematic dead zone enforcement ($R_{min}$). |
| **`--verbose`** | `bool` | *Flag* | Enable verbose ATS operational logging. |

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
