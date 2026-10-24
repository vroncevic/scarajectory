.. image:: https://raw.githubusercontent.com/vroncevic/scarajectory/dev/docs/scarajectory_logo.png
   :align: right
   :width: 25%

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

.. image:: https://raw.githubusercontent.com/vroncevic/scarajectory/dev/docs/scarajectory_in_progress.png
   :alt: SCARA Trajectory Studio in Progress
   :align: center
   :width: 100%

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
* `scaralang - SCARA Domain-Specific Language, Kinematics & Protocol Engine <https://github.com/vroncevic/scaralang>`_ |scaralang gplv3|

.. |ats gplv3| image:: https://img.shields.io/badge/License-GPLv3-blue.svg
   :target: https://www.gnu.org/licenses/gpl-3.0

.. |ats apache| image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
   :target: https://opensource.org/licenses/Apache-2.0

.. |pyserial bsd| image:: https://img.shields.io/badge/License-BSD_3--Clause-blue.svg
   :target: https://opensource.org/licenses/BSD-3-Clause

.. |scaralang gplv3| image:: https://img.shields.io/badge/License-GPLv3-blue.svg
   :target: https://www.gnu.org/licenses/gpl-3.0

.. note::
   **Core Robotics & Language Engine Dependency (scaralang):** `scarajectory` directly integrates `scaralang <https://github.com/vroncevic/scaralang>`_ as its foundational domain dependency. `scaralang` provides the SCARA Domain-Specific Language (DSL) lexer, parser, and AST compiler, the analytical forward and inverse kinematics engine (``solve_fk``, ``solve_ik``), trajectory reachability and feedrate boundary validation, and the low-level binary wire framing protocol codecs.

📁 Tool structure
-----------------

**scarajectory** is based on OOP and Clean Architecture.

Tool structure

.. code-block:: bash

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
     - ``86.08 mm``
     - Minimum reach radius limit (governed by mechanical joint :math:`J_2 \le 145^\circ` limit; theoretical :math:`|L_1 - L_2| = 30.0\text{ mm}`).
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

📜 SCARA Domain-Specific Language (DSL) & .scara Programs
---------------------------------------------------------

**scarajectory** includes a dedicated, industrial-grade Domain-Specific Language designed specifically for SCARA robotic manipulators. Programs are written in plain text files with the ``.scara`` extension and compiled into validated Cartesian trajectories via a clean AST pipeline:

.. code-block:: text

                    ┌─────────────────────────┐
                    │      .scara Source      │
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

