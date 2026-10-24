# -*- coding: UTF-8 -*-

'''
Module
    panel.py
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
    Manipulator override panel composing actuator and speed override sections.
'''

from __future__ import annotations

from tkinter import Widget, X
from tkinter.ttk import Frame

from scarajectory.infrastructure.gui.manipulator.override.actuator import ActuatorSection
from scarajectory.infrastructure.gui.manipulator.override.feedrate import OverrideSection
from scarajectory.infrastructure.gui.manipulator.override.idelegate import IManipulatorActionDelegate

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ManipulatorOverridePanel(Frame):
    '''
        Composite panel orchestrating actuator action buttons and speed override slider.

        It defines:

            :attributes:
                | _actuator_section - Leaf section for actuator and homing buttons.
                | _override_section - Leaf section for feedrate speed override slider.
            :methods:
                | __init__ - Initializes composite override panel and mounts sections.
                | set_pump_active - Updates vacuum pump button indicator based on active state.
                | set_override_label - Updates feedrate override percentage readout label.
                | actuator_section - Returns child actuator section.
                | override_section - Returns child speed override section.
    '''

    _actuator_section: ActuatorSection
    _override_section: OverrideSection

    def __init__(
        self,
        parent: Widget,
        *,
        action_delegate: IManipulatorActionDelegate,
    ) -> None:
        '''
            Initializes composite override panel layout and mounts child sections.

            :param parent: Parent container widget.
            :param action_delegate: Injected action delegate collaborator.
            :exceptions: None.
        '''
        super().__init__(parent)
        self._actuator_section = ActuatorSection(
            self,
            action_delegate=action_delegate,
        )
        self._actuator_section.pack(fill=X, pady=2)

        self._override_section = OverrideSection(
            self,
            action_delegate=action_delegate,
        )
        self._override_section.pack(fill=X, pady=2)

    def set_pump_active(self, active: bool) -> None:
        '''
            Updates vacuum pump button indicator based on active state.

            :param active: True if pump is active, False otherwise.
            :exceptions: None.
        '''
        self._actuator_section.set_pump_active(active)

    def set_override_label(self, pct: int) -> None:
        '''
            Updates feedrate override percentage readout label.

            :param pct: Speed override percentage (10 to 200).
            :exceptions: None.
        '''
        self._override_section.set_override_label(pct)

    @property
    def actuator_section(self) -> ActuatorSection:
        '''
            Returns child actuator section.

            :return: ActuatorSection instance.
            :exceptions: None.
        '''
        return self._actuator_section

    @property
    def override_section(self) -> OverrideSection:
        '''
            Returns child speed override section.

            :return: OverrideSection instance.
            :exceptions: None.
        '''
        return self._override_section
