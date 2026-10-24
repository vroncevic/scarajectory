# -*- coding: UTF-8 -*-

'''
Module
    assembler.py
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

from scaralang.core.model.kinematics.profile.bounds import ScaraBounds
from scaralang.core.model.kinematics.profile.transmission import TransmissionParameters
from scaralang.core.service.kinematics.dependencies import KinematicsDependencies
from scaralang.core.service.kinematics.factory import KinematicsFactory
from scaralang.core.service.kinematics.profile.default_scara_profile import DefaultScaraProfile
from scaralang.core.service.kinematics.provides import KinematicsProvides
from scaralang.core.service.trajectory.validation.dependencies import ValidationDependencies
from scaralang.core.service.trajectory.validation.factory import ValidationFactory
from scaralang.core.service.trajectory.validation.provides import ValidationProvides

from scarajectory.core.service.trajectory.validation.ivalidator import ITrajectoryValidator
from scarajectory.infrastructure.scaralang.dependencies import ScaralangDependencies
from scarajectory.infrastructure.scaralang.factory import ScaralangFactory
from scarajectory.infrastructure.scaralang.provides import ScaralangProvides
from scarajectory.infrastructure.scaralang.validation.dependencies import TrajectoryValidationDependencies
from scarajectory.infrastructure.scaralang.validation.factory import TrajectoryValidationAdapterFactory
from scarajectory.infrastructure.settings.dependencies import SettingsDependencies
from scarajectory.infrastructure.settings.factory import SettingsFactory
from scarajectory.infrastructure.settings.provides import SettingsProvides
from scarajectory.infrastructure.settings.reader.reader import SettingsReader
from scarajectory.infrastructure.storage.config_io.dependencies import ConfigIODependencies
from scarajectory.infrastructure.storage.config_io.factory import ConfigIOFactory
from scarajectory.setup.assembly.core.bundle import AppCoreBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
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
        io_provides = ConfigIOFactory.create(
            ConfigIODependencies(context_bundle=context_bundle)
        )
        settings_provides: SettingsProvides = SettingsFactory.create(
            SettingsDependencies(
                config_loader=io_provides.config_loader,
                config_path=SettingsReader.DEFAULT_GEOMETRY_CONFIG,
                scheme_path=SettingsReader.DEFAULT_SCHEME_CONFIG,
            )
        )
        transmission: TransmissionParameters = (
            settings_provides.transmission_provides.transmission_loader.load_transmission()
        )
        kinematics_provides: KinematicsProvides = KinematicsFactory.create(
            dependencies=KinematicsDependencies(
                bounds=bounds,
                dls_config=DefaultScaraProfile.create_dls_config(),
            )
        )
        validation_provides: ValidationProvides = ValidationFactory.create(
            dependencies=ValidationDependencies(
                workspace=kinematics_provides.workspace,
                envelope=kinematics_provides.envelope,
            )
        )
        validator: ITrajectoryValidator = TrajectoryValidationAdapterFactory.create(
            dependencies=TrajectoryValidationDependencies(
                workspace_envelope=kinematics_provides.envelope,
                waypoint_validator=validation_provides.waypoint,
                plan_validator=validation_provides.plan,
            )
        )
        scaralang_provides: ScaralangProvides = ScaralangFactory.create(
            dependencies=ScaralangDependencies(bounds=bounds)
        )

        return AppCoreBundle(
            bounds=bounds,
            transmission=transmission,
            kinematics=kinematics_provides,
            validator=validator,
            avoidance_adapter=scaralang_provides.dead_zone_avoidance,
            planner_adapter=scaralang_provides.shape_planner,
            boundary_adapter=scaralang_provides.boundary,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns assembler version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