SCARA DSL Instruction Reference
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table:: SCARA DSL Instruction Reference
   :widths: 15 35 25 35
   :header-rows: 1

   * - Category
     - Instruction & Syntax
     - Parameters
     - Description
   * - **Motion**
     - ``MOVE_J X <x> Y <y> Z <z> [P <phi>]``
     - ``X, Y, Z`` (mm), ``P`` (deg)
     - Rapid Cartesian point-to-point motion.
   * - 
     - ``MOVE_L X <x> Y <y> Z <z> [P <phi>]``
     - ``X, Y, Z`` (mm), ``P`` (deg)
     - Linear interpolated Cartesian path.
   * - 
     - ``ARC_CW X <x> Y <y> I <i> J <j> [Z <z>]``
     - ``X, Y`` target, ``I, J`` center offset
     - Clockwise circular arc interpolation.
   * - 
     - ``ARC_CCW X <x> Y <y> I <i> J <j> [Z <z>]``
     - ``X, Y`` target, ``I, J`` center offset
     - Counter-clockwise circular arc interpolation.
   * - 
     - ``APPROACH DIST <d>``
     - ``DIST`` (mm)
     - Vertical descent towards workpiece along Z.
   * - 
     - ``RETRACT DIST <d>``
     - ``DIST`` (mm)
     - Vertical clearance ascent along Z.
   * - **Macros**
     - ``JUMP X <x> Y <y> Z <z> [ARCH <h>]``
     - ``X, Y, Z``, ``ARCH`` apex clearance
     - Smooth 3D parabolic pick-and-place arch motion.
   * - 
     - ``PALLET ROWS <r> COLS <c> DX <dx> DY <dy>``
     - Grid dimensions & spacing
     - Generates structured 2D Cartesian pallet matrix.
   * - 
     - ``TANGENT_ARC RADIUS <r> ANGLE <a>``
     - ``RADIUS`` (mm), ``ANGLE`` (deg)
     - Smooth tangential curve blending into path.
   * - **Actuators**
     - ``PUMP <ON|OFF>``
     - ``ON`` or ``OFF``
     - Actuates end-effector vacuum pump.
   * - 
     - ``VALVE <ON|OFF>``
     - ``ON`` or ``OFF``
     - Opens or closes pneumatic release blow-off valve.
   * - 
     - ``WAIT <ms>``
     - ``ms`` (milliseconds)
     - Dwells execution for specified hardware duration.
   * - 
     - ``HOME``
     - None
     - Triggers complete multi-axis homing routine.
   * - **Dynamics**
     - ``SPEED <RAPID|WORK> <val>``
     - ``RAPID`` or ``WORK``, feedrate (mm/s)
     - Configures travel or working linear feedrate.
   * - 
     - ``ACCEL <val>``
     - ``val`` (mm/s²)
     - Configures linear path acceleration limit.
   * - 
     - ``OVERRIDE <percent>``
     - ``percent`` (10% - 200%)
     - Scales path execution velocity dynamically.
   * - 
     - ``ZONE <OFF|FINE|Z1..Z50>``
     - Corner rounding tolerance
     - Corner tolerance zone for trajectory smoothing.
   * - **Config**
     - ``CONFIG ELBOW <LEFT|RIGHT>``
     - ``LEFT`` or ``RIGHT``
     - Sets arm kinematic inverse solution branch.
   * - 
     - ``FRAME X <x> Y <y> Z <z> [PHI <p>]``
     - Cartesian offset coordinates
     - Defines user workpiece reference coordinate frame.
   * - 
     - ``PROBE AXIS <Z> FEED <f>``
     - Axis identifier, search feedrate
     - Probes touch switch / surface sensor.

Example .scara Program: Industrial Pick & Place
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

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

Bundled Industrial .scara Demonstration Programs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**scarajectory** includes a comprehensive suite of 50 industrial-grade ``.scara`` demonstration programs showcasing the full capabilities of the DSL syntax, kinematics, trajectory smoothing, and pneumatic tool sequencing:

