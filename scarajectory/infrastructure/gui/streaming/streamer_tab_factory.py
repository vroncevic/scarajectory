# -*- coding: UTF-8 -*-

'''
Module
    streamer_tab_factory.py
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

from tkinter import Widget

from scarajectory.infrastructure.gui.streaming.bundle import StreamerBundle
from scarajectory.infrastructure.gui.streaming.handler.playback_handler_bundle import PlaybackHandlerBundle
from scarajectory.infrastructure.gui.streaming.handler.stream_playback_action_handler import StreamPlaybackActionHandler
from scarajectory.infrastructure.gui.streaming.handler.stream_playback_action_handler_factory import StreamPlaybackActionHandlerFactory
from scarajectory.infrastructure.gui.streaming.handler.stream_tool_action_handler import StreamToolActionHandler
from scarajectory.infrastructure.gui.streaming.handler.stream_tool_action_handler_factory import StreamToolActionHandlerFactory
from scarajectory.infrastructure.gui.streaming.streamer_action_bundle import StreamerActionBundle
from scarajectory.infrastructure.gui.streaming.streamer_tab import StreamerTab

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
        tab: StreamerTab = StreamerTab(
            parent,
            connection_repository=bundle.connection_repository,
        )
        playback_bundle: PlaybackHandlerBundle = PlaybackHandlerBundle(
            plan=bundle.plan,
            validator=bundle.validator,
            connection=bundle.connection,
            playback_controller=bundle.playback_controller,
            progress_adapter=tab.progress_adapter,
            port_panel=tab.port_panel,
        )
        playback_handler: StreamPlaybackActionHandler = (
            StreamPlaybackActionHandlerFactory.create(
                bundle=playback_bundle,
            )
        )
        tool_handler: StreamToolActionHandler = (
            StreamToolActionHandlerFactory.create(
                connection=bundle.connection,
                controllers=bundle.controllers,
                override_panel=tab.override_panel,
            )
        )
        actions: StreamerActionBundle = StreamerActionBundle(
            playback_handler=playback_handler,
            tool_handler=tool_handler,
        )
        tab.mount_actions(actions)

        return tab

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
