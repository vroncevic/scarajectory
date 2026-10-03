# -*- coding: UTF-8 -*-

'''
Module
    bundle.py
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
    Parameter bundle containing dependencies and settings required by ToolbarFactory.
'''

from __future__ import annotations

from dataclasses import dataclass

from scarajectory.core.service.trajectory.plan.itrajectory_history import ITrajectoryHistory
from scarajectory.infrastructure.gui.canvas.icanvas import ICanvas
from scarajectory.infrastructure.gui.canvas.status.icanvas_status_presenter import ICanvasStatusPresenter
from scarajectory.infrastructure.gui.canvas.navigation.icanvas_view_navigator import ICanvasViewNavigator
from scarajectory.infrastructure.gui.model.canvas_settings import CanvasSettings

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True, kw_only=True)
class ToolbarBundle:
    '''
        Configuration and collaborator bundle for Toolbar component assembly.

        It defines:

            :attributes:
                | canvas - Main canvas interface.
                | navigator - Viewport camera navigator interface.
                | status_presenter - Canvas coordinate/status presenter interface.
                | history - Trajectory undo/redo history service interface.
                | r_min - Minimum reach radius in millimeters.
                | r_max - Maximum reach radius in millimeters.
                | settings - Canvas display and default kinematic settings.
    '''

    canvas: ICanvas
    navigator: ICanvasViewNavigator
    status_presenter: ICanvasStatusPresenter
    history: ITrajectoryHistory
    r_min: float
    r_max: float
    settings: CanvasSettings
