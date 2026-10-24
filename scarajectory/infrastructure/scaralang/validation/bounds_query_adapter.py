# -*- coding: UTF-8 -*-

'''
Module
    bounds_query_adapter.py
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
    Infrastructure adapter delegating workspace bounds and reach queries to workspace envelope.
'''

from __future__ import annotations

from typing import Final

from scaralang.core.model.kinematics.profile.bounds import ScaraBounds
from scaralang.core.service.kinematics.envelope.ienvelope import IWorkspaceEnvelope

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class WorkspaceBoundsQueryAdapter:
    '''
        Adapter delegating workspace bounds and reach queries to workspace envelope.

        It defines:

            :attributes:
                | _envelope - Injected workspace envelope provider.
            :methods:
                | __init__ - Initializes adapter with workspace envelope.
                | bounds - Returns underlying manipulator kinematic bounds model.
                | envelope - Returns active workspace envelope provider.
                | r_min - Returns inner workspace reach radius in mm.
                | r_max - Returns outer workspace reach radius in mm.
    '''

    _envelope: IWorkspaceEnvelope

    def __init__(self, envelope: IWorkspaceEnvelope) -> None:
        '''
            Initializes WorkspaceBoundsQueryAdapter with workspace envelope.

            :param envelope: IWorkspaceEnvelope collaborator.
            :exceptions: None.
        '''
        self._envelope: Final[IWorkspaceEnvelope] = envelope

    @property
    def bounds(self) -> ScaraBounds:
        '''
            Returns underlying manipulator kinematic bounds model.

            :return: ScaraBounds domain model.
            :exceptions: None.
        '''
        return self._envelope.bounds

    @property
    def envelope(self) -> IWorkspaceEnvelope:
        '''
            Returns active workspace envelope provider.

            :return: IWorkspaceEnvelope instance.
            :exceptions: None.
        '''
        return self._envelope

    @property
    def r_min(self) -> float:
        '''
            Returns inner workspace reach radius in mm.

            :return: Minimum reach radius float value.
            :exceptions: None.
        '''
        return self._envelope.r_min

    @property
    def r_max(self) -> float:
        '''
            Returns outer workspace reach radius in mm.

            :return: Maximum reach radius float value.
            :exceptions: None.
        '''
        return self._envelope.r_max
