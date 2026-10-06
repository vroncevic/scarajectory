# -*- coding: UTF-8 -*-

'''
Module
    tool_panel_factory.py
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
    Factory providing JogToolPanel instances.
'''

from __future__ import annotations

from tkinter import Widget

from scarajectory.core.service.tool.itool_controller import IToolController
from scarajectory.infrastructure.gui.manipulator.jog.tool_panel import JogToolPanel

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class JogToolPanelFactory:
    '''
        Factory providing JogToolPanel instances.

        It defines:

            :methods:
                | create - Instantiates a JogToolPanel instance.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        parent: Widget,
        *,
        tool_controller: IToolController,
    ) -> JogToolPanel:
        '''
            Instantiates a JogToolPanel instance.

            :param parent: Parent container widget.
            :param tool_controller: Injected IToolController collaborator.
            :return: Configured JogToolPanel instance.
            :exceptions: None.
        '''
        return JogToolPanel(
            parent,
            tool_controller=tool_controller,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
