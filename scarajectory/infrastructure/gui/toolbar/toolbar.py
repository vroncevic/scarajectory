# -*- coding: UTF-8 -*-

'''
Module
    toolbar.py
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
    Top toolbar housing CAD drawing tools, zoom controls, plan undo/redo
    and default settings.
'''

from __future__ import annotations

from tkinter import LEFT, VERTICAL, Widget, X, Y
from tkinter.ttk import Frame, Label, Separator

from scarajectory.infrastructure.gui.toolbar.tool_selector import ToolbarToolSelector
from scarajectory.infrastructure.gui.toolbar.navigation_controls import ToolbarNavigationControls
from scarajectory.infrastructure.gui.toolbar.parameter_inputs import ToolbarParameterInputs

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class Toolbar(Frame):
    '''
        Application toolbar for mode selection, CAD actions, and kinematic
        defaults.

        It defines:

            :attributes:
                | _tool_selector - CAD tool mode selector subcomponent.
                | _nav_controls - Navigation and history controls component.
                | _param_inputs - Parameter defaults and cursor component.
            :methods:
                | __init__ - Initializes toolbar container.
                | mount_controls - Mounts injected toolbar sub-panels.
                | set_deadzone - Sets deadzone enforcement checkbox state.
                | get_cursor_label - Returns cursor info label widget.
    '''

    _tool_selector: ToolbarToolSelector
    _nav_controls: ToolbarNavigationControls
    _param_inputs: ToolbarParameterInputs

    def __init__(self, parent: Widget) -> None:
        '''
            Initializes toolbar container.

            :param parent: Parent container widget.
            :exceptions: None.
        '''
        super().__init__(parent, padding=(8, 6))

    def mount_controls(
        self,
        tool_selector: ToolbarToolSelector,
        nav_controls: ToolbarNavigationControls,
        param_inputs: ToolbarParameterInputs,
    ) -> None:
        '''
            Mounts injected toolbar sub-panels.

            :param tool_selector: Tool selector component.
            :param nav_controls: Navigation controls component.
            :param param_inputs: Parameter inputs component.
            :exceptions: None.
        '''
        self._tool_selector = tool_selector
        self._tool_selector.pack(side=LEFT)

        Separator(self, orient=VERTICAL).pack(side=LEFT, fill=Y, padx=8)
        self._nav_controls = nav_controls
        self._nav_controls.pack(side=LEFT)

        Separator(self, orient=VERTICAL).pack(side=LEFT, fill=Y, padx=8)
        self._param_inputs = param_inputs
        self._param_inputs.pack(side=LEFT, fill=X, expand=True)

    def set_deadzone(self, enabled: bool) -> None:
        '''
            Sets deadzone enforcement checkbox state.

            :param enabled: True to enforce deadzone, False to disable.
            :exceptions: None.
        '''
        self._param_inputs.set_deadzone(enabled)

    def get_cursor_label(self) -> Label:
        '''
            Returns cursor info label widget.

            :return: Label widget displaying coordinates and zoom.
            :exceptions: None.
        '''
        return self._param_inputs.get_cursor_label()
