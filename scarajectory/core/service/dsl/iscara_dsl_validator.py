# -*- coding: UTF-8 -*-

'''
Module
    iscara_dsl_validator.py
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
    Defines interface IScaraDslValidator for syntax validation and linting of SCARA DSL scripts.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scarajectory.core.model.dsl.diagnostic.scara_diagnostic import ScaraDiagnostic
from scarajectory.core.model.kinematics.scara_bounds import ScaraBounds

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IScaraDslValidator(Protocol):
    '''
        Role interface protocol for SCARA DSL validation and static analysis.

        It defines:

            :methods:
                | validate_script - Checks syntax and kinematics of DSL script.
                | lint_script - Performs static analysis checks on DSL script string.
    '''

    def validate_script(
        self,
        *,
        source: str,
        bounds: ScaraBounds | None = None,
    ) -> tuple[bool, list[str]]:
        '''
            Validates syntax, static analysis rules, and kinematics of a DSL script.

            :param source: Raw .scara script text.
            :param bounds: Optional robot kinematic boundary constraints.
            :return: Tuple of (is_valid, messages_list).
            :exceptions: None.
        '''

    def lint_script(
        self,
        *,
        source: str,
    ) -> tuple[ScaraDiagnostic, ...]:
        '''
            Performs static analysis checks on a DSL script string.

            :param source: Raw .scara script text.
            :return: Tuple of ScaraDiagnostic findings.
            :exceptions: None.
        '''
