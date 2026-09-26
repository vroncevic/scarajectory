# -*- coding: UTF-8 -*-

'''
Module
    scara_diagnostic_formatter.py
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
    Service for formatting SCARA diagnostic findings into standardized human-readable reports.
'''

from __future__ import annotations

from scarajectory.core.model.dsl.diagnostic.diagnostic import Diagnostic
from scarajectory.core.model.dsl.diagnostic.diagnostic_severity import DiagnosticSeverity

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaraDiagnosticFormatter:
    '''
        Domain service for formatting Diagnostic findings into report strings.

        It defines:

            :methods:
                | format_report - Formats diagnostic into standardized report text with status indicator.
    '''

    @classmethod
    def format_report(cls, *, diagnostic: Diagnostic) -> str:
        '''
            Formats the diagnostic finding into a standardized report string.

            :param diagnostic: Diagnostic value object to format.
            :return: Formatted report text string.
        '''
        prefix: str = (
            '❌ [ERROR]'
            if diagnostic.severity == DiagnosticSeverity.ERROR
            else (
                '⚠️ [WARN]'
                if diagnostic.severity == DiagnosticSeverity.WARNING
                else 'ℹ️ [INFO]'
            )
        )

        location: str = (
            f'Line {diagnostic.line}: ' if diagnostic.line > 0 else ''
        )

        return f'{prefix} {location}[{diagnostic.code}] {diagnostic.message}'
