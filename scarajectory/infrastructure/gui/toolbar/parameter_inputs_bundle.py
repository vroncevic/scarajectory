# -*- coding: UTF-8 -*-

'''
Module
    parameter_inputs_bundle.py
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
    Parameter bundle containing dependencies and settings required by ToolbarParameterInputs.
'''

from __future__ import annotations

from dataclasses import dataclass

from scarajectory.infrastructure.gui.canvas.icanvas import ICanvas
from scarajectory.infrastructure.gui.canvas.status.icanvas_status_presenter import ICanvasStatusPresenter
from scarajectory.infrastructure.gui.model.canvas_settings import CanvasSettings

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True, kw_only=True)
class ParameterInputsBundle:
    '''
        Configuration and collaborator bundle for ToolbarParameterInputs assembly.

        It defines:

            :attributes:
                | canvas - Active CAD canvas interface.
                | status_presenter - Cursor status presenter interface.
                | r_min - Minimum reach distance from origin in mm.
                | r_max - Maximum reach distance from origin in mm.
                | settings - Active canvas creation parameters.
    '''

    canvas: ICanvas
    status_presenter: ICanvasStatusPresenter
    r_min: float
    r_max: float
    settings: CanvasSettings
