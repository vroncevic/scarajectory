# -*- coding: UTF-8 -*-

'''
Module
    app_presentation_assembler.py
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
    Dedicated sub-assembler for GUI, CLI, and presentation adapters.
'''

from __future__ import annotations

from ats_utilities.base.setup.bundle import BaseBundle
from scarajectory.core.service.engine import Service
from scarajectory.core.service.service_factory import ServiceFactory
from scarajectory.infrastructure.cli.engine import CLI
from scarajectory.infrastructure.cli.setup.bundle import CLIBundle
from scarajectory.infrastructure.cli.setup.factory import CLIBundleFactory
from scarajectory.infrastructure.cli.setup.options import CLIBundleOptions
from scarajectory.infrastructure.gui.scarajectory_gui import ScarajectoryGUI
from scarajectory.infrastructure.gui.scarajectory_gui_factory import ScarajectoryGUIFactory
from scarajectory.infrastructure.gui.scarajectory_gui_init_bundle import ScarajectoryGUIInitBundle
from scarajectory.setup.assembly.app_core_bundle import AppCoreBundle
from scarajectory.setup.assembly.app_runtime_bundle import AppRuntimeBundle
from scarajectory.setup.bundle import SCARAjectoryBundle
from scarajectory.setup.dependencies import SCARAjectoryBundleDependencies
from scarajectory.setup.pipeline.dsl_pipeline_builder import DslPipelineBuilder
from scarajectory.setup.pipeline.dsl_pipeline_bundle import DslPipelineBundle
from scarajectory.setup.pipeline.plan_pipeline_bundle import PlanPipelineBundle
from scarajectory.setup.registry import SCARAjectoryBundleRegistry

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class AppPresentationAssembler:
    '''
        Assembles presentation GUI, CLI, DSL and bundles top-level package.

        It defines:

            :methods:
                | assemble - Constructs GUI, CLI, and top-level bundle.
                | get_version - Returns assembler version string.
    '''

    @classmethod
    def assemble(
        cls,
        base_bundle: BaseBundle,
        core_bundle: AppCoreBundle,
        runtime_bundle: AppRuntimeBundle,
        plan_bundle: PlanPipelineBundle,
    ) -> SCARAjectoryBundle:
        '''
            Constructs GUI, CLI, and top-level application bundle.

            :param base_bundle: BaseBundle framework foundation.
            :param core_bundle: AppCoreBundle core kinematics and validation.
            :param runtime_bundle: AppRuntimeBundle runtime storage.
            :param plan_bundle: PlanPipelineBundle trajectory plan interfaces.
            :return: Fully assembled SCARAjectoryBundle instance.
            :exceptions: None.
        '''
        dsl_bundle: DslPipelineBundle = DslPipelineBuilder.build(
            validator=core_bundle.validator,
        )
        service: Service = ServiceFactory.create(
            validator=core_bundle.validator,
            storage=runtime_bundle.storage,
            store=plan_bundle.store,
            mutation=plan_bundle.mutation,
        )
        gui_init_bundle: ScarajectoryGUIInitBundle = (
            ScarajectoryGUIInitBundle(
                plan=plan_bundle,
                validator=core_bundle.validator,
                streaming=runtime_bundle.streaming,
                storage=runtime_bundle.storage,
                dsl=dsl_bundle,
                connection_repository=runtime_bundle.connection_repo,
            )
        )
        gui: ScarajectoryGUI = ScarajectoryGUIFactory.create(
            bundle=gui_init_bundle,
        )
        cli_bundle: CLIBundle = CLIBundleFactory.create_bundle(
            options=CLIBundleOptions(
                service=service,
                parser=base_bundle.option_manager,
                gui=gui,
            )
        )
        cli: CLI = CLI(bundle=cli_bundle)

        return SCARAjectoryBundleRegistry.create_bundle(
            dependencies=SCARAjectoryBundleDependencies(
                base=base_bundle,
                service=service,
                gui=gui,
                streamer=runtime_bundle.streamer,
                cli=cli,
            )
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns assembler version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
