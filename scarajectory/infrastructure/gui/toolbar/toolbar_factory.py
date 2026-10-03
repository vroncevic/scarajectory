# -*- coding: UTF-8 -*-

'''
Module
    toolbar_factory.py
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
    Factory module for assembling and instantiating Toolbar GUI components.
'''

from __future__ import annotations

from tkinter import Widget

from scarajectory.infrastructure.gui.toolbar.toolbar import Toolbar
from scarajectory.infrastructure.gui.toolbar.bundle import ToolbarBundle
from scarajectory.infrastructure.gui.toolbar.parameter_inputs_bundle import ParameterInputsBundle
from scarajectory.infrastructure.gui.toolbar.tool_selector_factory import ToolbarToolSelectorFactory
from scarajectory.infrastructure.gui.toolbar.navigation_controls_factory import ToolbarNavigationControlsFactory
from scarajectory.infrastructure.gui.toolbar.parameter_inputs_factory import ToolbarParameterInputsFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ToolbarFactory:
    '''
        Factory responsible for assembling Toolbar instances.

        It defines:

            :methods:
                | create - Assembles and instantiates a Toolbar widget.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls, parent: Widget, bundle: ToolbarBundle) -> Toolbar:
        '''
            Assembles and instantiates a Toolbar widget using parameter bundle.

            :param parent: Parent container widget.
            :param bundle: Injected ToolbarBundle collaborator and settings bundle.
            :return: Fully assembled Toolbar instance.
            :exceptions: None.
        '''
        toolbar = Toolbar(parent)
        tool_selector = ToolbarToolSelectorFactory.create(toolbar, bundle.canvas)
        nav_controls = ToolbarNavigationControlsFactory.create(
            toolbar, bundle.navigator, bundle.history
        )
        param_bundle = ParameterInputsBundle(
            canvas=bundle.canvas,
            status_presenter=bundle.status_presenter,
            r_min=bundle.r_min,
            r_max=bundle.r_max,
            settings=bundle.settings,
        )
        param_inputs = ToolbarParameterInputsFactory.create(toolbar, param_bundle)
        toolbar.mount_controls(
            tool_selector=tool_selector,
            nav_controls=nav_controls,
            param_inputs=param_inputs,
        )

        return toolbar

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