.. list-table:: Bundled Industrial Demonstration Programs
   :widths: 22 20 28 40
   :header-rows: 1

   * - File Name
     - Functional Category
     - Primary DSL Instructions
     - Description
   * - **01_homing.scara**
     - Calibration & Safety
     - ``ENABLE``, ``HOME``
     - Coordinated multi-axis homing sequence (Z limit switch, J2 elbow, J1 shoulder) and zero-reference calibration.
   * - **02_linear_motion.scara**
     - Cartesian Interpolation
     - ``SPEED WORK/RAPID``, ``MOVE_L``
     - Continuous linear interpolated path between Cartesian coordinates with configurable working and rapid feedrates.
   * - **03_joint_rapid.scara**
     - Rapid Transit
     - ``MOVE_J``
     - High-speed joint-interpolated transit across workspace quadrants, prioritizing transition speed over straight-line paths.
   * - **04_circular_arc.scara**
     - Planar Contouring
     - ``ARC_CW``, ``ARC_CCW``
     - Clockwise and counter-clockwise circular arc interpolation using relative center offsets (``I``, ``J``).
   * - **05_jump_arch.scara**
     - 3D Pick & Place
     - ``JUMP``, ``ARCH``
     - Parabolic 3D clearance arch: vertical ascent, horizontal transit, and descent with configurable clearance height.
   * - **06_pneumatics.scara**
     - Actuator Sequencing
     - ``PUMP ON/OFF``, ``VALVE ON/OFF``, ``WAIT_MS``
     - Pneumatic vacuum pump and blow-off valve actuation with safety interlocks preventing simultaneous engagement.
   * - **07_approach_retract.scara**
     - Z-Axis Tooling
     - ``APPROACH DIST``, ``RETRACT DIST``
     - Relative descent to workpiece at controlled creep speed and fast clearance ascent along the Z-axis.
   * - **08_work_frames.scara**
     - Coordinate Systems
     - ``FRAME_SET``, ``FRAME_RESET``
     - User Work Coordinate System (WCS) shifting and rotated reference systems for inclined assembly stations.
   * - **09_pallet_matrix.scara**
     - Parametric Palletizing
     - ``PALLET_DEF``, ``MOVE_PALLET``
     - 2D pallet grid matrix indexing by row, column, pitch (``DX``, ``DY``), and zero-based cell index.
   * - **10_tangent_orientation.scara**
     - 4th-Axis Tool Control
     - ``TOOL_ORIENT TANGENTIAL/FIXED``
     - Automatic continuous rotation of the 4th axis (:math:`\Phi`) tangential to trajectory heading (knife cutting, dispensing).
   * - **11_zone_blending.scara**
     - Trajectory Smoothing
     - ``ZONE BLEND``, ``ZONE FINE``
     - Continuous curvature trajectory blending and corner rounding radius for high-speed continuous motion.
   * - **12_industrial_pick_place.scara**
     - Full Automation Cycle
     - ``FRAME_SET``, ``MOVE_J``, ``ZONE BLEND``, ``PUMP``, ``VALVE``, ``RETRACT``
     - Comprehensive production pick-and-place cycle combining homing, frames, blended transit, vacuum grip, and blow-off release.
   * - **13_elbow_reconfiguration.scara**
     - Arm Pose Configuration
     - ``CONFIG_ELBOW LEFT/RIGHT``
     - Dynamic arm posture reconfiguration between Righty and Lefty configurations through intermediate workspace transit.
   * - **14_singularity_avoidance.scara**
     - Kinematic Boundary Avoidance
     - ``SPEED WORK``, ``MOVE_L``
     - Central singular dead zone bypass detour routing end-effector around unreachable central boundary.
   * - **15_boundary_reach_limits.scara**
     - Reach Envelope Inspection
     - ``MOVE_L``, ``WAIT_MS``
     - Safe perimeter scanning near maximum reach envelope avoiding outer singular deadband.
   * - **16_multi_frame_palletizing.scara**
     - Multi-WCS Palletizing
     - ``FRAME_SET``, ``PALLET_DEF``, ``MOVE_PALLET``, ``PUMP``, ``VALVE``
     - Multi-station pick-and-place material handling combining user frames, pallet matrix traversal, and pneumatic grip.
   * - **17_bidirectional_elbow_assembly.scara**
     - Bidirectional Reconfiguration
     - ``CONFIG_ELBOW``, ``MOVE_L``, ``PUMP``, ``VALVE``
     - Bidirectional elbow reconfiguration cycle (RIGHT -> LEFT -> RIGHT) accessing rear assembly slot and returning to front cradle.
   * - **18_tangential_contour_dispensing.scara**
     - Tangential Dispensing
     - ``TOOL_ORIENT TANGENTIAL``, ``ZONE BLEND``, ``ARC_CW``, ``VALVE``
     - Continuous fluid dispensing along composite linear and circular arc contours with dynamic tangential nozzle orientation.
   * - **19_high_speed_sorter_jump.scara**
     - Quality Sorter Cell
     - ``JUMP``, ``ACCEL``, ``OVERRIDE``, ``PUMP``, ``VALVE``
     - High-speed multi-bin sorting sequence using parabolic jump arches, dynamic acceleration scaling, and speed overrides.
   * - **20_annular_inspection_scan.scara**
     - Annular Quality Inspection
     - ``ARC_CCW``, ``ARC_CW``, ``MOVE_L``, ``WAIT_MS``
     - Multi-level concentric circular inspection scanning clear of inner deadzone and outer boundary singularities.
   * - **21_relative_motion_incremental.scara**
     - Incremental Positioning
     - ``MOVE_REL``, ``WAIT_MS``
     - Incremental workpiece positioning using relative Cartesian offsets along X, Y, and Z.
   * - **22_conveyor_tracking_relative.scara**
     - Conveyor Tracking
     - ``MOVE_REL``, ``APPROACH``, ``RETRACT``
     - Dynamic conveyor tracking and pick sequence using relative motions coordinated with line speed.
   * - **23_bidirectional_arc_contour.scara**
     - S-Curve Contouring
     - ``ARC_CW``, ``ARC_CCW``, ``TOOL_ORIENT``
     - Continuous S-shaped contour combining bidirectional circular arcs with dynamic tangential orientation.
   * - **24_matrix_pallet_depalletizing.scara**
     - Dual-Pallet Transfer
     - ``PALLET_DEF``, ``MOVE_PALLET``, ``PUMP``, ``VALVE``
     - Automated material transfer between dual matrix pallets (infeed to outfeed) with vacuum grip.
   * - **25_stepper_motor_calibration.scara**
     - Stepper Calibration
     - ``CONFIG_MOTOR``, ``MOVE_J``, ``WAIT_MS``
     - Dynamic motor drive mode reconfiguration switching between open-loop and closed-loop actuation.
   * - **26_multi_zone_high_speed_blending.scara**
     - Multi-Tier Blending
     - ``ZONE BLEND``, ``SPEED WORK``, ``MOVE_L``
     - Multi-tier corner zone blending profiles evaluating trajectory continuous curvature smoothing.
   * - **27_emergency_hold_recovery.scara**
     - Safety & Interlocks
     - ``HOLD``, ``RESUME``, ``MOVE_L``
     - Feed hold, dwell, and resume motion execution state management and recovery routines.
   * - **28_three_frame_assembly_station.scara**
     - Multi-WCS Stations
     - ``FRAME_SET``, ``FRAME_RESET``, ``MOVE_L``
     - Assembly sequence traversing three distinct user work coordinate frames (assembly, inspection, packaging).
   * - **29_precision_dispensing_tangent.scara**
     - Precision Dispensing
     - ``TOOL_ORIENT TANGENTIAL``, ``MOVE_L``, ``ARC_CW``
     - Continuous fluid gasket dispensing path around closed boundary with dynamic tangential nozzle tracking.
   * - **30_complex_automation_workcell.scara**
     - Full Workcell Routine
     - ``CONFIG_ELBOW``, ``FRAME_SET``, ``PALLET_DEF``, ``JUMP``
     - Comprehensive industrial workcell routine combining all core motion primitives, frames, and pallets.
   * - **31_subroutine_pick_place.scara**
     - Modular Subroutines
     - ``DEF``, ``CALL``, ``END``, ``MOVE_L``, ``PUMP``
     - Reusable macro subroutine encapsulation for industrial pick, transfer, and place cycles.
   * - **32_repeat_loop_array.scara**
     - Iterative Array Loops
     - ``REPEAT``, ``END``, ``MOVE_REL``
     - Fixed-iteration macro loop scanning an inspection array with incremental relative motions.
   * - **33_nested_repeat_palletizing.scara**
     - Nested Macro Loops
     - ``REPEAT``, ``END``, ``MOVE_REL``, ``APPROACH``
     - Multi-level nested iteration loops traversing a 2D raster pallet grid without explicit pallet definitions.
   * - **34_subroutine_with_relative_motion.scara**
     - Subroutine Relative Motion
     - ``DEF``, ``CALL``, ``MOVE_REL``, ``CONFIG_ELBOW``
     - Parameterized dispensing subroutines combined with relative motions across alternating elbow configurations.
   * - **35_complex_cycle_subroutines_and_loops.scara**
     - Integrated Workcell Routine
     - ``DEF``, ``CALL``, ``REPEAT``, ``CONFIG_ELBOW``, ``ZONE``
     - Enterprise workcell demonstration integrating subroutines, repeat loops, and dynamic reconfiguration.
   * - **36_spatial_keepout_zones.scara**
     - Obstacle Avoidance
     - ``ZONE_DEF BOX``, ``MOVE_L``
     - Rectangular keep-out obstacle zone definition and collision-free transit around safety perimeter.
   * - **37_obstacle_avoidance_dual_elbow.scara**
     - Multi-Obstacle Dual-Elbow
     - ``ZONE_DEF BOX/CIRCLE``, ``CONFIG_ELBOW``
     - Multi-obstacle avoidance (box and cylinder) combined with elbow reconfiguration during transit.
   * - **38_nested_matrix_frame_sorting.scara**
     - Matrix Frame Sorting
     - ``DEF``, ``CALL``, ``PALLET_DEF``, ``FRAME_SET``
     - Subroutine-driven component acquisition from matrix pallet with frame transformation sorting.
   * - **39_closed_loop_contour_hold_recovery.scara**
     - Closed-Loop Contouring
     - ``CONFIG_MOTOR CLOSED_LOOP``, ``ZONE BLEND``, ``HOLD``
     - High-precision closed-loop contouring with feed hold pause, recovery, and corner rounding.
   * - **40_pallet_obstacle_jump_transfer.scara**
     - Obstacle-Aware Palletizing
     - ``ZONE_DEF``, ``PALLET_DEF``, ``JUMP``, ``MOVE_PALLET``
     - Collision-aware dual-pallet transfer navigating parabolic jump arches over obstacle boundaries.
   * - **41_dynamic_feedrate_accel_profiling.scara**
     - Dynamic Speed Profiling
     - ``SPEED WORK/RAPID``, ``ACCEL``, ``OVERRIDE``
     - Multi-stage dynamic feedrate and acceleration profile scheduling for delicate workpiece entry.
   * - **42_vacuum_decay_pressure_equalization.scara**
     - Pneumatic Timing
     - ``PUMP ON/OFF``, ``VALVE ON/OFF``, ``WAIT_MS``
     - Vacuum decay monitoring and micro-dwell pressure equalization for airtight fixture handling.
   * - **43_tangential_pocket_milling.scara**
     - Pocket Milling & Contouring
     - ``TOOL_ORIENT TANGENTIAL``, ``ARC_CW``, ``MOVE_L``
     - Multi-depth concentric circular pocket profiling with continuous tool tangency.
   * - **44_hierarchical_subroutine_chain.scara**
     - Nested Subroutine Chain
     - ``DEF``, ``CALL``, ``END``
     - 3-level hierarchical subroutine call stack expansion (atomic, operation, workflow).
   * - **45_polar_rotary_inspection_sweep.scara**
     - Polar Rotary Sweep
     - ``ARC_CCW``, ``ARC_CW``, ``WAIT_MS``
     - Polar optical inspection sweeps tracing concentric annular workpiece perimeters.
   * - **46_rotated_frame_relative_stepping.scara**
     - Rotated Frame Stepping
     - ``FRAME_SET``, ``MOVE_REL``, ``APPROACH``
     - Relative Cartesian incremental stepping within an angled work coordinate frame.
   * - **47_asymmetric_dual_obstacle_channel.scara**
     - Channel Corridor Transit
     - ``ZONE_DEF BOX``, ``MOVE_L``, ``SPEED WORK``
     - Collision-free trajectory navigation through an asymmetric corridor between keep-out obstacles.
   * - **48_hybrid_motor_mode_torque_switch.scara**
     - Hybrid Drive Reconfiguration
     - ``CONFIG_MOTOR OPEN_LOOP/CLOSED_LOOP``
     - Runtime stepper drive mode switching between high-speed open-loop and precision closed-loop phases.
   * - **49_serpentine_raster_dispensing.scara**
     - Serpentine Surface Raster
     - ``TOOL_ORIENT TANGENTIAL``, ``ARC_CW``, ``MOVE_L``
     - Continuous planar serpentine dispensing path with continuous tangential nozzle tracking.
   * - **50_master_multisystem_production_cell.scara**
     - Capstone Production Cell
     - ``CONFIG_ELBOW``, ``CONFIG_MOTOR``, ``ZONE_DEF``, ``DEF``
     - Master industrial production cell combining all SCARA DSL language, motion, and hardware capabilities.

