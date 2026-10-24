# -*- coding: UTF-8 -*-

'''
Module
    assembler.py
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

from scarajectory.infrastructure.gui.controls.assembly.bundle import TabsBundle
from scarajectory.infrastructure.gui.controls.bundle import ControlsBundle
from scarajectory.infrastructure.gui.controls.controllers.bundle import TabControllersBundle
from scarajectory.infrastructure.gui.controls.controllers.factory import TabControllersFactory
from scarajectory.infrastructure.gui.dsl.bundle import DslEditorBundle
from scarajectory.infrastructure.gui.dsl.factory import DslEditorTabFactory
from scarajectory.infrastructure.gui.dsl.tab import DslEditorTab
from scarajectory.infrastructure.gui.manipulator.jog.dependencies import JogDependencies
from scarajectory.infrastructure.gui.manipulator.jog.factory import JogTabFactory
from scarajectory.infrastructure.gui.manipulator.jog.tab import JogTab
from scarajectory.infrastructure.gui.preview.dependencies import PreviewDependencies
from scarajectory.infrastructure.gui.preview.factory import PreviewTabFactory
from scarajectory.infrastructure.gui.preview.tab import PreviewTab
from scarajectory.infrastructure.gui.streaming.bundle import StreamerBundle
from scarajectory.infrastructure.gui.streaming.controllers_bundle import StreamerControllersBundle
from scarajectory.infrastructure.gui.streaming.factory import StreamerTabFactory
from scarajectory.infrastructure.gui.streaming.tab import StreamerTab
from scarajectory.infrastructure.gui.validation.dependencies import ValidationDependencies
from scarajectory.infrastructure.gui.validation.factory import ValidationTabFactory
from scarajectory.infrastructure.gui.validation.tab import ValidationTab

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TabsAssembler:
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
    ) -> TabsBundle:
        '''
            Assembles and instantiates child tab widgets into TabsBundle.

            :param notebook: Notebook container widget.
            :param bundle: ControlsBundle dependency container.
            :return: Fully configured TabsBundle container.
            :exceptions: None.
        '''
        ctrls: TabControllersBundle = TabControllersFactory.create(
            raw_channel=bundle.streaming.raw_channel
        )
        dsl_bundle: DslEditorBundle = DslEditorBundle(
            store=bundle.store,
            mutation=bundle.mutation,
            dsl=bundle.dsl,
            loader=bundle.loader,
            storer=bundle.storer,
            workspace=bundle.workspace,
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
            avoidance_adapter=bundle.avoidance_adapter,
            connection_manager=bundle.streaming.connection_manager,
            playback_controller=bundle.streaming.playback_controller,
            connection_repository=bundle.connection_repository,
            controllers=streamer_ctrls,
        )
        stream_tab: StreamerTab = StreamerTabFactory.create(
            notebook,
            bundle=streamer_bundle,
        )
        val_deps: ValidationDependencies = ValidationDependencies(
            plan=bundle.store,
            validator=bundle.validator,
            avoidance_adapter=bundle.avoidance_adapter,
        )
        val_tab: ValidationTab = ValidationTabFactory.create(
            notebook,
            dependencies=val_deps,
        )
        jog_deps: JogDependencies = JogDependencies(
            raw_channel=bundle.streaming.raw_channel,
            motion_controller=ctrls.motion_ctrl,
            jog_controller=ctrls.jog_ctrl,
            tool_controller=ctrls.tool_ctrl,
            query_controller=ctrls.query_ctrl,
        )
        jog_tab: JogTab = JogTabFactory.create(
            notebook,
            dependencies=jog_deps,
        )
        prev_deps: PreviewDependencies = PreviewDependencies(
            plan=bundle.store,
            exporter=bundle.dsl.plan_exporter,
        )
        prev_tab: PreviewTab = PreviewTabFactory.create(
            notebook,
            dependencies=prev_deps,
        )

        return TabsBundle(
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
