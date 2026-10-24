# -*- coding: UTF-8 -*-

'''
Module
    factory.py
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
    Factory providing StreamerTab instances.
'''

from __future__ import annotations

from tkinter import BOTH, Widget, X

from scarajectory.infrastructure.gui.connection.panel.panel import PortConnectionPanel
from scarajectory.infrastructure.gui.console.panel import SerialConsole
from scarajectory.infrastructure.gui.manipulator.override.panel import ManipulatorOverridePanel
from scarajectory.infrastructure.gui.streaming.bundle import StreamerBundle
from scarajectory.infrastructure.gui.streaming.control.panel import StreamControlPanel
from scarajectory.infrastructure.gui.streaming.playback.bundle import PlaybackHandlerBundle
from scarajectory.infrastructure.gui.streaming.playback.factory import StreamPlaybackActionHandlerFactory
from scarajectory.infrastructure.gui.streaming.playback.handler import StreamPlaybackActionHandler
from scarajectory.infrastructure.gui.streaming.progress.adapter import StreamProgressAdapter
from scarajectory.infrastructure.gui.streaming.status.status_bar import StreamStatusBar
from scarajectory.infrastructure.gui.streaming.tab import StreamerTab
from scarajectory.infrastructure.gui.streaming.tool.factory import StreamToolActionHandlerFactory
from scarajectory.infrastructure.gui.streaming.tool.handler import StreamToolActionHandler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamerTabFactory:
    '''
        Factory providing StreamerTab instances.

        It defines:

            :methods:
                | create - Instantiates and assembles a StreamerTab instance.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        parent: Widget,
        *,
        bundle: StreamerBundle,
    ) -> StreamerTab:
        '''
            Instantiates and assembles a StreamerTab instance.

            :param parent: Parent container widget.
            :param bundle: Injected StreamerBundle dependencies.
            :return: Configured and assembled StreamerTab instance.
            :exceptions: None.
        '''
        tab: StreamerTab = StreamerTab(parent)

        status_bar: StreamStatusBar = StreamStatusBar(tab)
        status_bar.pack(fill=X, pady=2)

        playback_bundle: PlaybackHandlerBundle = PlaybackHandlerBundle(
            plan=bundle.plan,
            validator=bundle.validator,
            avoidance_adapter=bundle.avoidance_adapter,
            connection_manager=bundle.connection_manager,
            playback_controller=bundle.playback_controller,
            status_bar=status_bar,
        )
        playback_handler: StreamPlaybackActionHandler = (
            StreamPlaybackActionHandlerFactory.create(
                bundle=playback_bundle,
            )
        )

        port_panel: PortConnectionPanel = PortConnectionPanel(
            tab,
            connection_repository=bundle.connection_repository,
            connection_delegate=playback_handler,
        )
        port_panel.pack(fill=X, pady=2)

        progress_adapter: StreamProgressAdapter = StreamProgressAdapter(
            port_panel=port_panel,
            status_bar=status_bar,
        )

        tool_handler: StreamToolActionHandler = (
            StreamToolActionHandlerFactory.create(
                connection_manager=bundle.connection_manager,
                controllers=bundle.controllers,
            )
        )

        override_panel: ManipulatorOverridePanel = ManipulatorOverridePanel(
            tab,
            action_delegate=tool_handler,
        )
        override_panel.pack(fill=X, pady=2)

        ctrl_panel: StreamControlPanel = StreamControlPanel(
            tab,
            control_delegate=playback_handler,
        )
        ctrl_panel.pack(fill=X, pady=4)

        console: SerialConsole = SerialConsole(tab)
        console.pack(fill=BOTH, expand=True, pady=2)

        tab.bind_components(
            port_panel=port_panel,
            progress_adapter=progress_adapter,
            console=console,
        )

        return tab

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
