# -*- coding: UTF-8 -*-

'''
Module
    scara_diagnostic_test.py
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
    Unit tests for Diagnostic value object model.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from pathlib import Path
from sys import path
from unittest import TestCase, main

pkg_dir = str(Path(__file__).resolve().parent.parent)
if pkg_dir not in path:
    path.insert(0, pkg_dir)

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


class ScaraDiagnosticTest(TestCase):
    '''Unit tests validating Diagnostic purity and value object semantics.'''

    def test_instantiation_and_attributes(self) -> None:
        '''Verify proper initialization of fields in Diagnostic.'''
        diag = Diagnostic(
            code='BAD_COORDINATE',
            severity=DiagnosticSeverity.ERROR,
            message='Coordinate X exceeds boundary limit',
            line=12,
            command='MOVE_L',
        )
        self.assertEqual(diag.code, 'BAD_COORDINATE')
        self.assertEqual(diag.severity, DiagnosticSeverity.ERROR)
        self.assertEqual(diag.message, 'Coordinate X exceeds boundary limit')
        self.assertEqual(diag.line, 12)
        self.assertEqual(diag.command, 'MOVE_L')

    def test_frozen_immutability(self) -> None:
        '''Verify modifying attribute raises FrozenInstanceError.'''
        diag = Diagnostic(
            code='WARN_SPEED',
            severity=DiagnosticSeverity.WARNING,
            message='Speed is near maximum',
            line=5,
            command='SPEED',
        )
        with self.assertRaises(FrozenInstanceError):
            diag.line = 10  # type: ignore[misc]


if __name__ == '__main__':
    main()