User Workspace Auto-Provisioning (~/.scarajectory/workspace/)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To allow users to modify, test, and develop custom routines without modifying the installed package assets, **scarajectory** implements an automated personal workspace architecture:

* **Automatic Archive Extraction:** All 50 demonstration scripts are packaged inside ``examples.tgz`` within the package configuration. Upon application launch or when initializing the DSL Editor tab, ``WorkspaceService`` verifies that the workspace directory (``~/.scarajectory/workspace/``) exists. If the folder does not exist or any bundled scripts are absent, the archive unpacks missing examples automatically into the user's workspace.
* **Integrated Examples Catalog:** The **Examples:** dropdown combobox on the DSL Editor toolbar dynamically discovers and lists all ``.scara`` files present in the user workspace. Selecting an example and clicking **📂 Load Demo** immediately populates the syntax-highlighted editor with the script.
* **Streamlined File Dialogs:** File operations such as **📂 Open...** (``Ctrl+O``) and **💾 Save As...** (``Ctrl+S``) default directly to ``~/.scarajectory/workspace/``, enabling quick access to user scripts and personal templates.
* **Safe User Customization:** Users can freely edit existing examples, save variations, or create new industrial programs directly in ``~/.scarajectory/workspace/`` with full persistence.

📡 Unified Serial ASCII Communication Protocol
----------------------------------------------

