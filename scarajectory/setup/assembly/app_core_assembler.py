# -*- coding: UTF-8 -*-

'''
Module
    app_core_assembler.py
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
    Dedicated sub-assembler for kinematics, validation, and parameters.
'''

from __future__ import annotations

from ats_utilities.context.bundle import ContextBundle
from scaralang.core.model.kinematics.scara_bounds import ScaraBounds
from scaralang.core.model.kinematics.transmission_parameters import TransmissionParameters
from scaralang.core.service.kinematics.ikinematics_service import IKinematicsService
from scaralang.core.service.kinematics.kinematics_service_factory import KinematicsServiceFactory
from scaralang.core.service.trajectory.validation.itrajectory_validator import ITrajectoryValidator
from scaralang.core.service.trajectory.validation.trajectory_validator_factory import TrajectoryValidatorFactory
from scarajectory.core.service.settings.iscara_transmission_loader import IScaraTransmissionLoader
from scarajectory.infrastructure.settings.settings_reader import SettingsReader
from scarajectory.infrastructure.settings.settings_reader_factory import SettingsReaderFactory
from scarajectory.infrastructure.settings.transmission.scara_transmission_loader_factory import ScaraTransmissionLoaderFactory
from scarajectory.setup.assembly.app_core_bundle import AppCoreBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class AppCoreAssembler:
    '''
        Assembles domain core kinematics and trajectory validation subsystems.

        It defines:

            :methods:
                | assemble - Constructs kinematics, validation, and parameters.
                | get_version - Returns assembler version string.
    '''

    @classmethod
    def assemble(
        cls,
        *,
        bounds: ScaraBounds,
        context_bundle: ContextBundle,
    ) -> AppCoreBundle:
        '''
            Constructs kinematics, validation, and transmission core bundle.

            :param bounds: Resolved ScaraBounds workspace bounds.
            :param context_bundle: Shared ATS ContextBundle instance.
            :return: AppCoreBundle holding configured core services.
            :exceptions: None.
        '''
        reader: SettingsReader = SettingsReaderFactory.create_with_context(
            context_bundle=context_bundle
        )
        trans_loader: IScaraTransmissionLoader = (
            ScaraTransmissionLoaderFactory.create_with_reader(reader=reader)
        )
        transmission: TransmissionParameters = (
            trans_loader.load_transmission()
        )
        kinematics: IKinematicsService = KinematicsServiceFactory.create(
            bounds=bounds,
        )
        validator: ITrajectoryValidator = TrajectoryValidatorFactory.create(
            kinematics=kinematics,
        )
        return AppCoreBundle(
            bounds=bounds,
            transmission=transmission,
            kinematics=kinematics,
            validator=validator,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns assembler version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
