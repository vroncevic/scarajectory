# -*- coding: UTF-8 -*-

'''
Module
    assembler_test.py
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
    Unit tests for DslPipelineBuilder component.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.kinematics.profile.bounds import ScaraBounds
from scaralang.core.service.compiler.icompiler import IScaraCompiler
from scaralang.core.service.compiler.plan.script.icompiler import IScriptPlanCompiler
from scaralang.core.service.decompiler.idecompiler import IScaraDecompiler
from scaralang.core.service.exporter.scara.iexporter import IScaraPlanExporter
from scaralang.core.service.kinematics.dependencies import KinematicsDependencies
from scaralang.core.service.kinematics.factory import KinematicsFactory
from scaralang.core.service.kinematics.profile.default_scara_profile import DefaultScaraProfile
from scaralang.core.service.kinematics.provides import KinematicsProvides
from scaralang.core.service.linter.validator.ivalidator import IScriptValidator
from scaralang.core.service.trajectory.validation.dependencies import ValidationDependencies
from scaralang.core.service.trajectory.validation.factory import ValidationFactory
from scaralang.core.service.trajectory.validation.provides import ValidationProvides

from scarajectory.core.service.trajectory.validation.ivalidator import ITrajectoryValidator
from scarajectory.infrastructure.scaralang.validation.dependencies import TrajectoryValidationDependencies
from scarajectory.infrastructure.scaralang.validation.factory import TrajectoryValidationAdapterFactory
from scarajectory.setup.factory import SCARAjectoryBundleFactory
from scarajectory.setup.assembly.dsl.assembler import DslPipelineBuilder
from scarajectory.setup.assembly.dsl.bundle import DslPipelineBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DslPipelineAssemblerTest(TestCase):
    '''
        Tests assembling the DSL pipeline through DslPipelineBuilder.

        It defines:

            :methods:
                | test_build_pipeline - Verifies successful pipeline assembly.
                | test_get_version - Verifies version string retrieval.
    '''

    def test_build_pipeline(self) -> None:
        '''
            Tests DslPipelineBuilder.build assembling DslPipelineBundle.

            :exceptions: None.
        '''
        bounds: ScaraBounds = SCARAjectoryBundleFactory.resolve_bounds()
        kinematics_provides: KinematicsProvides = KinematicsFactory.create(
            dependencies=KinematicsDependencies(
                bounds=bounds,
                dls_config=DefaultScaraProfile.create_dls_config(),
            ),
        )
        validation_provides: ValidationProvides = ValidationFactory.create(
            dependencies=ValidationDependencies(
                workspace=kinematics_provides.workspace,
                envelope=kinematics_provides.envelope,
            ),
        )
        validator: ITrajectoryValidator = TrajectoryValidationAdapterFactory.create(
            dependencies=TrajectoryValidationDependencies(
                workspace_envelope=kinematics_provides.envelope,
                waypoint_validator=validation_provides.waypoint,
                plan_validator=validation_provides.plan,
            ),
        )
        bundle: DslPipelineBundle = DslPipelineBuilder.build(
            validator=validator,
        )
        self.assertIsInstance(bundle, DslPipelineBundle)
        self.assertIsInstance(bundle.compiler, IScaraCompiler)
        self.assertIsInstance(bundle.decompiler, IScaraDecompiler)
        self.assertIsInstance(bundle.plan_compiler, IScriptPlanCompiler)
        self.assertIsInstance(bundle.plan_exporter, IScaraPlanExporter)
        self.assertIsInstance(bundle.validator, IScriptValidator)

    def test_get_version(self) -> None:
        '''
            Verifies builder version string format and presence.

            :exceptions: None.
        '''
        version: str = DslPipelineBuilder.get_version()
        self.assertIsInstance(version, str)
        self.assertTrue(len(version) > 0)


if __name__ == '__main__':
    main()
