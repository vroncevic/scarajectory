# -*- coding: UTF-8 -*-

'''
Module
    validator_test.py
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
    Unit tests for SCARAjectoryBundleValidator.
'''

from __future__ import annotations

from unittest import TestCase, main

from ats_utilities.exceptions import ATSValueError, ATSTypeError

from scarajectory.setup.factory import SCARAjectoryBundleFactory
from scarajectory.setup.validator import SCARAjectoryBundleValidator
from scarajectory.setup.bundle import SCARAjectoryBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestSCARAjectoryBundleValidator(TestCase):
    '''
        Test cases for SCARAjectoryBundleValidator.

        It defines:

            :methods:
                | test_validate_valid_bundle - Tests validation of valid bundle.
                | test_validate_invalid_bundle - Tests validation failures on invalid input.
                | test_is_valid_success_and_failure - Tests is_valid boolean check.
    '''

    def test_validate_valid_bundle(self) -> None:
        '''
            Tests validation of a valid bundle.

            :exceptions: None.
        '''
        bundle: SCARAjectoryBundle = SCARAjectoryBundleFactory.create_bundle()
        SCARAjectoryBundleValidator.validate(bundle)
        self.assertTrue(SCARAjectoryBundleValidator.is_valid(bundle))

    def test_validate_invalid_bundle(self) -> None:
        '''
            Tests validation failures when invalid bundle or types are provided.

            :exceptions: None.
        '''
        with self.assertRaises(ATSValueError):
            SCARAjectoryBundleValidator.validate(None)  # type: ignore[arg-type]

        with self.assertRaises(ATSTypeError):
            SCARAjectoryBundleValidator.validate('not_a_bundle')  # type: ignore[arg-type]

        valid_bundle: SCARAjectoryBundle = SCARAjectoryBundleFactory.create_bundle()
        invalid_bundle = SCARAjectoryBundle(
            base=valid_bundle.base,
            service='not_a_service',  # type: ignore[arg-type]
            gui=valid_bundle.gui,
            streamer=valid_bundle.streamer,
            cli=valid_bundle.cli,
        )
        with self.assertRaises(ATSTypeError):
            SCARAjectoryBundleValidator.validate(invalid_bundle)

    def test_is_valid_success_and_failure(self) -> None:
        '''
            Tests is_valid method on valid and invalid inputs.

            :exceptions: None.
        '''
        valid_bundle: SCARAjectoryBundle = SCARAjectoryBundleFactory.create_bundle()
        self.assertTrue(SCARAjectoryBundleValidator.is_valid(valid_bundle))
        self.assertFalse(SCARAjectoryBundleValidator.is_valid(None))  # type: ignore[arg-type]
        self.assertFalse(SCARAjectoryBundleValidator.is_valid(12345))  # type: ignore[arg-type]


if __name__ == '__main__':
    main()
