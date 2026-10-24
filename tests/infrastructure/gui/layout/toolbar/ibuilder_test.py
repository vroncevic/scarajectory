# -*- coding: UTF-8 -*-

'''
Module
    ibuilder_test.py
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
    Unit testing for IToolbarLayoutBuilder protocol conformance.
'''

from __future__ import annotations

from tkinter import Tk
from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.canvas.trajectory_canvas import TrajectoryCanvas
from scarajectory.infrastructure.gui.dependencies import GUIDependencies
from scarajectory.infrastructure.gui.layout.toolbar.ibuilder import IToolbarLayoutBuilder
from scarajectory.infrastructure.gui.model.canvas_settings import CanvasSettings
from scarajectory.infrastructure.gui.toolbar.toolbar import Toolbar

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConformingToolbarBuilderStub:
    '''Conforming stub satisfying IToolbarLayoutBuilder protocol.'''

    def build(
        self,
        root: Tk,
        *,
        canvas: TrajectoryCanvas,
        bundle: GUIDependencies,
        settings: CanvasSettings,
    ) -> Toolbar:
        '''Builds toolbar.'''
        _ = (root, canvas, bundle, settings)
        return MagicMock(spec=Toolbar)

    def get_version(self) -> str:
        '''Returns version string.'''
        return '1.0.0'


class IncompleteToolbarBuilderStub:
    '''Non-conforming stub missing build method.'''

    def get_version(self) -> str:
        '''Returns version string.'''
        return '1.0.0'

    def dummy_action(self) -> None:
        '''Dummy method for public method threshold.'''


class ToolbarLayoutBuilderProtocolTestCase(TestCase):
    '''
        Tests IToolbarLayoutBuilder runtime checkable protocol conformance.

        It defines:

            :methods:
                | test_protocol_conformance_success - Verifies conforming class passes check.
                | test_protocol_conformance_failure - Verifies non-conforming class fails check.
    '''

    def test_protocol_conformance_success(self) -> None:
        '''
            Verifies compliant class satisfies IToolbarLayoutBuilder protocol.

            :exceptions: None.
        '''
        stub = ConformingToolbarBuilderStub()
        self.assertIsInstance(stub, IToolbarLayoutBuilder)

    def test_protocol_conformance_failure(self) -> None:
        '''
            Verifies non-compliant class fails IToolbarLayoutBuilder protocol check.

            :exceptions: None.
        '''
        stub = IncompleteToolbarBuilderStub()
        self.assertNotIsInstance(stub, IToolbarLayoutBuilder)


if __name__ == '__main__':
    main()
