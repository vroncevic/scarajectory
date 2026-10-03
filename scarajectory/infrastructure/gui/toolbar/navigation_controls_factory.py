# -*- coding: UTF-8 -*-

'''
Module
    navigation_controls_factory.py
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
    Factory for instantiating ToolbarNavigationControls components.
'''

from __future__ import annotations

from tkinter import Widget

from scarajectory.core.service.trajectory.plan.itrajectory_history import ITrajectoryHistory
from scarajectory.infrastructure.gui.canvas.navigation.icanvas_view_navigator import ICanvasViewNavigator
from scarajectory.infrastructure.gui.toolbar.navigation_controls import ToolbarNavigationControls

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ToolbarNavigationControlsFactory:
    '''
        Factory responsible for creating ToolbarNavigationControls instances.

        It defines:

            :methods:
                | create - Creates a ToolbarNavigationControls widget instance.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        parent: Widget,
        navigator: ICanvasViewNavigator,
        history: ITrajectoryHistory,
    ) -> ToolbarNavigationControls:
        '''
            Creates a ToolbarNavigationControls widget instance.

            :param parent: Parent container widget.
            :param navigator: Viewport navigation interface.
            :param history: Trajectory history service interface.
            :return: Fully configured ToolbarNavigationControls instance.
            :exceptions: None.
        '''
        return ToolbarNavigationControls(parent, navigator, history)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
