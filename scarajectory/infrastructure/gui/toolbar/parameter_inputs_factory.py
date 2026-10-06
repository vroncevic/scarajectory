# -*- coding: UTF-8 -*-

'''
Module
    parameter_inputs_factory.py
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
    Factory for instantiating ToolbarParameterInputs components.
'''

from __future__ import annotations

from tkinter import Widget

from scarajectory.infrastructure.gui.toolbar.parameter_inputs import ToolbarParameterInputs
from scarajectory.infrastructure.gui.toolbar.parameter_inputs_bundle import ParameterInputsBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ToolbarParameterInputsFactory:
    '''
        Factory responsible for creating ToolbarParameterInputs instances.

        It defines:

            :methods:
                | get_version - Returns factory version string.
                | create - Creates a ToolbarParameterInputs widget instance.
    '''

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__

    @classmethod
    def create(
        cls,
        parent: Widget,
        bundle: ParameterInputsBundle,
    ) -> ToolbarParameterInputs:
        '''
            Creates a ToolbarParameterInputs widget instance.

            :param parent: Parent container widget.
            :param bundle: ParameterInputsBundle containing dependencies and bounds.
            :return: Fully configured ToolbarParameterInputs instance.
            :exceptions: None.
        '''
        return ToolbarParameterInputs(parent, bundle)
