# -*- coding: UTF-8 -*-

'''
Module
    steps_factory.py
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
    Factory service constructing JointStepsDiagnostics domain models.
'''

from __future__ import annotations

from scarajectory.core.model.telemetry.diagnostics.steps import JointStepsDiagnostics

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class JointStepsDiagnosticsFactory:
    '''
        Factory service constructing JointStepsDiagnostics domain models.

        It defines:

            :methods:
                | create - Constructs JointStepsDiagnostics model with explicit parameters.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        j1: int,
        j2: int,
        z: int,
        j4: int,
    ) -> JointStepsDiagnostics:
        '''
            Constructs JointStepsDiagnostics model instance.

            :param j1: Monotonic executed steps for joint 1.
            :param j2: Monotonic executed steps for joint 2.
            :param z: Monotonic executed steps for Z vertical axis.
            :param j4: Monotonic executed steps for wrist joint 4.
            :return: JointStepsDiagnostics model instance.
            :exceptions: None.
        '''
        return JointStepsDiagnostics(j1=j1, j2=j2, z=z, j4=j4)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
