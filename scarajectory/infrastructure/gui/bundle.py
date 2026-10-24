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
    Parameter bundle holding assembled GUI presentation collaborators.
'''

from __future__ import annotations

from dataclasses import dataclass
from tkinter import Tk

from scarajectory.core.service.storage.iloader import IPlanLoader
from scarajectory.core.service.streaming.playback.icontroller import IPlaybackController
from scarajectory.core.service.trajectory.plan.mutation.bulk_mutation.ibulk_mutation import IPlanBulkMutator
from scarajectory.infrastructure.gui.canvas.navigation.inavigator import ICanvasViewNavigator
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
class GUIBundle:
    '''
    Bundle containing assembled GUI presentation collaborators.

    It defines:

        :attributes:
            | root - Root Tk application window.
            | playback_controller - Robot motion streaming playback controller.
            | loader - Plan loader service port.
            | mutation - Plan modification service.
            | navigator - Canvas viewport and navigation controller.
            | toolbar - Top toolbar presentation component.
        :methods:
            | streamer - Returns playback controller for backward compatibility.
    '''

    root: Tk
    playback_controller: IPlaybackController
    loader: IPlanLoader
    mutation: IPlanBulkMutator
    navigator: ICanvasViewNavigator
    toolbar: Toolbar

    @property
    def streamer(self) -> IPlaybackController:
        '''
        Returns motion streaming playback controller.

        :return: IPlaybackController instance.
        '''
        return self.playback_controller
