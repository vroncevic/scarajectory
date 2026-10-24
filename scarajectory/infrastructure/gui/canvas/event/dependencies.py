# -*- coding: UTF-8 -*-

'''
Module
    dependencies.py
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
    Parameter bundle dependencies for CanvasEventBinder component.
'''

from __future__ import annotations

from dataclasses import dataclass
from tkinter import Widget

from scarajectory.infrastructure.gui.canvas.handler.mouse.ihandler import ICanvasMouseHandler
from scarajectory.infrastructure.gui.canvas.navigation.inavigator import ICanvasViewNavigator
from scarajectory.infrastructure.gui.canvas.status.ipresenter import ICanvasStatusPresenter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True)
class EventBinderDependencies:
    '''
        Parameter bundle encapsulating external collaborators for CanvasEventBinder.

        It defines:

            :attributes:
                | canvas - Target canvas widget instance.
                | mouse_handler - Injected ICanvasMouseHandler interface.
                | navigator - Injected ICanvasViewNavigator interface.
                | status_presenter - Injected ICanvasStatusPresenter interface.
    '''

    canvas: Widget
    mouse_handler: ICanvasMouseHandler
    navigator: ICanvasViewNavigator
    status_presenter: ICanvasStatusPresenter
