# -*- coding: UTF-8 -*-

'''
Module
    steps_factory_test.py
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
    Unit tests for JointStepsDiagnosticsFactory domain factory service.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.model.telemetry.diagnostics.steps import JointStepsDiagnostics
from scarajectory.core.service.telemetry.diagnostics.steps_factory import JointStepsDiagnosticsFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class JointStepsDiagnosticsFactoryTestCase(TestCase):
    '''
        Tests for JointStepsDiagnosticsFactory component.

        It defines:

            :methods:
                | test_create_joint_steps - Verifies model creation.
                | test_get_version - Verifies factory version accessor string.
    '''

    def test_create_joint_steps(self) -> None:
        '''
            Verifies joint steps diagnostics model creation.

            :exceptions: None.
        '''
        model = JointStepsDiagnosticsFactory.create(
            j1=100,
            j2=200,
            z=50,
            j4=25,
        )
        self.assertIsInstance(model, JointStepsDiagnostics)
        self.assertEqual(model.j1, 100)
        self.assertEqual(model.j2, 200)
        self.assertEqual(model.z, 50)
        self.assertEqual(model.j4, 25)

    def test_get_version(self) -> None:
        '''
            Verifies factory version accessor string.

            :exceptions: None.
        '''
        self.assertEqual(JointStepsDiagnosticsFactory.get_version(), '1.0.3')


if __name__ == '__main__':
    main()
