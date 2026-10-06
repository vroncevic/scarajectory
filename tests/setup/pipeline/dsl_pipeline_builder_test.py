# -*- coding: UTF-8 -*-

'''
Module
    dsl_pipeline_builder_test.py
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

from scaralang.core.model.kinematics.scara_bounds import ScaraBounds
from scaralang.core.service.compiler.iscara_compiler import IScaraCompiler
from scaralang.core.service.compiler.plan.iscara_plan_compiler import IScaraPlanCompiler
from scaralang.core.service.decompiler.iscara_decompiler import IScaraDecompiler
from scaralang.core.service.exporter.scara.iscara_plan_exporter import IScaraPlanExporter
from scaralang.core.service.kinematics.ikinematics_service import IKinematicsService
from scaralang.core.service.kinematics.kinematics_service_factory import KinematicsServiceFactory
from scaralang.core.service.linter.script.iscara_dsl_validator import IScaraDslValidator
from scaralang.core.service.trajectory.validation.itrajectory_validator import ITrajectoryValidator
from scaralang.core.service.trajectory.validation.trajectory_validator_factory import TrajectoryValidatorFactory
from scarajectory.infrastructure.settings.bounds.scara_bounds_loader_factory import ScaraBoundsLoaderFactory
from scarajectory.setup.pipeline.dsl_pipeline_builder import DslPipelineBuilder
from scarajectory.setup.pipeline.dsl_pipeline_bundle import DslPipelineBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DslPipelineBuilderTestCase(TestCase):
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
        bounds: ScaraBounds = ScaraBoundsLoaderFactory.create().load_bounds()
        kinematics: IKinematicsService = KinematicsServiceFactory.create(
            bounds=bounds,
        )
        validator: ITrajectoryValidator = TrajectoryValidatorFactory.create(
            kinematics=kinematics,
        )
        bundle: DslPipelineBundle = DslPipelineBuilder.build(
            validator=validator,
        )
        self.assertIsInstance(bundle, DslPipelineBundle)
        self.assertIsInstance(bundle.compiler, IScaraCompiler)
        self.assertIsInstance(bundle.decompiler, IScaraDecompiler)
        self.assertIsInstance(bundle.plan_compiler, IScaraPlanCompiler)
        self.assertIsInstance(bundle.plan_exporter, IScaraPlanExporter)
        self.assertIsInstance(bundle.validator, IScaraDslValidator)

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
