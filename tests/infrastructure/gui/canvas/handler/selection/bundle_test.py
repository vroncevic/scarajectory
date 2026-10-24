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
    Unit tests for SelectionHandlerBundle parameter bundle.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.canvas.handler.selection.bundle import SelectionHandlerBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestSelectionHandlerBundle(TestCase):
    '''
        Test cases verifying SelectionHandlerBundle immutability and attributes.

        It defines:

            :methods:
                | test_bundle_creation - Tests instantiation with valid attributes.
    '''

    def test_bundle_creation(self) -> None:
        '''
            Verifies bundle stores all injected attributes correctly.

            :exceptions: None.
        '''
        store = MagicMock()
        selection = MagicMock()
        mutation = MagicMock()
        vp = MagicMock()
        state = MagicMock()
        validator = MagicMock()

        bundle = SelectionHandlerBundle(
            store=store,
            selection=selection,
            mutation=mutation,
            vp=vp,
            state=state,
            validator=validator,
        )
        self.assertIs(bundle.store, store)
        self.assertIs(bundle.selection, selection)
        self.assertIs(bundle.mutation, mutation)
        self.assertIs(bundle.vp, vp)
        self.assertIs(bundle.state, state)
        self.assertIs(bundle.validator, validator)


if __name__ == '__main__':
    main()
