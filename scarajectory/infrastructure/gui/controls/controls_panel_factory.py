# -*- coding: UTF-8 -*-

'''
Module
    controls_panel_factory.py
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
    Factory instantiating ControlsPanel and coordinating child tab factories.
'''

from __future__ import annotations

from tkinter import Widget

from scarajectory.core.service.iservice import IService
from scarajectory.core.service.communication.stream.itrajectory_streamer import ITrajectoryStreamer
from scarajectory.core.service.communication.stream.config_factory import ConfigFactory
from scaralang.core.service.dsl.iscara_dsl_service import IScaraDslService
from scarajectory.core.service.trajectory.contract.iplan_storage_service import IPlanStorageService
from scarajectory.core.service.trajectory.plan.itrajectory_plan import ITrajectoryPlan
from scarajectory.core.service.trajectory.validation.itrajectory_validator import ITrajectoryValidator
from scarajectory.infrastructure.communication.preferences.iconnection_repository import IConnectionRepository
from scarajectory.infrastructure.gui.controls.controls import ControlsPanel
from scarajectory.infrastructure.gui.dsl.dsl_editor_tab import DslEditorTab
from scarajectory.infrastructure.gui.dsl.dsl_editor_tab_factory import DslEditorTabFactory
from scarajectory.infrastructure.gui.editor.preview_tab import PreviewTab
from scarajectory.infrastructure.gui.editor.preview_tab_factory import PreviewTabFactory
from scarajectory.infrastructure.gui.editor.validation_tab import ValidationTab
from scarajectory.infrastructure.gui.stream.jog_tab import JogTab
from scarajectory.infrastructure.gui.stream.streamer_tab import StreamerTab

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ControlsPanelFactory:
    '''
        Factory constructing ControlsPanel and hierarchically assembling child tabs.
    '''

    @classmethod
    def create(
        cls,
        parent: Widget,
        *,
        plan: ITrajectoryPlan,
        validator: ITrajectoryValidator,
        streamer: ITrajectoryStreamer,
        storage: IPlanStorageService,
        dsl_service: IScaraDslService,
        service: IService,
        connection_repository: IConnectionRepository,
        **kwargs: object
    ) -> ControlsPanel:
        panel = ControlsPanel(parent, **kwargs)

        dsl_tab: DslEditorTab = DslEditorTabFactory.create(
            panel.notebook,
            plan=plan,
            dsl_service=dsl_service,
            storage=storage,
        )
        stream_tab: StreamerTab = StreamerTab(
            panel.notebook,
            plan=plan,
            validator=validator,
            streamer=streamer,
            connection_repository=connection_repository,
            service=service,
            stream_config_factory=ConfigFactory,
        )
        val_tab: ValidationTab = ValidationTab(
            panel.notebook,
            plan=plan,
            validator=validator,
            service=service,
        )
        jog_tab: JogTab = JogTab(panel.notebook, streamer=streamer)
        prev_tab: PreviewTab = PreviewTabFactory.create(panel.notebook, plan=plan)

        panel.mount_tabs(
            dsl_editor_tab=dsl_tab,
            streamer_tab=stream_tab,
            validation_tab=val_tab,
            jog_tab=jog_tab,
            preview_tab=prev_tab,
        )

        return panel

    @classmethod
    def get_version(cls) -> str:
        return __version__