All communication between **scarajectory**, the physical **scara_base** firmware, and the **scaraemu** digital twin is governed by a packetized ASCII streaming protocol:

Command Packets (PC to Robot)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table:: Command Packets
   :widths: 35 35 40
   :header-rows: 1

   * - Command Packet
     - Description
     - Response Handshake
   * - ``<pt#X#Y#Z#PHI#SPEED#end>``
     - Push Cartesian trajectory point to FIFO motion buffer
     - ``<RESP:ACK#QUEUE=n>`` then ``<RESP:MOVE_DONE#...>``
   * - ``<CMD:JOG#axis#step>``
     - Incremental manual jog (``X``, ``Y``, ``Z``, ``P``) by ``step`` mm/deg
     - ``<RESP:ACK#JOG_QUEUED#QUEUE=n>``
   * - ``<CMD:OVERRIDE#percent>``
     - Real-time feedrate override scaling (``10`` to ``200`` %)
     - ``<RESP:ACK#OVERRIDE=percent>``
   * - ``<CMD:WAIT#ms>``
     - Synchronous dwell delay pause on motion controller
     - ``<RESP:ACK#WAIT_DONE#MS=ms>``
   * - ``<CMD:PUMP#1>`` / ``<CMD:PUMP#0>``
     - Energize / de-energize vacuum pump actuator
     - ``<RESP:ACK#PUMP_ON>`` / ``<RESP:ACK#PUMP_OFF>``
   * - ``<CMD:VALVE#1>`` / ``<CMD:VALVE#0>``
     - Open / close pneumatic air release valve
     - ``<RESP:ACK#VALVE_ON>`` / ``<RESP:ACK#VALVE_OFF>``
   * - ``<CMD:HOME>``
     - Execute multi-axis homing and calibrate zero
     - ``<RESP:ACK#HOMING_STARTED>`` then ``<RESP:HOMED_SUCCESS#...>``
   * - ``<CMD:ENABLE>`` / ``<CMD:DISABLE>``
     - Energize / de-energize stepper driver stages
     - ``<RESP:ACK#MOTORS_ENABLED>`` / ``<RESP:ACK#MOTORS_DISABLED>``
   * - ``<CMD:ESTOP>``
     - Instant emergency stop and motion queue abort
     - ``<RESP:ACK#ESTOP_TRIGGERED>``
   * - ``<CMD:HOLD>`` / ``<CMD:RESUME>``
     - Decelerate to feed hold / resume paused trajectory
     - ``<RESP:ACK#FEED_HOLD_ACTIVE>`` / ``<RESP:ACK#MOTION_RESUMED>``
   * - ``<CMD:STATUS>``
     - Query operational machine state and endstop flags
     - ``<RESP:STATUS#STATE=...#ENDSTOPS=...>``
   * - ``<CMD:GETPOS>``
     - Read active Cartesian tool coordinates and orientation
     - ``<RESP:POS#X=...#Y=...#Z=...#PHI=...>``
   * - ``<CMD:SET_ELBOW#LEFT|RIGHT>``
     - Select inverse kinematic arm solution branch
     - ``<RESP:ACK#ELBOW=LEFT|RIGHT>``
   * - ``<CMD:GET_ELBOW>``
     - Query active elbow configuration branch
     - ``<RESP:ELBOW#CONFIG=LEFT|RIGHT>``
   * - ``<CMD:GET_CONFIG>``
     - Read persisted geometry, dynamics, and stroke bounds
     - ``<RESP:CONFIG#L1=...#L2=...#MIN_SPD=...>``
   * - ``<CMD:SET_CONFIG#...>``
     - Update robot link lengths, stroke, and speed bounds
     - ``<RESP:ACK#CONFIG_STORED...>``
   * - ``<CMD:SAVE_CONFIG>``
     - Commit active configuration to RP2040 Flash (CRC32)
     - ``<RESP:ACK#CONFIG_SAVED>``
   * - ``<CMD:RESET_CONFIG>``
     - Restore factory default geometry and kinematic bounds
     - ``<RESP:ACK#CONFIG_RESET>``

