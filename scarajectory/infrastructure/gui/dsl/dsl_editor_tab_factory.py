# -*- coding: UTF-8 -*-

'''
Module
    dsl_editor_tab_factory.py
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
    Factory module for assembling and instantiating DslEditorTab components.
'''

from __future__ import annotations

from tkinter import Widget

from scarajectory.core.service.trajectory.plan.itrajectory_plan import ITrajectoryPlan
from scaralang.core.service.dsl.iscara_dsl_service import IScaraDslService
from scarajectory.core.service.trajectory.contract.iplan_storage_service import IPlanStorageService
from scarajectory.infrastructure.gui.dsl.dsl_document_manager import DslDocumentManager
from scarajectory.infrastructure.gui.dsl.dsl_editor_tab import DslEditorTab
from scarajectory.infrastructure.gui.dsl.dsl_example_catalog import DslExampleCatalog
from scarajectory.infrastructure.gui.dsl.iemulator_launcher import IEmulatorLauncher

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DslEditorTabFactory:
    '''
        Factory responsible for assembling DslEditorTab GUI instances.

        It defines:

            :methods:
                | create - Assembles and instantiates a DslEditorTab with standard collaborators.
                | create_with_collaborators - Assembles a DslEditorTab with explicit collaborators.
    '''

    @classmethod
    def create(
        cls,
        parent: Widget,
        *,
        plan: ITrajectoryPlan,
        dsl_service: IScaraDslService,
        storage: IPlanStorageService,
        **kwargs: object,
    ) -> DslEditorTab:
        '''
            Assembles and instantiates a DslEditorTab with standard collaborators.

            :param parent: Parent container widget.
            :param plan: Active ITrajectoryPlan instance.
            :param dsl_service: Required IScaraDslService instance.
            :param storage: Required IPlanStorageService instance.
            :return: Fully assembled DslEditorTab.
            :exceptions: None.
        '''
        return DslEditorTab(
            parent,
            plan=plan,
            dsl_service=dsl_service,
            storage=storage,
            **kwargs,
        )

    @classmethod
    def create_with_collaborators(
        cls,
        parent: Widget,
        *,
        plan: ITrajectoryPlan,
        dsl_service: IScaraDslService,
        storage: IPlanStorageService,
        launcher: IEmulatorLauncher,
        catalog: DslExampleCatalog,
        document_manager: DslDocumentManager,
        **kwargs: object,
    ) -> DslEditorTab:
        '''
            Assembles and instantiates a DslEditorTab with explicit collaborators.

            :param parent: Parent container widget.
            :param plan: Active ITrajectoryPlan instance.
            :param dsl_service: Required IScaraDslService instance.
            :param storage: Required IPlanStorageService instance.
            :param launcher: Required IEmulatorLauncher instance.
            :param catalog: Required DslExampleCatalog instance.
            :param document_manager: Required DslDocumentManager instance.
            :return: Fully assembled DslEditorTab.
            :exceptions: None.
        '''
        return DslEditorTab(
            parent,
            plan=plan,
            dsl_service=dsl_service,
            storage=storage,
            launcher=launcher,
            catalog=catalog,
            document_manager=document_manager,
            **kwargs,
        )

