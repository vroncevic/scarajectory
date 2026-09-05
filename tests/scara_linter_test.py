# -*- coding: UTF-8 -*-

'''
Module
    scara_linter_test.py
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
    Unit tests for ScaraLinter ahead-of-time static analysis and diagnostic checks.
'''

from __future__ import annotations

from pathlib import Path
from sys import path
from unittest import TestCase, main

pkg_dir = str(Path(__file__).resolve().parent.parent)
if pkg_dir not in path:
    path.insert(0, pkg_dir)

from scarajectory.core.model.dsl.scara_diagnostic_severity import ScaraDiagnosticSeverity
from scarajectory.core.model.dsl.scara_program import ScaraProgram
from scarajectory.core.service.dsl.linter.scara_linter import ScaraLinter
from scarajectory.core.service.dsl.scara_lexer import ScaraLexer
from scarajectory.core.service.dsl.scara_parser import ScaraParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestScaraLinter(TestCase):
    '''
        Test cases verifying ahead-of-time static analysis rules in ScaraLinter.

        It defines:

            :methods:
                | setUp - Initializes lexer, parser, and linter instances.
                | test_empty_program_error - Verifies ERROR on empty program AST.
                | test_pneumatic_conflict_error - Verifies ERROR on simultaneous pump and valve contention.
                | test_uncalibrated_motion_warning - Verifies WARNING on motion prior to homing.
                | test_tool_in_flyby_warning - Verifies WARNING on tool command during active zone blending.
                | test_redundant_tool_command_warning - Verifies WARNING on consecutive identical tool states.
                | test_dead_wait_info - Verifies INFO on non-positive dwell delay.
                | test_duplicate_motion_info - Verifies INFO on consecutive identical motion targets.
                | test_clean_program_no_diagnostics - Verifies zero diagnostics on fully compliant script.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixtures before each test execution.
        '''
        self._lexer = ScaraLexer()
        self._parser = ScaraParser()
        self._linter = ScaraLinter()

    def _parse(self, source: str) -> ScaraProgram:
        '''
            Helper parsing source code into a ScaraProgram AST.

            :param source: SCARA DSL source text.
            :return: ScaraProgram AST.
        '''
        tokens = self._lexer.tokenize(source=source)
        return self._parser.parse_tokens(tokens=tokens)

    def test_empty_program_error(self) -> None:
        '''
            Verifies ERROR diagnostic on empty program AST.
        '''
        empty_prog = ScaraProgram(instructions=[])
        diagnostics = self._linter.lint(program=empty_prog)
        self.assertEqual(len(diagnostics), 1)
        self.assertEqual(diagnostics[0].severity, ScaraDiagnosticSeverity.ERROR)
        self.assertEqual(diagnostics[0].code, 'EMPTY_PROGRAM')

    def test_pneumatic_conflict_error(self) -> None:
        '''
            Verifies ERROR on simultaneous pump and valve contention.
        '''
        source = (
            'HOME\n'
            'PUMP ON\n'
            'VALVE ON\n'
        )
        program = self._parse(source)
        diagnostics = self._linter.lint(program=program)
        conflict_diags = [d for d in diagnostics if d.code == 'PNEUMATIC_CONFLICT']
        self.assertEqual(len(conflict_diags), 1)
        self.assertEqual(conflict_diags[0].severity, ScaraDiagnosticSeverity.ERROR)
        self.assertEqual(conflict_diags[0].line, 3)

    def test_uncalibrated_motion_warning(self) -> None:
        '''
            Verifies WARNING on motion prior to homing.
        '''
        source = 'MOVE_L X=150.0 Y=50.0 Z=20.0\n'
        program = self._parse(source)
        diagnostics = self._linter.lint(program=program)
        uncal_diags = [d for d in diagnostics if d.code == 'UNCALIBRATED_MOTION']
        self.assertEqual(len(uncal_diags), 1)
        self.assertEqual(uncal_diags[0].severity, ScaraDiagnosticSeverity.WARNING)

    def test_tool_in_flyby_warning(self) -> None:
        '''
            Verifies WARNING on tool command during active zone blending.
        '''
        source = (
            'HOME\n'
            'ZONE BLEND R=10.0\n'
            'PUMP ON\n'
        )
        program = self._parse(source)
        diagnostics = self._linter.lint(program=program)
        flyby_diags = [d for d in diagnostics if d.code == 'TOOL_IN_FLYBY']
        self.assertEqual(len(flyby_diags), 1)
        self.assertEqual(flyby_diags[0].severity, ScaraDiagnosticSeverity.WARNING)

    def test_redundant_tool_command_warning(self) -> None:
        '''
            Verifies WARNING on consecutive identical tool states.
        '''
        source = (
            'HOME\n'
            'PUMP ON\n'
            'PUMP ON\n'
        )
        program = self._parse(source)
        diagnostics = self._linter.lint(program=program)
        redundant_diags = [d for d in diagnostics if d.code == 'REDUNDANT_TOOL_CMD']
        self.assertEqual(len(redundant_diags), 1)
        self.assertEqual(redundant_diags[0].severity, ScaraDiagnosticSeverity.WARNING)

    def test_dead_wait_info(self) -> None:
        '''
            Verifies INFO on non-positive dwell delay.
        '''
        source = (
            'HOME\n'
            'WAIT_MS 0\n'
        )
        program = self._parse(source)
        diagnostics = self._linter.lint(program=program)
        wait_diags = [d for d in diagnostics if d.code == 'DEAD_WAIT']
        self.assertEqual(len(wait_diags), 1)
        self.assertEqual(wait_diags[0].severity, ScaraDiagnosticSeverity.INFO)

    def test_duplicate_motion_info(self) -> None:
        '''
            Verifies INFO on consecutive identical motion targets.
        '''
        source = (
            'HOME\n'
            'MOVE_L X=150.0 Y=50.0 Z=20.0\n'
            'MOVE_L X=150.0 Y=50.0 Z=20.0\n'
        )
        program = self._parse(source)
        diagnostics = self._linter.lint(program=program)
        dup_diags = [d for d in diagnostics if d.code == 'DUPLICATE_MOTION']
        self.assertEqual(len(dup_diags), 1)
        self.assertEqual(dup_diags[0].severity, ScaraDiagnosticSeverity.INFO)

    def test_clean_program_no_diagnostics(self) -> None:
        '''
            Verifies zero diagnostics on fully compliant script.
        '''
        source = (
            'HOME\n'
            'MOVE_L X=150.0 Y=50.0 Z=20.0\n'
            'PUMP ON\n'
            'WAIT_MS 100\n'
            'MOVE_L X=160.0 Y=60.0 Z=20.0\n'
            'PUMP OFF\n'
        )
        program = self._parse(source)
        diagnostics = self._linter.lint(program=program)
        self.assertEqual(len(diagnostics), 0)


if __name__ == '__main__':
    main()
