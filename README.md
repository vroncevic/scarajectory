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
    - [🌐 SCARA Ecosystem & Dual-Mode Motor Actuation](#-scara-ecosystem--dual-mode-motor-actuation)
  - [✨ Features](#-features)
  - [📐 SCARA Kinematic & Geometric Configuration](#-scara-kinematic--geometric-configuration)
    - [🔄 Singularity Dead Zone Avoidance & Dual-Elbow Routing](#-singularity-dead-zone-avoidance--dual-elbow-routing)
  - [📜 SCARA Domain-Specific Language (DSL) & `.scara` Programs](#-scara-domain-specific-language-dsl--scara-programs)
    - [SCARA DSL Instruction Reference](#scara-dsl-instruction-reference)
    - [Example `.scara` Program: Industrial Pick & Place](#example-scara-program-industrial-pick--place)
    - [Bundled Industrial `.scara` Demonstration Programs](#bundled-industrial-scara-demonstration-programs)
    - [User Workspace Auto-Provisioning (`~/.scarajectory/workspace/`)](#user-workspace-auto-provisioning-scarajectoryworkspace)
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
* [scaracom - SCARA Robot Communication Library](https://github.com/vroncevic/scaracom) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
* [scaralang - SCARA Domain-Specific Language, Kinematics & Protocol Engine](https://github.com/vroncevic/scaralang) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

> **Hardware Communication & Transport Dependency ([scaracom](https://github.com/vroncevic/scaracom)):** `scarajectory` integrates `scaracom` as its foundational hardware communication dependency. `scaracom` provides low-level serial transport, hardware transceiver abstraction, connection lifecycle management, and flow control synchronization.

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
         │   │   │   ├── axis.py
         │   │   │   ├── command.py
         │   │   │   ├── direction.py
         │   │   │   └── __init__.py
         │   │   ├── streaming/
         │   │   │   ├── config.py
         │   │   │   ├── __init__.py
         │   │   │   ├── pacing_config.py
         │   │   │   ├── session.py
         │   │   │   └── state.py
         │   │   ├── telemetry/
         │   │   │   ├── counts.py
         │   │   │   ├── diagnostics/
         │   │   │   │   ├── bundle.py
         │   │   │   │   ├── comm.py
         │   │   │   │   ├── driver.py
         │   │   │   │   ├── errors.py
         │   │   │   │   ├── __init__.py
         │   │   │   │   └── steps.py
         │   │   │   ├── fault.py
         │   │   │   ├── __init__.py
         │   │   │   ├── move.py
         │   │   │   ├── progress.py
         │   │   │   ├── status.py
         │   │   │   └── summary.py
         │   │   └── trajectory/
         │   │       ├── __init__.py
         │   │       └── waypoint.py
         │   └── service/
         │       ├── __init__.py
         │       ├── manipulator/
         │       │   ├── ijog.py
         │       │   ├── imotion.py
         │       │   ├── __init__.py
         │       │   └── iquery.py
         │       ├── storage/
         │       │   ├── iloader.py
         │       │   ├── __init__.py
         │       │   └── istorer.py
         │       ├── streaming/
         │       │   ├── config_factory.py
         │       │   ├── control/
         │       │   │   ├── __init__.py
         │       │   │   └── itransmitter.py
         │       │   ├── __init__.py
         │       │   ├── observer/
         │       │   │   ├── idispatcher.py
         │       │   │   ├── __init__.py
         │       │   │   ├── iobserver.py
         │       │   │   └── iregistry.py
         │       │   ├── pacing_config_factory.py
         │       │   ├── playback/
         │       │   │   ├── icontroller.py
         │       │   │   └── __init__.py
         │       │   └── session_factory.py
         │       ├── telemetry/
         │       │   ├── diagnostics/
         │       │   │   ├── bundle_factory.py
         │       │   │   ├── driver_factory.py
         │       │   │   ├── errors_factory.py
         │       │   │   ├── __init__.py
         │       │   │   └── steps_factory.py
         │       │   ├── fault_factory.py
         │       │   ├── __init__.py
         │       │   └── move_factory.py
         │       ├── tool/
         │       │   ├── iactuator.py
         │       │   ├── icontroller.py
         │       │   └── __init__.py
         │       └── trajectory/
         │           ├── history/
         │           │   ├── dependencies.py
         │           │   ├── factory.py
         │           │   ├── __init__.py
         │           │   ├── navigator/
         │           │   │   ├── dependencies.py
         │           │   │   ├── factory.py
         │           │   │   ├── inavigator.py
         │           │   │   ├── __init__.py
         │           │   │   └── navigator.py
         │           │   ├── provides.py
         │           │   ├── saver/
         │           │   │   ├── dependencies.py
         │           │   │   ├── factory.py
         │           │   │   ├── __init__.py
         │           │   │   ├── isaver.py
         │           │   │   └── saver.py
         │           │   └── stack/
         │           │       ├── factory.py
         │           │       ├── __init__.py
         │           │       ├── istack.py
         │           │       └── stack.py
         │           ├── __init__.py
         │           ├── plan/
         │           │   ├── history/
         │           │   │   ├── dependencies.py
         │           │   │   ├── factory.py
         │           │   │   ├── history.py
         │           │   │   ├── ihistory.py
         │           │   │   ├── __init__.py
         │           │   │   └── provides.py
         │           │   ├── __init__.py
         │           │   ├── mutation/
         │           │   │   ├── bulk_mutation/
         │           │   │   │   ├── bulk_mutation.py
         │           │   │   │   ├── ibulk_mutation.py
         │           │   │   │   └── __init__.py
         │           │   │   ├── dependencies.py
         │           │   │   ├── factory.py
         │           │   │   ├── __init__.py
         │           │   │   ├── point_mutation/
         │           │   │   │   ├── __init__.py
         │           │   │   │   ├── ipoint_mutation.py
         │           │   │   │   └── point_mutation.py
         │           │   │   └── provides.py
         │           │   ├── observer/
         │           │   │   ├── dispatcher.py
         │           │   │   ├── factory.py
         │           │   │   ├── idispatcher.py
         │           │   │   ├── __init__.py
         │           │   │   ├── itrajectory_observer.py
         │           │   │   └── provides.py
         │           │   ├── selection/
         │           │   │   ├── coordinator/
         │           │   │   │   ├── coordinator.py
         │           │   │   │   ├── dependencies.py
         │           │   │   │   ├── factory.py
         │           │   │   │   ├── icoordinator.py
         │           │   │   │   └── __init__.py
         │           │   │   ├── dependencies.py
         │           │   │   ├── factory.py
         │           │   │   ├── __init__.py
         │           │   │   ├── navigator/
         │           │   │   │   ├── factory.py
         │           │   │   │   ├── inavigator.py
         │           │   │   │   ├── __init__.py
         │           │   │   │   └── navigator.py
         │           │   │   ├── provides.py
         │           │   │   └── state/
         │           │   │       ├── factory.py
         │           │   │       ├── __init__.py
         │           │   │       ├── istate.py
         │           │   │       └── state.py
         │           │   └── store/
         │           │       ├── bulk_mutator/
         │           │       │   ├── bulk_mutator.py
         │           │       │   ├── ibulk_mutator.py
         │           │       │   └── __init__.py
         │           │       ├── dependencies.py
         │           │       ├── factory.py
         │           │       ├── __init__.py
         │           │       ├── istore.py
         │           │       ├── mutator/
         │           │       │   ├── imutator.py
         │           │       │   ├── __init__.py
         │           │       │   └── mutator.py
         │           │       ├── provides.py
         │           │       ├── query/
         │           │       │   ├── __init__.py
         │           │       │   ├── iquery.py
         │           │       │   └── query.py
         │           │       └── store.py
         │           └── validation/
         │               ├── __init__.py
         │               └── ivalidator.py
         ├── engine.py
         ├── infrastructure/
         │   ├── barrier/
         │   │   ├── factory.py
         │   │   ├── __init__.py
         │   │   └── provides.py
         │   ├── cli/
         │   │   ├── dependencies.py
         │   │   ├── engine.py
         │   │   ├── factory.py
         │   │   ├── icli.py
         │   │   ├── __init__.py
         │   │   ├── provides.py
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
         │   │   ├── bundle.py
         │   │   ├── dependencies.py
         │   │   ├── factory.py
         │   │   ├── idefinition.py
         │   │   ├── iexecutor.py
         │   │   ├── __init__.py
         │   │   ├── provides.py
         │   │   └── studio/
         │   │       ├── definition.py
         │   │       ├── dependencies.py
         │   │       ├── executor.py
         │   │       ├── factory.py
         │   │       ├── __init__.py
         │   │       └── provides.py
         │   ├── config/
         │   │   ├── communication.json
         │   │   ├── communication_scheme.json
         │   │   ├── examples.tgz
         │   │   ├── scara_geometry.json
         │   │   ├── scara_geometry_scheme.json
         │   │   ├── scaraemu.json
         │   │   ├── scaraemu_scheme.json
         │   │   ├── scarajectory.cfg
         │   │   └── scarajectory.logo
         │   ├── connection/
         │   │   ├── dependencies.py
         │   │   ├── dispatcher/
         │   │   │   ├── dependencies.py
         │   │   │   ├── dispatcher.py
         │   │   │   ├── factory.py
         │   │   │   ├── idispatcher.py
         │   │   │   ├── __init__.py
         │   │   │   └── provides.py
         │   │   ├── factory.py
         │   │   ├── __init__.py
         │   │   ├── listener/
         │   │   │   ├── factory.py
         │   │   │   ├── __init__.py
         │   │   │   └── listener.py
         │   │   ├── manager/
         │   │   │   ├── dependencies.py
         │   │   │   ├── factory.py
         │   │   │   ├── imanager.py
         │   │   │   ├── __init__.py
         │   │   │   ├── manager.py
         │   │   │   └── provides.py
         │   │   ├── provides.py
         │   │   ├── receiver/
         │   │   │   ├── bootstrap.py
         │   │   │   ├── ibytes_receiver.py
         │   │   │   └── __init__.py
         │   │   └── router/
         │   │       ├── factory.py
         │   │       ├── __init__.py
         │   │       └── provides.py
         │   ├── gui/
         │   │   ├── bundle.py
         │   │   ├── canvas/
         │   │   │   ├── adapter_bundle.py
         │   │   │   ├── bundle.py
         │   │   │   ├── event/
         │   │   │   │   ├── binder.py
         │   │   │   │   ├── dependencies.py
         │   │   │   │   ├── factory.py
         │   │   │   │   ├── ibinder.py
         │   │   │   │   └── __init__.py
         │   │   │   ├── handler/
         │   │   │   │   ├── coordinator/
         │   │   │   │   │   ├── bundle.py
         │   │   │   │   │   ├── coordinator.py
         │   │   │   │   │   ├── factory.py
         │   │   │   │   │   ├── icoordinator.py
         │   │   │   │   │   └── __init__.py
         │   │   │   │   ├── drag/
         │   │   │   │   │   ├── bundle.py
         │   │   │   │   │   ├── factory.py
         │   │   │   │   │   ├── handler.py
         │   │   │   │   │   ├── ihandler.py
         │   │   │   │   │   └── __init__.py
         │   │   │   │   ├── __init__.py
         │   │   │   │   ├── mouse/
         │   │   │   │   │   ├── bundle.py
         │   │   │   │   │   ├── context.py
         │   │   │   │   │   ├── factory.py
         │   │   │   │   │   ├── handler.py
         │   │   │   │   │   ├── ihandler.py
         │   │   │   │   │   ├── __init__.py
         │   │   │   │   │   └── init_bundle.py
         │   │   │   │   ├── pan/
         │   │   │   │   │   ├── factory.py
         │   │   │   │   │   ├── handler.py
         │   │   │   │   │   ├── ihandler.py
         │   │   │   │   │   └── __init__.py
         │   │   │   │   ├── selection/
         │   │   │   │   │   ├── bundle.py
         │   │   │   │   │   ├── factory.py
         │   │   │   │   │   ├── handler.py
         │   │   │   │   │   ├── ihandler.py
         │   │   │   │   │   └── __init__.py
         │   │   │   │   ├── shape/
         │   │   │   │   │   ├── factory.py
         │   │   │   │   │   ├── handler.py
         │   │   │   │   │   ├── ibuilder.py
         │   │   │   │   │   ├── ihandler.py
         │   │   │   │   │   └── __init__.py
         │   │   │   │   └── state.py
         │   │   │   ├── icanvas.py
         │   │   │   ├── __init__.py
         │   │   │   ├── navigation/
         │   │   │   │   ├── dependencies.py
         │   │   │   │   ├── factory.py
         │   │   │   │   ├── inavigator.py
         │   │   │   │   ├── __init__.py
         │   │   │   │   ├── itarget.py
         │   │   │   │   └── navigator.py
         │   │   │   ├── observer/
         │   │   │   │   ├── bridge.py
         │   │   │   │   ├── factory.py
         │   │   │   │   ├── __init__.py
         │   │   │   │   └── iredraw_delegate.py
         │   │   │   ├── renderer/
         │   │   │   │   ├── boundary/
         │   │   │   │   │   ├── __init__.py
         │   │   │   │   │   ├── reach.py
         │   │   │   │   │   ├── zone.py
         │   │   │   │   │   └── zone_factory.py
         │   │   │   │   ├── grid/
         │   │   │   │   │   ├── __init__.py
         │   │   │   │   │   └── renderer.py
         │   │   │   │   ├── __init__.py
         │   │   │   │   ├── layer/
         │   │   │   │   │   ├── ilayer.py
         │   │   │   │   │   └── __init__.py
         │   │   │   │   ├── preview/
         │   │   │   │   │   ├── __init__.py
         │   │   │   │   │   └── renderer.py
         │   │   │   │   ├── renderer.py
         │   │   │   │   └── trajectory/
         │   │   │   │       ├── bundle.py
         │   │   │   │       ├── __init__.py
         │   │   │   │       ├── node.py
         │   │   │   │       ├── node_factory.py
         │   │   │   │       └── renderer.py
         │   │   │   ├── settings/
         │   │   │   │   ├── __init__.py
         │   │   │   │   ├── ipresenter.py
         │   │   │   │   └── presenter.py
         │   │   │   ├── status/
         │   │   │   │   ├── factory.py
         │   │   │   │   ├── __init__.py
         │   │   │   │   ├── ipresenter.py
         │   │   │   │   └── presenter.py
         │   │   │   ├── tool/
         │   │   │   │   ├── coordinator.py
         │   │   │   │   ├── icoordinator.py
         │   │   │   │   └── __init__.py
         │   │   │   ├── trajectory_canvas.py
         │   │   │   ├── trajectory_canvas_factory.py
         │   │   │   └── transform/
         │   │   │       ├── camera.py
         │   │   │       ├── icamera.py
         │   │   │       ├── __init__.py
         │   │   │       ├── iprojector.py
         │   │   │       ├── projector.py
         │   │   │       └── transform.py
         │   │   ├── connection/
         │   │   │   ├── action/
         │   │   │   │   ├── action.py
         │   │   │   │   ├── iaction.py
         │   │   │   │   ├── idelegate.py
         │   │   │   │   └── __init__.py
         │   │   │   ├── __init__.py
         │   │   │   ├── panel/
         │   │   │   │   ├── __init__.py
         │   │   │   │   ├── ipanel.py
         │   │   │   │   └── panel.py
         │   │   │   └── selector/
         │   │   │       ├── __init__.py
         │   │   │       ├── iselector.py
         │   │   │       └── selector.py
         │   │   ├── console/
         │   │   │   ├── __init__.py
         │   │   │   └── panel.py
         │   │   ├── controls/
         │   │   │   ├── assembly/
         │   │   │   │   ├── assembler.py
         │   │   │   │   ├── bundle.py
         │   │   │   │   ├── iassembler.py
         │   │   │   │   └── __init__.py
         │   │   │   ├── bundle.py
         │   │   │   ├── controllers/
         │   │   │   │   ├── bundle.py
         │   │   │   │   ├── factory.py
         │   │   │   │   └── __init__.py
         │   │   │   ├── factory.py
         │   │   │   ├── __init__.py
         │   │   │   ├── ipanel.py
         │   │   │   └── panel.py
         │   │   ├── dependencies.py
         │   │   ├── dsl/
         │   │   │   ├── bundle.py
         │   │   │   ├── catalog/
         │   │   │   │   ├── catalog.py
         │   │   │   │   ├── factory.py
         │   │   │   │   ├── icatalog.py
         │   │   │   │   └── __init__.py
         │   │   │   ├── console/
         │   │   │   │   ├── console.py
         │   │   │   │   ├── factory.py
         │   │   │   │   ├── iconsole.py
         │   │   │   │   └── __init__.py
         │   │   │   ├── document/
         │   │   │   │   ├── factory.py
         │   │   │   │   ├── imanager.py
         │   │   │   │   ├── __init__.py
         │   │   │   │   └── manager.py
         │   │   │   ├── editor/
         │   │   │   │   ├── editor.py
         │   │   │   │   ├── factory.py
         │   │   │   │   ├── ieditor.py
         │   │   │   │   └── __init__.py
         │   │   │   ├── factory.py
         │   │   │   ├── handler/
         │   │   │   │   ├── binary/
         │   │   │   │   │   ├── bundle.py
         │   │   │   │   │   ├── factory.py
         │   │   │   │   │   ├── handler.py
         │   │   │   │   │   ├── idelegate.py
         │   │   │   │   │   └── __init__.py
         │   │   │   │   ├── execution/
         │   │   │   │   │   ├── bundle.py
         │   │   │   │   │   ├── factory.py
         │   │   │   │   │   ├── handler.py
         │   │   │   │   │   ├── idelegate.py
         │   │   │   │   │   └── __init__.py
         │   │   │   │   ├── file/
         │   │   │   │   │   ├── bundle.py
         │   │   │   │   │   ├── factory.py
         │   │   │   │   │   ├── handler.py
         │   │   │   │   │   ├── idelegate.py
         │   │   │   │   │   └── __init__.py
         │   │   │   │   └── __init__.py
         │   │   │   ├── __init__.py
         │   │   │   ├── itab.py
         │   │   │   ├── syntax/
         │   │   │   │   ├── highlighter/
         │   │   │   │   │   ├── factory.py
         │   │   │   │   │   ├── highlighter.py
         │   │   │   │   │   ├── ihighlighter.py
         │   │   │   │   │   └── __init__.py
         │   │   │   │   ├── __init__.py
         │   │   │   │   ├── tag/
         │   │   │   │   │   ├── applier.py
         │   │   │   │   │   ├── factory.py
         │   │   │   │   │   ├── iapplier.py
         │   │   │   │   │   └── __init__.py
         │   │   │   │   ├── token.py
         │   │   │   │   └── tokenizer/
         │   │   │   │       ├── factory.py
         │   │   │   │       ├── __init__.py
         │   │   │   │       ├── itokenizer.py
         │   │   │   │       └── tokenizer.py
         │   │   │   ├── tab.py
         │   │   │   └── toolbar/
         │   │   │       ├── bundle.py
         │   │   │       ├── factory.py
         │   │   │       ├── __init__.py
         │   │   │       ├── itoolbar.py
         │   │   │       └── toolbar.py
         │   │   ├── editor/
         │   │   │   ├── applier/
         │   │   │   │   ├── applier.py
         │   │   │   │   ├── factory.py
         │   │   │   │   ├── iapplier.py
         │   │   │   │   ├── __init__.py
         │   │   │   │   └── inputs.py
         │   │   │   ├── editor.py
         │   │   │   ├── factory.py
         │   │   │   ├── ieditor.py
         │   │   │   ├── __init__.py
         │   │   │   └── table/
         │   │   │       ├── bundle.py
         │   │   │       ├── factory.py
         │   │   │       ├── __init__.py
         │   │   │       ├── itable.py
         │   │   │       ├── resize/
         │   │   │       │   ├── factory.py
         │   │   │       │   ├── handler.py
         │   │   │       │   ├── ihandler.py
         │   │   │       │   └── __init__.py
         │   │   │       ├── selection/
         │   │   │       │   ├── factory.py
         │   │   │       │   ├── handler.py
         │   │   │       │   ├── ihandler.py
         │   │   │       │   └── __init__.py
         │   │   │       └── table.py
         │   │   ├── emulator/
         │   │   │   ├── __init__.py
         │   │   │   ├── launcher/
         │   │   │   │   ├── factory.py
         │   │   │   │   ├── ilauncher.py
         │   │   │   │   ├── __init__.py
         │   │   │   │   └── launcher.py
         │   │   │   └── locator/
         │   │   │       ├── factory.py
         │   │   │       ├── ilocator.py
         │   │   │       ├── __init__.py
         │   │   │       └── locator.py
         │   │   ├── factory.py
         │   │   ├── gui.py
         │   │   ├── igui.py
         │   │   ├── __init__.py
         │   │   ├── layout/
         │   │   │   ├── builder.py
         │   │   │   ├── canvas/
         │   │   │   │   ├── builder.py
         │   │   │   │   ├── factory.py
         │   │   │   │   ├── ibuilder.py
         │   │   │   │   └── __init__.py
         │   │   │   ├── editor/
         │   │   │   │   ├── builder.py
         │   │   │   │   ├── factory.py
         │   │   │   │   ├── ibuilder.py
         │   │   │   │   └── __init__.py
         │   │   │   ├── factory.py
         │   │   │   ├── __init__.py
         │   │   │   └── toolbar/
         │   │   │       ├── builder.py
         │   │   │       ├── factory.py
         │   │   │       ├── ibuilder.py
         │   │   │       └── __init__.py
         │   │   ├── manipulator/
         │   │   │   ├── __init__.py
         │   │   │   ├── jog/
         │   │   │   │   ├── dependencies.py
         │   │   │   │   ├── factory.py
         │   │   │   │   ├── __init__.py
         │   │   │   │   ├── panel/
         │   │   │   │   │   ├── axis_grid.py
         │   │   │   │   │   ├── bundle.py
         │   │   │   │   │   ├── __init__.py
         │   │   │   │   │   ├── power.py
         │   │   │   │   │   ├── raw_command.py
         │   │   │   │   │   └── tool.py
         │   │   │   │   └── tab.py
         │   │   │   └── override/
         │   │   │       ├── actuator.py
         │   │   │       ├── feedrate.py
         │   │   │       ├── idelegate.py
         │   │   │       ├── __init__.py
         │   │   │       └── panel.py
         │   │   ├── menu/
         │   │   │   ├── builder/
         │   │   │   │   ├── bundle.py
         │   │   │   │   ├── factory.py
         │   │   │   │   ├── hotkey.py
         │   │   │   │   ├── ihotkey.py
         │   │   │   │   ├── ilayout.py
         │   │   │   │   ├── __init__.py
         │   │   │   │   └── layout.py
         │   │   │   ├── bundle.py
         │   │   │   ├── dependencies.py
         │   │   │   ├── factory.py
         │   │   │   ├── imenu_bar.py
         │   │   │   ├── __init__.py
         │   │   │   └── menu_bar.py
         │   │   ├── model/
         │   │   │   ├── canvas_settings.py
         │   │   │   ├── canvas_tool_mode.py
         │   │   │   └── __init__.py
         │   │   ├── preview/
         │   │   │   ├── dependencies.py
         │   │   │   ├── factory.py
         │   │   │   ├── __init__.py
         │   │   │   └── tab.py
         │   │   ├── provides.py
         │   │   ├── splash/
         │   │   │   ├── factory.py
         │   │   │   ├── __init__.py
         │   │   │   ├── iscreen.py
         │   │   │   └── screen.py
         │   │   ├── storage_dependencies.py
         │   │   ├── streaming/
         │   │   │   ├── bundle.py
         │   │   │   ├── control/
         │   │   │   │   ├── idelegate.py
         │   │   │   │   ├── __init__.py
         │   │   │   │   └── panel.py
         │   │   │   ├── controllers_bundle.py
         │   │   │   ├── factory.py
         │   │   │   ├── __init__.py
         │   │   │   ├── observer/
         │   │   │   │   ├── bridge.py
         │   │   │   │   ├── factory.py
         │   │   │   │   ├── ibridge.py
         │   │   │   │   └── __init__.py
         │   │   │   ├── playback/
         │   │   │   │   ├── bundle.py
         │   │   │   │   ├── factory.py
         │   │   │   │   ├── handler.py
         │   │   │   │   └── __init__.py
         │   │   │   ├── progress/
         │   │   │   │   ├── adapter.py
         │   │   │   │   └── __init__.py
         │   │   │   ├── status/
         │   │   │   │   ├── __init__.py
         │   │   │   │   ├── istatus_bar.py
         │   │   │   │   └── status_bar.py
         │   │   │   ├── tab.py
         │   │   │   └── tool/
         │   │   │       ├── factory.py
         │   │   │       ├── handler.py
         │   │   │       └── __init__.py
         │   │   ├── theme/
         │   │   │   ├── __init__.py
         │   │   │   └── manager.py
         │   │   ├── toolbar/
         │   │   │   ├── bundle.py
         │   │   │   ├── factory.py
         │   │   │   ├── __init__.py
         │   │   │   ├── section/
         │   │   │   │   ├── assembler.py
         │   │   │   │   ├── bundle.py
         │   │   │   │   ├── iassembler.py
         │   │   │   │   ├── __init__.py
         │   │   │   │   ├── navigation.py
         │   │   │   │   ├── parameter.py
         │   │   │   │   ├── status.py
         │   │   │   │   └── tool.py
         │   │   │   └── toolbar.py
         │   │   └── validation/
         │   │       ├── dependencies.py
         │   │       ├── factory.py
         │   │       ├── __init__.py
         │   │       └── tab.py
         │   ├── __init__.py
         │   ├── manipulator/
         │   │   ├── dependencies.py
         │   │   ├── factory.py
         │   │   ├── __init__.py
         │   │   ├── jog/
         │   │   │   ├── controller.py
         │   │   │   ├── dependencies.py
         │   │   │   ├── factory.py
         │   │   │   ├── __init__.py
         │   │   │   └── provides.py
         │   │   ├── motion/
         │   │   │   ├── controller.py
         │   │   │   ├── dependencies.py
         │   │   │   ├── factory.py
         │   │   │   ├── __init__.py
         │   │   │   └── provides.py
         │   │   ├── provides.py
         │   │   └── query/
         │   │       ├── controller.py
         │   │       ├── dependencies.py
         │   │       ├── factory.py
         │   │       ├── __init__.py
         │   │       └── provides.py
         │   ├── pacing/
         │   │   ├── controller/
         │   │   │   ├── controller.py
         │   │   │   ├── dependencies.py
         │   │   │   ├── factory.py
         │   │   │   ├── icontroller.py
         │   │   │   ├── __init__.py
         │   │   │   └── provides.py
         │   │   ├── coordinator/
         │   │   │   ├── coordinator.py
         │   │   │   ├── dependencies.py
         │   │   │   ├── factory.py
         │   │   │   ├── icoordinator.py
         │   │   │   ├── __init__.py
         │   │   │   └── provides.py
         │   │   ├── dependencies.py
         │   │   ├── factory.py
         │   │   ├── __init__.py
         │   │   └── provides.py
         │   ├── packet/
         │   │   ├── dependencies.py
         │   │   ├── factory.py
         │   │   ├── __init__.py
         │   │   ├── istrategy.py
         │   │   ├── provides.py
         │   │   └── strategy.py
         │   ├── preferences/
         │   │   ├── dependencies.py
         │   │   ├── factory.py
         │   │   ├── __init__.py
         │   │   ├── provides.py
         │   │   └── serial/
         │   │       ├── dependencies.py
         │   │       ├── factory.py
         │   │       ├── __init__.py
         │   │       ├── provides.py
         │   │       └── repository.py
         │   ├── scaralang/
         │   │   ├── avoidance/
         │   │   │   ├── adapter.py
         │   │   │   ├── factory.py
         │   │   │   ├── iadapter.py
         │   │   │   └── __init__.py
         │   │   ├── boundary/
         │   │   │   ├── adapter.py
         │   │   │   ├── factory.py
         │   │   │   ├── iadapter.py
         │   │   │   └── __init__.py
         │   │   ├── dependencies.py
         │   │   ├── discretizer/
         │   │   │   ├── dependencies.py
         │   │   │   ├── discretizer.py
         │   │   │   ├── factory.py
         │   │   │   ├── __init__.py
         │   │   │   └── provides.py
         │   │   ├── factory.py
         │   │   ├── __init__.py
         │   │   ├── provides.py
         │   │   ├── shape/
         │   │   │   ├── adapter.py
         │   │   │   ├── factory.py
         │   │   │   ├── iadapter.py
         │   │   │   └── __init__.py
         │   │   └── validation/
         │   │       ├── adapter.py
         │   │       ├── bounds_query_adapter.py
         │   │       ├── dependencies.py
         │   │       ├── factory.py
         │   │       ├── ibounds_query.py
         │   │       └── __init__.py
         │   ├── settings/
         │   │   ├── bounds/
         │   │   │   ├── dependencies.py
         │   │   │   ├── factory.py
         │   │   │   ├── __init__.py
         │   │   │   ├── loader/
         │   │   │   │   ├── dependencies.py
         │   │   │   │   ├── factory.py
         │   │   │   │   ├── iloader.py
         │   │   │   │   ├── __init__.py
         │   │   │   │   ├── loader.py
         │   │   │   │   └── provides.py
         │   │   │   ├── parser/
         │   │   │   │   ├── factory.py
         │   │   │   │   ├── __init__.py
         │   │   │   │   ├── iparser.py
         │   │   │   │   ├── parser.py
         │   │   │   │   └── provides.py
         │   │   │   └── provides.py
         │   │   ├── communication/
         │   │   │   ├── dependencies.py
         │   │   │   ├── factory.py
         │   │   │   ├── iloader.py
         │   │   │   ├── __init__.py
         │   │   │   ├── loader.py
         │   │   │   └── provides.py
         │   │   ├── dependencies.py
         │   │   ├── factory.py
         │   │   ├── __init__.py
         │   │   ├── provides.py
         │   │   ├── reader/
         │   │   │   ├── dependencies.py
         │   │   │   ├── factory.py
         │   │   │   ├── __init__.py
         │   │   │   ├── ireader.py
         │   │   │   ├── provides.py
         │   │   │   └── reader.py
         │   │   └── transmission/
         │   │       ├── dependencies.py
         │   │       ├── factory.py
         │   │       ├── iloader.py
         │   │       ├── __init__.py
         │   │       ├── loader.py
         │   │       └── provides.py
         │   ├── state/
         │   │   ├── dependencies.py
         │   │   ├── factory.py
         │   │   ├── imachine.py
         │   │   ├── __init__.py
         │   │   ├── machine.py
         │   │   └── provides.py
         │   ├── storage/
         │   │   ├── config_io/
         │   │   │   ├── dependencies.py
         │   │   │   ├── factory.py
         │   │   │   ├── __init__.py
         │   │   │   ├── loader/
         │   │   │   │   ├── dependencies.py
         │   │   │   │   ├── factory.py
         │   │   │   │   ├── iloader.py
         │   │   │   │   ├── __init__.py
         │   │   │   │   ├── loader.py
         │   │   │   │   └── provides.py
         │   │   │   ├── provides.py
         │   │   │   └── storer/
         │   │   │       ├── dependencies.py
         │   │   │       ├── factory.py
         │   │   │       ├── __init__.py
         │   │   │       ├── istorer.py
         │   │   │       ├── provides.py
         │   │   │       └── storer.py
         │   │   ├── dependencies.py
         │   │   ├── factory.py
         │   │   ├── __init__.py
         │   │   ├── plan/
         │   │   │   ├── dependencies.py
         │   │   │   ├── factory.py
         │   │   │   ├── __init__.py
         │   │   │   ├── loader.py
         │   │   │   ├── provides.py
         │   │   │   └── storer.py
         │   │   ├── provides.py
         │   │   ├── serializer/
         │   │   │   ├── __init__.py
         │   │   │   ├── iserializer.py
         │   │   │   └── serializer.py
         │   │   └── workspace/
         │   │       ├── config.py
         │   │       ├── dependencies.py
         │   │       ├── factory.py
         │   │       ├── imanager.py
         │   │       ├── __init__.py
         │   │       ├── manager.py
         │   │       └── provides.py
         │   ├── streaming/
         │   │   ├── assembly/
         │   │   │   ├── __init__.py
         │   │   │   ├── stream_pacing_assembler.py
         │   │   │   ├── stream_pipeline_assembler.py
         │   │   │   ├── stream_transport_assembler.py
         │   │   │   ├── stream_worker_assembler.py
         │   │   │   └── worker_bundle.py
         │   │   ├── binary/
         │   │   │   ├── dependencies.py
         │   │   │   ├── factory.py
         │   │   │   ├── __init__.py
         │   │   │   ├── istreamer.py
         │   │   │   ├── provides.py
         │   │   │   └── streamer.py
         │   │   ├── control/
         │   │   │   ├── dependencies.py
         │   │   │   ├── factory.py
         │   │   │   ├── __init__.py
         │   │   │   ├── provides.py
         │   │   │   └── transmitter.py
         │   │   ├── dependencies.py
         │   │   ├── factory.py
         │   │   ├── __init__.py
         │   │   ├── observer/
         │   │   │   ├── dispatcher.py
         │   │   │   ├── factory.py
         │   │   │   ├── __init__.py
         │   │   │   ├── provides.py
         │   │   │   └── registry.py
         │   │   ├── playback/
         │   │   │   ├── controller.py
         │   │   │   ├── dependencies.py
         │   │   │   ├── factory.py
         │   │   │   ├── __init__.py
         │   │   │   └── provides.py
         │   │   └── provides.py
         │   ├── tool/
         │   │   ├── controller/
         │   │   │   ├── controller.py
         │   │   │   ├── dependencies.py
         │   │   │   ├── factory.py
         │   │   │   ├── __init__.py
         │   │   │   └── provides.py
         │   │   ├── dependencies.py
         │   │   ├── factory.py
         │   │   ├── __init__.py
         │   │   ├── provides.py
         │   │   └── worker/
         │   │       ├── factory.py
         │   │       ├── __init__.py
         │   │       ├── irunner.py
         │   │       ├── provides.py
         │   │       ├── runner.py
         │   │       └── worker.py
         │   └── worker/
         │       ├── dependencies.py
         │       ├── dispatcher/
         │       │   ├── bundle.py
         │       │   ├── dispatcher.py
         │       │   ├── factory.py
         │       │   ├── idispatcher.py
         │       │   └── __init__.py
         │       ├── drainer/
         │       │   ├── dependencies.py
         │       │   ├── drainer.py
         │       │   ├── factory.py
         │       │   ├── idrainer.py
         │       │   └── __init__.py
         │       ├── execution/
         │       │   ├── dependencies.py
         │       │   ├── factory.py
         │       │   ├── __init__.py
         │       │   └── worker.py
         │       ├── factory.py
         │       ├── handler/
         │       │   ├── dependencies.py
         │       │   ├── factory.py
         │       │   ├── handler.py
         │       │   ├── ihandler.py
         │       │   └── __init__.py
         │       ├── holder.py
         │       ├── iexecution_worker.py
         │       ├── __init__.py
         │       ├── parser/
         │       │   ├── bundle.py
         │       │   └── __init__.py
         │       ├── provides.py
         │       ├── receiver/
         │       │   ├── dependencies.py
         │       │   ├── factory.py
         │       │   ├── __init__.py
         │       │   └── receiver.py
         │       ├── runner/
         │       │   ├── bundle.py
         │       │   ├── factory.py
         │       │   ├── __init__.py
         │       │   ├── irunner.py
         │       │   ├── loop_bundle.py
         │       │   └── runner.py
         │       └── thread/
         │           ├── coordinator.py
         │           ├── factory.py
         │           ├── icoordinator.py
         │           └── __init__.py
         ├── __init__.py
         ├── py.typed
         └── setup/
             ├── assembly/
             │   ├── core/
             │   │   ├── assembler.py
             │   │   ├── bundle.py
             │   │   └── __init__.py
             │   ├── dsl/
             │   │   ├── assembler.py
             │   │   ├── bundle.py
             │   │   ├── diagnostic_bundle.py
             │   │   └── __init__.py
             │   ├── __init__.py
             │   ├── plan/
             │   │   ├── assembler.py
             │   │   ├── bundle.py
             │   │   └── __init__.py
             │   ├── presentation/
             │   │   ├── assembler.py
             │   │   └── __init__.py
             │   └── runtime/
             │       ├── assembler.py
             │       ├── bundle.py
             │       └── __init__.py
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

     183 directories, 776 files
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
┌──────────────────┐      ┌─────────────────┐      ┌────────────────────┐      ┌──────────────────┐
│ TrajectoryCanvas │      │ TrajectoryTable │      │   DslEditorTab     │      │   StreamerTab    │
│   (Vector CAD)   │      │   (Data Grid)   │      │(Syntax Highlighter)│      │ (Live Feedrate & │
└────────┬─────────┘      └────────┬────────┘      └─────────┬──────────┘      │  Device Control) │
         │                         │                         │                 └────────┬─────────┘
         │                         │                         │                          │
         └────────────┬────────────┴─────────────────────────┘                          │
                      │ Observes / Modifies TrajectoryPlan                              │
                      ▼                                                                 │
         ┌──────────────────────────┐                                                   │
         │      TrajectoryPlan      │ (Domain Model)                                    │
         └────────────┬─────────────┘                                                   │
                      │                                                                 │
         ┌────────────┴────────────┬────────────────────────┐                           │ Uses ITransport &
         ▼                         ▼                        ▼                           │ Classifiers
┌──────────────────┐      ┌──────────────────┐     ┌─────────────────┐                  ▼
│TrajectoryValidat.│      │  ScaraDslService │     │ ScaraPlanExport │         ┌──────────────────┐
│(Workspace Bounds)│      │  (DSL Compiler)  │     │  (Plan to DSL)  │         │  SerialStreamer  │
└──────────────────┘      └────────┬─────────┘     └─────────────────┘         └────────┬─────────┘
                                   │                                                    │
              ┌────────────────────┼────────────────────┐                               ▼
              ▼                    ▼                    ▼                      ┌──────────────────┐
     ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐             │Response & FlowCls│
     │   ScaraLexer    │  │   ScaraParser   │  │  ScaraCompiler  │             └──────────────────┘
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
* **Automated Singularity Dead Zone Detour Routing**: Intelligent tangent bypass arc path planning around the central singularity dead zone ($R_{min} = 86.08\text{ mm}$) preventing kinematic faults during multi-segment geometric drafting (rectangles, crossing lines, circles).
* **Dual-Elbow Kinematic Resolution**: Dynamic inverse kinematic validation with automated `LEFT` and `RIGHT` elbow configuration evaluation for complete workspace reachability.
* **Undo / Redo Transaction Stack**: Non-destructive history management for waypoint additions, modifications, insertions, and deletions (`Ctrl+Z`, `Ctrl+Y`).
* **Binary Protocol Frame Generation**: Formats trajectory waypoints into wire-protocol binary frames packed with CRC16 and delimiters.
* **Sliding Window Hardware Streaming**: Multi-threaded USB serial (`/dev/ttyACM0`) and TCP socket streaming with dynamic ACK tracking, auto-pause on buffer full, progress monitoring, and live Feedrate Override (10% - 200%).
* **Manual Jogging & Diagnostics**: Interactive jog grid (X, Y, Z, Phi), vacuum pump and release valve toggles, homing, status queries, and raw serial command console.
* **Configurable Kinematics & Dimensions**: Dynamic robot link lengths ($L_1, L_2$), stroke limits ($Z_{min}, Z_{max}$), and speed bounds configurable via CLI options and JSON schema.
* **Strict Quality & SOLID Standards**: 100% protocol conformity, zero ISP/SRP violations, 100% test coverage, and 10.00 / 10.00 Pylint score.

#### 📐 SCARA Kinematic & Geometric Configuration

The robot dimensions and physical boundaries can be customized in [`scara_geometry.json`](scarajectory/infrastructure/config/scara_geometry.json) or injected programmatically:

| Parameter | Default Value | Description |
|---|:---:|---|
| **`l1`** | `150.0 mm` | Primary arm link length (shoulder to elbow). |
| **`l2`** | `120.0 mm` | Secondary arm link length (elbow to wrist). |
| **`r_min`** | `86.08 mm` | Minimum reach radius limit (governed by mechanical joint $J_2 \le 145^\circ$ limit; theoretical $|L_1 - L_2| = 30.0\text{ mm}$). |
| **`r_max`** | `270.0 mm` | Maximum horizontal reach boundary ($L_1 + L_2$). |
| **`z_min`** | `0.0 mm` | Minimum vertical height limit (bed level). |
| **`z_max`** | `100.0 mm` | Maximum vertical stroke limit. |
| **`min_speed`** | `1.0 mm/s` | Minimum allowable feedrate speed. |
| **`max_speed`** | `100.0 mm/s` | Maximum allowable safe feedrate speed. |

##### 🔄 Singularity Dead Zone Avoidance & Dual-Elbow Routing

Trajectory planning incorporates real-time geometric intersection checking against the inner dead zone boundary ($R_{min} = 86.08\text{ mm}$). When a drafted line or polygon segment intersects this central singularity, `scarajectory` automatically computes tangential detour waypoints to route motion safely around the dead zone. Waypoints are evaluated with dual-elbow kinematics (`LEFT` and `RIGHT` configurations) to ensure continuous inverse-kinematic reachability:

```
[Start / End Points] ──► [Ray-Circle Intersection] ──► [Central Dead Zone?]
                                                            │
                                    ┌───────────────────────┴───────────────────────┐
                                    ▼ YES                                           ▼ NO
                       [Tangential Detour Arc]                         [Direct Motion Segment]
                       [Left/Right Elbow IK Check]                     [Left/Right Elbow IK Check]
                                    │                                               │
                                    └───────────────────────┬───────────────────────┘
                                                            ▼
                                               [Validated Trajectory Plan]
```

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

##### Bundled Industrial `.scara` Demonstration Programs

**scarajectory** includes a comprehensive suite of 50 industrial-grade `.scara` demonstration programs showcasing the full capabilities of the DSL syntax, kinematics, trajectory smoothing, and pneumatic tool sequencing:

| File Name | Functional Category | Primary DSL Instructions | Description |
|---|---|---|---|
| **`01_homing.scara`** | Calibration & Safety | `ENABLE`, `HOME` | Coordinated multi-axis homing sequence (Z limit switch, J2 elbow, J1 shoulder) and zero-reference calibration. |
| **`02_linear_motion.scara`** | Cartesian Interpolation | `SPEED WORK/RAPID`, `MOVE_L` | Continuous linear interpolated path between Cartesian coordinates with configurable working and rapid feedrates. |
| **`03_joint_rapid.scara`** | Rapid Transit | `MOVE_J` | High-speed joint-interpolated transit across workspace quadrants, prioritizing transition speed over straight-line paths. |
| **`04_circular_arc.scara`** | Planar Contouring | `ARC_CW`, `ARC_CCW` | Clockwise and counter-clockwise circular arc interpolation using relative center offsets (`I`, `J`). |
| **`05_jump_arch.scara`** | 3D Pick & Place | `JUMP`, `ARCH` | Parabolic 3D clearance arch: vertical ascent, horizontal transit, and descent with configurable clearance height. |
| **`06_pneumatics.scara`** | Actuator Sequencing | `PUMP ON/OFF`, `VALVE ON/OFF`, `WAIT_MS` | Pneumatic vacuum pump and blow-off valve actuation with safety interlocks preventing simultaneous engagement. |
| **`07_approach_retract.scara`** | Z-Axis Tooling | `APPROACH DIST`, `RETRACT DIST` | Relative descent to workpiece at controlled creep speed and fast clearance ascent along the Z-axis. |
| **`08_work_frames.scara`** | Coordinate Systems | `FRAME_SET`, `FRAME_RESET` | User Work Coordinate System (WCS) shifting and rotated reference systems for inclined assembly stations. |
| **`09_pallet_matrix.scara`** | Parametric Palletizing | `PALLET_DEF`, `MOVE_PALLET` | 2D pallet grid matrix indexing by row, column, pitch (`DX`, `DY`), and zero-based cell index. |
| **`10_tangent_orientation.scara`** | 4th-Axis Tool Control | `TOOL_ORIENT TANGENTIAL/FIXED` | Automatic continuous rotation of the 4th axis ($\Phi$) tangential to trajectory heading (knife cutting, dispensing). |
| **`11_zone_blending.scara`** | Trajectory Smoothing | `ZONE BLEND`, `ZONE FINE` | Continuous curvature trajectory blending and corner rounding radius for high-speed continuous motion. |
| **`12_industrial_pick_place.scara`** | Full Automation Cycle | `FRAME_SET`, `MOVE_J`, `ZONE BLEND`, `PUMP`, `VALVE`, `RETRACT` | Comprehensive production pick-and-place cycle combining homing, frames, blended transit, vacuum grip, and blow-off release. |
| **`13_elbow_reconfiguration.scara`** | Arm Pose Configuration | `CONFIG_ELBOW LEFT/RIGHT` | Dynamic arm posture reconfiguration between Righty and Lefty configurations through intermediate workspace transit. |
| **`14_singularity_avoidance.scara`** | Kinematic Boundary Avoidance | `SPEED WORK`, `MOVE_L` | Central singular dead zone bypass detour routing end-effector around unreachable central boundary. |
| **`15_boundary_reach_limits.scara`** | Reach Envelope Inspection | `MOVE_L`, `WAIT_MS` | Safe perimeter scanning near maximum reach envelope avoiding outer singular deadband. |
| **`16_multi_frame_palletizing.scara`** | Multi-WCS Palletizing | `FRAME_SET`, `PALLET_DEF`, `MOVE_PALLET`, `PUMP`, `VALVE` | Multi-station pick-and-place material handling combining user frames, pallet matrix traversal, and pneumatic grip. |
| **`17_bidirectional_elbow_assembly.scara`** | Bidirectional Reconfiguration | `CONFIG_ELBOW`, `MOVE_L`, `PUMP`, `VALVE` | Bidirectional elbow reconfiguration cycle (RIGHT -> LEFT -> RIGHT) accessing rear assembly slot and returning to front cradle. |
| **`18_tangential_contour_dispensing.scara`** | Tangential Dispensing | `TOOL_ORIENT TANGENTIAL`, `ZONE BLEND`, `ARC_CW`, `VALVE` | Continuous fluid dispensing along composite linear and circular arc contours with dynamic tangential nozzle orientation. |
| **`19_high_speed_sorter_jump.scara`** | Quality Sorter Cell | `JUMP`, `ACCEL`, `OVERRIDE`, `PUMP`, `VALVE` | High-speed multi-bin sorting sequence using parabolic jump arches, dynamic acceleration scaling, and speed overrides. |
| **`20_annular_inspection_scan.scara`** | Annular Quality Inspection | `ARC_CCW`, `ARC_CW`, `MOVE_L`, `WAIT_MS` | Multi-level concentric circular inspection scanning clear of inner deadzone and outer boundary singularities. |
| **`21_relative_motion_incremental.scara`** | Incremental Positioning | `MOVE_REL`, `WAIT_MS` | Incremental workpiece positioning using relative Cartesian offsets along X, Y, and Z. |
| **`22_conveyor_tracking_relative.scara`** | Conveyor Tracking | `MOVE_REL`, `APPROACH`, `RETRACT` | Dynamic conveyor tracking and pick sequence using relative motions coordinated with line speed. |
| **`23_bidirectional_arc_contour.scara`** | S-Curve Contouring | `ARC_CW`, `ARC_CCW`, `TOOL_ORIENT` | Continuous S-shaped contour combining bidirectional circular arcs with dynamic tangential orientation. |
| **`24_matrix_pallet_depalletizing.scara`** | Dual-Pallet Transfer | `PALLET_DEF`, `MOVE_PALLET`, `PUMP`, `VALVE` | Automated material transfer between dual matrix pallets (infeed to outfeed) with vacuum grip. |
| **`25_stepper_motor_calibration.scara`** | Stepper Calibration | `CONFIG_MOTOR`, `MOVE_J`, `WAIT_MS` | Dynamic motor drive mode reconfiguration switching between open-loop and closed-loop actuation. |
| **`26_multi_zone_high_speed_blending.scara`** | Multi-Tier Blending | `ZONE BLEND`, `SPEED WORK`, `MOVE_L` | Multi-tier corner zone blending profiles evaluating trajectory continuous curvature smoothing. |
| **`27_emergency_hold_recovery.scara`** | Safety & Interlocks | `HOLD`, `RESUME`, `MOVE_L` | Feed hold, dwell, and resume motion execution state management and recovery routines. |
| **`28_three_frame_assembly_station.scara`** | Multi-WCS Stations | `FRAME_SET`, `FRAME_RESET`, `MOVE_L` | Assembly sequence traversing three distinct user work coordinate frames (assembly, inspection, packaging). |
| **`29_precision_dispensing_tangent.scara`** | Precision Dispensing | `TOOL_ORIENT TANGENTIAL`, `MOVE_L`, `ARC_CW` | Continuous fluid gasket dispensing path around closed boundary with dynamic tangential nozzle tracking. |
| **`30_complex_automation_workcell.scara`** | Full Workcell Routine | `CONFIG_ELBOW`, `FRAME_SET`, `PALLET_DEF`, `JUMP` | Comprehensive industrial workcell routine combining all core motion primitives, frames, and pallets. |
| **`31_subroutine_pick_place.scara`** | Modular Subroutines | `DEF`, `CALL`, `END`, `MOVE_L`, `PUMP` | Reusable macro subroutine encapsulation for industrial pick, transfer, and place cycles. |
| **`32_repeat_loop_array.scara`** | Iterative Array Loops | `REPEAT`, `END`, `MOVE_REL` | Fixed-iteration macro loop scanning an inspection array with incremental relative motions. |
| **`33_nested_repeat_palletizing.scara`** | Nested Macro Loops | `REPEAT`, `END`, `MOVE_REL`, `APPROACH` | Multi-level nested iteration loops traversing a 2D raster pallet grid without explicit pallet definitions. |
| **`34_subroutine_with_relative_motion.scara`** | Subroutine Relative Motion | `DEF`, `CALL`, `MOVE_REL`, `CONFIG_ELBOW` | Parameterized dispensing subroutines combined with relative motions across alternating elbow configurations. |
| **`35_complex_cycle_subroutines_and_loops.scara`** | Integrated Workcell Routine | `DEF`, `CALL`, `REPEAT`, `CONFIG_ELBOW`, `ZONE` | Enterprise workcell demonstration integrating subroutines, repeat loops, and dynamic reconfiguration. |
| **`36_spatial_keepout_zones.scara`** | Obstacle Avoidance | `ZONE_DEF BOX`, `MOVE_L` | Rectangular keep-out obstacle zone definition and collision-free transit around safety perimeter. |
| **`37_obstacle_avoidance_dual_elbow.scara`** | Multi-Obstacle Dual-Elbow | `ZONE_DEF BOX/CIRCLE`, `CONFIG_ELBOW` | Multi-obstacle avoidance (box and cylinder) combined with elbow reconfiguration during transit. |
| **`38_nested_matrix_frame_sorting.scara`** | Matrix Frame Sorting | `DEF`, `CALL`, `PALLET_DEF`, `FRAME_SET` | Subroutine-driven component acquisition from matrix pallet with frame transformation sorting. |
| **`39_closed_loop_contour_hold_recovery.scara`** | Closed-Loop Contouring | `CONFIG_MOTOR CLOSED_LOOP`, `ZONE BLEND`, `HOLD` | High-precision closed-loop contouring with feed hold pause, recovery, and corner rounding. |
| **`40_pallet_obstacle_jump_transfer.scara`** | Obstacle-Aware Palletizing | `ZONE_DEF`, `PALLET_DEF`, `JUMP`, `MOVE_PALLET` | Collision-aware dual-pallet transfer navigating parabolic jump arches over obstacle boundaries. |
| **`41_dynamic_feedrate_accel_profiling.scara`** | Dynamic Speed Profiling | `SPEED WORK/RAPID`, `ACCEL`, `OVERRIDE` | Multi-stage dynamic feedrate and acceleration profile scheduling for delicate workpiece entry. |
| **`42_vacuum_decay_pressure_equalization.scara`** | Pneumatic Timing | `PUMP ON/OFF`, `VALVE ON/OFF`, `WAIT_MS` | Vacuum decay monitoring and micro-dwell pressure equalization for airtight fixture handling. |
| **`43_tangential_pocket_milling.scara`** | Pocket Milling & Contouring | `TOOL_ORIENT TANGENTIAL`, `ARC_CW`, `MOVE_L` | Multi-depth concentric circular pocket profiling with continuous tool tangency. |
| **`44_hierarchical_subroutine_chain.scara`** | Nested Subroutine Chain | `DEF`, `CALL`, `END` | 3-level hierarchical subroutine call stack expansion (atomic, operation, workflow). |
| **`45_polar_rotary_inspection_sweep.scara`** | Polar Rotary Sweep | `ARC_CCW`, `ARC_CW`, `WAIT_MS` | Polar optical inspection sweeps tracing concentric annular workpiece perimeters. |
| **`46_rotated_frame_relative_stepping.scara`** | Rotated Frame Stepping | `FRAME_SET`, `MOVE_REL`, `APPROACH` | Relative Cartesian incremental stepping within an angled work coordinate frame. |
| **`47_asymmetric_dual_obstacle_channel.scara`** | Channel Corridor Transit | `ZONE_DEF BOX`, `MOVE_L`, `SPEED WORK` | Collision-free trajectory navigation through an asymmetric corridor between keep-out obstacles. |
| **`48_hybrid_motor_mode_torque_switch.scara`** | Hybrid Drive Reconfiguration | `CONFIG_MOTOR OPEN_LOOP/CLOSED_LOOP` | Runtime stepper drive mode switching between high-speed open-loop and precision closed-loop phases. |
| **`49_serpentine_raster_dispensing.scara`** | Serpentine Surface Raster | `TOOL_ORIENT TANGENTIAL`, `ARC_CW`, `MOVE_L` | Continuous planar serpentine dispensing path with continuous tangential nozzle tracking. |
| **`50_master_multisystem_production_cell.scara`** | Capstone Production Cell | `CONFIG_ELBOW`, `CONFIG_MOTOR`, `ZONE_DEF`, `DEF` | Master industrial production cell combining all SCARA DSL language, motion, and hardware capabilities. |

##### User Workspace Auto-Provisioning (`~/.scarajectory/workspace/`)

To allow users to modify, test, and develop custom routines without modifying the installed package assets, **scarajectory** implements an automated personal workspace architecture:

* **Automatic Archive Extraction:** All 50 demonstration scripts are packaged inside `examples.tgz` within the package configuration. Upon application launch or when initializing the DSL Editor tab, `WorkspaceService` verifies that the workspace directory (`~/.scarajectory/workspace/`) exists. If the folder does not exist or any bundled scripts are absent, the archive unpacks missing examples automatically into the user's workspace.
* **Integrated Examples Catalog:** The **Examples:** dropdown combobox on the DSL Editor toolbar dynamically discovers and lists all `.scara` files present in the user workspace. Selecting an example and clicking **📂 Load Demo** immediately populates the syntax-highlighted editor with the script.
* **Streamlined File Dialogs:** File operations such as **📂 Open...** (`Ctrl+O`) and **💾 Save As...** (`Ctrl+S`) default directly to `~/.scarajectory/workspace/`, enabling quick access to user scripts and personal templates.
* **Safe User Customization:** Users can freely edit existing examples, save variations, or create new industrial programs directly in `~/.scarajectory/workspace/` with full persistence.

### 📊 Code coverage

<details>
<summary><b>Click to expand code coverage</b></summary>

| Name | Stmts | Miss | Cover |
|------|-------|------|-------|
| `scarajectory/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/model/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/model/jog/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/model/jog/axis.py` | 16 | 0 | 100%|
| `scarajectory/core/model/jog/command.py` | 18 | 0 | 100%|
| `scarajectory/core/model/jog/direction.py` | 14 | 0 | 100%|
| `scarajectory/core/model/streaming/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/model/streaming/config.py` | 16 | 0 | 100%|
| `scarajectory/core/model/streaming/pacing_config.py` | 15 | 0 | 100%|
| `scarajectory/core/model/streaming/session.py` | 19 | 0 | 100%|
| `scarajectory/core/model/streaming/state.py` | 17 | 0 | 100%|
| `scarajectory/core/model/telemetry/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/model/telemetry/counts.py` | 16 | 0 | 100%|
| `scarajectory/core/model/telemetry/diagnostics/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/model/telemetry/diagnostics/bundle.py` | 20 | 0 | 100%|
| `scarajectory/core/model/telemetry/diagnostics/comm.py` | 19 | 0 | 100%|
| `scarajectory/core/model/telemetry/diagnostics/driver.py` | 14 | 0 | 100%|
| `scarajectory/core/model/telemetry/diagnostics/errors.py` | 16 | 0 | 100%|
| `scarajectory/core/model/telemetry/diagnostics/steps.py` | 16 | 0 | 100%|
| `scarajectory/core/model/telemetry/fault.py` | 15 | 0 | 100%|
| `scarajectory/core/model/telemetry/move.py` | 14 | 0 | 100%|
| `scarajectory/core/model/telemetry/progress.py` | 20 | 0 | 100%|
| `scarajectory/core/model/telemetry/status.py` | 19 | 0 | 100%|
| `scarajectory/core/model/telemetry/summary.py` | 18 | 0 | 100%|
| `scarajectory/core/model/trajectory/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/model/trajectory/waypoint.py` | 19 | 0 | 100%|
| `scarajectory/core/service/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/manipulator/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/manipulator/ijog.py` | 14 | 0 | 100%|
| `scarajectory/core/service/manipulator/imotion.py` | 16 | 0 | 100%|
| `scarajectory/core/service/manipulator/iquery.py` | 14 | 0 | 100%|
| `scarajectory/core/service/storage/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/storage/iloader.py` | 16 | 0 | 100%|
| `scarajectory/core/service/storage/istorer.py` | 16 | 0 | 100%|
| `scarajectory/core/service/streaming/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/streaming/config_factory.py` | 25 | 0 | 100%|
| `scarajectory/core/service/streaming/control/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/streaming/control/itransmitter.py` | 16 | 0 | 100%|
| `scarajectory/core/service/streaming/observer/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/streaming/observer/idispatcher.py` | 16 | 0 | 100%|
| `scarajectory/core/service/streaming/observer/iobserver.py` | 15 | 0 | 100%|
| `scarajectory/core/service/streaming/observer/iregistry.py` | 17 | 0 | 100%|
| `scarajectory/core/service/streaming/pacing_config_factory.py` | 20 | 0 | 100%|
| `scarajectory/core/service/streaming/playback/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/streaming/playback/icontroller.py` | 18 | 0 | 100%|
| `scarajectory/core/service/streaming/session_factory.py` | 22 | 0 | 100%|
| `scarajectory/core/service/telemetry/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/telemetry/diagnostics/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/telemetry/diagnostics/bundle_factory.py` | 21 | 0 | 100%|
| `scarajectory/core/service/telemetry/diagnostics/driver_factory.py` | 17 | 0 | 100%|
| `scarajectory/core/service/telemetry/diagnostics/errors_factory.py` | 17 | 0 | 100%|
| `scarajectory/core/service/telemetry/diagnostics/steps_factory.py` | 17 | 0 | 100%|
| `scarajectory/core/service/telemetry/fault_factory.py` | 17 | 0 | 100%|
| `scarajectory/core/service/telemetry/move_factory.py` | 17 | 0 | 100%|
| `scarajectory/core/service/tool/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/tool/iactuator.py` | 14 | 0 | 100%|
| `scarajectory/core/service/tool/icontroller.py` | 15 | 0 | 100%|
| `scarajectory/core/service/trajectory/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/trajectory/history/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/trajectory/history/dependencies.py` | 14 | 0 | 100%|
| `scarajectory/core/service/trajectory/history/factory.py` | 26 | 0 | 100%|
| `scarajectory/core/service/trajectory/history/navigator/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/trajectory/history/navigator/dependencies.py` | 14 | 0 | 100%|
| `scarajectory/core/service/trajectory/history/navigator/factory.py` | 18 | 0 | 100%|
| `scarajectory/core/service/trajectory/history/navigator/inavigator.py` | 18 | 0 | 100%|
| `scarajectory/core/service/trajectory/history/navigator/navigator.py` | 33 | 0 | 100%|
| `scarajectory/core/service/trajectory/history/provides.py` | 16 | 0 | 100%|
| `scarajectory/core/service/trajectory/history/saver/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/trajectory/history/saver/dependencies.py` | 14 | 0 | 100%|
| `scarajectory/core/service/trajectory/history/saver/factory.py` | 18 | 0 | 100%|
| `scarajectory/core/service/trajectory/history/saver/isaver.py` | 16 | 0 | 100%|
| `scarajectory/core/service/trajectory/history/saver/saver.py` | 26 | 0 | 100%|
| `scarajectory/core/service/trajectory/history/stack/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/trajectory/history/stack/factory.py` | 17 | 0 | 100%|
| `scarajectory/core/service/trajectory/history/stack/istack.py` | 18 | 0 | 100%|
| `scarajectory/core/service/trajectory/history/stack/stack.py` | 25 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/history/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/history/dependencies.py` | 20 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/history/factory.py` | 20 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/history/history.py` | 40 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/history/ihistory.py` | 14 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/history/provides.py` | 14 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/mutation/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/mutation/bulk_mutation/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/mutation/bulk_mutation/bulk_mutation.py` | 38 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/mutation/bulk_mutation/ibulk_mutation.py` | 16 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/mutation/dependencies.py` | 20 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/mutation/factory.py` | 24 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/mutation/point_mutation/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/mutation/point_mutation/ipoint_mutation.py` | 17 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/mutation/point_mutation/point_mutation.py` | 52 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/mutation/provides.py` | 16 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/observer/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/observer/dispatcher.py` | 26 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/observer/factory.py` | 20 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/observer/idispatcher.py` | 18 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/observer/itrajectory_observer.py` | 14 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/observer/provides.py` | 14 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/selection/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/selection/coordinator/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/selection/coordinator/coordinator.py` | 27 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/selection/coordinator/dependencies.py` | 18 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/selection/coordinator/factory.py` | 18 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/selection/coordinator/icoordinator.py` | 15 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/selection/dependencies.py` | 17 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/selection/factory.py` | 28 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/selection/navigator/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/selection/navigator/factory.py` | 18 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/selection/navigator/inavigator.py` | 17 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/selection/navigator/navigator.py` | 25 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/selection/provides.py` | 18 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/selection/state/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/selection/state/factory.py` | 17 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/selection/state/istate.py` | 17 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/selection/state/state.py` | 28 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/store/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/store/bulk_mutator/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/store/bulk_mutator/bulk_mutator.py` | 21 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/store/bulk_mutator/ibulk_mutator.py` | 16 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/store/dependencies.py` | 15 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/store/factory.py` | 32 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/store/istore.py` | 15 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/store/mutator/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/store/mutator/imutator.py` | 17 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/store/mutator/mutator.py` | 29 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/store/provides.py` | 20 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/store/query/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/store/query/iquery.py` | 18 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/store/query/query.py` | 22 | 0 | 100%|
| `scarajectory/core/service/trajectory/plan/store/store.py` | 32 | 0 | 100%|
| `scarajectory/core/service/trajectory/validation/__init__.py` | 9 | 0 | 100%|
| `scarajectory/core/service/trajectory/validation/ivalidator.py` | 25 | 0 | 100%|
| `scarajectory/engine.py` | 58 | 0 | 100%|
| `scarajectory/infrastructure/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/barrier/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/barrier/factory.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/barrier/provides.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/cli/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/cli/dependencies.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/cli/engine.py` | 38 | 0 | 100%|
| `scarajectory/infrastructure/cli/factory.py` | 19 | 0 | 100%|
| `scarajectory/infrastructure/cli/icli.py` | 15 | 0 | 100%|
| `scarajectory/infrastructure/cli/provides.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/cli/setup/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/cli/setup/bundle.py` | 20 | 0 | 100%|
| `scarajectory/infrastructure/cli/setup/dep_validator.py` | 36 | 0 | 100%|
| `scarajectory/infrastructure/cli/setup/dependencies.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/cli/setup/factory.py` | 30 | 0 | 100%|
| `scarajectory/infrastructure/cli/setup/keys.py` | 25 | 0 | 100%|
| `scarajectory/infrastructure/cli/setup/opt_validator.py` | 36 | 0 | 100%|
| `scarajectory/infrastructure/cli/setup/options.py` | 15 | 0 | 100%|
| `scarajectory/infrastructure/cli/setup/registry.py` | 24 | 0 | 100%|
| `scarajectory/infrastructure/cli/setup/validator.py` | 38 | 0 | 100%|
| `scarajectory/infrastructure/command/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/command/bundle.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/command/dependencies.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/command/factory.py` | 21 | 0 | 100%|
| `scarajectory/infrastructure/command/idefinition.py` | 21 | 0 | 100%|
| `scarajectory/infrastructure/command/iexecutor.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/command/provides.py` | 15 | 0 | 100%|
| `scarajectory/infrastructure/command/studio/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/command/studio/definition.py` | 26 | 0 | 100%|
| `scarajectory/infrastructure/command/studio/dependencies.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/command/studio/executor.py` | 38 | 0 | 100%|
| `scarajectory/infrastructure/command/studio/factory.py` | 26 | 0 | 100%|
| `scarajectory/infrastructure/command/studio/provides.py` | 19 | 0 | 100%|
| `scarajectory/infrastructure/connection/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/connection/dependencies.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/connection/dispatcher/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/connection/dispatcher/dependencies.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/connection/dispatcher/dispatcher.py` | 33 | 0 | 100%|
| `scarajectory/infrastructure/connection/dispatcher/factory.py` | 20 | 0 | 100%|
| `scarajectory/infrastructure/connection/dispatcher/idispatcher.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/connection/dispatcher/provides.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/connection/factory.py` | 33 | 0 | 100%|
| `scarajectory/infrastructure/connection/listener/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/connection/listener/factory.py` | 19 | 0 | 100%|
| `scarajectory/infrastructure/connection/listener/listener.py` | 22 | 0 | 100%|
| `scarajectory/infrastructure/connection/manager/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/connection/manager/dependencies.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/connection/manager/factory.py` | 20 | 0 | 100%|
| `scarajectory/infrastructure/connection/manager/imanager.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/connection/manager/manager.py` | 24 | 0 | 100%|
| `scarajectory/infrastructure/connection/manager/provides.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/connection/provides.py` | 22 | 0 | 100%|
| `scarajectory/infrastructure/connection/receiver/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/connection/receiver/bootstrap.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/connection/receiver/ibytes_receiver.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/connection/router/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/connection/router/factory.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/connection/router/provides.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/gui/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/bundle.py` | 27 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/adapter_bundle.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/bundle.py` | 46 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/event/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/event/binder.py` | 59 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/event/dependencies.py` | 20 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/event/factory.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/event/ibinder.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/handler/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/handler/coordinator/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/handler/coordinator/bundle.py` | 24 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/handler/coordinator/coordinator.py` | 99 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/handler/coordinator/factory.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/handler/coordinator/icoordinator.py` | 17 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/handler/drag/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/handler/drag/bundle.py` | 24 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/handler/drag/factory.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/handler/drag/handler.py` | 59 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/handler/drag/ihandler.py` | 15 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/handler/mouse/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/handler/mouse/bundle.py` | 24 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/handler/mouse/context.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/handler/mouse/factory.py` | 43 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/handler/mouse/handler.py` | 73 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/handler/mouse/ihandler.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/handler/mouse/init_bundle.py` | 42 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/handler/pan/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/handler/pan/factory.py` | 19 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/handler/pan/handler.py` | 41 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/handler/pan/ihandler.py` | 17 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/handler/selection/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/handler/selection/bundle.py` | 24 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/handler/selection/factory.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/handler/selection/handler.py` | 62 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/handler/selection/ihandler.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/handler/shape/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/handler/shape/factory.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/handler/shape/handler.py` | 35 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/handler/shape/ibuilder.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/handler/shape/ihandler.py` | 19 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/handler/state.py` | 31 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/icanvas.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/navigation/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/navigation/dependencies.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/navigation/factory.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/navigation/inavigator.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/navigation/itarget.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/navigation/navigator.py` | 34 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/observer/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/observer/bridge.py` | 19 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/observer/factory.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/observer/iredraw_delegate.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/renderer/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/renderer/boundary/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/renderer/boundary/reach.py` | 30 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/renderer/boundary/zone.py` | 37 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/renderer/boundary/zone_factory.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/renderer/grid/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/renderer/grid/renderer.py` | 36 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/renderer/layer/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/renderer/layer/ilayer.py` | 17 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/renderer/preview/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/renderer/preview/renderer.py` | 34 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/renderer/renderer.py` | 39 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/renderer/trajectory/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/renderer/trajectory/bundle.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/renderer/trajectory/node.py` | 30 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/renderer/trajectory/node_factory.py` | 17 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/renderer/trajectory/renderer.py` | 33 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/settings/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/settings/ipresenter.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/settings/presenter.py` | 24 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/status/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/status/factory.py` | 17 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/status/ipresenter.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/status/presenter.py` | 24 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/tool/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/tool/coordinator.py` | 30 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/tool/icoordinator.py` | 17 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/trajectory_canvas.py` | 57 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/trajectory_canvas_factory.py` | 48 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/transform/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/transform/camera.py` | 36 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/transform/icamera.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/transform/iprojector.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/transform/projector.py` | 24 | 0 | 100%|
| `scarajectory/infrastructure/gui/canvas/transform/transform.py` | 28 | 0 | 100%|
| `scarajectory/infrastructure/gui/connection/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/connection/action/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/connection/action/action.py` | 40 | 0 | 100%|
| `scarajectory/infrastructure/gui/connection/action/iaction.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/gui/connection/action/idelegate.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/gui/connection/panel/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/connection/panel/ipanel.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/gui/connection/panel/panel.py` | 40 | 0 | 100%|
| `scarajectory/infrastructure/gui/connection/selector/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/connection/selector/iselector.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/gui/connection/selector/selector.py` | 56 | 0 | 100%|
| `scarajectory/infrastructure/gui/console/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/console/panel.py` | 50 | 0 | 100%|
| `scarajectory/infrastructure/gui/controls/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/controls/assembly/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/controls/assembly/assembler.py` | 47 | 0 | 100%|
| `scarajectory/infrastructure/gui/controls/assembly/bundle.py` | 22 | 0 | 100%|
| `scarajectory/infrastructure/gui/controls/assembly/iassembler.py` | 17 | 0 | 100%|
| `scarajectory/infrastructure/gui/controls/bundle.py` | 50 | 0 | 100%|
| `scarajectory/infrastructure/gui/controls/controllers/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/controls/controllers/bundle.py` | 20 | 0 | 100%|
| `scarajectory/infrastructure/gui/controls/controllers/factory.py` | 28 | 0 | 100%|
| `scarajectory/infrastructure/gui/controls/factory.py` | 21 | 0 | 100%|
| `scarajectory/infrastructure/gui/controls/ipanel.py` | 15 | 0 | 100%|
| `scarajectory/infrastructure/gui/controls/panel.py` | 35 | 0 | 100%|
| `scarajectory/infrastructure/gui/dependencies.py` | 50 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/bundle.py` | 24 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/catalog/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/catalog/catalog.py` | 37 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/catalog/factory.py` | 24 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/catalog/icatalog.py` | 17 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/console/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/console/console.py` | 57 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/console/factory.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/console/iconsole.py` | 17 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/document/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/document/factory.py` | 19 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/document/imanager.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/document/manager.py` | 53 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/editor/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/editor/editor.py` | 46 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/editor/factory.py` | 23 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/editor/ieditor.py` | 17 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/factory.py` | 57 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/handler/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/handler/binary/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/handler/binary/bundle.py` | 36 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/handler/binary/factory.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/handler/binary/handler.py` | 71 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/handler/binary/idelegate.py` | 15 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/handler/execution/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/handler/execution/bundle.py` | 24 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/handler/execution/factory.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/handler/execution/handler.py` | 78 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/handler/execution/idelegate.py` | 17 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/handler/file/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/handler/file/bundle.py` | 22 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/handler/file/factory.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/handler/file/handler.py` | 49 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/handler/file/idelegate.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/itab.py` | 23 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/syntax/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/syntax/highlighter/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/syntax/highlighter/factory.py` | 24 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/syntax/highlighter/highlighter.py` | 29 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/syntax/highlighter/ihighlighter.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/syntax/tag/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/syntax/tag/applier.py` | 41 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/syntax/tag/factory.py` | 17 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/syntax/tag/iapplier.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/syntax/token.py` | 15 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/syntax/tokenizer/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/syntax/tokenizer/factory.py` | 17 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/syntax/tokenizer/itokenizer.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/syntax/tokenizer/tokenizer.py` | 68 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/tab.py` | 50 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/toolbar/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/toolbar/bundle.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/toolbar/factory.py` | 19 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/toolbar/itoolbar.py` | 17 | 0 | 100%|
| `scarajectory/infrastructure/gui/dsl/toolbar/toolbar.py` | 74 | 0 | 100%|
| `scarajectory/infrastructure/gui/editor/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/editor/applier/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/editor/applier/applier.py` | 36 | 0 | 100%|
| `scarajectory/infrastructure/gui/editor/applier/factory.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/gui/editor/applier/iapplier.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/gui/editor/applier/inputs.py` | 17 | 0 | 100%|
| `scarajectory/infrastructure/gui/editor/editor.py` | 73 | 0 | 100%|
| `scarajectory/infrastructure/gui/editor/factory.py` | 25 | 0 | 100%|
| `scarajectory/infrastructure/gui/editor/ieditor.py` | 17 | 0 | 100%|
| `scarajectory/infrastructure/gui/editor/table/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/editor/table/bundle.py` | 22 | 0 | 100%|
| `scarajectory/infrastructure/gui/editor/table/factory.py` | 26 | 0 | 100%|
| `scarajectory/infrastructure/gui/editor/table/itable.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/gui/editor/table/resize/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/editor/table/resize/factory.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/gui/editor/table/resize/handler.py` | 29 | 0 | 100%|
| `scarajectory/infrastructure/gui/editor/table/resize/ihandler.py` | 15 | 0 | 100%|
| `scarajectory/infrastructure/gui/editor/table/selection/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/editor/table/selection/factory.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/gui/editor/table/selection/handler.py` | 31 | 0 | 100%|
| `scarajectory/infrastructure/gui/editor/table/selection/ihandler.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/gui/editor/table/table.py` | 83 | 0 | 100%|
| `scarajectory/infrastructure/gui/emulator/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/emulator/launcher/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/emulator/launcher/factory.py` | 23 | 0 | 100%|
| `scarajectory/infrastructure/gui/emulator/launcher/ilauncher.py` | 15 | 0 | 100%|
| `scarajectory/infrastructure/gui/emulator/launcher/launcher.py` | 46 | 0 | 100%|
| `scarajectory/infrastructure/gui/emulator/locator/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/emulator/locator/factory.py` | 21 | 0 | 100%|
| `scarajectory/infrastructure/gui/emulator/locator/ilocator.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/gui/emulator/locator/locator.py` | 96 | 0 | 100%|
| `scarajectory/infrastructure/gui/factory.py` | 68 | 0 | 100%|
| `scarajectory/infrastructure/gui/gui.py` | 65 | 0 | 100%|
| `scarajectory/infrastructure/gui/igui.py` | 17 | 0 | 100%|
| `scarajectory/infrastructure/gui/layout/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/layout/builder.py` | 41 | 0 | 100%|
| `scarajectory/infrastructure/gui/layout/canvas/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/layout/canvas/builder.py` | 33 | 0 | 100%|
| `scarajectory/infrastructure/gui/layout/canvas/factory.py` | 19 | 0 | 100%|
| `scarajectory/infrastructure/gui/layout/canvas/ibuilder.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/gui/layout/editor/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/layout/editor/builder.py` | 42 | 0 | 100%|
| `scarajectory/infrastructure/gui/layout/editor/factory.py` | 19 | 0 | 100%|
| `scarajectory/infrastructure/gui/layout/editor/ibuilder.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/gui/layout/factory.py` | 26 | 0 | 100%|
| `scarajectory/infrastructure/gui/layout/toolbar/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/layout/toolbar/builder.py` | 28 | 0 | 100%|
| `scarajectory/infrastructure/gui/layout/toolbar/factory.py` | 19 | 0 | 100%|
| `scarajectory/infrastructure/gui/layout/toolbar/ibuilder.py` | 19 | 0 | 100%|
| `scarajectory/infrastructure/gui/manipulator/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/manipulator/jog/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/manipulator/jog/dependencies.py` | 22 | 0 | 100%|
| `scarajectory/infrastructure/gui/manipulator/jog/factory.py` | 31 | 0 | 100%|
| `scarajectory/infrastructure/gui/manipulator/jog/panel/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/manipulator/jog/panel/axis_grid.py` | 60 | 0 | 100%|
| `scarajectory/infrastructure/gui/manipulator/jog/panel/bundle.py` | 20 | 0 | 100%|
| `scarajectory/infrastructure/gui/manipulator/jog/panel/power.py` | 27 | 0 | 100%|
| `scarajectory/infrastructure/gui/manipulator/jog/panel/raw_command.py` | 36 | 0 | 100%|
| `scarajectory/infrastructure/gui/manipulator/jog/panel/tool.py` | 26 | 0 | 100%|
| `scarajectory/infrastructure/gui/manipulator/jog/tab.py` | 30 | 0 | 100%|
| `scarajectory/infrastructure/gui/manipulator/override/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/manipulator/override/actuator.py` | 32 | 0 | 100%|
| `scarajectory/infrastructure/gui/manipulator/override/feedrate.py` | 37 | 0 | 100%|
| `scarajectory/infrastructure/gui/manipulator/override/idelegate.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/gui/manipulator/override/panel.py` | 33 | 0 | 100%|
| `scarajectory/infrastructure/gui/menu/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/menu/builder/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/menu/builder/bundle.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/gui/menu/builder/factory.py` | 19 | 0 | 100%|
| `scarajectory/infrastructure/gui/menu/builder/hotkey.py` | 31 | 0 | 100%|
| `scarajectory/infrastructure/gui/menu/builder/ihotkey.py` | 17 | 0 | 100%|
| `scarajectory/infrastructure/gui/menu/builder/ilayout.py` | 17 | 0 | 100%|
| `scarajectory/infrastructure/gui/menu/builder/layout.py` | 46 | 0 | 100%|
| `scarajectory/infrastructure/gui/menu/bundle.py` | 36 | 0 | 100%|
| `scarajectory/infrastructure/gui/menu/dependencies.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/gui/menu/factory.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/gui/menu/imenu_bar.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/gui/menu/menu_bar.py` | 85 | 0 | 100%|
| `scarajectory/infrastructure/gui/model/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/model/canvas_settings.py` | 19 | 0 | 100%|
| `scarajectory/infrastructure/gui/model/canvas_tool_mode.py` | 17 | 0 | 100%|
| `scarajectory/infrastructure/gui/preview/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/preview/dependencies.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/gui/preview/factory.py` | 19 | 0 | 100%|
| `scarajectory/infrastructure/gui/preview/tab.py` | 34 | 0 | 100%|
| `scarajectory/infrastructure/gui/provides.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/gui/splash/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/splash/factory.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/gui/splash/iscreen.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/gui/splash/screen.py` | 63 | 0 | 100%|
| `scarajectory/infrastructure/gui/storage_dependencies.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/gui/streaming/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/streaming/bundle.py` | 26 | 0 | 100%|
| `scarajectory/infrastructure/gui/streaming/control/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/streaming/control/idelegate.py` | 15 | 0 | 100%|
| `scarajectory/infrastructure/gui/streaming/control/panel.py` | 21 | 0 | 100%|
| `scarajectory/infrastructure/gui/streaming/controllers_bundle.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/gui/streaming/factory.py` | 46 | 0 | 100%|
| `scarajectory/infrastructure/gui/streaming/observer/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/streaming/observer/bridge.py` | 23 | 0 | 100%|
| `scarajectory/infrastructure/gui/streaming/observer/factory.py` | 19 | 0 | 100%|
| `scarajectory/infrastructure/gui/streaming/observer/ibridge.py` | 15 | 0 | 100%|
| `scarajectory/infrastructure/gui/streaming/playback/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/streaming/playback/bundle.py` | 24 | 0 | 100%|
| `scarajectory/infrastructure/gui/streaming/playback/factory.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/gui/streaming/playback/handler.py` | 81 | 0 | 100%|
| `scarajectory/infrastructure/gui/streaming/progress/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/streaming/progress/adapter.py` | 35 | 0 | 100%|
| `scarajectory/infrastructure/gui/streaming/status/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/streaming/status/istatus_bar.py` | 15 | 0 | 100%|
| `scarajectory/infrastructure/gui/streaming/status/status_bar.py` | 30 | 0 | 100%|
| `scarajectory/infrastructure/gui/streaming/tab.py` | 32 | 0 | 100%|
| `scarajectory/infrastructure/gui/streaming/tool/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/streaming/tool/factory.py` | 19 | 0 | 100%|
| `scarajectory/infrastructure/gui/streaming/tool/handler.py` | 47 | 0 | 100%|
| `scarajectory/infrastructure/gui/theme/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/theme/manager.py` | 50 | 0 | 100%|
| `scarajectory/infrastructure/gui/toolbar/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/toolbar/bundle.py` | 24 | 0 | 100%|
| `scarajectory/infrastructure/gui/toolbar/factory.py` | 21 | 0 | 100%|
| `scarajectory/infrastructure/gui/toolbar/section/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/toolbar/section/assembler.py` | 32 | 0 | 100%|
| `scarajectory/infrastructure/gui/toolbar/section/bundle.py` | 20 | 0 | 100%|
| `scarajectory/infrastructure/gui/toolbar/section/iassembler.py` | 17 | 0 | 100%|
| `scarajectory/infrastructure/gui/toolbar/section/navigation.py` | 32 | 0 | 100%|
| `scarajectory/infrastructure/gui/toolbar/section/parameter.py` | 55 | 0 | 100%|
| `scarajectory/infrastructure/gui/toolbar/section/status.py` | 27 | 0 | 100%|
| `scarajectory/infrastructure/gui/toolbar/section/tool.py` | 33 | 0 | 100%|
| `scarajectory/infrastructure/gui/toolbar/toolbar.py` | 23 | 0 | 100%|
| `scarajectory/infrastructure/gui/validation/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/gui/validation/dependencies.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/gui/validation/factory.py` | 19 | 0 | 100%|
| `scarajectory/infrastructure/gui/validation/tab.py` | 49 | 0 | 100%|
| `scarajectory/infrastructure/manipulator/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/manipulator/dependencies.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/manipulator/factory.py` | 30 | 0 | 100%|
| `scarajectory/infrastructure/manipulator/jog/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/manipulator/jog/controller.py` | 29 | 0 | 100%|
| `scarajectory/infrastructure/manipulator/jog/dependencies.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/manipulator/jog/factory.py` | 24 | 0 | 100%|
| `scarajectory/infrastructure/manipulator/jog/provides.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/manipulator/motion/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/manipulator/motion/controller.py` | 34 | 0 | 100%|
| `scarajectory/infrastructure/manipulator/motion/dependencies.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/manipulator/motion/factory.py` | 24 | 0 | 100%|
| `scarajectory/infrastructure/manipulator/motion/provides.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/manipulator/provides.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/manipulator/query/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/manipulator/query/controller.py` | 28 | 0 | 100%|
| `scarajectory/infrastructure/manipulator/query/dependencies.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/manipulator/query/factory.py` | 24 | 0 | 100%|
| `scarajectory/infrastructure/manipulator/query/provides.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/pacing/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/pacing/controller/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/pacing/controller/controller.py` | 42 | 0 | 100%|
| `scarajectory/infrastructure/pacing/controller/dependencies.py` | 15 | 0 | 100%|
| `scarajectory/infrastructure/pacing/controller/factory.py` | 19 | 0 | 100%|
| `scarajectory/infrastructure/pacing/controller/icontroller.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/pacing/controller/provides.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/pacing/coordinator/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/pacing/coordinator/coordinator.py` | 23 | 0 | 100%|
| `scarajectory/infrastructure/pacing/coordinator/dependencies.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/pacing/coordinator/factory.py` | 20 | 0 | 100%|
| `scarajectory/infrastructure/pacing/coordinator/icoordinator.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/pacing/coordinator/provides.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/pacing/dependencies.py` | 15 | 0 | 100%|
| `scarajectory/infrastructure/pacing/factory.py` | 26 | 0 | 100%|
| `scarajectory/infrastructure/pacing/provides.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/packet/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/packet/dependencies.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/packet/factory.py` | 20 | 0 | 100%|
| `scarajectory/infrastructure/packet/istrategy.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/packet/provides.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/packet/strategy.py` | 43 | 0 | 100%|
| `scarajectory/infrastructure/preferences/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/preferences/dependencies.py` | 19 | 0 | 100%|
| `scarajectory/infrastructure/preferences/factory.py` | 22 | 0 | 100%|
| `scarajectory/infrastructure/preferences/provides.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/preferences/serial/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/preferences/serial/dependencies.py` | 19 | 0 | 100%|
| `scarajectory/infrastructure/preferences/serial/factory.py` | 20 | 0 | 100%|
| `scarajectory/infrastructure/preferences/serial/provides.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/preferences/serial/repository.py` | 58 | 0 | 100%|
| `scarajectory/infrastructure/scaralang/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/scaralang/avoidance/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/scaralang/avoidance/adapter.py` | 28 | 0 | 100%|
| `scarajectory/infrastructure/scaralang/avoidance/factory.py` | 23 | 0 | 100%|
| `scarajectory/infrastructure/scaralang/avoidance/iadapter.py` | 17 | 0 | 100%|
| `scarajectory/infrastructure/scaralang/boundary/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/scaralang/boundary/adapter.py` | 23 | 0 | 100%|
| `scarajectory/infrastructure/scaralang/boundary/factory.py` | 19 | 0 | 100%|
| `scarajectory/infrastructure/scaralang/boundary/iadapter.py` | 17 | 0 | 100%|
| `scarajectory/infrastructure/scaralang/dependencies.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/scaralang/discretizer/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/scaralang/discretizer/dependencies.py` | 22 | 0 | 100%|
| `scarajectory/infrastructure/scaralang/discretizer/discretizer.py` | 65 | 0 | 100%|
| `scarajectory/infrastructure/scaralang/discretizer/factory.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/scaralang/discretizer/provides.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/scaralang/factory.py` | 21 | 0 | 100%|
| `scarajectory/infrastructure/scaralang/provides.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/scaralang/shape/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/scaralang/shape/adapter.py` | 32 | 0 | 100%|
| `scarajectory/infrastructure/scaralang/shape/factory.py` | 27 | 0 | 100%|
| `scarajectory/infrastructure/scaralang/shape/iadapter.py` | 19 | 0 | 100%|
| `scarajectory/infrastructure/scaralang/validation/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/scaralang/validation/adapter.py` | 70 | 0 | 100%|
| `scarajectory/infrastructure/scaralang/validation/bounds_query_adapter.py` | 28 | 0 | 100%|
| `scarajectory/infrastructure/scaralang/validation/dependencies.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/scaralang/validation/factory.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/scaralang/validation/ibounds_query.py` | 22 | 0 | 100%|
| `scarajectory/infrastructure/settings/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/settings/bounds/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/settings/bounds/dependencies.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/settings/bounds/factory.py` | 25 | 0 | 100%|
| `scarajectory/infrastructure/settings/bounds/loader/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/settings/bounds/loader/dependencies.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/settings/bounds/loader/factory.py` | 20 | 0 | 100%|
| `scarajectory/infrastructure/settings/bounds/loader/iloader.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/settings/bounds/loader/loader.py` | 34 | 0 | 100%|
| `scarajectory/infrastructure/settings/bounds/loader/provides.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/settings/bounds/parser/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/settings/bounds/parser/factory.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/settings/bounds/parser/iparser.py` | 17 | 0 | 100%|
| `scarajectory/infrastructure/settings/bounds/parser/parser.py` | 24 | 0 | 100%|
| `scarajectory/infrastructure/settings/bounds/parser/provides.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/settings/bounds/provides.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/settings/communication/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/settings/communication/dependencies.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/settings/communication/factory.py` | 20 | 0 | 100%|
| `scarajectory/infrastructure/settings/communication/iloader.py` | 20 | 0 | 100%|
| `scarajectory/infrastructure/settings/communication/loader.py` | 61 | 0 | 100%|
| `scarajectory/infrastructure/settings/communication/provides.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/settings/dependencies.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/settings/factory.py` | 30 | 0 | 100%|
| `scarajectory/infrastructure/settings/provides.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/settings/reader/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/settings/reader/dependencies.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/settings/reader/factory.py` | 20 | 0 | 100%|
| `scarajectory/infrastructure/settings/reader/ireader.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/settings/reader/provides.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/settings/reader/reader.py` | 35 | 0 | 100%|
| `scarajectory/infrastructure/settings/transmission/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/settings/transmission/dependencies.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/settings/transmission/factory.py` | 20 | 0 | 100%|
| `scarajectory/infrastructure/settings/transmission/iloader.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/settings/transmission/loader.py` | 24 | 0 | 100%|
| `scarajectory/infrastructure/settings/transmission/provides.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/state/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/state/dependencies.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/state/factory.py` | 20 | 0 | 100%|
| `scarajectory/infrastructure/state/imachine.py` | 17 | 0 | 100%|
| `scarajectory/infrastructure/state/machine.py` | 24 | 0 | 100%|
| `scarajectory/infrastructure/state/provides.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/storage/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/storage/config_io/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/storage/config_io/dependencies.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/storage/config_io/factory.py` | 26 | 0 | 100%|
| `scarajectory/infrastructure/storage/config_io/loader/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/storage/config_io/loader/dependencies.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/storage/config_io/loader/factory.py` | 20 | 0 | 100%|
| `scarajectory/infrastructure/storage/config_io/loader/iloader.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/storage/config_io/loader/loader.py` | 34 | 0 | 100%|
| `scarajectory/infrastructure/storage/config_io/loader/provides.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/storage/config_io/provides.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/storage/config_io/storer/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/storage/config_io/storer/dependencies.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/storage/config_io/storer/factory.py` | 20 | 0 | 100%|
| `scarajectory/infrastructure/storage/config_io/storer/istorer.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/storage/config_io/storer/provides.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/storage/config_io/storer/storer.py` | 25 | 0 | 100%|
| `scarajectory/infrastructure/storage/dependencies.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/storage/factory.py` | 28 | 0 | 100%|
| `scarajectory/infrastructure/storage/plan/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/storage/plan/dependencies.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/storage/plan/factory.py` | 22 | 0 | 100%|
| `scarajectory/infrastructure/storage/plan/loader.py` | 32 | 0 | 100%|
| `scarajectory/infrastructure/storage/plan/provides.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/storage/plan/storer.py` | 34 | 0 | 100%|
| `scarajectory/infrastructure/storage/provides.py` | 22 | 0 | 100%|
| `scarajectory/infrastructure/storage/serializer/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/storage/serializer/iserializer.py` | 20 | 0 | 100%|
| `scarajectory/infrastructure/storage/serializer/serializer.py` | 40 | 0 | 100%|
| `scarajectory/infrastructure/storage/workspace/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/storage/workspace/config.py` | 17 | 0 | 100%|
| `scarajectory/infrastructure/storage/workspace/dependencies.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/storage/workspace/factory.py` | 20 | 0 | 100%|
| `scarajectory/infrastructure/storage/workspace/imanager.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/storage/workspace/manager.py` | 48 | 0 | 100%|
| `scarajectory/infrastructure/storage/workspace/provides.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/streaming/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/streaming/assembly/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/streaming/assembly/stream_pacing_assembler.py` | 22 | 0 | 100%|
| `scarajectory/infrastructure/streaming/assembly/stream_pipeline_assembler.py` | 55 | 0 | 100%|
| `scarajectory/infrastructure/streaming/assembly/stream_transport_assembler.py` | 30 | 0 | 100%|
| `scarajectory/infrastructure/streaming/assembly/stream_worker_assembler.py` | 67 | 0 | 100%|
| `scarajectory/infrastructure/streaming/assembly/worker_bundle.py` | 23 | 0 | 100%|
| `scarajectory/infrastructure/streaming/binary/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/streaming/binary/dependencies.py` | 22 | 0 | 100%|
| `scarajectory/infrastructure/streaming/binary/factory.py` | 20 | 0 | 100%|
| `scarajectory/infrastructure/streaming/binary/istreamer.py` | 15 | 0 | 100%|
| `scarajectory/infrastructure/streaming/binary/provides.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/streaming/binary/streamer.py` | 49 | 0 | 100%|
| `scarajectory/infrastructure/streaming/control/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/streaming/control/dependencies.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/streaming/control/factory.py` | 20 | 0 | 100%|
| `scarajectory/infrastructure/streaming/control/provides.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/streaming/control/transmitter.py` | 35 | 0 | 100%|
| `scarajectory/infrastructure/streaming/dependencies.py` | 15 | 0 | 100%|
| `scarajectory/infrastructure/streaming/factory.py` | 19 | 0 | 100%|
| `scarajectory/infrastructure/streaming/observer/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/streaming/observer/dispatcher.py` | 35 | 0 | 100%|
| `scarajectory/infrastructure/streaming/observer/factory.py` | 21 | 0 | 100%|
| `scarajectory/infrastructure/streaming/observer/provides.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/streaming/observer/registry.py` | 24 | 0 | 100%|
| `scarajectory/infrastructure/streaming/playback/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/streaming/playback/controller.py` | 70 | 0 | 100%|
| `scarajectory/infrastructure/streaming/playback/dependencies.py` | 24 | 0 | 100%|
| `scarajectory/infrastructure/streaming/playback/factory.py` | 20 | 0 | 100%|
| `scarajectory/infrastructure/streaming/playback/provides.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/streaming/provides.py` | 24 | 0 | 100%|
| `scarajectory/infrastructure/tool/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/tool/controller/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/tool/controller/controller.py` | 41 | 0 | 100%|
| `scarajectory/infrastructure/tool/controller/dependencies.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/tool/controller/factory.py` | 20 | 0 | 100%|
| `scarajectory/infrastructure/tool/controller/provides.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/tool/dependencies.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/tool/factory.py` | 29 | 0 | 100%|
| `scarajectory/infrastructure/tool/provides.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/tool/worker/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/tool/worker/factory.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/tool/worker/irunner.py` | 15 | 0 | 100%|
| `scarajectory/infrastructure/tool/worker/provides.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/tool/worker/runner.py` | 21 | 0 | 100%|
| `scarajectory/infrastructure/tool/worker/worker.py` | 23 | 0 | 100%|
| `scarajectory/infrastructure/worker/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/worker/dependencies.py` | 26 | 0 | 100%|
| `scarajectory/infrastructure/worker/dispatcher/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/worker/dispatcher/bundle.py` | 22 | 0 | 100%|
| `scarajectory/infrastructure/worker/dispatcher/dispatcher.py` | 32 | 0 | 100%|
| `scarajectory/infrastructure/worker/dispatcher/factory.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/worker/dispatcher/idispatcher.py` | 17 | 0 | 100%|
| `scarajectory/infrastructure/worker/drainer/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/worker/drainer/dependencies.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/worker/drainer/drainer.py` | 37 | 0 | 100%|
| `scarajectory/infrastructure/worker/drainer/factory.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/worker/drainer/idrainer.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/worker/execution/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/worker/execution/dependencies.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/worker/execution/factory.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/worker/execution/worker.py` | 35 | 0 | 100%|
| `scarajectory/infrastructure/worker/factory.py` | 39 | 0 | 100%|
| `scarajectory/infrastructure/worker/handler/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/worker/handler/dependencies.py` | 20 | 0 | 100%|
| `scarajectory/infrastructure/worker/handler/factory.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/worker/handler/handler.py` | 59 | 0 | 100%|
| `scarajectory/infrastructure/worker/handler/ihandler.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/worker/holder.py` | 14 | 0 | 100%|
| `scarajectory/infrastructure/worker/iexecution_worker.py` | 19 | 0 | 100%|
| `scarajectory/infrastructure/worker/parser/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/worker/parser/bundle.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/worker/provides.py` | 16 | 0 | 100%|
| `scarajectory/infrastructure/worker/receiver/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/worker/receiver/dependencies.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/worker/receiver/factory.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/worker/receiver/receiver.py` | 27 | 0 | 100%|
| `scarajectory/infrastructure/worker/runner/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/worker/runner/bundle.py` | 26 | 0 | 100%|
| `scarajectory/infrastructure/worker/runner/factory.py` | 35 | 0 | 100%|
| `scarajectory/infrastructure/worker/runner/irunner.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/worker/runner/loop_bundle.py` | 22 | 0 | 100%|
| `scarajectory/infrastructure/worker/runner/runner.py` | 53 | 0 | 100%|
| `scarajectory/infrastructure/worker/thread/__init__.py` | 9 | 0 | 100%|
| `scarajectory/infrastructure/worker/thread/coordinator.py` | 45 | 0 | 100%|
| `scarajectory/infrastructure/worker/thread/factory.py` | 18 | 0 | 100%|
| `scarajectory/infrastructure/worker/thread/icoordinator.py` | 17 | 0 | 100%|
| `scarajectory/setup/__init__.py` | 9 | 0 | 100%|
| `scarajectory/setup/assembly/__init__.py` | 9 | 0 | 100%|
| `scarajectory/setup/assembly/core/__init__.py` | 9 | 0 | 100%|
| `scarajectory/setup/assembly/core/assembler.py` | 46 | 0 | 100%|
| `scarajectory/setup/assembly/core/bundle.py` | 26 | 0 | 100%|
| `scarajectory/setup/assembly/dsl/__init__.py` | 9 | 0 | 100%|
| `scarajectory/setup/assembly/dsl/assembler.py` | 47 | 0 | 100%|
| `scarajectory/setup/assembly/dsl/bundle.py` | 24 | 0 | 100%|
| `scarajectory/setup/assembly/dsl/diagnostic_bundle.py` | 22 | 0 | 100%|
| `scarajectory/setup/assembly/plan/__init__.py` | 9 | 0 | 100%|
| `scarajectory/setup/assembly/plan/assembler.py` | 51 | 0 | 100%|
| `scarajectory/setup/assembly/plan/bundle.py` | 27 | 0 | 100%|
| `scarajectory/setup/assembly/presentation/__init__.py` | 9 | 0 | 100%|
| `scarajectory/setup/assembly/presentation/assembler.py` | 45 | 0 | 100%|
| `scarajectory/setup/assembly/runtime/__init__.py` | 9 | 0 | 100%|
| `scarajectory/setup/assembly/runtime/assembler.py` | 48 | 0 | 100%|
| `scarajectory/setup/assembly/runtime/bundle.py` | 28 | 0 | 100%|
| `scarajectory/setup/bundle.py` | 23 | 0 | 100%|
| `scarajectory/setup/dep_validator.py` | 36 | 0 | 100%|
| `scarajectory/setup/dependencies.py` | 19 | 0 | 100%|
| `scarajectory/setup/factory.py` | 76 | 0 | 100%|
| `scarajectory/setup/keys.py` | 35 | 0 | 100%|
| `scarajectory/setup/opt_validator.py` | 36 | 0 | 100%|
| `scarajectory/setup/options.py` | 20 | 0 | 100%|
| `scarajectory/setup/registry.py` | 33 | 0 | 100%|
| `scarajectory/setup/validator.py` | 48 | 0 | 100%|
| **Total** | 16252 | 0 | 100% |

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
3. **Program Preview**:
   * Inspect the exported SCARA DSL trajectory program under the **Program Preview** tab.
4. **Hardware Streaming & Execution**:
   * Connect to `/dev/ttyACM0` (or TCP host) under the **Hardware Streamer** tab.
   * Trigger streaming to execute real-time motion on the physical SCARA robot.
5. **Manual Jogging & Diagnostics**:
   * Use the **Manual Jog** tab for directional jog movements, vacuum pump activation, release valve triggers, and homing.

##### 🤖 Digital Twin Integration with SCARAEmu

**scarajectory** seamlessly integrates with **[scaraemu](https://github.com/vroncevic/scaraemu)** as a software-in-the-loop (SITL) Digital Twin. This allows you to visually simulate, animate, and validate trajectories and `.scara` DSL programs in 2D/3D before deploying to physical hardware.

###### Mode 1: One-Click Simulation from DSL Editor
1. In **scarajectory**, open the **SCARA DSL Editor** tab.
2. Write or load any `.scara` program (or select from bundled examples in `~/.scarajectory/workspace/` via the **Examples** dropdown).
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
   * Trajectory waypoints stream live as binary protocol frames over the loopback TCP socket.
   * **scaraemu** smoothly animates the dual-link arm and carriage along the path.
   * Closed-loop protocol acknowledgments flow back to **scarajectory**, dynamically driving the streaming progress bar.

###### Mode 3: Direct File Loading in SCARAEmu
* Open **scaraemu** and navigate to the **Trajectories** tab.
* In the **SCARA DSL Script** dropdown, select any of the 50 bundled programs from the user workspace (e.g. `12_industrial_pick_place.scara`, `04_circular_arc.scara`, `09_pallet_matrix.scara`).
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
