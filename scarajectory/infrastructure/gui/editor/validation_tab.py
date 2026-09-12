# -*- coding: UTF-8 -*-

'''
Module
    validation_tab.py
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

from scarajectory.core.model.trajectory.itrajectory_plan import ITrajectoryPlan
from scarajectory.core.service.trajectory.itrajectory_validator import ITrajectoryValidator
from scarajectory.core.service.trajectory.iplan_validation_service import IPlanValidationService

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
                | _plan - Optional active trajectory plan domain abstraction.
                | _validator - Optional kinematic reachability validator.
                | _service - Optional core trajectory service instance.
                | _txt_val - Text widget displaying validation logs and summary.
            :methods:
                | __init__ - Initializes the validation tab layout.
                | run_validation - Executes full validation on current plan and updates view.
    '''

    _plan: ITrajectoryPlan | None
    _validator: ITrajectoryValidator | None
    _service: IPlanValidationService | None
    _txt_val: Text

    def __init__(
        self,
        parent: Widget,
        plan: ITrajectoryPlan | None = None,
        validator: ITrajectoryValidator | None = None,
        service: IPlanValidationService | None = None,
        **kwargs: object
    ) -> None:
        '''
            Initializes the validation tab layout.

            :param parent: Parent notebook widget.
            :param plan: Optional active ITrajectoryPlan.
            :param validator: Optional ITrajectoryValidator instance.
            :param service: Optional IPlanValidationService instance.
            :exceptions: None.
        '''
        super().__init__(parent, padding=6, **kwargs)
        self._plan: Final[ITrajectoryPlan | None] = plan
        self._validator: Final[ITrajectoryValidator | None] = validator
        self._service: Final[IPlanValidationService | None] = service
        self._build_layout()

    def _build_layout(self) -> None:
        '''
            Constructs validation controls and result display text area.

            :exceptions: None.
        '''
        top: Frame = Frame(self)
        top.pack(fill=X, pady=2)
        Button(top, text='Run Full Plan Validation', style='Accent.TButton', command=self.run_validation).pack(side=LEFT)

        self._txt_val = Text(self, width=1, height=6, bg='#14161a', fg='#abb2bf', font=('DejaVu Sans Mono', 8), wrap='word')
        self._txt_val.pack(fill=BOTH, expand=True, pady=4)

    def run_validation(self) -> None:
        '''
            Executes full validation on current plan and updates view.

            :exceptions: None.
        '''
        if self._service is not None:
            _, msgs = self._service.validate_plan()
        elif self._validator is not None and self._plan is not None:
            _, msgs = self._validator.validate_plan(self._plan)
        else:
            msgs = ['Validation failed: No plan or validator configured.']

        self._txt_val.delete('1.0', END)

        for msg in msgs:
            prefix: str = '✅ ' if 'PASSED' in msg else '❌ '
            self._txt_val.insert(END, f'{prefix}{msg}\n')