Microcontroller Response Packets (Robot to PC)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table:: Response Packets
   :widths: 35 25 50
   :header-rows: 1

   * - Response Packet
     - Category
     - Streamer Meaning
   * - ``<RESP:ACK#QUEUE=n>``
     - Acknowledgment
     - Waypoint accepted into ring buffer; ``n`` slots remaining.
   * - ``<RESP:MOVE_DONE#X=..#Y=..#Z=..#PHI=..>``
     - Move Complete
     - Physical execution of waypoint completed. Advances done counter.
   * - ``<RESP:ACK#WAIT_DONE#...>``
     - Action Complete
     - Hardware dwell delay elapsed. Advances streamer progress.
   * - ``<RESP:ACK#PUMP_ON|OFF>``
     - Action Complete
     - Tool actuation complete. Advances streamer progress.
   * - ``<RESP:ACK#VALVE_ON|OFF>``
     - Action Complete
     - Valve actuation complete. Advances streamer progress.
   * - ``<RESP:HOMED_SUCCESS#...>``
     - Homing Complete
     - Machine homed and zero-reference established.
   * - ``<RESP:NACK_BUFFER_FULL>``
     - Flow Control
     - Microcontroller queue full; streamer enters auto-pause.
   * - ``<RESP:NACK_ESTOP_ACTIVE>``
     - Error / Safety
     - E-Stop asserted; all motions rejected until reset.
   * - ``<RESP:NACK_OUT_OF_REACH>``
     - Kinematic Rejection
     - Target coordinate outside reachable arm envelope (:math:`R_{max}`).
   * - ``<RESP:NACK_SINGULARITY_LIMIT>``
     - Kinematic Rejection
     - Target inside inner deadzone (:math:`R_{min} = |L_1 - L_2|`).

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

