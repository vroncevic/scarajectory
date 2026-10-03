# -*- coding: UTF-8 -*-

'''
Module
    tabs_assembler.py
Copyright
    Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>
    scarajectory is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the
    Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    scarajectory is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.
    You should have received a copy of the GNU General Public License along
    with this program. If not, see <http://www.gnu.org/licenses/>.
Info
    Assembler service coordinating instantiation of ControlsPanel child tabs.
'''

from __future__ import annotations

from tkinter.ttk import Notebook

from scarajectory.infrastructure.gui.controls.bundle import ControlsBundle
from scarajectory.infrastructure.gui.controls.manipulator_controllers_bundle import ManipulatorControllersBundle
from scarajectory.infrastructure.gui.controls.manipulator_controllers_factory import ManipulatorControllersFactory
from scarajectory.infrastructure.gui.controls.tabs_bundle import ControlsTabsBundle
from scarajectory.infrastructure.gui.dsl.bundle import DslEditorBundle
from scarajectory.infrastructure.gui.dsl.dsl_editor_tab import DslEditorTab
from scarajectory.infrastructure.gui.dsl.dsl_editor_tab_factory import DslEditorTabFactory
from scarajectory.infrastructure.gui.manipulator.jog.controllers_bundle import JogControllersBundle
from scarajectory.infrastructure.gui.manipulator.jog.jog_tab import JogTab
from scarajectory.infrastructure.gui.manipulator.jog.jog_tab_factory import JogTabFactory
from scarajectory.infrastructure.gui.preview.preview_tab import PreviewTab
from scarajectory.infrastructure.gui.preview.preview_tab_factory import PreviewTabFactory
from scarajectory.infrastructure.gui.streaming.bundle import StreamerBundle
from scarajectory.infrastructure.gui.streaming.streamer_controllers_bundle import StreamerControllersBundle
from scarajectory.infrastructure.gui.streaming.streamer_tab import StreamerTab
from scarajectory.infrastructure.gui.streaming.streamer_tab_factory import StreamerTabFactory
from scarajectory.infrastructure.gui.validation.validation_tab import ValidationTab
from scarajectory.infrastructure.gui.validation.validation_tab_factory import ValidationTabFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ControlsTabsAssembler:
    '''
        Assembler service coordinating instantiation of ControlsPanel child tabs.

        It defines:

            :methods:
                | assemble_tabs - Assembles and mounts child control tabs.
                | get_version - Returns component version string.
    '''

    def assemble_tabs(
        self,
        notebook: Notebook,
        bundle: ControlsBundle,
    ) -> ControlsTabsBundle:
        '''
            Assembles and instantiates child tab widgets into ControlsTabsBundle.

            :param notebook: Notebook container widget.
            :param bundle: ControlsBundle dependency container.
            :return: Fully configured ControlsTabsBundle container.
            :exceptions: None.
        '''
        ctrls: ManipulatorControllersBundle = (
            ManipulatorControllersFactory.create(
                raw_channel=bundle.streaming.raw_channel
            )
        )
        dsl_bundle: DslEditorBundle = DslEditorBundle(
            store=bundle.store,
            mutation=bundle.mutation,
            dsl_service=bundle.dsl_service,
            storage=bundle.storage,
        )
        dsl_tab: DslEditorTab = DslEditorTabFactory.create(
            notebook,
            bundle=dsl_bundle,
        )
        streamer_ctrls: StreamerControllersBundle = StreamerControllersBundle(
            motion_controller=ctrls.motion_ctrl,
            jog_controller=ctrls.jog_ctrl,
            tool_controller=ctrls.tool_ctrl,
        )
        streamer_bundle: StreamerBundle = StreamerBundle(
            plan=bundle.store,
            validator=bundle.validator,
            connection=bundle.streaming.connection,
            playback_controller=bundle.streaming.playback_controller,
            connection_repository=bundle.connection_repository,
            controllers=streamer_ctrls,
        )
        stream_tab: StreamerTab = StreamerTabFactory.create(
            notebook,
            bundle=streamer_bundle,
        )
        val_tab: ValidationTab = ValidationTabFactory.create(
            notebook,
            plan=bundle.store,
            validator=bundle.validator,
        )
        jog_bundle: JogControllersBundle = JogControllersBundle(
            raw_channel=bundle.streaming.raw_channel,
            motion_controller=ctrls.motion_ctrl,
            jog_controller=ctrls.jog_ctrl,
            tool_controller=ctrls.tool_ctrl,
            query_controller=ctrls.query_ctrl,
        )
        jog_tab: JogTab = JogTabFactory.create(
            notebook,
            bundle=jog_bundle,
        )
        prev_tab: PreviewTab = PreviewTabFactory.create(
            notebook, plan=bundle.store
        )

        return ControlsTabsBundle(
            dsl_editor_tab=dsl_tab,
            streamer_tab=stream_tab,
            validation_tab=val_tab,
            jog_tab=jog_tab,
            preview_tab=prev_tab,
        )

    def get_version(self) -> str:
        '''
            Returns component version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
