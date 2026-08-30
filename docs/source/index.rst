SCARA Motion Trajectory Studio & Streamer
-----------------------------------------

**scarajectory** is a standalone CAD/CAM motion planning, kinematic validation, and real-time trajectory streaming software for SCARA robotic manipulators.

Developed in `python <https://www.python.org/>`_ code.

The README is used to introduce the tool and provide instructions on
how to install the tool, any machine dependencies it may have and any
other information that should be provided before the tool is installed.

|scarajectory python checker| |scarajectory python package| |scarajectory interface checker| |scarajectory isp checker| |scarajectory srp checker| |gplv3 license| |apache license| |python version| |github issues| |documentation status| |github contributors|

.. |scarajectory python checker| image:: https://github.com/vroncevic/scarajectory/actions/workflows/scarajectory_python_checker.yml/badge.svg
   :target: https://github.com/vroncevic/scarajectory/actions/workflows/scarajectory_python_checker.yml

.. |scarajectory python package| image:: https://github.com/vroncevic/scarajectory/actions/workflows/scarajectory_package_checker.yml/badge.svg
   :target: https://github.com/vroncevic/scarajectory/actions/workflows/scarajectory_package.yml

.. |scarajectory interface checker| image:: https://github.com/vroncevic/scarajectory/actions/workflows/scarajectory_interface_checker.yml/badge.svg
   :target: https://github.com/vroncevic/scarajectory/actions/workflows/scarajectory_interface_checker.yml

.. |scarajectory isp checker| image:: https://github.com/vroncevic/scarajectory/actions/workflows/scarajectory_isp_checker.yml/badge.svg
   :target: https://github.com/vroncevic/scarajectory/actions/workflows/scarajectory_isp_checker.yml

.. |scarajectory srp checker| image:: https://github.com/vroncevic/scarajectory/actions/workflows/scarajectory_srp_checker.yml/badge.svg
   :target: https://github.com/vroncevic/scarajectory/actions/workflows/scarajectory_srp_checker.yml

.. |gplv3 license| image:: https://img.shields.io/badge/License-GPLv3-blue.svg
   :target: https://www.gnu.org/licenses/gpl-3.0

.. |apache license| image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
   :target: https://opensource.org/licenses/Apache-2.0

.. |python version| image:: https://img.shields.io/badge/python-3.10+-blue.svg
   :target: https://www.python.org/downloads/

.. |github issues| image:: https://img.shields.io/github/issues/vroncevic/scarajectory.svg
   :target: https://github.com/vroncevic/scarajectory/issues

.. |github contributors| image:: https://img.shields.io/github/contributors/vroncevic/scarajectory.svg
   :target: https://github.com/vroncevic/scarajectory/graphs/contributors

.. |documentation status| image:: https://readthedocs.org/projects/scarajectory/badge/?version=latest
   :target: https://scarajectory.readthedocs.io/en/latest/?badge=latest

.. toctree::
   :maxdepth: 4
   :caption: Contents

   self
   modules

🚀 Installation
---------------

|scarajectory python3 build|

.. |scarajectory python3 build| image:: https://github.com/vroncevic/scarajectory/actions/workflows/scarajectory_python3_build.yml/badge.svg
   :target: https://github.com/vroncevic/scarajectory/actions/workflows/scarajectory_python3_build.yml

Navigate to release `page`_ download and extract release archive.

.. _page: https://github.com/vroncevic/scarajectory/releases

To install **scarajectory** type the following

.. code-block:: bash

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

You can use Docker to create image/container, or You can use pip to install

.. code-block:: bash

    # python3
    pip3 install scarajectory

📦 Dependencies
---------------

**scarajectory** requires next modules and libraries

* `ats-utilities - Python App/Tool/Script Utilities <https://pypi.org/project/ats-utilities/>`_ |ats gplv3| |ats apache|
* `pyserial - Python Serial Port Extension <https://pypi.org/project/pyserial/>`_ |pyserial bsd|

.. |ats gplv3| image:: https://img.shields.io/badge/License-GPLv3-blue.svg
   :target: https://www.gnu.org/licenses/gpl-3.0

.. |ats apache| image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
   :target: https://opensource.org/licenses/Apache-2.0

.. |pyserial bsd| image:: https://img.shields.io/badge/License-BSD_3--Clause-blue.svg
   :target: https://opensource.org/licenses/BSD-3-Clause

📁 Tool structure
-----------------

**scarajectory** is based on OOP and Clean Architecture.

Tool structure

.. code-block:: bash

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

✨ Features
-----------