Launch with initial trajectory plan file, deadzone restriction, and verbose output:

.. code-block:: bash

    python3 main.py studio --file ./trajectories/rectangle_demo.json --dead-zone --verbose

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
     - ``bool``
     - *Flag*
     - Enable kinematic dead zone enforcement (:math:`R_{min}`).
   * - **--verbose**
     - ``bool``
     - *Flag*
     - Enable verbose ATS operational logging.

Interactive Motion Planning Workflow
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. image:: https://raw.githubusercontent.com/vroncevic/scarajectory/dev/docs/scarajectory_in_progress.png
   :alt: SCARA Trajectory Studio in Progress
   :align: center
   :width: 100%

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

🤖 Digital Twin Integration with SCARAEmu
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**scarajectory** seamlessly integrates with `scaraemu <https://github.com/vroncevic/scaraemu>`_ as a software-in-the-loop (SITL) Digital Twin. This allows you to visually simulate, animate, and validate trajectories and ``.scara`` DSL programs in 2D/3D before deploying to physical hardware.

Mode 1: One-Click Simulation from DSL Editor
""""""""""""""""""""""""""""""""""""""""""""

1. In **scarajectory**, open the **SCARA DSL Editor** tab.
2. Write or load any ``.scara`` program (or select from bundled examples in ``~/.scarajectory/workspace/`` via the **Examples** dropdown).
3. Click the **🚀 Preview in SCARAEmu** button located at the bottom toolbar.
4. **scarajectory** automatically launches **scaraemu** in a background subprocess, passing the active trajectory file via ``--file``.
5. The 2D Planar and 3D Z-Tower canvases immediately render the robot arm executing the trajectory.

