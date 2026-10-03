# -*- coding: UTF-8 -*-

'''
Module
    preview_tab.py
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
    Program preview tab generating ASCII protocol trajectory instruction blocks.
'''

from __future__ import annotations

from tkinter import BOTH, END, LEFT, X, Text, Widget
from tkinter.ttk import Button, Frame
from typing import Final

from scaralang.core.service.exporter.scara.iscara_plan_exporter import IScaraPlanExporter
from scarajectory.core.service.trajectory.plan.itrajectory_read_only import ITrajectoryReadOnly

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PreviewTab(Frame):
    '''
        ASCII trajectory stream generator and microcontroller program preview tab.

        It defines:

            :attributes:
                | _plan - Active trajectory read-only domain abstraction.
                | _txt_preview - Text area rendering ASCII trajectory stream.
            :methods:
                | __init__ - Initializes program preview tab layout.
                | generate_preview - Generates and displays ASCII trajectory protocol program.
    '''

    _plan: ITrajectoryReadOnly
    _exporter: IScaraPlanExporter
    _txt_preview: Text

    def __init__(
        self,
        parent: Widget,
        plan: ITrajectoryReadOnly,
        exporter: IScaraPlanExporter,
    ) -> None:
        '''
            Initializes program preview tab layout.

            :param parent: Parent notebook widget.
            :param plan: Active ITrajectoryReadOnly instance.
            :param exporter: Injected IScaraPlanExporter instance.
            :exceptions: None.
        '''
        super().__init__(parent, padding=6)
        self._plan: Final[ITrajectoryReadOnly] = plan
        self._exporter: Final[IScaraPlanExporter] = exporter
        self.build_layout()

    def build_layout(self) -> None:
        '''
            Constructs generate button and output text area.

            :exceptions: None.
        '''
        top: Frame = Frame(self)
        top.pack(fill=X, pady=2)
        Button(top, text='Generate Microcontroller Program', style='Accent.TButton', command=self.generate_preview).pack(side=LEFT)

        self._txt_preview = Text(self, width=1, height=6, bg='#14161a', fg='#98c379', font=('DejaVu Sans Mono', 8), wrap='none')
        self._txt_preview.pack(fill=BOTH, expand=True, pady=4)

    def generate_preview(self) -> None:
        '''
            Generates and renders SCARA DSL trajectory program.

            :exceptions: None.
        '''
        scara_prog: str = self._exporter.export_plan(plan=self._plan)
        self._txt_preview.delete('1.0', END)
        self._txt_preview.insert(END, scara_prog)
