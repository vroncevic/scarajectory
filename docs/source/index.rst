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
2. Write or load any ``.scara`` program (or select from bundled examples in ``examples/``).
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
* In the **SCARA DSL Script** dropdown, select any of the 12 bundled programs (e.g. ``pick_and_place.scara``, ``engrave_spiral.scara``, ``pallet_matrix.scara``).
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