* **Interactive Vector CAD Editor**: Real-time vector drafting with dedicated Point, Line, Rectangle, Circle, and Freehand tools with live vertex dragging and viewport zoom/pan.
* **Kinematic Reachability & Deadzone Enforcement**: Annular geometric validation ensuring trajectories stay within reachable workspace boundaries (:math:`R_{min} = |L_1 - L_2|`, :math:`R_{max} = L_1 + L_2`).
* **Undo / Redo Transaction Stack**: Non-destructive history management for waypoint additions, modifications, insertions, and deletions (``Ctrl+Z``, ``Ctrl+Y``).
* **ASCII Protocol Generation**: Generates micro-command streaming packets for RP2040 firmware (``<pt#X#Y#Z#PHI#SPEED#end>``).
* **Sliding Window Hardware Streaming**: Multi-threaded USB serial (``/dev/ttyACM0``) and TCP socket streaming with dynamic ACK tracking, auto-pause on buffer full, and progress monitoring.
* **Manual Jogging & Diagnostics**: Interactive jog grid (X, Y, Z, Phi), vacuum pump and release valve toggles, homing, status queries, and raw serial command console.
* **Configurable Kinematics & Dimensions**: Dynamic robot link lengths (:math:`L_1, L_2`), stroke limits (:math:`Z_{min}, Z_{max}`), and speed bounds configurable via CLI options and JSON schema.
* **Strict Quality & SOLID Standards**: 100% protocol conformity, zero ISP/SRP violations, 81% test coverage, and 10.00 / 10.00 Pylint score.

📐 SCARA Kinematic & Geometric Configuration
--------------------------------------------

The robot dimensions and physical boundaries can be customized in ``scara_geometry.json`` or injected programmatically:

.. list-table:: Kinematic Limits
   :widths: 20 20 60
   :header-rows: 1

   * - Parameter
     - Default Value
     - Description
   * - **l1**
     - ``150.0 mm``
     - Primary arm link length (shoulder to elbow).
   * - **l2**
     - ``120.0 mm``
     - Secondary arm link length (elbow to wrist).
   * - **r_min**
     - ``30.0 mm``
     - Inner singular deadzone radius (:math:`|L_1 - L_2|`).
   * - **r_max**
     - ``270.0 mm``
     - Maximum horizontal reach boundary (:math:`L_1 + L_2`).
   * - **z_min**
     - ``0.0 mm``
     - Minimum vertical height limit (bed level).
   * - **z_max**
     - ``100.0 mm``
     - Maximum vertical stroke limit.
   * - **min_speed**
     - ``1.0 mm/s``
     - Minimum allowable feedrate speed.
   * - **max_speed**
     - ``100.0 mm/s``
     - Maximum allowable safe feedrate speed.

📊 Code coverage
----------------

.. csv-table:: Code coverage
   :file: coverage_table.csv
   :widths: 60, 10, 10, 20
   :header-rows: 1

🛠 Usage
--------

Install package

.. code-block:: bash

    pip3 install scarajectory

Prepare main entry point by downloading `main.py` or create your own.

.. code-block:: bash

    wget -O main.py https://raw.githubusercontent.com/vroncevic/scarajectory/main/main.py

CLI Command Options
^^^^^^^^^^^^^^^^^^^

Launch the graphical studio with default configuration:

.. code-block:: bash

    python3 main.py studio

Launch with initial trajectory plan file and disabled deadzone restriction:

.. code-block:: bash

    python3 main.py studio --file ./trajectories/rectangle_demo.json --dead-zone disable --verbose enable

.. list-table:: Studio CLI Options
   :widths: 20 15 25 40
   :header-rows: 1

   * - Option
     - Type
     - Choices
     - Description
   * - **--file**
     - ``str``
     - *File path*
     - Path to initial trajectory JSON plan file to load on startup.
   * - **--dead-zone**
     - ``str``
     - ``enable``, ``disable``
     - Enable or disable inner deadzone geometric validation (:math:`R_{min}`).
   * - **--verbose**
     - ``str``
     - ``enable``, ``disable``
     - Enable or disable verbose ATS operational logging.

Interactive Motion Planning Workflow
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. **Design Trajectory & Geometry**:
   * Use **Point**, **Line**, **Rectangle**, **Circle**, or **Freehand** tools directly on the interactive vector canvas.
   * Fine-tune Cartesian parameters (:math:`X, Y, Z, \phi, \text{speed}`) using the Waypoint Data Table or interactive vertex drag.
2. **Kinematic Validation**:
   * Open the **Plan Validation** tab and run validation against reachability limits (:math:`L_1 = 150\text{ mm}, L_2 = 120\text{ mm}`).
   * Verify total path length and estimated execution time.
3. **ASCII Program Preview**:
   * Inspect the formatted ASCII micro-command stream (``<pt#...#end>``) under the **Program Preview** tab.
4. **Hardware Streaming & Execution**:
   * Connect to ``/dev/ttyACM0`` (or TCP host) under the **Hardware Streamer** tab.
   * Trigger streaming to execute real-time motion on the physical SCARA robot.
5. **Manual Jogging & Diagnostics**:
   * Use the **Manual Jog** tab for directional jog movements, vacuum pump activation, release valve triggers, and homing.

📚 Docs
-------

More documentation and info at

* `scarajectory.readthedocs.io <https://scarajectory.readthedocs.io>`_
* `www.python.org <https://www.python.org/>`_

👥 Contributing
---------------

`Contributing to scarajectory <https://github.com/vroncevic/scarajectory/blob/dev/CONTRIBUTING.md>`_

📄 Copyright and licence
-------------------------

Copyright (C) 2026 by `vroncevic.github.io/scarajectory <https://vroncevic.github.io/scarajectory>`_

**scarajectory** is free software; you can redistribute it and/or modify
it under the same terms as Python itself, either Python version 3.x or,
at your option, any later version of Python 3 you may have available.

Special thanks to **Google** and the Google developer ecosystem for their tremendous support and innovative tools from the Google bundle that empowered the development and realization of this project. *Google, you make this world a better place!* 🌍✨

Lets help and support PSF.

|python software foundation|

.. |python software foundation| image:: https://raw.githubusercontent.com/vroncevic/scarajectory/dev/docs/psf-logo-alpha.png
   :target: https://www.python.org/psf/

|donate|

.. |donate| image:: https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif
   :target: https://www.python.org/psf/donations/
