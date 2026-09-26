# -*- coding: UTF-8 -*-

'''
Module
    step_discretizer_factory.py
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
    Factory instantiating and wiring StepDiscretizer component with kinematics and transmission.
'''

from __future__ import annotations

from scarajectory.core.model.kinematics.transmission_parameters import TransmissionParameters
from scarajectory.core.service.dsl.binary.step.istep_discretizer import IStepDiscretizer
from scarajectory.core.service.dsl.binary.step.step_discretizer import StepDiscretizer
from scarajectory.core.service.kinematics.ikinematics_service import IKinematicsService

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StepDiscretizerFactory:
    '''
        Factory instantiating and wiring StepDiscretizer component.

        It defines:

            :methods:
                | create - Builds StepDiscretizer instance with injected models.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls, *, kinematics: IKinematicsService, transmission: TransmissionParameters) -> IStepDiscretizer:
        '''
            Builds StepDiscretizer instance with injected models.

            :param kinematics: Injected IKinematicsService instance.
            :param transmission: Injected TransmissionParameters instance.
            :return: IStepDiscretizer structural protocol instance.
            :exceptions: None.
        '''
        return StepDiscretizer(kinematics=kinematics, transmission=transmission)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
