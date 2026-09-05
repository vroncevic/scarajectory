# -*- coding: UTF-8 -*-

'''
Module
    scara_diagnostic.py
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
    Defines ScaraDiagnostic value object representing a static analysis finding.
'''

from __future__ import annotations

from dataclasses import dataclass

from scarajectory.core.model.dsl.scara_diagnostic_severity import (
    ScaraDiagnosticSeverity,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True, kw_only=True)
class ScaraDiagnostic:
    '''
        Immutable value object encapsulating a static analysis warning, error, or info notice.

        It defines:

            :attributes:
                | code - Diagnostic identifier code string.
                | severity - ScaraDiagnosticSeverity classification.
                | message - Human-readable diagnostic description.
                | line - 1-indexed source line position (0 if global).
                | command - Name or text of offending command node.
            :methods:
                | format_report - Formats diagnostic as human-readable report string.
    '''

    code: str
    severity: ScaraDiagnosticSeverity
    message: str
    line: int = 0
    command: str = ''

    def format_report(self) -> str:
        '''
            Formats the diagnostic finding into a standardized report string.

            :return: Formatted report text string.
            :exceptions: None.
        '''
        prefix: str = (
            '❌ [ERROR]'
            if self.severity == ScaraDiagnosticSeverity.ERROR
            else (
                '⚠️ [WARN]'
                if self.severity == ScaraDiagnosticSeverity.WARNING
                else 'ℹ️ [INFO]'
            )
        )
        location: str = f'Line {self.line}: ' if self.line > 0 else ''
        return f'{prefix} {location}[{self.code}] {self.message}'
