# -*- coding: UTF-8 -*-

'''
Module
    engine_test.py
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
    Unit tests for SCARAjectory top-level application engine.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from ats_utilities.exceptions import ATSValueError
from scarajectory.engine import SCARAjectory
from scarajectory.setup.factory import SCARAjectoryBundleFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SCARAjectoryEngineTestCase(TestCase):
    '''
        Tests for SCARAjectory top-level engine orchestration.

        It defines:

            :methods:
                | test_initialization_success - Verifies successful engine bootstrap.
                | test_initialization_invalid_bundle - Verifies initialization failure on bad bundle.
                | test_process_success - Verifies process execution when CLI returns 0.
                | test_process_cli_failure - Verifies process execution when CLI returns non-zero.
                | test_process_cli_exceptions - Verifies exception handling during command process.
                | test_process_when_not_initialized - Verifies process returns False if uninitialized.
    '''

    def test_initialization_success(self) -> None:
        '''
            Verifies successful engine bootstrap.

            :exceptions: None.
        '''
        bundle = SCARAjectoryBundleFactory.create_bundle()
        app = SCARAjectory(bundle)
        self.assertTrue(app.is_initialized())

    @patch('scarajectory.engine.stdout.write')
    def test_initialization_invalid_bundle(self, mock_stdout: MagicMock) -> None:
        '''
            Verifies initialization failure on bad bundle.

            :exceptions: None.
        '''
        app = SCARAjectory(None)  # type: ignore[arg-type]
        self.assertFalse(app.is_initialized())
        mock_stdout.assert_called()

        valid_bundle = SCARAjectoryBundleFactory.create_bundle()
        with patch('scarajectory.setup.validator.SCARAjectoryBundleValidator.validate', side_effect=RuntimeError('Unexpected failure')):
            unexpected_app = SCARAjectory(valid_bundle)
            self.assertFalse(unexpected_app.is_initialized())

    def test_process_success(self) -> None:
        '''
            Verifies process execution when CLI returns 0.

            :exceptions: None.
        '''
        bundle = SCARAjectoryBundleFactory.create_bundle()
        mock_run = MagicMock(return_value={'returncode': 0, 'stdout': 'completed'})
        bundle.cli.run = mock_run  # type: ignore[method-assign]
        app = SCARAjectory(bundle)

        success = app.process()
        self.assertTrue(success)
        mock_run.assert_called_once()

    def test_process_cli_failure(self) -> None:
        '''
            Verifies process execution when CLI returns non-zero.

            :exceptions: None.
        '''
        bundle = SCARAjectoryBundleFactory.create_bundle()
        mock_run = MagicMock(
            return_value={'returncode': 1, 'stderr': 'Execution error'}
        )
        bundle.cli.run = mock_run  # type: ignore[method-assign]
        app = SCARAjectory(bundle)

        success = app.process()
        self.assertFalse(success)
        mock_run.assert_called_once()

    @patch('scarajectory.engine.stdout.write')
    def test_process_cli_exceptions(self, mock_stdout: MagicMock) -> None:
        '''
            Verifies exception handling during command process.

            :exceptions: None.
        '''
        bundle = SCARAjectoryBundleFactory.create_bundle()
        mock_run = MagicMock(side_effect=ATSValueError('Invalid configuration'))
        bundle.cli.run = mock_run  # type: ignore[method-assign]
        app = SCARAjectory(bundle)

        self.assertFalse(app.process())
        mock_stdout.assert_called()

        mock_run.side_effect = RuntimeError('Hardware crash')
        self.assertFalse(app.process())

    @patch('scarajectory.engine.stdout.write')
    def test_process_when_not_initialized(self, mock_stdout: MagicMock) -> None:
        '''
            Verifies process returns False if engine is not initialized.

            :exceptions: None.
        '''
        app = SCARAjectory(None)  # type: ignore[arg-type]
        self.assertFalse(app.process())
        mock_stdout.assert_called()


if __name__ == '__main__':
    main()
