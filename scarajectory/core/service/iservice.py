# -*- coding: UTF-8 -*-

'''
Module
    iservice.py
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
    Defines abstract interface IService for trajectory business logic.
'''

from __future__ import annotations

from abc import ABC, abstractmethod

from scarajectory.core.model.trajectory_plan import TrajectoryPlan
from scarajectory.core.service.itrajectory_validator import ITrajectoryValidator
from scarajectory.core.service.iserial_streamer import ISerialStreamer

__author__: str = 'Vladimir Roncevic'
__copyright__: str = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__: list[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__: str = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__: str = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class IService(ABC):
    '''
        Abstract interface for orchestrating trajectory operations and services.

        It defines:

            :methods:
                | is_initialized - Checks if the service is properly initialized.
                | get_plan - Returns the active TrajectoryPlan.
                | get_validator - Returns the active ITrajectoryValidator.
                | get_streamer - Returns the active ISerialStreamer.
                | validate_plan - Validates the current trajectory plan.
                | save_plan - Saves current plan to file path.
                | load_plan - Loads plan from file path.
                | start_streaming - Initiates streaming of current plan.
                | stop_streaming - Aborts active streaming.
    '''

    @abstractmethod
    def is_initialized(self) -> bool:
        '''
            Checks if the service is properly initialized.

            :return: True if initialized, False otherwise.
            :exceptions: None.
        '''

    @abstractmethod
    def get_plan(self) -> TrajectoryPlan:
        '''
            Returns the active TrajectoryPlan.

            :return: TrajectoryPlan instance.
            :exceptions: None.
        '''

    @abstractmethod
    def get_validator(self) -> ITrajectoryValidator:
        '''
            Returns the active ITrajectoryValidator.

            :return: ITrajectoryValidator instance.
            :exceptions: None.
        '''

    @abstractmethod
    def get_streamer(self) -> ISerialStreamer:
        '''
            Returns the active ISerialStreamer.

            :return: ISerialStreamer instance.
            :exceptions: None.
        '''

    @abstractmethod
    def validate_plan(self) -> tuple[bool, list[str]]:
        '''
            Validates the current trajectory plan against robot kinematic bounds.

            :return: Tuple of (is_valid, messages_list).
            :exceptions: None.
        '''

    @abstractmethod
    def save_plan(self, filepath: str) -> None:
        '''
            Saves current plan to file path.

            :param filepath: Target file path.
            :exceptions: OSError.
        '''

    @abstractmethod
    def load_plan(self, filepath: str) -> None:
        '''
            Loads plan from file path.

            :param filepath: Source file path.
            :exceptions: OSError.
        '''

    @abstractmethod
    def start_streaming(self) -> bool:
        '''
            Initiates streaming of current plan.

            :return: True if stream started, False otherwise.
            :exceptions: None.
        '''

    @abstractmethod
    def stop_streaming(self) -> None:
        '''
            Aborts active streaming.

            :exceptions: None.
        '''
