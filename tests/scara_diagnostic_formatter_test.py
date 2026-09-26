# -*- coding: UTF-8 -*-

'''
Module
    scara_diagnostic_formatter_test.py
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
    Unit tests for ScaraDiagnosticFormatter.
'''

from __future__ import annotations

from pathlib import Path
from sys import path
from unittest import TestCase, main

pkg_dir = str(Path(__file__).resolve().parent.parent)
if pkg_dir not in path:
    path.insert(0, pkg_dir)

from scarajectory.core.model.dsl.diagnostic.diagnostic import Diagnostic
from scarajectory.core.model.dsl.diagnostic.diagnostic_severity import DiagnosticSeverity
from scarajectory.core.service.dsl.diagnostic.scara_diagnostic_formatter import ScaraDiagnosticFormatter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaraDiagnosticFormatterTest(TestCase):
    '''Unit tests validating formatting of Diagnostic reports.'''

    def test_format_error(self) -> None:
        '''Verify formatting an ERROR severity diagnostic.'''
        diag = Diagnostic(
            code='ERR01',
            severity=DiagnosticSeverity.ERROR,
            message='Invalid coordinate syntax',
            line=15,
            command='MOVE_L',
        )
        report = ScaraDiagnosticFormatter.format_report(diagnostic=diag)
        self.assertIn('❌ [ERROR]', report)
        self.assertIn('Line 15:', report)
        self.assertIn('[ERR01]', report)
        self.assertIn('Invalid coordinate syntax', report)

    def test_format_warning(self) -> None:
        '''Verify formatting a WARNING severity diagnostic.'''
        diag = Diagnostic(
            code='WARN02',
            severity=DiagnosticSeverity.WARNING,
            message='Near reach limit',
            line=8,
            command='MOVE_J',
        )
        report = ScaraDiagnosticFormatter.format_report(diagnostic=diag)
        self.assertIn('⚠️ [WARN]', report)
        self.assertIn('Line 8:', report)
        self.assertIn('[WARN02]', report)
        self.assertIn('Near reach limit', report)

    def test_format_info_without_command(self) -> None:
        '''Verify formatting an INFO severity diagnostic without command.'''
        diag = Diagnostic(
            code='INFO03',
            severity=DiagnosticSeverity.INFO,
            message='Optimization note',
            line=1,
            command='',
        )
        report = ScaraDiagnosticFormatter.format_report(diagnostic=diag)
        self.assertIn('ℹ️ [INFO]', report)
        self.assertIn('Line 1:', report)
        self.assertIn('[INFO03]', report)
        self.assertIn('Optimization note', report)


if __name__ == '__main__':
    main()
