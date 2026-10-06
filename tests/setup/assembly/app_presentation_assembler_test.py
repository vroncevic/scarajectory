# -*- coding: UTF-8 -*-

'''
Module
    app_presentation_assembler_test.py
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
    Unit tests for AppPresentationAssembler presentation assembly.
'''

from __future__ import annotations

from os.path import abspath, dirname, join
from unittest import TestCase, main

from ats_utilities.base.setup.bundle import BaseBundle
from ats_utilities.base.setup.factory import BaseBundleFactory
from ats_utilities.base.setup.options import BaseBundleOptions
from ats_utilities.context.factory import ContextBundleFactory
from scarajectory.infrastructure.settings.bounds.scara_bounds_loader_factory import ScaraBoundsLoaderFactory
from scarajectory.setup.assembly.app_core_assembler import AppCoreAssembler
from scarajectory.setup.assembly.app_core_bundle import AppCoreBundle
from scarajectory.setup.assembly.app_presentation_assembler import AppPresentationAssembler
from scarajectory.setup.assembly.app_runtime_assembler import AppRuntimeAssembler
from scarajectory.setup.assembly.app_runtime_bundle import AppRuntimeBundle
from scarajectory.setup.bundle import SCARAjectoryBundle
from scarajectory.setup.pipeline.plan_pipeline_builder import PlanPipelineBuilder
from scarajectory.setup.pipeline.plan_pipeline_bundle import PlanPipelineBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestAppPresentationAssembler(TestCase):
    '''
        Test cases for AppPresentationAssembler presentation construction.

        It defines:

            :methods:
                | setUp - Initializes fixtures for base, core, runtime, plan.
                | test_assemble_presentation - Tests top-level bundle assembly.
                | test_get_version - Tests assembler version query.
    '''

    def setUp(self) -> None:
        '''
            Initializes fixtures for base, core, runtime, and plan bundles.

            :exceptions: None.
        '''
        info_file: str = join(
            dirname(dirname(dirname(dirname(abspath(__file__))))),
            'scarajectory', 'infrastructure', 'config', 'scarajectory.cfg'
        )
        self.base_bundle: BaseBundle = BaseBundleFactory.create_bundle(
            options=BaseBundleOptions(
                info_file=info_file,
                use_generator=False,
                context_bundle=ContextBundleFactory.create_bundle(),
            )
        )
        bounds = ScaraBoundsLoaderFactory.create().load_bounds()
        self.core_bundle: AppCoreBundle = AppCoreAssembler.assemble(
            bounds=bounds,
            context_bundle=self.base_bundle.context_bundle,
        )
        self.runtime_bundle: AppRuntimeBundle = AppRuntimeAssembler.assemble(
            context_bundle=self.base_bundle.context_bundle
        )
        self.plan_bundle: PlanPipelineBundle = PlanPipelineBuilder.build()

    def test_assemble_presentation(self) -> None:
        '''
            Tests top-level application bundle assembly.

            :exceptions: None.
        '''
        bundle: SCARAjectoryBundle = AppPresentationAssembler.assemble(
            base_bundle=self.base_bundle,
            core_bundle=self.core_bundle,
            runtime_bundle=self.runtime_bundle,
            plan_bundle=self.plan_bundle,
        )
        self.assertIsInstance(bundle, SCARAjectoryBundle)
        self.assertIsNotNone(bundle.service)
        self.assertIsNotNone(bundle.gui)
        self.assertIsNotNone(bundle.cli)
        self.assertIsNotNone(bundle.streamer)

    def test_get_version(self) -> None:
        '''
            Tests assembler version query.

            :exceptions: None.
        '''
        version: str = AppPresentationAssembler.get_version()
        self.assertIsInstance(version, str)
        self.assertTrue(len(version) > 0)


if __name__ == '__main__':
    main()
