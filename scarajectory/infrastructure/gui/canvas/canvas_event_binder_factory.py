# -*- coding: UTF-8 -*-

'''
Module
    canvas_event_binder_factory.py
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
    Factory service constructing CanvasEventBinder instances.
'''

from __future__ import annotations

from tkinter import Widget

from scarajectory.infrastructure.gui.canvas.canvas_event_binder import CanvasEventBinder
from scarajectory.infrastructure.gui.canvas.handler.icanvas_mouse_handler import ICanvasMouseHandler
from scarajectory.infrastructure.gui.canvas.status.icanvas_status_presenter import ICanvasStatusPresenter
from scarajectory.infrastructure.gui.canvas.navigation.icanvas_view_navigator import ICanvasViewNavigator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CanvasEventBinderFactory:
    '''
        Factory providing instantiation of CanvasEventBinder components.

        It defines:

            :methods:
                | create - Constructs a CanvasEventBinder instance.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        canvas: Widget,
        *,
        mouse_handler: ICanvasMouseHandler,
        navigator: ICanvasViewNavigator,
        status_presenter: ICanvasStatusPresenter,
    ) -> CanvasEventBinder:
        '''
            Constructs and returns a CanvasEventBinder instance.

            :param canvas: Target canvas widget instance.
            :param mouse_handler: Injected ICanvasMouseHandler interface.
            :param navigator: Injected ICanvasViewNavigator interface.
            :param status_presenter: Injected ICanvasStatusPresenter interface.
            :return: CanvasEventBinder instance.
            :exceptions: None.
        '''
        return CanvasEventBinder(
            canvas,
            mouse_handler=mouse_handler,
            navigator=navigator,
            status_presenter=status_presenter,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
