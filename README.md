# SCARA Motion Trajectory Studio & Streamer

<img align="right" src="https://raw.githubusercontent.com/vroncevic/scarajectory/dev/docs/scarajectory_logo.png" width="25%">

**scarajectory** is a standalone CAD/CAM motion planning, kinematic validation, and real-time trajectory streaming software for SCARA robotic manipulators.

Developed in **[python](https://www.python.org/)** code.

The README is used to introduce the modules and provide instructions on
how to install the modules, any machine dependencies it may have and any
other information that should be provided before the modules are installed.

[![scarajectory python checker](https://github.com/vroncevic/scarajectory/actions/workflows/scarajectory_python_checker.yml/badge.svg)](https://github.com/vroncevic/scarajectory/actions/workflows/scarajectory_python_checker.yml) [![scarajectory package checker](https://github.com/vroncevic/scarajectory/actions/workflows/scarajectory_package_checker.yml/badge.svg)](https://github.com/vroncevic/scarajectory/actions/workflows/scarajectory_package_checker.yml) [![scarajectory interface checker](https://github.com/vroncevic/scarajectory/actions/workflows/scarajectory_interface_checker.yml/badge.svg)](https://github.com/vroncevic/scarajectory/actions/workflows/scarajectory_interface_checker.yml) [![scarajectory isp checker](https://github.com/vroncevic/scarajectory/actions/workflows/scarajectory_isp_checker.yml/badge.svg)](https://github.com/vroncevic/scarajectory/actions/workflows/scarajectory_isp_checker.yml) [![scarajectory srp checker](https://github.com/vroncevic/scarajectory/actions/workflows/scarajectory_srp_checker.yml/badge.svg)](https://github.com/vroncevic/scarajectory/actions/workflows/scarajectory_srp_checker.yml) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0) [![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/) [![GitHub issues open](https://img.shields.io/github/issues/vroncevic/scarajectory.svg)](https://github.com/vroncevic/scarajectory/issues) [![GitHub contributors](https://img.shields.io/github/contributors/vroncevic/scarajectory.svg)](https://github.com/vroncevic/scarajectory/graphs/contributors)

<p align="center">
  <img src="https://raw.githubusercontent.com/vroncevic/scarajectory/dev/docs/scarajectory_in_progress.png" alt="SCARA Trajectory Studio in Progress" width="95%">
</p>

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
    - [SCARA Ecosystem & Dual-Mode Motor Actuation](#-scara-ecosystem--dual-mode-motor-actuation)
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
* [scaralang - SCARA Domain-Specific Language, Kinematics & Protocol Engine](https://github.com/vroncevic/scaralang) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

> **Core Robotics & Language Engine Dependency ([scaralang](https://github.com/vroncevic/scaralang)):** `scarajectory` directly integrates `scaralang` as its foundational domain dependency. `scaralang` provides the SCARA Domain-Specific Language (DSL) lexer, parser, and AST compiler, the analytical forward and inverse kinematics engine (`solve_fk`, `solve_ik`), trajectory reachability and feedrate boundary validation, and the low-level binary wire framing protocol codecs.

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
         │   │   ├── __init__.py
         │   │   ├── jog/
         │   │   │   ├── __init__.py
         │   │   │   ├── jog_axis.py
         │   │   │   ├── jog_command.py
         │   │   │   └── jog_direction.py
         │   │   ├── preferences/
         │   │   │   ├── connection_preference.py
         │   │   │   └── __init__.py
         │   │   ├── protocol/
         │   │   │   ├── __init__.py
         │   │   │   ├── protocol_mode.py
         │   │   │   └── scara_response.py
         │   │   ├── state/
         │   │   │   ├── __init__.py
         │   │   │   ├── stream_session.py
         │   │   │   └── stream_state.py
         │   │   ├── streaming/
         │   │   │   ├── __init__.py
         │   │   │   ├── stream_config.py
         │   │   │   └── stream_pacing_config.py
         │   │   ├── telemetry/
         │   │   │   ├── diagnostics_bundle.py
         │   │   │   ├── diagnostics_snapshot.py
         │   │   │   ├── fault_event.py
         │   │   │   ├── __init__.py
         │   │   │   ├── move_event.py
         │   │   │   ├── scara_status.py
         │   │   │   ├── stream_progress.py
         │   │   │   └── stream_summary.py
         │   │   └── trajectory/
         │   │       ├── plan_metrics.py
         │   │       ├── validation_report.py
         │   │       └── waypoint.py
         │   └── service/
         │       ├── barrier/
         │       │   ├── iflow_barrier.py
         │       │   ├── iflow_barrier_coordinator.py
         │       │   └── __init__.py
         │       ├── classifier/
         │       │   ├── iflow_status_classifier.py
         │       │   ├── ihoming_status_classifier.py
         │       │   ├── imotion_status_classifier.py
         │       │   ├── __init__.py
         │       │   └── iresponse_parser.py
         │       ├── connection/
         │       │   ├── ichannel_dispatcher.py
         │       │   ├── iconnection.py
         │       │   ├── __init__.py
         │       │   ├── iraw_channel.py
         │       │   └── istream_connection.py
         │       ├── engine.py
         │       ├── event/
         │       │   ├── ibinary_frame_dispatcher.py
         │       │   ├── ibinary_frame_handler.py
         │       │   └── __init__.py
         │       ├── __init__.py
         │       ├── iservice.py
         │       ├── kinematics/
         │       │   ├── __init__.py
         │       │   ├── iscara_deadzone_calculator.py
         │       │   ├── scara_deadzone_calculator.py
         │       │   └── scara_deadzone_calculator_factory.py
         │       ├── manipulator/
         │       │   ├── ijog_controller.py
         │       │   ├── imotion_controller.py
         │       │   ├── __init__.py
         │       │   └── iquery_controller.py
         │       ├── pacing/
         │       │   ├── iflow_pacing_controller.py
         │       │   └── __init__.py
         │       ├── packet/
         │       │   ├── __init__.py
         │       │   └── ipacket_strategy.py
         │       ├── preferences/
         │       │   ├── connection_preference_factory.py
         │       │   ├── iconnection_repository.py
         │       │   └── __init__.py
         │       ├── service_factory.py
         │       ├── settings/
         │       │   ├── __init__.py
         │       │   ├── iscara_bounds_loader.py
         │       │   ├── iscara_bounds_parser.py
         │       │   ├── iscara_transmission_loader.py
         │       │   └── istream_config_loader.py
         │       ├── state/
         │       │   ├── __init__.py
         │       │   ├── istream_state_controller.py
         │       │   ├── istream_state_machine.py
         │       │   └── session_factory.py
         │       ├── storage/
         │       │   ├── __init__.py
         │       │   ├── iplan_loader.py
         │       │   ├── iplan_storage_service.py
         │       │   └── iplan_storer.py
         │       ├── streaming/
         │       │   ├── config_factory.py
         │       │   ├── ibinary_program_streamer.py
         │       │   ├── imotion_streamer.py
         │       │   ├── __init__.py
         │       │   ├── istream_control_transmitter.py
         │       │   ├── istream_dispatcher.py
         │       │   ├── istream_playback_controller.py
         │       │   ├── observer/
         │       │   │   ├── __init__.py
         │       │   │   ├── iobservable.py
         │       │   │   ├── iobserver.py
         │       │   │   └── istream_observer_dispatcher.py
         │       │   └── stream_pacing_config_factory.py
         │       ├── telemetry/
         │       │   ├── diagnostics_snapshot_factory.py
         │       │   ├── fault_event_factory.py
         │       │   ├── __init__.py
         │       │   └── move_event_factory.py
         │       ├── tool/
         │       │   ├── __init__.py
         │       │   ├── ipurge_valve_actuator.py
         │       │   └── itool_controller.py
         │       ├── trajectory/
         │       │   ├── contract/
         │       │   │   ├── __init__.py
         │       │   │   ├── iplan_command_service.py
         │       │   │   ├── iplan_persistence_service.py
         │       │   │   └── iplan_validation_service.py
         │       │   ├── history/
         │       │   │   ├── __init__.py
         │       │   │   ├── iplan_history.py
         │       │   │   ├── iplan_history_saver.py
         │       │   │   ├── plan_history.py
         │       │   │   └── plan_history_factory.py
         │       │   ├── __init__.py
         │       │   └── plan/
         │       │       ├── history/
         │       │       │   ├── __init__.py
         │       │       │   ├── plan_history_service.py
         │       │       │   └── plan_history_service_factory.py
         │       │       ├── __init__.py
         │       │       ├── itrajectory_history.py
         │       │       ├── itrajectory_mutable.py
         │       │       ├── itrajectory_read_only.py
         │       │       ├── mutation/
         │       │       │   ├── __init__.py
         │       │       │   ├── iplan_bulk_mutator.py
         │       │       │   ├── iplan_mutation_service.py
         │       │       │   ├── iplan_point_mutator.py
         │       │       │   ├── plan_mutation_service.py
         │       │       │   └── plan_mutation_service_factory.py
         │       │       ├── observer/
         │       │       │   ├── __init__.py
         │       │       │   ├── iplan_observer_dispatcher.py
         │       │       │   ├── itrajectory_observer.py
         │       │       │   ├── plan_observer_dispatcher.py
         │       │       │   └── plan_observer_dispatcher_factory.py
         │       │       ├── selection/
         │       │       │   ├── __init__.py
         │       │       │   ├── iplan_selection_coordinator.py
         │       │       │   ├── iplan_selection_manager.py
         │       │       │   ├── iplan_selection_navigator.py
         │       │       │   ├── iplan_selection_state.py
         │       │       │   ├── plan_selection_coordinator.py
         │       │       │   ├── plan_selection_coordinator_factory.py
         │       │       │   ├── plan_selection_manager.py
         │       │       │   ├── plan_selection_manager_factory.py
         │       │       │   ├── plan_selection_navigator.py
         │       │       │   ├── plan_selection_navigator_factory.py
         │       │       │   └── plan_selection_state.py
         │       │       └── store/
         │       │           ├── __init__.py
         │       │           ├── iwaypoint_bulk_mutator.py
         │       │           ├── iwaypoint_mutator.py
         │       │           ├── iwaypoint_query.py
         │       │           ├── iwaypoint_store.py
         │       │           ├── waypoint_bulk_mutator.py
         │       │           ├── waypoint_mutator.py
         │       │           ├── waypoint_query.py
         │       │           ├── waypoint_store.py
         │       │           └── waypoint_store_factory.py
         │       ├── transmission/
         │       │   ├── __init__.py
         │       │   └── itransmission_step_calculator.py
         │       └── worker/
         │           ├── ibyte_sender.py
         │           ├── icommand_formatter.py
         │           ├── icommand_sender.py
         │           ├── iexecution_service.py
         │           ├── iexecution_worker.py
         │           ├── __init__.py
         │           ├── istream_bytes_receiver.py
         │           ├── istream_line_receiver.py
         │           └── istream_loop_runner.py
         ├── engine.py
         ├── infrastructure/
         │   ├── barrier/
         │   │   ├── flow_barrier.py
         │   │   ├── flow_barrier_factory.py
         │   │   └── __init__.py
         │   ├── classifier/
         │   │   ├── __init__.py
         │   │   ├── iresponse_classification_rule.py
         │   │   ├── response_classification_registry.py
         │   │   ├── response_classification_registry_factory.py
         │   │   ├── response_classification_rule.py
         │   │   ├── response_parser.py
         │   │   ├── response_parser_factory.py
         │   │   └── status/
         │   │       ├── flow_status_classifier.py
         │   │       ├── flow_status_classifier_factory.py
         │   │       ├── homing_status_classifier.py
         │   │       ├── homing_status_classifier_factory.py
         │   │       ├── __init__.py
         │   │       ├── motion_status_classifier.py
         │   │       └── motion_status_classifier_factory.py
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
         │   │   ├── command_bundle.py
         │   │   ├── icommand_definition.py
         │   │   ├── icommand_executor.py
         │   │   ├── __init__.py
         │   │   ├── studio_command_definition.py
         │   │   └── studio_command_executor.py
         │   ├── config/
         │   │   ├── scara_geometry.json
         │   │   ├── scarajectory.cfg
         │   │   ├── scarajectory.logo
         │   │   └── scheme.json
         │   ├── connection/
         │   │   ├── channel_dispatcher.py
         │   │   ├── channel_dispatcher_factory.py
         │   │   ├── __init__.py
         │   │   ├── istream_raw_transceiver.py
         │   │   ├── stream_connection_manager.py
         │   │   ├── stream_connection_manager_factory.py
         │   │   ├── stream_raw_transceiver.py
         │   │   └── stream_raw_transceiver_factory.py
         │   ├── event/
         │   │   ├── binary_frame_dispatcher.py
         │   │   ├── binary_frame_dispatcher_factory.py
         │   │   └── __init__.py
         │   ├── formatter/
         │   │   ├── command/
         │   │   │   ├── config_command_formatter.py
         │   │   │   ├── __init__.py
         │   │   │   ├── jog_command_formatter.py
         │   │   │   ├── motion_command_formatter.py
         │   │   │   ├── query_command_formatter.py
         │   │   │   ├── system_command_formatter.py
         │   │   │   └── tool_command_formatter.py
         │   │   ├── command_formatter.py
         │   │   ├── command_formatter_factory.py
         │   │   ├── command_templates.py
         │   │   └── __init__.py
         │   ├── gui/
         │   │   ├── canvas/
         │   │   │   ├── bundle.py
         │   │   │   ├── canvas_event_binder.py
         │   │   │   ├── canvas_event_binder_factory.py
         │   │   │   ├── handler/
         │   │   │   │   ├── canvas_drag_handler.py
         │   │   │   │   ├── canvas_event_context.py
         │   │   │   │   ├── canvas_mouse_handler.py
         │   │   │   │   ├── canvas_mouse_handler_factory.py
         │   │   │   │   ├── canvas_shape_handler.py
         │   │   │   │   ├── canvas_tool_handler.py
         │   │   │   │   ├── icanvas_mouse_handler.py
         │   │   │   │   ├── __init__.py
         │   │   │   │   ├── mouse_handler_bundle.py
         │   │   │   │   ├── mouse_handler_init_bundle.py
         │   │   │   │   ├── pan/
         │   │   │   │   │   ├── canvas_viewport_pan_handler.py
         │   │   │   │   │   ├── canvas_viewport_pan_handler_factory.py
         │   │   │   │   │   ├── icanvas_viewport_pan_handler.py
         │   │   │   │   │   └── __init__.py
         │   │   │   │   └── selection/
         │   │   │   │       ├── canvas_selection_mouse_handler.py
         │   │   │   │       ├── canvas_selection_mouse_handler_factory.py
         │   │   │   │       ├── icanvas_selection_mouse_handler.py
         │   │   │   │       └── __init__.py
         │   │   │   ├── icanvas.py
         │   │   │   ├── __init__.py
         │   │   │   ├── navigation/
         │   │   │   │   ├── canvas_view_navigator.py
         │   │   │   │   ├── canvas_view_navigator_factory.py
         │   │   │   │   ├── icanvas_view_navigator.py
         │   │   │   │   ├── icanvas_view_target.py
         │   │   │   │   └── __init__.py
         │   │   │   ├── observer/
         │   │   │   │   ├── canvas_plan_observer_bridge.py
         │   │   │   │   ├── canvas_plan_observer_bridge_factory.py
         │   │   │   │   ├── icanvas_plan_observer_bridge.py
         │   │   │   │   └── __init__.py
         │   │   │   ├── render/
         │   │   │   │   ├── forbidden_zone_renderer.py
         │   │   │   │   ├── ilayer_renderer.py
         │   │   │   │   ├── __init__.py
         │   │   │   │   ├── polar_grid_renderer.py
         │   │   │   │   ├── preview_renderer.py
         │   │   │   │   ├── reach_boundary_renderer.py
         │   │   │   │   ├── renderer.py
         │   │   │   │   ├── trajectory_renderer.py
         │   │   │   │   ├── waypoint_node_renderer.py
         │   │   │   │   └── waypoint_node_renderer_factory.py
         │   │   │   ├── status/
         │   │   │   │   ├── canvas_status_presenter.py
         │   │   │   │   ├── canvas_status_presenter_factory.py
         │   │   │   │   ├── icanvas_status_presenter.py
         │   │   │   │   └── __init__.py
         │   │   │   ├── trajectory_canvas.py
         │   │   │   └── trajectory_canvas_factory.py
         │   │   ├── connection/
         │   │   │   ├── __init__.py
         │   │   │   ├── iport_connection_delegate.py
         │   │   │   ├── null_port_connection_delegate.py
         │   │   │   └── port_connection_panel.py
         │   │   ├── console/
         │   │   │   ├── __init__.py
         │   │   │   ├── serial_console.py
         │   │   │   ├── serial_console_builder.py
         │   │   │   └── serial_console_builder_factory.py
         │   │   ├── controls/
         │   │   │   ├── bundle.py
         │   │   │   ├── controls_panel.py
         │   │   │   ├── controls_panel_factory.py
         │   │   │   ├── icontrols_panel.py
         │   │   │   ├── __init__.py
         │   │   │   ├── itabs_assembler.py
         │   │   │   ├── manipulator_controllers_bundle.py
         │   │   │   ├── manipulator_controllers_factory.py
         │   │   │   ├── tabs_assembler.py
         │   │   │   ├── tabs_assembler_factory.py
         │   │   │   └── tabs_bundle.py
         │   │   ├── dsl/
         │   │   │   ├── bundle.py
         │   │   │   ├── code_editor.py
         │   │   │   ├── code_editor_factory.py
         │   │   │   ├── console_view.py
         │   │   │   ├── document/
         │   │   │   │   ├── document_manager.py
         │   │   │   │   ├── document_manager_factory.py
         │   │   │   │   ├── example_catalog.py
         │   │   │   │   ├── example_catalog_factory.py
         │   │   │   │   └── __init__.py
         │   │   │   ├── dsl_editor_tab.py
         │   │   │   ├── dsl_editor_tab_factory.py
         │   │   │   ├── handler/
         │   │   │   │   ├── execution_handler.py
         │   │   │   │   ├── execution_handler_bundle.py
         │   │   │   │   ├── execution_handler_factory.py
         │   │   │   │   ├── file_handler.py
         │   │   │   │   ├── file_handler_bundle.py
         │   │   │   │   ├── file_handler_factory.py
         │   │   │   │   ├── iexecution_delegate.py
         │   │   │   │   ├── ifile_delegate.py
         │   │   │   │   └── __init__.py
         │   │   │   ├── __init__.py
         │   │   │   ├── syntax/
         │   │   │   │   ├── highlighter.py
         │   │   │   │   ├── highlighter_factory.py
         │   │   │   │   ├── ihighlighter.py
         │   │   │   │   ├── __init__.py
         │   │   │   │   ├── itag_applier.py
         │   │   │   │   ├── itokenizer.py
         │   │   │   │   ├── tag_applier.py
         │   │   │   │   ├── tag_applier_factory.py
         │   │   │   │   ├── token.py
         │   │   │   │   ├── tokenizer.py
         │   │   │   │   └── tokenizer_factory.py
         │   │   │   └── toolbar.py
         │   │   ├── editor/
         │   │   │   ├── __init__.py
         │   │   │   ├── table/
         │   │   │   │   ├── bundle.py
         │   │   │   │   ├── __init__.py
         │   │   │   │   ├── itable.py
         │   │   │   │   ├── selection_handler.py
         │   │   │   │   ├── selection_handler_factory.py
         │   │   │   │   └── trajectory_table.py
         │   │   │   ├── waypoint_coordinate_inputs.py
         │   │   │   ├── waypoint_edit_applier.py
         │   │   │   ├── waypoint_edit_applier_factory.py
         │   │   │   └── waypoint_editor.py
         │   │   ├── emulator/
         │   │   │   ├── emulator_launcher.py
         │   │   │   ├── emulator_launcher_factory.py
         │   │   │   ├── iemulator_launcher.py
         │   │   │   └── __init__.py
         │   │   ├── igui.py
         │   │   ├── __init__.py
         │   │   ├── layout/
         │   │   │   ├── canvas_pane_builder.py
         │   │   │   ├── canvas_pane_builder_factory.py
         │   │   │   ├── editor_pane_builder.py
         │   │   │   ├── editor_pane_builder_factory.py
         │   │   │   ├── icanvas_pane_builder.py
         │   │   │   ├── ieditor_pane_builder.py
         │   │   │   ├── __init__.py
         │   │   │   ├── itoolbar_layout_builder.py
         │   │   │   ├── main_content_builder.py
         │   │   │   ├── main_content_builder_factory.py
         │   │   │   ├── toolbar_layout_builder.py
         │   │   │   └── toolbar_layout_builder_factory.py
         │   │   ├── manipulator/
         │   │   │   ├── imanipulator_action_delegate.py
         │   │   │   ├── __init__.py
         │   │   │   ├── jog/
         │   │   │   │   ├── axis_grid_panel.py
         │   │   │   │   ├── axis_grid_panel_factory.py
         │   │   │   │   ├── controllers_bundle.py
         │   │   │   │   ├── __init__.py
         │   │   │   │   ├── jog_tab.py
         │   │   │   │   ├── jog_tab_factory.py
         │   │   │   │   ├── panel_bundle.py
         │   │   │   │   ├── power_panel.py
         │   │   │   │   ├── power_panel_factory.py
         │   │   │   │   ├── raw_command_panel.py
         │   │   │   │   ├── raw_command_panel_factory.py
         │   │   │   │   ├── tool_panel.py
         │   │   │   │   └── tool_panel_factory.py
         │   │   │   ├── manipulator_override_panel.py
         │   │   │   └── null_manipulator_action_delegate.py
         │   │   ├── menu/
         │   │   │   ├── app_menu_bar.py
         │   │   │   ├── app_menu_bar_factory.py
         │   │   │   ├── builders_bundle.py
         │   │   │   ├── bundle.py
         │   │   │   ├── iapp_menu_bar.py
         │   │   │   ├── __init__.py
         │   │   │   ├── menu_hotkey_binder.py
         │   │   │   ├── menu_hotkey_binder_factory.py
         │   │   │   ├── menu_layout_builder.py
         │   │   │   └── menu_layout_builder_factory.py
         │   │   ├── model/
         │   │   │   ├── canvas_interaction_state.py
         │   │   │   ├── canvas_settings.py
         │   │   │   ├── canvas_tool_mode.py
         │   │   │   ├── __init__.py
         │   │   │   └── viewport_transform.py
         │   │   ├── preview/
         │   │   │   ├── __init__.py
         │   │   │   ├── preview_tab.py
         │   │   │   └── preview_tab_factory.py
         │   │   ├── scarajectory_gui.py
         │   │   ├── scarajectory_gui_bundle.py
         │   │   ├── scarajectory_gui_factory.py
         │   │   ├── scarajectory_gui_init_bundle.py
         │   │   ├── streaming/
         │   │   │   ├── bundle.py
         │   │   │   ├── handler/
         │   │   │   │   ├── __init__.py
         │   │   │   │   ├── playback_handler_bundle.py
         │   │   │   │   ├── stream_playback_action_handler.py
         │   │   │   │   ├── stream_playback_action_handler_factory.py
         │   │   │   │   ├── stream_tool_action_handler.py
         │   │   │   │   └── stream_tool_action_handler_factory.py
         │   │   │   ├── __init__.py
         │   │   │   ├── observer/
         │   │   │   │   ├── gui_stream_observer_bridge.py
         │   │   │   │   ├── gui_stream_observer_bridge_factory.py
         │   │   │   │   ├── igui_stream_observer_bridge.py
         │   │   │   │   └── __init__.py
         │   │   │   ├── panel/
         │   │   │   │   ├── __init__.py
         │   │   │   │   ├── istream_control_delegate.py
         │   │   │   │   ├── stream_control_panel.py
         │   │   │   │   ├── stream_progress_adapter.py
         │   │   │   │   └── stream_status_bar.py
         │   │   │   ├── streamer_action_bundle.py
         │   │   │   ├── streamer_controllers_bundle.py
         │   │   │   ├── streamer_tab.py
         │   │   │   └── streamer_tab_factory.py
         │   │   ├── theme/
         │   │   │   ├── __init__.py
         │   │   │   ├── theme_button_styler.py
         │   │   │   ├── theme_button_styler_factory.py
         │   │   │   ├── theme_manager.py
         │   │   │   ├── theme_notebook_styler.py
         │   │   │   └── theme_notebook_styler_factory.py
         │   │   ├── toolbar/
         │   │   │   ├── bundle.py
         │   │   │   ├── __init__.py
         │   │   │   ├── itoolbar.py
         │   │   │   ├── navigation_controls.py
         │   │   │   ├── navigation_controls_factory.py
         │   │   │   ├── parameter_inputs.py
         │   │   │   ├── parameter_inputs_bundle.py
         │   │   │   ├── parameter_inputs_factory.py
         │   │   │   ├── tool_selector.py
         │   │   │   ├── tool_selector_factory.py
         │   │   │   ├── toolbar.py
         │   │   │   └── toolbar_factory.py
         │   │   └── validation/
         │   │       ├── __init__.py
         │   │       ├── validation_tab.py
         │   │       └── validation_tab_factory.py
         │   ├── __init__.py
         │   ├── manipulator/
         │   │   ├── __init__.py
         │   │   ├── jog_controller.py
         │   │   ├── jog_controller_factory.py
         │   │   ├── motion_controller.py
         │   │   ├── motion_controller_factory.py
         │   │   ├── query_controller.py
         │   │   └── query_controller_factory.py
         │   ├── pacing/
         │   │   ├── bundle.py
         │   │   ├── flow_barrier_coordinator.py
         │   │   ├── flow_barrier_coordinator_factory.py
         │   │   ├── flow_pacing_bundle_factory.py
         │   │   ├── flow_pacing_controller.py
         │   │   ├── flow_pacing_controller_factory.py
         │   │   └── __init__.py
         │   ├── packet/
         │   │   ├── binary_packet_strategy.py
         │   │   ├── binary_packet_strategy_factory.py
         │   │   └── __init__.py
         │   ├── preferences/
         │   │   ├── connection_repository.py
         │   │   ├── connection_repository_factory.py
         │   │   └── __init__.py
         │   ├── settings/
         │   │   ├── bounds/
         │   │   │   ├── __init__.py
         │   │   │   ├── scara_bounds_loader.py
         │   │   │   ├── scara_bounds_loader_factory.py
         │   │   │   ├── scara_bounds_parser.py
         │   │   │   └── scara_bounds_parser_factory.py
         │   │   ├── __init__.py
         │   │   ├── isettings_reader.py
         │   │   ├── settings_reader.py
         │   │   ├── settings_reader_factory.py
         │   │   ├── stream/
         │   │   │   ├── __init__.py
         │   │   │   ├── stream_config_loader.py
         │   │   │   └── stream_config_loader_factory.py
         │   │   └── transmission/
         │   │       ├── __init__.py
         │   │       ├── scara_transmission_loader.py
         │   │       └── scara_transmission_loader_factory.py
         │   ├── state/
         │   │   ├── __init__.py
         │   │   ├── stream_state_machine.py
         │   │   └── stream_state_machine_factory.py
         │   ├── storage/
         │   │   ├── __init__.py
         │   │   ├── plan_loader.py
         │   │   ├── plan_storage_service.py
         │   │   ├── plan_storage_service_factory.py
         │   │   ├── plan_storer.py
         │   │   └── trajectory_serializer.py
         │   ├── streaming/
         │   │   ├── assembly/
         │   │   │   ├── __init__.py
         │   │   │   ├── stream_pacing_assembler.py
         │   │   │   ├── stream_pipeline_assembler.py
         │   │   │   ├── stream_transport_assembler.py
         │   │   │   ├── stream_worker_assembler.py
         │   │   │   └── worker_bundle.py
         │   │   ├── binary_program_streamer.py
         │   │   ├── binary_program_streamer_factory.py
         │   │   ├── bundle.py
         │   │   ├── __init__.py
         │   │   ├── observer/
         │   │   │   ├── __init__.py
         │   │   │   ├── istream_observer_registry.py
         │   │   │   ├── istream_telemetry_notifier.py
         │   │   │   ├── stream_observer_dispatcher.py
         │   │   │   ├── stream_observer_dispatcher_factory.py
         │   │   │   ├── stream_observer_registry.py
         │   │   │   ├── stream_observer_registry_factory.py
         │   │   │   ├── stream_telemetry_notifier.py
         │   │   │   └── stream_telemetry_notifier_factory.py
         │   │   ├── stream_control_transmitter.py
         │   │   ├── stream_control_transmitter_factory.py
         │   │   ├── stream_playback_controller.py
         │   │   └── stream_playback_controller_factory.py
         │   ├── tool/
         │   │   ├── __init__.py
         │   │   ├── tool_controller.py
         │   │   ├── tool_controller_factory.py
         │   │   ├── valve_pulse_worker.py
         │   │   └── valve_pulse_worker_factory.py
         │   ├── transmission/
         │   │   ├── __init__.py
         │   │   ├── transmission_step_calculator.py
         │   │   └── transmission_step_calculator_factory.py
         │   ├── transport/
         │   │   ├── bundle.py
         │   │   ├── driver/
         │   │   │   ├── ichannel.py
         │   │   │   ├── __init__.py
         │   │   │   ├── serial_channel.py
         │   │   │   ├── serial_channel_factory.py
         │   │   │   ├── serial_port_scanner.py
         │   │   │   ├── tcp_channel.py
         │   │   │   └── tcp_channel_factory.py
         │   │   ├── __init__.py
         │   │   ├── istream_transport_connection.py
         │   │   ├── istream_transport_transceiver.py
         │   │   ├── listener/
         │   │   │   ├── __init__.py
         │   │   │   ├── itransport_listener.py
         │   │   │   ├── itransport_listener_holder.py
         │   │   │   ├── null_transport_listener.py
         │   │   │   ├── stream_ascii_transport_listener.py
         │   │   │   ├── stream_ascii_transport_listener_factory.py
         │   │   │   ├── stream_binary_transport_listener.py
         │   │   │   ├── stream_binary_transport_listener_factory.py
         │   │   │   └── transport_listener_holder.py
         │   │   ├── stream_transport_connection.py
         │   │   ├── stream_transport_connection_factory.py
         │   │   ├── stream_transport_transceiver.py
         │   │   ├── stream_transport_transceiver_factory.py
         │   │   ├── transport_factory.py
         │   │   └── worker/
         │   │       ├── __init__.py
         │   │       ├── itransport_reader_worker.py
         │   │       ├── transport_reader_worker.py
         │   │       └── transport_reader_worker_factory.py
         │   └── worker/
         │       ├── binary/
         │       │   ├── binary_stream_execution_worker.py
         │       │   ├── binary_stream_execution_worker_factory.py
         │       │   ├── binary_stream_frame_handler.py
         │       │   ├── binary_stream_frame_handler_factory.py
         │       │   ├── binary_stream_loop_runner.py
         │       │   ├── binary_stream_loop_runner_factory.py
         │       │   ├── ibinary_stream_frame_handler.py
         │       │   ├── ibinary_stream_loop_runner.py
         │       │   └── __init__.py
         │       ├── __init__.py
         │       ├── istream_queue_drainer.py
         │       ├── istream_step_dispatcher.py
         │       ├── stream_execution_worker.py
         │       ├── stream_execution_worker_factory.py
         │       ├── stream_loop_runner.py
         │       ├── stream_loop_runner_factory.py
         │       ├── stream_queue_drainer.py
         │       ├── stream_queue_drainer_factory.py
         │       ├── stream_step_dispatcher.py
         │       └── stream_step_dispatcher_factory.py
         ├── __init__.py
         ├── py.typed
         └── setup/
             ├── assembly/
             │   ├── app_core_assembler.py
             │   ├── app_core_bundle.py
             │   ├── app_presentation_assembler.py
             │   ├── app_runtime_assembler.py
             │   ├── app_runtime_bundle.py
             │   └── __init__.py
             ├── bundle.py
             ├── dep_validator.py
             ├── dependencies.py
             ├── factory.py
             ├── __init__.py
             ├── keys.py
             ├── opt_validator.py
             ├── options.py
             ├── pipeline/
             │   ├── dsl_pipeline_builder.py
             │   ├── __init__.py
             │   ├── plan_pipeline_builder.py
             │   ├── plan_pipeline_bundle.py
             │   ├── stream_pipeline_builder.py
             │   └── stream_pipeline_bundle.py
             ├── registry.py
             └── validator.py

     106 directories, 578 files
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
         ▼                         ▼                        ▼                          │ Classifiers
┌──────────────────┐      ┌──────────────────┐     ┌─────────────────┐                 ▼
│TrajectoryValidat.│      │  ScaraDslService │     │ ScaraPlanExport │        ┌──────────────────┐
│(Workspace Bounds)│      │  (DSL Compiler)  │     │  (Plan to DSL)  │        │  SerialStreamer  │
└──────────────────┘      └────────┬─────────┘     └─────────────────┘        └────────┬─────────┘
                                   │                                                   │
              ┌────────────────────┼────────────────────┐                              ▼
              ▼                    ▼                    ▼                     ┌──────────────────┐
     ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐            │Response & FlowCls│
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

##### 🌐 SCARA Ecosystem & Dual-Mode Motor Actuation

**scarajectory** is the desktop CAD/CAM studio and trajectory streaming hub within the unified SCARA robotics architecture:
* **[scaralang](https://github.com/vroncevic/scaralang) Integration:** `scarajectory` uses `scaralang` as the Single Source of Truth (SSoT) to parse, validate, and compile Cartesian trajectories and `.scara` DSL scripts into deterministic binary wire protocol frames (`0xAA 0x55`).
* **Hardware Streaming to [scara_base](https://github.com/dof2bot/scara):** Wire frames stream over UART / USB-CDC to the Raspberry Pi Pico (RP2040) firmware, which executes real-time motion across dual motor drive modes:
  * **Open-Loop Mode (TMC2209):** Coordinated microstepping pulses generated by RP2040 PIO state machines driving silent TMC2209 stepper stages.
  * **Closed-Loop Mode (MKS SERVO42D over CAN Bus):** NEMA stepper motors equipped with **MKS SERVO42D** closed-loop modules communicating with the Raspberry Pi Pico over high-speed differential **CAN bus** (CAN_H / CAN_L) for stall-free closed-loop positioning with magnetic encoder feedback.
* **Digital Twin Synchronization with [scaraemu](https://github.com/vroncevic/scaraemu):** Real-time closed-loop TCP loopback streaming to `scaraemu` for visual motion animation and validation before physical execution.

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
| `scarajectory/core/model/jog/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/model/jog/jog_axis.py` | 16 | 0 | 100%|
| `scarajectory/core/model/jog/jog_command.py` | 18 | 0 | 100%|
| `scarajectory/core/model/jog/jog_direction.py` | 14 | 0 | 100%|
| `scarajectory/core/model/preferences/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/model/preferences/connection_preference.py` | 14 | 0 | 100%|
| `scarajectory/core/model/protocol/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/model/protocol/protocol_mode.py` | 14 | 0 | 100%|
| `scarajectory/core/model/protocol/scara_response.py` | 16 | 0 | 100%|
| `scarajectory/core/model/state/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/model/state/stream_session.py` | 19 | 0 | 100%|
| `scarajectory/core/model/state/stream_state.py` | 17 | 0 | 100%|
| `scarajectory/core/model/streaming/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/model/streaming/stream_config.py` | 18 | 0 | 100%|
| `scarajectory/core/model/streaming/stream_pacing_config.py` | 15 | 0 | 100%|
| `scarajectory/core/model/telemetry/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/model/telemetry/diagnostics_bundle.py` | 29 | 0 | 100%|
| `scarajectory/core/model/telemetry/diagnostics_snapshot.py` | 29 | 0 | 100%|
| `scarajectory/core/model/telemetry/fault_event.py` | 15 | 0 | 100%|
| `scarajectory/core/model/telemetry/move_event.py` | 14 | 0 | 100%|
| `scarajectory/core/model/telemetry/scara_status.py` | 19 | 0 | 100%|
| `scarajectory/core/model/telemetry/stream_progress.py` | 22 | 0 | 100%|
| `scarajectory/core/model/telemetry/stream_summary.py` | 18 | 0 | 100%|
| `scarajectory/core/model/trajectory/waypoint.py` | 19 | 0 | 100%|
| `scarajectory/core/service/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/barrier/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/barrier/iflow_barrier.py` | 16 | 0 | 100%|
| `scarajectory/core/service/barrier/iflow_barrier_coordinator.py` | 16 | 0 | 100%|
| `scarajectory/core/service/classifier/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/classifier/iflow_status_classifier.py` | 15 | 0 | 100%|
| `scarajectory/core/service/classifier/ihoming_status_classifier.py` | 14 | 0 | 100%|
| `scarajectory/core/service/classifier/imotion_status_classifier.py` | 16 | 0 | 100%|
| `scarajectory/core/service/classifier/iresponse_parser.py` | 16 | 0 | 100%|
| `scarajectory/core/service/connection/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/connection/ichannel_dispatcher.py` | 22 | 0 | 100%|
| `scarajectory/core/service/connection/iconnection.py` | 16 | 0 | 100%|
| `scarajectory/core/service/connection/iraw_channel.py` | 15 | 0 | 100%|
| `scarajectory/core/service/connection/istream_connection.py` | 14 | 0 | 100%|
| `scarajectory/core/service/engine.py` | 38 | 0 | 100%|
| `scarajectory/core/service/event/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/event/ibinary_frame_dispatcher.py` | 15 | 0 | 100%|
| `scarajectory/core/service/event/ibinary_frame_handler.py` | 13 | 0 | 100%|
| `scarajectory/core/service/iservice.py` | 19 | 0 | 100%|
| `scarajectory/core/service/kinematics/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/kinematics/iscara_deadzone_calculator.py` | 14 | 0 | 100%|
| `scarajectory/core/service/kinematics/scara_deadzone_calculator.py` | 16 | 0 | 100%|
| `scarajectory/core/service/kinematics/scara_deadzone_calculator_factory.py` | 17 | 0 | 100%|
| `scarajectory/core/service/manipulator/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/manipulator/ijog_controller.py` | 14 | 0 | 100%|
| `scarajectory/core/service/manipulator/imotion_controller.py` | 16 | 0 | 100%|
| `scarajectory/core/service/manipulator/iquery_controller.py` | 14 | 0 | 100%|
| `scarajectory/core/service/pacing/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/pacing/iflow_pacing_controller.py` | 18 | 0 | 100%|
| `scarajectory/core/service/packet/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/packet/ipacket_strategy.py` | 14 | 0 | 100%|
| `scarajectory/core/service/preferences/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/preferences/connection_preference_factory.py` | 23 | 0 | 100%|
| `scarajectory/core/service/preferences/iconnection_repository.py` | 16 | 0 | 100%|
| `scarajectory/core/service/service_factory.py` | 21 | 1 | 95%|
| `scarajectory/core/service/settings/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/settings/iscara_bounds_loader.py` | 16 | 0 | 100%|
| `scarajectory/core/service/settings/iscara_bounds_parser.py` | 17 | 0 | 100%|
| `scarajectory/core/service/settings/iscara_transmission_loader.py` | 16 | 0 | 100%|
| `scarajectory/core/service/settings/istream_config_loader.py` | 16 | 0 | 100%|
| `scarajectory/core/service/state/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/state/istream_state_controller.py` | 16 | 0 | 100%|
| `scarajectory/core/service/state/istream_state_machine.py` | 18 | 0 | 100%|
| `scarajectory/core/service/state/session_factory.py` | 19 | 1 | 95%|
| `scarajectory/core/service/storage/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/storage/iplan_loader.py` | 16 | 0 | 100%|
| `scarajectory/core/service/storage/iplan_storage_service.py` | 14 | 0 | 100%|
| `scarajectory/core/service/storage/iplan_storer.py` | 17 | 0 | 100%|
| `scarajectory/core/service/streaming/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/streaming/config_factory.py` | 18 | 0 | 100%|
| `scarajectory/core/service/streaming/ibinary_program_streamer.py` | 14 | 0 | 100%|
| `scarajectory/core/service/streaming/imotion_streamer.py` | 14 | 0 | 100%|
| `scarajectory/core/service/streaming/istream_control_transmitter.py` | 17 | 0 | 100%|
| `scarajectory/core/service/streaming/istream_dispatcher.py` | 14 | 0 | 100%|
| `scarajectory/core/service/streaming/istream_playback_controller.py` | 18 | 0 | 100%|
| `scarajectory/core/service/streaming/observer/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/streaming/observer/iobservable.py` | 14 | 0 | 100%|
| `scarajectory/core/service/streaming/observer/iobserver.py` | 15 | 0 | 100%|
| `scarajectory/core/service/streaming/observer/istream_observer_dispatcher.py` | 16 | 0 | 100%|
| `scarajectory/core/service/streaming/stream_pacing_config_factory.py` | 23 | 0 | 100%|
| `scarajectory/core/service/telemetry/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/telemetry/diagnostics_snapshot_factory.py` | 18 | 0 | 100%|
| `scarajectory/core/service/telemetry/fault_event_factory.py` | 17 | 0 | 100%|
| `scarajectory/core/service/telemetry/move_event_factory.py` | 17 | 0 | 100%|
| `scarajectory/core/service/tool/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/tool/ipurge_valve_actuator.py` | 13 | 0 | 100%|
| `scarajectory/core/service/tool/itool_controller.py` | 15 | 0 | 100%|
| `scarajectory/core/service/trajectory/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/trajectory/contract/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/trajectory/contract/iplan_command_service.py` | 16 | 0 | 100%|
| `scarajectory/core/service/trajectory/contract/iplan_persistence_service.py` | 14 | 0 | 100%|
| `scarajectory/core/service/trajectory/contract/iplan_validation_service.py` | 13 | 0 | 100%|
| `scarajectory/core/service/trajectory/history/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/trajectory/history/iplan_history.py` | 17 | 0 | 100%|
| `scarajectory/core/service/trajectory/history/iplan_history_saver.py` | 15 | 0 | 100%|
| `scarajectory/core/service/trajectory/history/plan_history.py` | 38 | 1 | 97%|
| `scarajectory/core/service/trajectory/history/plan_history_factory.py` | 17 | 1 | 94%|
| `scarajectory/core/service/trajectory/plan/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/history/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/history/plan_history_service.py` | 40 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/history/plan_history_service_factory.py` | 21 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/itrajectory_history.py` | 14 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/itrajectory_mutable.py` | 21 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/itrajectory_read_only.py` | 18 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/mutation/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/mutation/iplan_bulk_mutator.py` | 16 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/mutation/iplan_mutation_service.py` | 14 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/mutation/iplan_point_mutator.py` | 17 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/mutation/plan_mutation_service.py` | 63 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/mutation/plan_mutation_service_factory.py` | 21 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/observer/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/observer/iplan_observer_dispatcher.py` | 18 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/observer/itrajectory_observer.py` | 14 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/observer/plan_observer_dispatcher.py` | 29 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/observer/plan_observer_dispatcher_factory.py` | 17 | 1 | 94%|
| `scarajectory/core/service/trajectory/plan/selection/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/selection/iplan_selection_coordinator.py` | 15 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/selection/iplan_selection_manager.py` | 14 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/selection/iplan_selection_navigator.py` | 16 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/selection/iplan_selection_state.py` | 17 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/selection/plan_selection_coordinator.py` | 27 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/selection/plan_selection_coordinator_factory.py` | 20 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/selection/plan_selection_manager.py` | 35 | 1 | 97%|
| `scarajectory/core/service/trajectory/plan/selection/plan_selection_manager_factory.py` | 26 | 1 | 96%|
| `scarajectory/core/service/trajectory/plan/selection/plan_selection_navigator.py` | 23 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/selection/plan_selection_navigator_factory.py` | 18 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/selection/plan_selection_state.py` | 28 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/store/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/store/iwaypoint_bulk_mutator.py` | 16 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/store/iwaypoint_mutator.py` | 17 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/store/iwaypoint_query.py` | 18 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/store/iwaypoint_store.py` | 15 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/store/waypoint_bulk_mutator.py` | 21 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/store/waypoint_mutator.py` | 29 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/store/waypoint_query.py` | 22 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/store/waypoint_store.py` | 41 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/store/waypoint_store_factory.py` | 27 | 1 | 96%|
| `scarajectory/core/service/transmission/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/transmission/itransmission_step_calculator.py` | 15 | 0 | 100%|
| `scarajectory/core/service/worker/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/worker/ibyte_sender.py` | 13 | 0 | 100%|
| `scarajectory/core/service/worker/icommand_formatter.py` | 14 | 0 | 100%|
| `scarajectory/core/service/worker/icommand_sender.py` | 13 | 0 | 100%|
| `scarajectory/core/service/worker/iexecution_service.py` | 16 | 0 | 100%|
| `scarajectory/core/service/worker/iexecution_worker.py` | 18 | 0 | 100%|
| `scarajectory/core/service/worker/istream_bytes_receiver.py` | 14 | 0 | 100%|
| `scarajectory/core/service/worker/istream_line_receiver.py` | 14 | 0 | 100%|
| `scarajectory/core/service/worker/istream_loop_runner.py` | 16 | 0 | 100%|
| `scarajectory/engine.py` | 58 | 2 | 97%|
| `scarajectory/infrastructure/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/barrier/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/barrier/flow_barrier.py` | 23 | 0 | 100%|
| `scarajectory/infrastructure/barrier/flow_barrier_factory.py` | 17 | 0 | 100%|
| `scarajectory/infrastructure/classifier/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/classifier/iresponse_classification_rule.py` | 15 | 0 | 100%|
| `scarajectory/infrastructure/classifier/response_classification_registry.py` | 23 | 0 | 100%|
| `scarajectory/infrastructure/classifier/response_classification_registry_factory.py` | 22 | 0 | 100%|
| `scarajectory/infrastructure/classifier/response_classification_rule.py` | 28 | 0 | 100%|
| `scarajectory/infrastructure/classifier/response_parser.py` | 32 | 0 | 100%|
| `scarajectory/infrastructure/classifier/response_parser_factory.py` | 23 | 0 | 100%|
| `scarajectory/infrastructure/classifier/status/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/classifier/status/flow_status_classifier.py` | 24 | 0 | 100%|
| `scarajectory/infrastructure/classifier/status/flow_status_classifier_factory.py` | 22 | 0 | 100%|
| `scarajectory/infrastructure/classifier/status/homing_status_classifier.py` | 17 | 0 | 100%|
| `scarajectory/infrastructure/classifier/status/homing_status_classifier_factory.py` | 17 | 0 | 100%|
| `scarajectory/infrastructure/classifier/status/motion_status_classifier.py` | 28 | 0 | 100%|
| `scarajectory/infrastructure/classifier/status/motion_status_classifier_factory.py` | 22 | 0 | 100%|
| `scarajectory/infrastructure/cli/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/cli/engine.py` | 41 | 0 | 100%|
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
| `scarajectory/infrastructure/command/command_bundle.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/command/icommand_definition.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/command/icommand_executor.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/command/studio_command_definition.py` | 24 | 0 | 100%|
| `scarajectory/infrastructure/command/studio_command_executor.py` | 37 | 0 | 100%|
| `scarajectory/infrastructure/connection/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/connection/channel_dispatcher.py` | 46 | 0 | 100%|
| `scarajectory/infrastructure/connection/channel_dispatcher_factory.py` | 20 | 0 | 100%|
| `scarajectory/infrastructure/connection/istream_raw_transceiver.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/connection/stream_connection_manager.py` | 30 | 0 | 100%|
| `scarajectory/infrastructure/connection/stream_connection_manager_factory.py` | 19 | 0 | 100%|
| `scarajectory/infrastructure/connection/stream_raw_transceiver.py` | 28 | 0 | 100%|
| `scarajectory/infrastructure/connection/stream_raw_transceiver_factory.py` | 19 | 0 | 100%|
| `scarajectory/infrastructure/event/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/event/binary_frame_dispatcher.py` | 28 | 0 | 100%|
| `scarajectory/infrastructure/event/binary_frame_dispatcher_factory.py` | 17 | 0 | 100%|
| `scarajectory/infrastructure/formatter/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/formatter/command/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/formatter/command/config_command_formatter.py` | 22 | 0 | 100%|
| `scarajectory/infrastructure/formatter/command/jog_command_formatter.py` | 15 | 0 | 100%|
| `scarajectory/infrastructure/formatter/command/motion_command_formatter.py` | 38 | 0 | 100%|
| `scarajectory/infrastructure/formatter/command/query_command_formatter.py` | 21 | 0 | 100%|
| `scarajectory/infrastructure/formatter/command/system_command_formatter.py` | 29 | 0 | 100%|
| `scarajectory/infrastructure/formatter/command/tool_command_formatter.py` | 25 | 0 | 100%|
| `scarajectory/infrastructure/formatter/command_formatter.py` | 20 | 0 | 100%|
| `scarajectory/infrastructure/formatter/command_formatter_factory.py` | 17 | 1 | 94%|
| `scarajectory/infrastructure/formatter/command_templates.py` | 46 | 2 | 96%|
| `scarajectory/infrastructure/gui/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/bundle.py` | 24 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/canvas_event_binder.py` | 59 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/canvas_event_binder_factory.py` | 21 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/handler/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/handler/canvas_drag_handler.py` | 40 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/handler/canvas_event_context.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/handler/canvas_mouse_handler.py` | 73 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/handler/canvas_mouse_handler_factory.py` | 36 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/handler/canvas_shape_handler.py` | 55 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/handler/canvas_tool_handler.py` | 45 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/handler/icanvas_mouse_handler.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/handler/mouse_handler_bundle.py` | 24 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/handler/mouse_handler_init_bundle.py` | 22 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/handler/pan/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/handler/pan/canvas_viewport_pan_handler.py` | 41 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/handler/pan/canvas_viewport_pan_handler_factory.py` | 19 | 1 | 95%|
| `scarajectory/infrastructure/gui/canvas/handler/pan/icanvas_viewport_pan_handler.py` | 17 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/handler/selection/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/handler/selection/canvas_selection_mouse_handler.py` | 49 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/handler/selection/canvas_selection_mouse_handler_factory.py` | 22 | 1 | 95%|
| `scarajectory/infrastructure/gui/canvas/handler/selection/icanvas_selection_mouse_handler.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/icanvas.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/navigation/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/navigation/canvas_view_navigator.py` | 34 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/navigation/canvas_view_navigator_factory.py` | 20 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/navigation/icanvas_view_navigator.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/navigation/icanvas_view_target.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/observer/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/observer/canvas_plan_observer_bridge.py` | 20 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/observer/canvas_plan_observer_bridge_factory.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/observer/icanvas_plan_observer_bridge.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/render/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/render/forbidden_zone_renderer.py` | 56 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/render/ilayer_renderer.py` | 17 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/render/polar_grid_renderer.py` | 36 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/render/preview_renderer.py` | 31 | 1 | 97%|
| `scarajectory/infrastructure/gui/canvas/render/reach_boundary_renderer.py` | 31 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/render/renderer.py` | 34 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/render/trajectory_renderer.py` | 32 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/render/waypoint_node_renderer.py` | 25 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/render/waypoint_node_renderer_factory.py` | 17 | 1 | 94%|
| `scarajectory/infrastructure/gui/canvas/status/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/status/canvas_status_presenter.py` | 21 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/status/canvas_status_presenter_factory.py` | 17 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/status/icanvas_status_presenter.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/trajectory_canvas.py` | 68 | 4 | 94%|
| `scarajectory/infrastructure/gui/canvas/trajectory_canvas_factory.py` | 44 | 0 | 100%|
| `scarajectory/infrastructure/gui/connection/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/connection/iport_connection_delegate.py` | 13 | 0 | 100%|
| `scarajectory/infrastructure/gui/connection/null_port_connection_delegate.py` | 11 | 0 | 100%|
| `scarajectory/infrastructure/gui/connection/port_connection_panel.py` | 76 | 2 | 97%|
| `scarajectory/infrastructure/gui/console/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/console/serial_console.py` | 39 | 0 | 100%|
| `scarajectory/infrastructure/gui/console/serial_console_builder.py` | 30 | 1 | 97%|
| `scarajectory/infrastructure/gui/console/serial_console_builder_factory.py` | 17 | 1 | 94%|
| `scarajectory/infrastructure/gui/controls/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/controls/bundle.py` | 29 | 0 | 100%|
| `scarajectory/infrastructure/gui/controls/controls_panel.py` | 52 | 0 | 100%|
| `scarajectory/infrastructure/gui/controls/controls_panel_factory.py` | 29 | 0 | 100%|
| `scarajectory/infrastructure/gui/controls/icontrols_panel.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/gui/controls/itabs_assembler.py` | 17 | 0 | 100%|
| `scarajectory/infrastructure/gui/controls/manipulator_controllers_bundle.py` | 20 | 0 | 100%|
| `scarajectory/infrastructure/gui/controls/manipulator_controllers_factory.py` | 34 | 0 | 100%|
| `scarajectory/infrastructure/gui/controls/tabs_assembler.py` | 43 | 0 | 100%|
| `scarajectory/infrastructure/gui/controls/tabs_assembler_factory.py` | 17 | 0 | 100%|
| `scarajectory/infrastructure/gui/controls/tabs_bundle.py` | 22 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/bundle.py` | 20 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/code_editor.py` | 36 | 3 | 92%|
| `scarajectory/infrastructure/gui/dsl/code_editor_factory.py` | 24 | 1 | 96%|
| `scarajectory/infrastructure/gui/dsl/console_view.py` | 27 | 3 | 89%|
| `scarajectory/infrastructure/gui/dsl/document/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/document/document_manager.py` | 42 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/document/document_manager_factory.py` | 22 | 1 | 95%|
| `scarajectory/infrastructure/gui/dsl/document/example_catalog.py` | 35 | 4 | 89%|
| `scarajectory/infrastructure/gui/dsl/document/example_catalog_factory.py` | 23 | 1 | 96%|
| `scarajectory/infrastructure/gui/dsl/dsl_editor_tab.py` | 57 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/dsl_editor_tab_factory.py` | 52 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/handler/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/handler/execution_handler.py` | 61 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/handler/execution_handler_bundle.py` | 24 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/handler/execution_handler_factory.py` | 18 | 1 | 94%|
| `scarajectory/infrastructure/gui/dsl/handler/file_handler.py` | 47 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/handler/file_handler_bundle.py` | 22 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/handler/file_handler_factory.py` | 18 | 1 | 94%|
| `scarajectory/infrastructure/gui/dsl/handler/iexecution_delegate.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/handler/ifile_delegate.py` | 15 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/syntax/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/syntax/highlighter.py` | 29 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/syntax/highlighter_factory.py` | 24 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/syntax/ihighlighter.py` | 15 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/syntax/itag_applier.py` | 17 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/syntax/itokenizer.py` | 15 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/syntax/tag_applier.py` | 24 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/syntax/tag_applier_factory.py` | 17 | 1 | 94%|
| `scarajectory/infrastructure/gui/dsl/syntax/token.py` | 15 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/syntax/tokenizer.py` | 42 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/syntax/tokenizer_factory.py` | 17 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/toolbar.py` | 50 | 2 | 96%|
| `scarajectory/infrastructure/gui/editor/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/editor/table/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/editor/table/bundle.py` | 20 | 0 | 100%|
| `scarajectory/infrastructure/gui/editor/table/itable.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/gui/editor/table/selection_handler.py` | 28 | 3 | 89%|
| `scarajectory/infrastructure/gui/editor/table/selection_handler_factory.py` | 17 | 1 | 94%|
| `scarajectory/infrastructure/gui/editor/table/trajectory_table.py` | 87 | 2 | 98%|
| `scarajectory/infrastructure/gui/editor/waypoint_coordinate_inputs.py` | 17 | 0 | 100%|
| `scarajectory/infrastructure/gui/editor/waypoint_edit_applier.py` | 30 | 1 | 97%|
| `scarajectory/infrastructure/gui/editor/waypoint_edit_applier_factory.py` | 17 | 0 | 100%|
| `scarajectory/infrastructure/gui/editor/waypoint_editor.py` | 68 | 0 | 100%|
| `scarajectory/infrastructure/gui/emulator/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/emulator/emulator_launcher.py` | 40 | 0 | 100%|
| `scarajectory/infrastructure/gui/emulator/emulator_launcher_factory.py` | 17 | 0 | 100%|
| `scarajectory/infrastructure/gui/emulator/iemulator_launcher.py` | 13 | 0 | 100%|
| `scarajectory/infrastructure/gui/igui.py` | 17 | 0 | 100%|
| `scarajectory/infrastructure/gui/layout/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/layout/canvas_pane_builder.py` | 30 | 0 | 100%|
| `scarajectory/infrastructure/gui/layout/canvas_pane_builder_factory.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/gui/layout/editor_pane_builder.py` | 38 | 0 | 100%|
| `scarajectory/infrastructure/gui/layout/editor_pane_builder_factory.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/gui/layout/icanvas_pane_builder.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/gui/layout/ieditor_pane_builder.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/gui/layout/itoolbar_layout_builder.py` | 19 | 0 | 100%|
| `scarajectory/infrastructure/gui/layout/main_content_builder.py` | 39 | 0 | 100%|
| `scarajectory/infrastructure/gui/layout/main_content_builder_factory.py` | 26 | 0 | 100%|
| `scarajectory/infrastructure/gui/layout/toolbar_layout_builder.py` | 33 | 0 | 100%|
| `scarajectory/infrastructure/gui/layout/toolbar_layout_builder_factory.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/gui/manipulator/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/manipulator/imanipulator_action_delegate.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/gui/manipulator/jog/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/manipulator/jog/axis_grid_panel.py` | 46 | 0 | 100%|
| `scarajectory/infrastructure/gui/manipulator/jog/axis_grid_panel_factory.py` | 20 | 0 | 100%|
| `scarajectory/infrastructure/gui/manipulator/jog/controllers_bundle.py` | 22 | 0 | 100%|
| `scarajectory/infrastructure/gui/manipulator/jog/jog_tab.py` | 51 | 0 | 100%|
| `scarajectory/infrastructure/gui/manipulator/jog/jog_tab_factory.py` | 35 | 0 | 100%|
| `scarajectory/infrastructure/gui/manipulator/jog/panel_bundle.py` | 20 | 0 | 100%|
| `scarajectory/infrastructure/gui/manipulator/jog/power_panel.py` | 27 | 0 | 100%|
| `scarajectory/infrastructure/gui/manipulator/jog/power_panel_factory.py` | 19 | 0 | 100%|
| `scarajectory/infrastructure/gui/manipulator/jog/raw_command_panel.py` | 36 | 0 | 100%|
| `scarajectory/infrastructure/gui/manipulator/jog/raw_command_panel_factory.py` | 19 | 0 | 100%|
| `scarajectory/infrastructure/gui/manipulator/jog/tool_panel.py` | 26 | 0 | 100%|
| `scarajectory/infrastructure/gui/manipulator/jog/tool_panel_factory.py` | 19 | 0 | 100%|
| `scarajectory/infrastructure/gui/manipulator/manipulator_override_panel.py` | 60 | 0 | 100%|
| `scarajectory/infrastructure/gui/manipulator/null_manipulator_action_delegate.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/gui/menu/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/menu/app_menu_bar.py` | 77 | 0 | 100%|
| `scarajectory/infrastructure/gui/menu/app_menu_bar_factory.py` | 26 | 1 | 96%|
| `scarajectory/infrastructure/gui/menu/builders_bundle.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/gui/menu/bundle.py` | 26 | 0 | 100%|
| `scarajectory/infrastructure/gui/menu/iapp_menu_bar.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/gui/menu/menu_hotkey_binder.py` | 23 | 0 | 100%|
| `scarajectory/infrastructure/gui/menu/menu_hotkey_binder_factory.py` | 17 | 1 | 94%|
| `scarajectory/infrastructure/gui/menu/menu_layout_builder.py` | 40 | 0 | 100%|
| `scarajectory/infrastructure/gui/menu/menu_layout_builder_factory.py` | 17 | 1 | 94%|
| `scarajectory/infrastructure/gui/model/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/model/canvas_interaction_state.py` | 26 | 0 | 100%|
| `scarajectory/infrastructure/gui/model/canvas_settings.py` | 15 | 0 | 100%|
| `scarajectory/infrastructure/gui/model/canvas_tool_mode.py` | 17 | 0 | 100%|
| `scarajectory/infrastructure/gui/model/viewport_transform.py` | 47 | 0 | 100%|
| `scarajectory/infrastructure/gui/preview/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/preview/preview_tab.py` | 33 | 0 | 100%|
| `scarajectory/infrastructure/gui/preview/preview_tab_factory.py` | 21 | 0 | 100%|
| `scarajectory/infrastructure/gui/scarajectory_gui.py` | 65 | 2 | 97%|
| `scarajectory/infrastructure/gui/scarajectory_gui_bundle.py` | 27 | 0 | 100%|
| `scarajectory/infrastructure/gui/scarajectory_gui_factory.py` | 57 | 0 | 100%|
| `scarajectory/infrastructure/gui/scarajectory_gui_init_bundle.py` | 28 | 0 | 100%|
| `scarajectory/infrastructure/gui/streaming/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/streaming/bundle.py` | 24 | 0 | 100%|
| `scarajectory/infrastructure/gui/streaming/handler/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/streaming/handler/playback_handler_bundle.py` | 24 | 0 | 100%|
| `scarajectory/infrastructure/gui/streaming/handler/stream_playback_action_handler.py` | 61 | 0 | 100%|
| `scarajectory/infrastructure/gui/streaming/handler/stream_playback_action_handler_factory.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/gui/streaming/handler/stream_tool_action_handler.py` | 52 | 0 | 100%|
| `scarajectory/infrastructure/gui/streaming/handler/stream_tool_action_handler_factory.py` | 20 | 0 | 100%|
| `scarajectory/infrastructure/gui/streaming/observer/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/streaming/observer/gui_stream_observer_bridge.py` | 23 | 0 | 100%|
| `scarajectory/infrastructure/gui/streaming/observer/gui_stream_observer_bridge_factory.py` | 19 | 0 | 100%|
| `scarajectory/infrastructure/gui/streaming/observer/igui_stream_observer_bridge.py` | 15 | 0 | 100%|
| `scarajectory/infrastructure/gui/streaming/panel/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/streaming/panel/istream_control_delegate.py` | 15 | 0 | 100%|
| `scarajectory/infrastructure/gui/streaming/panel/stream_control_panel.py` | 21 | 0 | 100%|
| `scarajectory/infrastructure/gui/streaming/panel/stream_progress_adapter.py` | 35 | 0 | 100%|
| `scarajectory/infrastructure/gui/streaming/panel/stream_status_bar.py` | 30 | 0 | 100%|
| `scarajectory/infrastructure/gui/streaming/streamer_action_bundle.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/gui/streaming/streamer_controllers_bundle.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/gui/streaming/streamer_tab.py` | 70 | 0 | 100%|
| `scarajectory/infrastructure/gui/streaming/streamer_tab_factory.py` | 31 | 0 | 100%|
| `scarajectory/infrastructure/gui/theme/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/theme/theme_button_styler.py` | 23 | 0 | 100%|
| `scarajectory/infrastructure/gui/theme/theme_button_styler_factory.py` | 17 | 1 | 94%|
| `scarajectory/infrastructure/gui/theme/theme_manager.py` | 43 | 0 | 100%|
| `scarajectory/infrastructure/gui/theme/theme_notebook_styler.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/gui/theme/theme_notebook_styler_factory.py` | 17 | 1 | 94%|
| `scarajectory/infrastructure/gui/toolbar/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/toolbar/bundle.py` | 24 | 0 | 100%|
| `scarajectory/infrastructure/gui/toolbar/itoolbar.py` | 15 | 0 | 100%|
| `scarajectory/infrastructure/gui/toolbar/navigation_controls.py` | 32 | 0 | 100%|
| `scarajectory/infrastructure/gui/toolbar/navigation_controls_factory.py` | 20 | 0 | 100%|
| `scarajectory/infrastructure/gui/toolbar/parameter_inputs.py` | 56 | 1 | 98%|
| `scarajectory/infrastructure/gui/toolbar/parameter_inputs_bundle.py` | 20 | 0 | 100%|
| `scarajectory/infrastructure/gui/toolbar/parameter_inputs_factory.py` | 19 | 0 | 100%|
| `scarajectory/infrastructure/gui/toolbar/tool_selector.py` | 33 | 0 | 100%|
| `scarajectory/infrastructure/gui/toolbar/tool_selector_factory.py` | 19 | 0 | 100%|
| `scarajectory/infrastructure/gui/toolbar/toolbar.py` | 33 | 0 | 100%|
| `scarajectory/infrastructure/gui/toolbar/toolbar_factory.py` | 29 | 0 | 100%|
| `scarajectory/infrastructure/gui/validation/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/validation/validation_tab.py` | 35 | 0 | 100%|
| `scarajectory/infrastructure/gui/validation/validation_tab_factory.py` | 20 | 0 | 100%|
| `scarajectory/infrastructure/manipulator/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/manipulator/jog_controller.py` | 41 | 1 | 98%|
| `scarajectory/infrastructure/manipulator/jog_controller_factory.py` | 23 | 1 | 96%|
| `scarajectory/infrastructure/manipulator/motion_controller.py` | 46 | 0 | 100%|
| `scarajectory/infrastructure/manipulator/motion_controller_factory.py` | 23 | 1 | 96%|
| `scarajectory/infrastructure/manipulator/query_controller.py` | 36 | 1 | 97%|
| `scarajectory/infrastructure/manipulator/query_controller_factory.py` | 23 | 1 | 96%|
| `scarajectory/infrastructure/pacing/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/pacing/bundle.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/pacing/flow_barrier_coordinator.py` | 23 | 0 | 100%|
| `scarajectory/infrastructure/pacing/flow_barrier_coordinator_factory.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/pacing/flow_pacing_bundle_factory.py` | 26 | 0 | 100%|
| `scarajectory/infrastructure/pacing/flow_pacing_controller.py` | 77 | 0 | 100%|
| `scarajectory/infrastructure/pacing/flow_pacing_controller_factory.py` | 30 | 0 | 100%|
| `scarajectory/infrastructure/packet/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/packet/binary_packet_strategy.py` | 45 | 0 | 100%|
| `scarajectory/infrastructure/packet/binary_packet_strategy_factory.py` | 28 | 0 | 100%|
| `scarajectory/infrastructure/preferences/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/preferences/connection_repository.py` | 57 | 0 | 100%|
| `scarajectory/infrastructure/preferences/connection_repository_factory.py` | 22 | 0 | 100%|
| `scarajectory/infrastructure/settings/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/settings/bounds/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/settings/bounds/scara_bounds_loader.py` | 35 | 1 | 97%|
| `scarajectory/infrastructure/settings/bounds/scara_bounds_loader_factory.py` | 29 | 0 | 100%|
| `scarajectory/infrastructure/settings/bounds/scara_bounds_parser.py` | 19 | 0 | 100%|
| `scarajectory/infrastructure/settings/bounds/scara_bounds_parser_factory.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/settings/isettings_reader.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/settings/settings_reader.py` | 46 | 1 | 98%|
| `scarajectory/infrastructure/settings/settings_reader_factory.py` | 25 | 0 | 100%|
| `scarajectory/infrastructure/settings/stream/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/settings/stream/stream_config_loader.py` | 27 | 0 | 100%|
| `scarajectory/infrastructure/settings/stream/stream_config_loader_factory.py` | 22 | 0 | 100%|
| `scarajectory/infrastructure/settings/transmission/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/settings/transmission/scara_transmission_loader.py` | 21 | 0 | 100%|
| `scarajectory/infrastructure/settings/transmission/scara_transmission_loader_factory.py` | 22 | 0 | 100%|
| `scarajectory/infrastructure/state/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/state/stream_state_machine.py` | 28 | 0 | 100%|
| `scarajectory/infrastructure/state/stream_state_machine_factory.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/storage/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/storage/plan_loader.py` | 37 | 0 | 100%|
| `scarajectory/infrastructure/storage/plan_storage_service.py` | 33 | 0 | 100%|
| `scarajectory/infrastructure/storage/plan_storage_service_factory.py` | 26 | 0 | 100%|
| `scarajectory/infrastructure/storage/plan_storer.py` | 40 | 0 | 100%|
| `scarajectory/infrastructure/storage/trajectory_serializer.py` | 39 | 0 | 100%|
| `scarajectory/infrastructure/streaming/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/streaming/assembly/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/streaming/assembly/stream_pacing_assembler.py` | 21 | 0 | 100%|
| `scarajectory/infrastructure/streaming/assembly/stream_pipeline_assembler.py` | 52 | 1 | 98%|
| `scarajectory/infrastructure/streaming/assembly/stream_transport_assembler.py` | 24 | 0 | 100%|
| `scarajectory/infrastructure/streaming/assembly/stream_worker_assembler.py` | 57 | 0 | 100%|
| `scarajectory/infrastructure/streaming/assembly/worker_bundle.py` | 20 | 0 | 100%|
| `scarajectory/infrastructure/streaming/binary_program_streamer.py` | 50 | 0 | 100%|
| `scarajectory/infrastructure/streaming/binary_program_streamer_factory.py` | 21 | 0 | 100%|
| `scarajectory/infrastructure/streaming/bundle.py` | 22 | 0 | 100%|
| `scarajectory/infrastructure/streaming/observer/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/streaming/observer/istream_observer_registry.py` | 17 | 0 | 100%|
| `scarajectory/infrastructure/streaming/observer/istream_telemetry_notifier.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/streaming/observer/stream_observer_dispatcher.py` | 35 | 0 | 100%|
| `scarajectory/infrastructure/streaming/observer/stream_observer_dispatcher_factory.py` | 29 | 0 | 100%|
| `scarajectory/infrastructure/streaming/observer/stream_observer_registry.py` | 24 | 0 | 100%|
| `scarajectory/infrastructure/streaming/observer/stream_observer_registry_factory.py` | 23 | 0 | 100%|
| `scarajectory/infrastructure/streaming/observer/stream_telemetry_notifier.py` | 33 | 0 | 100%|
| `scarajectory/infrastructure/streaming/observer/stream_telemetry_notifier_factory.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/streaming/stream_control_transmitter.py` | 42 | 0 | 100%|
| `scarajectory/infrastructure/streaming/stream_control_transmitter_factory.py` | 19 | 0 | 100%|
| `scarajectory/infrastructure/streaming/stream_playback_controller.py` | 78 | 0 | 100%|
| `scarajectory/infrastructure/streaming/stream_playback_controller_factory.py` | 25 | 0 | 100%|
| `scarajectory/infrastructure/tool/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/tool/tool_controller.py` | 50 | 0 | 100%|
| `scarajectory/infrastructure/tool/tool_controller_factory.py` | 24 | 0 | 100%|
| `scarajectory/infrastructure/tool/valve_pulse_worker.py` | 23 | 0 | 100%|
| `scarajectory/infrastructure/tool/valve_pulse_worker_factory.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/transmission/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/transmission/transmission_step_calculator.py` | 24 | 0 | 100%|
| `scarajectory/infrastructure/transmission/transmission_step_calculator_factory.py` | 18 | 1 | 94%|
| `scarajectory/infrastructure/transport/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/transport/bundle.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/transport/driver/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/transport/driver/ichannel.py` | 19 | 0 | 100%|
| `scarajectory/infrastructure/transport/driver/serial_channel.py` | 37 | 0 | 100%|
| `scarajectory/infrastructure/transport/driver/serial_channel_factory.py` | 17 | 0 | 100%|
| `scarajectory/infrastructure/transport/driver/serial_port_scanner.py` | 36 | 0 | 100%|
| `scarajectory/infrastructure/transport/driver/tcp_channel.py` | 66 | 0 | 100%|
| `scarajectory/infrastructure/transport/driver/tcp_channel_factory.py` | 17 | 0 | 100%|
| `scarajectory/infrastructure/transport/istream_transport_connection.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/transport/istream_transport_transceiver.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/transport/listener/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/transport/listener/itransport_listener.py` | 15 | 0 | 100%|
| `scarajectory/infrastructure/transport/listener/itransport_listener_holder.py` | 17 | 0 | 100%|
| `scarajectory/infrastructure/transport/listener/null_transport_listener.py` | 13 | 0 | 100%|
| `scarajectory/infrastructure/transport/listener/stream_ascii_transport_listener.py` | 23 | 0 | 100%|
| `scarajectory/infrastructure/transport/listener/stream_ascii_transport_listener_factory.py` | 19 | 0 | 100%|
| `scarajectory/infrastructure/transport/listener/stream_binary_transport_listener.py` | 23 | 0 | 100%|
| `scarajectory/infrastructure/transport/listener/stream_binary_transport_listener_factory.py` | 19 | 0 | 100%|
| `scarajectory/infrastructure/transport/listener/transport_listener_holder.py` | 22 | 0 | 100%|
| `scarajectory/infrastructure/transport/stream_transport_connection.py` | 61 | 1 | 98%|
| `scarajectory/infrastructure/transport/stream_transport_connection_factory.py` | 20 | 0 | 100%|
| `scarajectory/infrastructure/transport/stream_transport_transceiver.py` | 54 | 0 | 100%|
| `scarajectory/infrastructure/transport/stream_transport_transceiver_factory.py` | 20 | 0 | 100%|
| `scarajectory/infrastructure/transport/transport_factory.py` | 35 | 1 | 97%|
| `scarajectory/infrastructure/transport/worker/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/transport/worker/itransport_reader_worker.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/transport/worker/transport_reader_worker.py` | 54 | 0 | 100%|
| `scarajectory/infrastructure/transport/worker/transport_reader_worker_factory.py` | 20 | 0 | 100%|
| `scarajectory/infrastructure/worker/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/worker/binary/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/worker/binary/binary_stream_execution_worker.py` | 60 | 0 | 100%|
| `scarajectory/infrastructure/worker/binary/binary_stream_execution_worker_factory.py` | 31 | 0 | 100%|
| `scarajectory/infrastructure/worker/binary/binary_stream_frame_handler.py` | 55 | 0 | 100%|
| `scarajectory/infrastructure/worker/binary/binary_stream_frame_handler_factory.py` | 20 | 0 | 100%|
| `scarajectory/infrastructure/worker/binary/binary_stream_loop_runner.py` | 98 | 2 | 98%|
| `scarajectory/infrastructure/worker/binary/binary_stream_loop_runner_factory.py` | 32 | 0 | 100%|
| `scarajectory/infrastructure/worker/binary/ibinary_stream_frame_handler.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/worker/binary/ibinary_stream_loop_runner.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/worker/istream_queue_drainer.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/worker/istream_step_dispatcher.py` | 15 | 0 | 100%|
| `scarajectory/infrastructure/worker/stream_execution_worker.py` | 52 | 0 | 100%|
| `scarajectory/infrastructure/worker/stream_execution_worker_factory.py` | 30 | 3 | 90%|
| `scarajectory/infrastructure/worker/stream_loop_runner.py` | 57 | 3 | 95%|
| `scarajectory/infrastructure/worker/stream_loop_runner_factory.py` | 38 | 1 | 97%|
| `scarajectory/infrastructure/worker/stream_queue_drainer.py` | 40 | 1 | 98%|
| `scarajectory/infrastructure/worker/stream_queue_drainer_factory.py` | 20 | 1 | 95%|
| `scarajectory/infrastructure/worker/stream_step_dispatcher.py` | 49 | 0 | 100%|
| `scarajectory/infrastructure/worker/stream_step_dispatcher_factory.py` | 22 | 1 | 95%|
| `scarajectory/setup/__init__.py` | 9 | 0 | 100%|
| `scarajectory/setup/assembly/__init__.py` | 9 | 0 | 100%|
| `scarajectory/setup/assembly/app_core_assembler.py` | 33 | 0 | 100%|
| `scarajectory/setup/assembly/app_core_bundle.py` | 20 | 0 | 100%|
| `scarajectory/setup/assembly/app_presentation_assembler.py` | 40 | 0 | 100%|
| `scarajectory/setup/assembly/app_runtime_assembler.py` | 33 | 0 | 100%|
| `scarajectory/setup/assembly/app_runtime_bundle.py` | 24 | 0 | 100%|
| `scarajectory/setup/bundle.py` | 25 | 1 | 96%|
| `scarajectory/setup/dep_validator.py` | 36 | 5 | 86%|
| `scarajectory/setup/dependencies.py` | 21 | 0 | 100%|
| `scarajectory/setup/factory.py` | 72 | 4 | 94%|
| `scarajectory/setup/keys.py` | 37 | 0 | 100%|
| `scarajectory/setup/opt_validator.py` | 36 | 5 | 86%|
| `scarajectory/setup/options.py` | 20 | 0 | 100%|
| `scarajectory/setup/pipeline/__init__.py` | 9 | 0 | 100%|
| `scarajectory/setup/pipeline/dsl_pipeline_builder.py` | 29 | 0 | 100%|
| `scarajectory/setup/pipeline/plan_pipeline_builder.py` | 35 | 0 | 100%|
| `scarajectory/setup/pipeline/plan_pipeline_bundle.py` | 22 | 0 | 100%|
| `scarajectory/setup/pipeline/stream_pipeline_builder.py` | 58 | 0 | 100%|
| `scarajectory/setup/pipeline/stream_pipeline_bundle.py` | 22 | 0 | 100%|
| `scarajectory/setup/registry.py` | 34 | 1 | 97%|
| `scarajectory/setup/validator.py` | 53 | 5 | 91%|
| **Total** | 13316 | 120 | 99% |

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

<p align="center">
  <img src="https://raw.githubusercontent.com/vroncevic/scarajectory/dev/docs/scarajectory_in_progress.png" alt="SCARA Trajectory Studio in Progress" width="95%">
</p>

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
