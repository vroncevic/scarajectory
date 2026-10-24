# -*- coding: UTF-8 -*-

'''
Module
    factory_test.py
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
    Unit tests for PlanFactory.
'''

from __future__ import annotations

from unittest import TestCase
from unittest.mock import MagicMock

from scarajectory.core.service.storage.iloader import IPlanLoader
from scarajectory.core.service.storage.istorer import IPlanStorer
from scarajectory.infrastructure.storage.config_io.loader.iloader import IConfigLoader
from scarajectory.infrastructure.storage.config_io.storer.istorer import IConfigStorer
from scarajectory.infrastructure.storage.plan.dependencies import PlanDependencies
from scarajectory.infrastructure.storage.plan.factory import PlanFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestPlanFactory(TestCase):
    '''
        Test cases verifying PlanFactory operations.

        It defines:

            :methods:
                | test_create - Verifies factory instantiates PlanProvides.
                | test_get_version - Verifies factory returns version string.
    '''

    def test_create(self) -> None:
        '''Verifies factory creates PlanProvides containing assembled components.'''
        mock_loader = MagicMock(spec=IConfigLoader)
        mock_storer = MagicMock(spec=IConfigStorer)
        deps = PlanDependencies(config_loader=mock_loader, config_storer=mock_storer)
        provides = PlanFactory.create(dependencies=deps)

        self.assertIsInstance(provides.plan_loader, IPlanLoader)
        self.assertIsInstance(provides.plan_storer, IPlanStorer)

    def test_get_version(self) -> None:
        '''Verifies factory returns version string.'''
        self.assertEqual(PlanFactory.get_version(), '1.0.3')
