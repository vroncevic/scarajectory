# -*- coding: UTF-8 -*-

'''
Module
    homing_status_classifier_test.py
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
    Unit tests for HomingStatusClassifier and HomingStatusClassifierFactory.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.infrastructure.classifier.status.ihoming_status_classifier import IHomingStatusClassifier
from scarajectory.infrastructure.classifier.status.homing_status_classifier import HomingStatusClassifier
from scarajectory.infrastructure.classifier.status.homing_status_classifier_factory import HomingStatusClassifierFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class HomingStatusClassifierTestCase(TestCase):
    '''
        Tests for HomingStatusClassifier homing and calibration verification.

        It defines:

            :methods:
                | test_factory_and_protocol_conformance - Tests factory and structural protocol.
                | test_is_homed_success - Tests successful homing packet recognition.
                | test_is_homed_failed - Tests homing failure recognition.
                | test_is_homing_failed_alias - Tests alias method for homing failure.
    '''

    def test_factory_and_protocol_conformance(self) -> None:
        '''
            Tests factory and structural protocol.

            :exceptions: None.
        '''
        classifier = HomingStatusClassifierFactory.create()
        self.assertIsInstance(classifier, HomingStatusClassifier)
        self.assertIsInstance(classifier, IHomingStatusClassifier)
        self.assertEqual(HomingStatusClassifierFactory.get_version(), '1.0.3')

    def test_is_homed_success(self) -> None:
        '''
            Tests successful homing packet recognition.

            :exceptions: None.
        '''
        classifier = HomingStatusClassifier()
        self.assertTrue(classifier.is_homed_success('ok: HOMED_SUCCESS all axes'))
        self.assertFalse(classifier.is_homed_success('ok: moving'))

    def test_is_homed_failed(self) -> None:
        '''
            Tests homing failure recognition.

            :exceptions: None.
        '''
        classifier = HomingStatusClassifier()
        self.assertTrue(classifier.is_homed_failed('err: HOMING_FAILED timeout'))
        self.assertTrue(classifier.is_homed_failed('err: HOMED_FAIL switch'))
        self.assertFalse(classifier.is_homed_failed('ok: HOMED_SUCCESS'))

    def test_is_homing_failed_alias(self) -> None:
        '''
            Tests alias method for homing failure.

            :exceptions: None.
        '''
        classifier = HomingStatusClassifier()
        self.assertTrue(classifier.is_homing_failed('err: HOMING_FAILED'))
        self.assertFalse(classifier.is_homing_failed('ok'))


if __name__ == '__main__':
    main()
