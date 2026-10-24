# -*- coding: UTF-8 -*-

'''
Module
    tab.py
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
    Kinematic validation tab displaying reachability checks and path metrics.
'''

from __future__ import annotations

from tkinter import BOTH, END, LEFT, X, Text, Widget
from tkinter.ttk import Button, Frame
from typing import Final

from scarajectory.infrastructure.gui.validation.dependencies import ValidationDependencies

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ValidationTab(Frame):
    '''
        Kinematic validation tab for inspecting trajectory plan workspace limits.

        It defines:

            :attributes:
                | _dependencies - Injected ValidationDependencies container.
                | _txt_val - Text widget displaying validation logs and summary.
            :methods:
                | __init__ - Initializes the validation tab layout.
                | build_layout - Constructs validation controls and result display text area.
                | run_validation - Executes full validation on current plan and updates view.
    '''

    _dependencies: ValidationDependencies
    _txt_val: Text

    def __init__(
        self,
        parent: Widget,
        *,
        dependencies: ValidationDependencies,
    ) -> None:
        '''
            Initializes the validation tab layout.

            :param parent: Parent notebook widget.
            :param dependencies: Injected ValidationDependencies container.
            :exceptions: None.
        '''
        super().__init__(parent, padding=6)
        self._dependencies: Final[ValidationDependencies] = dependencies
        self.build_layout()

    def build_layout(self) -> None:
        '''
            Constructs validation controls and result display text area.

            :exceptions: None.
        '''
        top: Frame = Frame(self)
        top.pack(fill=X, pady=2)
        Button(
            top,
            text='Run Full Plan Validation',
            style='Accent.TButton',
            command=self.run_validation,
        ).pack(side=LEFT)

        self._txt_val = Text(
            self,
            width=1,
            height=6,
            bg='#14161a',
            fg='#abb2bf',
            font=('DejaVu Sans Mono', 8),
            wrap='word',
        )
        self._txt_val.pack(fill=BOTH, expand=True, pady=4)
        self._txt_val.tag_config('pass', foreground='#98c379')
        self._txt_val.tag_config('fail', foreground='#e06c75')
        self._txt_val.tag_config('warn', foreground='#e5c07b')
        self._txt_val.tag_config('info', foreground='#61afef')

    def run_validation(self) -> None:
        '''
            Executes full validation on current plan and updates view.

            :exceptions: None.
        '''
        try:
            _, msgs = self._dependencies.validator.validate_plan(
                self._dependencies.plan
            )
            validation_msgs: list[str] = list(msgs)
            waypoints = self._dependencies.plan.waypoints

            for i in range(len(waypoints) - 1):
                p1 = waypoints[i]
                p2 = waypoints[i + 1]
                if self._dependencies.avoidance_adapter.crosses_dead_zone(p1, p2):
                    detour = self._dependencies.avoidance_adapter.plan_detour(
                        p1, p2
                    )
                    validation_msgs.append(
                        f'Segment P{i + 1} -> P{i + 2} crosses central dead zone. '
                        f'Bypass detour available with {len(detour)} waypoints.'
                    )

            self._txt_val.delete('1.0', END)

            for msg in validation_msgs:
                if 'PASSED' in msg:
                    prefix: str = '✅ '
                    tag: str = 'pass'
                elif 'WARNING' in msg or 'Bypass' in msg:
                    prefix = '⚠️ '
                    tag = 'warn'
                else:
                    prefix = '❌ '
                    tag = 'fail'
                self._txt_val.insert(END, f'{prefix}{msg}\n', tag)

        except Exception as exc:
            self._txt_val.delete('1.0', END)
            self._txt_val.insert(END, f'❌ Validation error: {exc}\n', 'fail')
