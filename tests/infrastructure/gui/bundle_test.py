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
    Unit tests for GUIBundle data container.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from tkinter import Tk
from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.core.service.storage.iloader import IPlanLoader
from scarajectory.core.service.streaming.playback.icontroller import IPlaybackController
from scarajectory.core.service.trajectory.plan.mutation.bulk_mutation.ibulk_mutation import IPlanBulkMutator
from scarajectory.infrastructure.gui.canvas.navigation.inavigator import ICanvasViewNavigator
from scarajectory.infrastructure.gui.bundle import GUIBundle
from scarajectory.infrastructure.gui.toolbar.toolbar import Toolbar

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class GUIBundleTestCase(TestCase):
    '''
        Tests GUIBundle construction and immutability.

        It defines:

            :methods:
                | test_bundle_creation_and_properties - Verifies attributes and streamer alias.
                | test_bundle_immutability - Verifies frozen dataclass behavior.
    '''

    def test_bundle_creation_and_properties(self) -> None:
        '''
            Verifies all attributes and streamer property.

            :exceptions: None.
        '''
        mock_root = MagicMock(spec=Tk)
        mock_playback = MagicMock(spec=IPlaybackController)
        mock_loader = MagicMock(spec=IPlanLoader)
        mock_mutation = MagicMock(spec=IPlanBulkMutator)
        mock_navigator = MagicMock(spec=ICanvasViewNavigator)
        mock_toolbar = MagicMock(spec=Toolbar)

        bundle = GUIBundle(
            root=mock_root,
            playback_controller=mock_playback,
            loader=mock_loader,
            mutation=mock_mutation,
            navigator=mock_navigator,
            toolbar=mock_toolbar,
        )

        self.assertIs(bundle.root, mock_root)
        self.assertIs(bundle.playback_controller, mock_playback)
        self.assertIs(bundle.loader, mock_loader)
        self.assertIs(bundle.mutation, mock_mutation)
        self.assertIs(bundle.navigator, mock_navigator)
        self.assertIs(bundle.toolbar, mock_toolbar)
        self.assertIs(bundle.streamer, mock_playback)

    def test_bundle_immutability(self) -> None:
        '''
            Verifies modifying attributes raises FrozenInstanceError.

            :exceptions: None.
        '''
        bundle = GUIBundle(
            root=MagicMock(spec=Tk),
            playback_controller=MagicMock(spec=IPlaybackController),
            loader=MagicMock(spec=IPlanLoader),
            mutation=MagicMock(spec=IPlanBulkMutator),
            navigator=MagicMock(spec=ICanvasViewNavigator),
            toolbar=MagicMock(spec=Toolbar),
        )

        with self.assertRaises(FrozenInstanceError):
            bundle.root = MagicMock(spec=Tk)  # type: ignore[misc]


if __name__ == '__main__':
    main()
