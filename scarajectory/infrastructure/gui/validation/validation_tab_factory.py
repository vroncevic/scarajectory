# -*- coding: UTF-8 -*-

'''
Module
    validation_tab_factory.py
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
    Factory module for creating and configuring ValidationTab instances.
'''

from __future__ import annotations

from tkinter import Widget

from scaralang.core.service.trajectory.validation.itrajectory_validator import ITrajectoryValidator

from scarajectory.core.service.trajectory.plan.itrajectory_read_only import ITrajectoryReadOnly
from scarajectory.infrastructure.gui.validation.validation_tab import ValidationTab

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ValidationTabFactory:
    '''
        Factory creating ValidationTab components.

        It defines:

            :methods:
                | create - Constructs and configures a ValidationTab instance.
                | get_version - Returns factory module semantic version string.
    '''

    @classmethod
    def create(
        cls,
        parent: Widget,
        *,
        plan: ITrajectoryReadOnly,
        validator: ITrajectoryValidator,
    ) -> ValidationTab:
        '''
            Constructs and configures a ValidationTab instance.

            :param parent: Parent container widget.
            :param plan: Active ITrajectoryReadOnly instance.
            :param validator: ITrajectoryValidator instance.
            :return: Configured ValidationTab instance.
            :exceptions: None.
        '''
        return ValidationTab(
            parent,
            plan=plan,
            validator=validator,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory module semantic version string.

            :return: Semantic version string (__version__).
            :exceptions: None.
        '''
        return __version__
