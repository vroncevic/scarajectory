# -*- coding: UTF-8 -*-

'''
Module
    diagnostic.py
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
    Defines immutable Diagnostic model representing a DSL diagnostic message.
'''

from __future__ import annotations

from dataclasses import dataclass

from scarajectory.core.model.dsl.diagnostic.diagnostic_severity import DiagnosticSeverity

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True, kw_only=True)
class Diagnostic:
    '''
        Immutable DSL diagnostic entity.

        It defines:

        :attributes:
            | code - Diagnostic error or warning code.
            | severity - Diagnostic severity level.
            | message - Diagnostic description message.
            | line - Source DSL line number.
            | command - Source DSL command string.
    '''

    code: str
    severity: DiagnosticSeverity
    message: str
    line: int = 0
    command: str = ''
