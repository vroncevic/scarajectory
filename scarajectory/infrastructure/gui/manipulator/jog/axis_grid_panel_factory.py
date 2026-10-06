# -*- coding: UTF-8 -*-

'''
Module
    axis_grid_panel_factory.py
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
    Factory providing JogAxisGridPanel instances.
'''

from __future__ import annotations

from tkinter import Widget

from scarajectory.core.service.manipulator.ijog_controller import IJogController
from scarajectory.core.service.manipulator.iquery_controller import IQueryController
from scarajectory.infrastructure.gui.manipulator.jog.axis_grid_panel import JogAxisGridPanel

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class JogAxisGridPanelFactory:
    '''
        Factory providing JogAxisGridPanel instances.

        It defines:

            :methods:
                | create - Instantiates a JogAxisGridPanel instance.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        parent: Widget,
        *,
        jog_controller: IJogController,
        query_controller: IQueryController,
    ) -> JogAxisGridPanel:
        '''
            Instantiates a JogAxisGridPanel instance with controllers.

            :param parent: Parent container widget.
            :param jog_controller: Injected relative axis movement controller.
            :param query_controller: Injected robot state inquiry controller.
            :return: JogAxisGridPanel instance.
            :exceptions: None.
        '''
        return JogAxisGridPanel(
            parent,
            jog_controller=jog_controller,
            query_controller=query_controller,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
