# -*- coding: UTF-8 -*-

'''
Module
    presenter.py
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
    Manages active canvas configuration settings and redraw synchronization.
'''

from __future__ import annotations

from typing import Final

from scarajectory.infrastructure.gui.canvas.observer.iredraw_delegate import ICanvasRedrawDelegate
from scarajectory.infrastructure.gui.model.canvas_settings import CanvasSettings

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CanvasSettingsPresenter:
    '''
        Manages active canvas configuration settings and redraw synchronization.

        It defines:

            :attributes:
                | _settings - Active canvas configuration DTO.
                | _redraw_delegate - Delegate to trigger canvas redraw.
            :methods:
                | __init__ - Initializes canvas settings presenter.
                | update_settings - Updates default parameters and deadzone settings.
                | settings - Returns active canvas configuration settings.
    '''

    _settings: CanvasSettings
    _redraw_delegate: ICanvasRedrawDelegate

    def __init__(
        self,
        initial_settings: CanvasSettings,
        redraw_delegate: ICanvasRedrawDelegate,
    ) -> None:
        '''
            Initializes canvas settings presenter.

            :param initial_settings: Initial CanvasSettings instance.
            :param redraw_delegate: Required ICanvasRedrawDelegate collaborator.
            :exceptions: None.
        '''
        self._settings = initial_settings
        self._redraw_delegate: Final[ICanvasRedrawDelegate] = redraw_delegate

    def update_settings(self, settings: CanvasSettings) -> None:
        '''
            Updates default parameters and deadzone settings.

            :param settings: Updated CanvasSettings instance.
            :exceptions: None.
        '''
        self._settings = settings
        self._redraw_delegate.redraw()

    @property
    def settings(self) -> CanvasSettings:
        '''
            Returns active canvas configuration settings.

            :return: CanvasSettings instance.
            :exceptions: None.
        '''
        return self._settings
