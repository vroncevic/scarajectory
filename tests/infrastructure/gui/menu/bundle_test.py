# -*- coding: UTF-8 -*-

'''
Module
    bundle_test.py
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
    Unit testing for MenuBundle collaborator container.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.menu.bundle import MenuBundle
from scarajectory.setup.assembly.dsl.bundle import DslPipelineBundle
from scarajectory.setup.assembly.plan.bundle import PlanPipelineBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MenuBundleTestCase(TestCase):
    '''
        Unit tests for MenuBundle.

        It defines:

            :methods:
                | test_menu_bundle_attributes_and_properties - Verifies bundle properties.
    '''

    def test_menu_bundle_attributes_and_properties(self) -> None:
        '''
            Verifies MenuBundle stores attributes and exposes delegated properties.

            :exceptions: None.
        '''
        mock_plan = MagicMock(spec=PlanPipelineBundle)
        mock_loader = MagicMock()
        mock_storer = MagicMock()
        mock_dsl = MagicMock(spec=DslPipelineBundle)
        mock_nav = MagicMock()
        mock_table = MagicMock()

        bundle = MenuBundle(
            plan=mock_plan,
            loader=mock_loader,
            storer=mock_storer,
            dsl=mock_dsl,
            navigator=mock_nav,
            table=mock_table,
        )

        self.assertIs(bundle.plan, mock_plan)
        self.assertIs(bundle.loader, mock_loader)
        self.assertIs(bundle.storer, mock_storer)
        self.assertIs(bundle.dsl, mock_dsl)
        self.assertIs(bundle.navigator, mock_nav)
        self.assertIs(bundle.table, mock_table)
        self.assertIs(bundle.store, mock_plan.store)
        self.assertIs(bundle.mutation, mock_plan.mutation)
        self.assertIs(bundle.history, mock_plan.history)


if __name__ == '__main__':
    main()
