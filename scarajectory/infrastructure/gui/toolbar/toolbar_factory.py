# -*- coding: UTF-8 -*-

'''
Module
    toolbar_factory.py
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
    Factory module for assembling and instantiating Toolbar GUI components.
'''

from __future__ import annotations

from tkinter import Widget

from scarajectory.core.service.trajectory.plan.itrajectory_plan import ITrajectoryPlan
from scarajectory.infrastructure.gui.canvas.icanvas import ICanvas
from scarajectory.infrastructure.gui.model.canvas_settings import CanvasSettings
from scarajectory.infrastructure.gui.toolbar.toolbar import Toolbar

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ToolbarFactory:
    '''
        Factory responsible for assembling Toolbar instances.

        It defines:

            :methods:
                | create - Assembles and instantiates a Toolbar widget.
    '''

    @classmethod
    def create(
        cls,
        parent: Widget,
        *,
        canvas: ICanvas,
        plan: ITrajectoryPlan,
        r_min: float,
        r_max: float,
        settings: CanvasSettings,
        **kwargs: object,
    ) -> Toolbar:
        '''
            Assembles and instantiates a Toolbar widget.

            :param parent: Parent container widget.
            :param canvas: ICanvas interface instance.
            :param plan: ITrajectoryPlan instance.
            :param r_min: Minimum reach radius in mm.
            :param r_max: Maximum reach radius in mm.
            :param settings: CanvasSettings instance.
            :return: Fully assembled Toolbar instance.
            :exceptions: None.
        '''
        return Toolbar(
            parent,
            canvas,
            plan,
            r_min=r_min,
            r_max=r_max,
            settings=settings,
            **kwargs,
        )