Mode 2: Real-Time Closed-Loop TCP Streaming
"""""""""""""""""""""""""""""""""""""""""""

1. Launch **scaraemu**:

   .. code-block:: bash

       python3 main.py emulator

2. Activate the Virtual Robot Server:
   * Click the **🌐 Virtual Server: OFF** toggle button on the top status bar.
   * The button turns green and displays **🌐 Virtual Server: 8888**, listening on ``127.0.0.1:8888``.
3. Launch **scarajectory**:

   .. code-block:: bash

       python3 main.py studio

4. Compile DSL code to trajectory:
   * In the **SCARA DSL Editor** tab, load or write your ``.scara`` script.
   * Click **⚡ Compile to Plan**. The AST compiler compiles Cartesian paths, macros, and action commands into the active trajectory plan.
5. Navigate to the **Hardware Streamer** tab.
6. In the **Port** dropdown, select **127.0.0.1:8888 (Digital Twin)**.
7. Click **Connect**. The status bar updates to ``Streamer: Connected to 127.0.0.1:8888``.
8. Click **Stream Trajectory** (or use the **Manual Jog** controls):
   * Trajectory waypoints (``<pt#X#Y#Z#PHI#SPEED#end>``) stream live over the loopback TCP socket.
   * **scaraemu** smoothly animates the dual-link arm and carriage along the path.
   * Closed-loop protocol acknowledgments (``<RESP:ACK#QUEUE=1>``, ``<RESP:MOVE_DONE#...>``) flow back to **scarajectory**, dynamically driving the streaming progress bar.

Mode 3: Direct File Loading in SCARAEmu
"""""""""""""""""""""""""""""""""""""""

* Open **scaraemu** and navigate to the **Trajectories** tab.
* In the **SCARA DSL Script** dropdown, select any of the 50 bundled programs from the user workspace (e.g. ``12_industrial_pick_place.scara``, ``04_circular_arc.scara``, ``09_pallet_matrix.scara``).
* Or click **📂 Load** to load any custom ``.scara`` script or exported ``plan.json`` file.

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
