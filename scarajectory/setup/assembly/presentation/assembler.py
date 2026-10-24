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
    Dedicated sub-assembler for GUI, CLI, and presentation adapters.
'''

from __future__ import annotations

from ats_utilities.base.setup.bundle import BaseBundle

from scarajectory.infrastructure.cli.dependencies import CLIDependencies
from scarajectory.infrastructure.cli.factory import CLIFactory
from scarajectory.infrastructure.cli.icli import ICLI
from scarajectory.infrastructure.cli.setup.bundle import CLIBundle
from scarajectory.infrastructure.cli.setup.factory import CLIBundleFactory
from scarajectory.infrastructure.cli.setup.options import CLIBundleOptions
from scarajectory.infrastructure.gui.dependencies import GUIDependencies
from scarajectory.infrastructure.gui.factory import GUIFactory
from scarajectory.infrastructure.gui.igui import IGUI
from scarajectory.infrastructure.gui.provides import GUIProvides
from scarajectory.infrastructure.gui.storage_dependencies import StorageDependencies
from scarajectory.infrastructure.scaralang.provides import ScaralangProvides
from scarajectory.setup.assembly.core.bundle import AppCoreBundle
from scarajectory.setup.assembly.dsl.assembler import DslPipelineBuilder
from scarajectory.setup.assembly.dsl.bundle import DslPipelineBundle
from scarajectory.setup.assembly.plan.bundle import PlanPipelineBundle
from scarajectory.setup.assembly.runtime.bundle import AppRuntimeBundle
from scarajectory.setup.bundle import SCARAjectoryBundle
from scarajectory.setup.dependencies import SCARAjectoryBundleDependencies
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
        gui_dependencies: GUIDependencies = (
            GUIDependencies(
                plan=plan_bundle,
                validator=core_bundle.validator,
                streaming=runtime_bundle.streaming,
                dsl=dsl_bundle,
                connection_repository=runtime_bundle.connection_repo,
                storage=StorageDependencies(
                    loader=runtime_bundle.loader,
                    storer=runtime_bundle.storer,
                    workspace=runtime_bundle.workspace,
                ),
                scaralang=ScaralangProvides(
                    dead_zone_avoidance=core_bundle.avoidance_adapter,
                    shape_planner=core_bundle.planner_adapter,
                    boundary=core_bundle.boundary_adapter,
                ),
            )
        )
        gui_provides: GUIProvides = GUIFactory.create(gui_dependencies)
        gui: IGUI = gui_provides.gui
        cli_bundle: CLIBundle = CLIBundleFactory.create_bundle(
            options=CLIBundleOptions(
                parser=base_bundle.option_manager,
                gui=gui,
            )
        )
        cli_dependencies: CLIDependencies = CLIDependencies(bundle=cli_bundle)
        cli: ICLI = CLIFactory.create(cli_dependencies).cli

        dependencies: SCARAjectoryBundleDependencies = {
            'base': base_bundle,
            'gui': gui,
            'streamer': runtime_bundle.streamer,
            'cli': cli,
        }
        return SCARAjectoryBundleRegistry.create_bundle(dependencies)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns assembler version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
