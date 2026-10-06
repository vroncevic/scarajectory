# -*- coding: UTF-8 -*-

'''
Module
    scarajectory_gui.py
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
    Main Tkinter graphical interface adapter coordinating menu, toolbar, canvas, table and controls.
'''

from __future__ import annotations

from tkinter import TclError, Tk
from tkinter.messagebox import showerror

from scarajectory.core.service.storage.iplan_storage_service import IPlanStorageService
from scarajectory.core.service.streaming.istream_playback_controller import IStreamPlaybackController
from scarajectory.core.service.trajectory.plan.mutation.iplan_bulk_mutator import IPlanBulkMutator
from scarajectory.infrastructure.gui.canvas.navigation.icanvas_view_navigator import ICanvasViewNavigator
from scarajectory.infrastructure.gui.scarajectory_gui_bundle import ScarajectoryGUIBundle
from scarajectory.infrastructure.gui.toolbar.toolbar import Toolbar

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScarajectoryGUI:
    '''
    Main Tkinter GUI adapter coordinating vector canvas, tabular view, and controls.

    It defines:

        :attributes:
            | _root - Root Tkinter application window.
            | _playback_controller - Robot motion streaming playback controller.
            | _storage - Plan persistence storage service.
            | _mutation - Plan modification service.
            | _navigator - Canvas viewport and navigation controller.
            | _toolbar - Top toolbar presentation component.
            | _stopped - Flag indicating whether GUI teardown has completed.
        :methods:
            | __init__ - Initializes GUI adapter with assembled presentation components.
            | is_initialized - Checks if GUI components are initialized.
            | start - Starts the Tkinter main event loop.
            | stop - Closes and destroys the window.
            | load_file - Loads trajectory JSON file into plan.
            | set_deadzone - Sets deadzone enforcement state.
    '''

    _root: Tk
    _playback_controller: IStreamPlaybackController
    _storage: IPlanStorageService
    _mutation: IPlanBulkMutator
    _navigator: ICanvasViewNavigator
    _toolbar: Toolbar
    _stopped: bool

    def __init__(self, *, bundle: ScarajectoryGUIBundle) -> None:
        '''
        Initializes GUI adapter with assembled presentation components.

        :param bundle: Injected ScarajectoryGUIBundle collaborator.
        '''
        self._root = bundle.root
        self._playback_controller = bundle.playback_controller
        self._storage = bundle.storage
        self._mutation = bundle.mutation
        self._navigator = bundle.navigator
        self._toolbar = bundle.toolbar
        self._stopped = False
        self._root.protocol('WM_DELETE_WINDOW', self.stop)

    def is_initialized(self) -> bool:
        '''
        Checks if GUI components are initialized.

        :return: True if initialized, False otherwise.
        '''
        return True

    def start(self) -> None:
        '''
        Starts the Tkinter main event loop.
        '''
        try:
            self._root.mainloop()

        finally:
            self.stop()

    def stop(self) -> None:
        '''
        Closes and destroys the window.
        '''
        if self._stopped:
            return
        self._stopped = True

        try:
            self._root.withdraw()

        except (AttributeError, RuntimeError, TclError):
            pass

        try:
            self._playback_controller.stop_streaming()

        except (AttributeError, RuntimeError):
            pass

        try:
            self._root.quit()

        except (AttributeError, RuntimeError, TclError):
            pass

        try:
            self._root.destroy()

        except (AttributeError, RuntimeError, TclError):
            pass

    def load_file(self, filepath: str) -> None:
        '''
        Loads trajectory JSON file into plan.

        :param filepath: JSON file path.
        '''
        try:
            waypoints = self._storage.load_plan(filepath)
            self._mutation.set_waypoints(waypoints)
            self._navigator.fit_reach_view()

        except OSError as exc:
            showerror('Load Error', f'Failed to load plan: {exc}')

    def set_deadzone(self, enabled: bool) -> None:
        '''
        Sets deadzone enforcement state.

        :param enabled: True to enforce deadzone, False to disable.
        '''
        self._toolbar.set_deadzone(enabled)
