# -*- coding: UTF-8 -*-

'''
Module
    scarajectory_gui_bundle.py
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
    Parameter bundle holding assembled GUI presentation collaborators.
'''

from __future__ import annotations

from dataclasses import dataclass
from tkinter import Tk

from scarajectory.core.service.storage.iplan_storage_service import IPlanStorageService
from scarajectory.core.service.streaming.istream_playback_controller import IStreamPlaybackController
from scarajectory.core.service.trajectory.plan.mutation.iplan_bulk_mutator import IPlanBulkMutator
from scarajectory.infrastructure.gui.canvas.navigation.icanvas_view_navigator import ICanvasViewNavigator
from scarajectory.infrastructure.gui.toolbar.toolbar import Toolbar

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(slots=True, frozen=True, kw_only=True)
class ScarajectoryGUIBundle:
    '''
    Bundle containing assembled GUI presentation collaborators.

    It defines:

        :attributes:
            | root - Root Tk application window.
            | playback_controller - Robot motion streaming playback controller.
            | storage - Plan persistence storage service.
            | mutation - Plan modification service.
            | navigator - Canvas viewport and navigation controller.
            | toolbar - Top toolbar presentation component.
        :methods:
            | streamer - Returns playback controller for backward compatibility.
    '''

    root: Tk
    playback_controller: IStreamPlaybackController
    storage: IPlanStorageService
    mutation: IPlanBulkMutator
    navigator: ICanvasViewNavigator
    toolbar: Toolbar

    @property
    def streamer(self) -> IStreamPlaybackController:
        '''
        Returns motion streaming playback controller.

        :return: IStreamPlaybackController instance.
        '''
        return self.playback_controller
