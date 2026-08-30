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

import tkinter as tk
from tkinter import ttk
from typing import Final

from scarajectory.core.model.trajectory_metrics import TrajectoryMetrics
from scarajectory.core.model.itrajectory_plan import ITrajectoryPlan

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PreviewTab(ttk.Frame):
    '''
        ASCII trajectory stream generator and microcontroller program preview tab.

        It defines:

            :attributes:
                | _plan - Active trajectory plan domain abstraction.
                | _txt_preview - Text area rendering ASCII trajectory stream.
            :methods:
                | __init__ - Initializes program preview tab layout.
                | generate_preview - Generates and displays ASCII trajectory protocol program.
    '''

    _plan: Final[ITrajectoryPlan]
    _txt_preview: tk.Text

    def __init__(self, parent: tk.Widget, plan: ITrajectoryPlan, **kwargs: object) -> None:
        '''
            Initializes program preview tab layout.

            :param parent: Parent notebook widget.
            :param plan: Active ITrajectoryPlan.
            :exceptions: None.
        '''
        super().__init__(parent, padding=6, **kwargs)
        self._plan = plan
        self._build_layout()

    def _build_layout(self) -> None:
        '''
            Constructs generate button and output text area.

            :exceptions: None.
        '''
        top: ttk.Frame = ttk.Frame(self)
        top.pack(fill=tk.X, pady=2)
        ttk.Button(top, text='Generate Microcontroller Program', style='Accent.TButton', command=self.generate_preview).pack(side=tk.LEFT)

        self._txt_preview = tk.Text(self, height=6, bg='#14161a', fg='#98c379', font=('DejaVu Sans Mono', 8), wrap='none')
        self._txt_preview.pack(fill=tk.BOTH, expand=True, pady=4)

    def generate_preview(self) -> None:
        '''
            Generates and renders ASCII trajectory packet block.

            :exceptions: None.
        '''
        waypoints = self._plan.waypoints
        ascii_prog: str = TrajectoryMetrics.to_ascii_program(waypoints)
        self._txt_preview.delete('1.0', tk.END)
        self._txt_preview.insert(tk.END, ascii_prog)
