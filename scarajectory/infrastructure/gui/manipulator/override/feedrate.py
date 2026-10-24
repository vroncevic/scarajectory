# -*- coding: UTF-8 -*-

'''
Module
    feedrate.py
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
    Manipulator feedrate speed override scale and percentage display section.
'''

from __future__ import annotations

from tkinter import LEFT, Widget, X
from tkinter.ttk import Frame, Label, Scale
from typing import ClassVar, Final

from scarajectory.infrastructure.gui.manipulator.override.idelegate import IManipulatorActionDelegate

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class OverrideSection(Frame):
    '''
        Section providing speed override slider and readout label.

        It defines:

            :attributes:
                | DEFAULT_OVERRIDE - Default speed override percentage.
                | MIN_OVERRIDE - Minimum allowable override percentage.
                | MAX_OVERRIDE - Maximum allowable override percentage.
                | _action_delegate - Action delegate handling override change commands.
                | _lbl_override - Percentage readout label for speed override.
                | _override_slider - Feedrate speed override scale widget.
            :methods:
                | __init__ - Initializes override slider and label layout.
                | handle_slider_change - Handles slider movement and dispatches integer percentage.
                | set_override_label - Updates percentage readout label for speed override.
                | override_text - Returns current text from the override label.
    '''

    DEFAULT_OVERRIDE: ClassVar[int] = 100
    MIN_OVERRIDE: ClassVar[int] = 10
    MAX_OVERRIDE: ClassVar[int] = 200

    _action_delegate: IManipulatorActionDelegate
    _lbl_override: Label
    _override_slider: Scale

    def __init__(
        self,
        parent: Widget,
        *,
        action_delegate: IManipulatorActionDelegate,
    ) -> None:
        '''
            Initializes override slider and label layout.

            :param parent: Parent container widget.
            :param action_delegate: Injected action delegate collaborator.
            :exceptions: None.
        '''
        super().__init__(parent)
        self._action_delegate: Final[IManipulatorActionDelegate] = action_delegate

        Label(self, text='Feedrate Override:').pack(side=LEFT, padx=(3, 2))
        self._lbl_override = Label(self, text=f'{self.DEFAULT_OVERRIDE}%', width=5)
        self._override_slider = Scale(
            self,
            from_=self.MIN_OVERRIDE,
            to=self.MAX_OVERRIDE,
            value=self.DEFAULT_OVERRIDE,
            command=self.handle_slider_change,
        )
        self._override_slider.pack(side=LEFT, fill=X, expand=True, padx=4)
        self._lbl_override.pack(side=LEFT, padx=2)

    def handle_slider_change(self, val: str) -> None:
        '''
            Handles slider movement and dispatches integer percentage.

            :param val: Slider position value string.
            :exceptions: None.
        '''
        pct: int = max(self.MIN_OVERRIDE, min(self.MAX_OVERRIDE, int(float(val))))
        self.set_override_label(pct)
        self._action_delegate.on_override_change(pct)

    def set_override_label(self, pct: int) -> None:
        '''
            Updates percentage readout label for speed override.

            :param pct: Speed override percentage (10 to 200).
            :exceptions: None.
        '''
        self._lbl_override.configure(text=f'{pct}%')

    @property
    def override_text(self) -> str:
        '''
            Returns text of feedrate override readout label.

            :return: Formatted override percentage string.
            :exceptions: None.
        '''
        return str(self._lbl_override.cget('text'))
