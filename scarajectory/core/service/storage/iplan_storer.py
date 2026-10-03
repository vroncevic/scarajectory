# -*- coding: UTF-8 -*-

'''
Module
    iplan_storer.py
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
    Defines segregated interface IPlanStorer for trajectory plan and file writing operations.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaralang.core.model.dsl.binary.program import BinaryProgram
from scarajectory.core.service.trajectory.plan.itrajectory_read_only import ITrajectoryReadOnly

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IPlanStorer(Protocol):
    '''
        Protocol for saving trajectory plan files and writing text/binary content.

        It defines:

            :methods:
                | save_plan - Saves current trajectory plan to JSON file path.
                | save_text_file - Writes text content to file path.
                | save_binary_program - Writes compiled binary program payload to destination file path.
    '''

    def save_plan(self, plan: ITrajectoryReadOnly, filepath: str) -> None:
        '''
            Saves current trajectory plan to JSON file path.

            :param plan: ITrajectoryReadOnly instance to save.
            :param filepath: Target JSON file path.
        '''

    def save_text_file(self, content: str, filepath: str) -> None:
        '''
            Writes text content to file path using UTF-8 encoding.

            :param content: String text to write.
            :param filepath: Destination file path.
        '''

    def save_binary_program(self, program: BinaryProgram, filepath: str) -> None:
        '''
            Writes compiled binary program payload to destination file path.

            :param program: BinaryProgram instance.
            :param filepath: Destination file path.
        '''
