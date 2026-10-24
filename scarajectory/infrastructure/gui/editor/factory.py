# -*- coding: UTF-8 -*-

'''
Module
    factory.py
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
    Factory providing WaypointEditor instances.
'''

from __future__ import annotations

from tkinter import Widget

from scarajectory.infrastructure.gui.editor.applier.factory import WaypointEditApplierFactory
from scarajectory.infrastructure.gui.editor.applier.iapplier import IWaypointEditApplier
from scarajectory.infrastructure.gui.editor.editor import WaypointEditor
from scarajectory.infrastructure.gui.editor.table.bundle import TableBundle
from scarajectory.infrastructure.gui.editor.table.factory import TrajectoryTableFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class WaypointEditorFactory:
    '''
        Factory providing WaypointEditor instances.

        It defines:

            :methods:
                | create - Constructs a new WaypointEditor instance with default collaborators.
                | create_with_collaborators - Constructs WaypointEditor with explicit collaborators.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        parent: Widget,
        *,
        bundle: TableBundle,
    ) -> WaypointEditor:
        '''
            Constructs a new WaypointEditor instance with default collaborators.

            :param parent: Parent container widget.
            :param bundle: Injected TableBundle instance.
            :return: Instance of WaypointEditor.
            :exceptions: None.
        '''
        return cls.create_with_collaborators(
            parent,
            bundle=bundle,
            table_factory=TrajectoryTableFactory,
            applier=WaypointEditApplierFactory.create(),
        )

    @classmethod
    def create_with_collaborators(
        cls,
        parent: Widget,
        *,
        bundle: TableBundle,
        table_factory: type[TrajectoryTableFactory],
        applier: IWaypointEditApplier,
    ) -> WaypointEditor:
        '''
            Constructs a new WaypointEditor instance with explicit collaborators.

            :param parent: Parent container widget.
            :param bundle: Injected TableBundle instance.
            :param table_factory: Factory type constructing TrajectoryTable.
            :param applier: Injected IWaypointEditApplier instance.
            :return: Instance of WaypointEditor.
            :exceptions: None.
        '''
        return WaypointEditor(
            parent,
            bundle=bundle,
            table_factory=table_factory,
            applier=applier,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
