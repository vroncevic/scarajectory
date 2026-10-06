# -*- coding: UTF-8 -*-

'''
Module
    controls_panel_factory.py
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
    Factory service constructing ControlsPanel instances.
'''

from __future__ import annotations

from tkinter import Widget

from scarajectory.infrastructure.gui.controls.bundle import ControlsBundle
from scarajectory.infrastructure.gui.controls.controls_panel import ControlsPanel
from scarajectory.infrastructure.gui.controls.itabs_assembler import ITabsAssembler
from scarajectory.infrastructure.gui.controls.tabs_assembler_factory import ControlsTabsAssemblerFactory
from scarajectory.infrastructure.gui.controls.tabs_bundle import ControlsTabsBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ControlsPanelFactory:
    '''
        Factory providing instantiation of ControlsPanel components.

        It defines:

            :methods:
                | create - Constructs ControlsPanel and mounts child tabs.
                | create_with_assembler - Constructs ControlsPanel with custom tabs assembler.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        parent: Widget,
        bundle: ControlsBundle,
    ) -> ControlsPanel:
        '''
            Constructs ControlsPanel and mounts child tabs using default assembler.

            :param parent: Parent container widget.
            :param bundle: Injected ControlsBundle dependency container.
            :return: Assembled ControlsPanel instance.
            :exceptions: None.
        '''
        assembler: ITabsAssembler = ControlsTabsAssemblerFactory.create()

        return cls.create_with_assembler(
            parent=parent,
            bundle=bundle,
            assembler=assembler,
        )

    @classmethod
    def create_with_assembler(
        cls,
        parent: Widget,
        bundle: ControlsBundle,
        assembler: ITabsAssembler,
    ) -> ControlsPanel:
        '''
            Constructs ControlsPanel and mounts child tabs using injected assembler.

            :param parent: Parent container widget.
            :param bundle: Injected ControlsBundle dependency container.
            :param assembler: Injected ITabsAssembler strategy.
            :return: Assembled ControlsPanel instance.
            :exceptions: None.
        '''
        panel = ControlsPanel(parent)
        tabs: ControlsTabsBundle = assembler.assemble_tabs(
            panel.notebook, bundle
        )
        panel.mount_tabs(tabs)

        return panel

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns component version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
