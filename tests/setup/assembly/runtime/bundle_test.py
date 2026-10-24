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
    Unit tests for AppRuntimeBundle value object.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scaracom.transport.itransport import ITransport
from scaracom.transport.preference.irepository import ISerialPreferenceRepository
from scarajectory.core.service.storage.iloader import IPlanLoader
from scarajectory.core.service.storage.istorer import IPlanStorer
from scarajectory.core.service.streaming.playback.icontroller import IPlaybackController
from scarajectory.infrastructure.storage.workspace.imanager import IWorkspaceManager
from scarajectory.infrastructure.streaming.provides import StreamingProvides
from scarajectory.setup.assembly.runtime.bundle import AppRuntimeBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class AppRuntimeBundleTest(TestCase):
    '''
        Test suite verifying AppRuntimeBundle structure.

        It defines:

            :methods:
                | test_bundle_creation - Tests creating bundle with mock components.
    '''

    def test_bundle_creation(self) -> None:
        '''
            Verifies AppRuntimeBundle exposes attributes and streamer property.

            :exceptions: None.
        '''
        repo: MagicMock = MagicMock(spec=ISerialPreferenceRepository)
        transport: MagicMock = MagicMock(spec=ITransport)
        streaming: MagicMock = MagicMock(spec=StreamingProvides)
        loader: MagicMock = MagicMock(spec=IPlanLoader)
        storer: MagicMock = MagicMock(spec=IPlanStorer)
        workspace: MagicMock = MagicMock(spec=IWorkspaceManager)
        controller: MagicMock = MagicMock(spec=IPlaybackController)
        streaming.playback_controller = controller

        bundle: AppRuntimeBundle = AppRuntimeBundle(
            connection_repo=repo,
            transport=transport,
            streaming=streaming,
            loader=loader,
            storer=storer,
            workspace=workspace,
        )
        self.assertIs(bundle.connection_repo, repo)
        self.assertIs(bundle.transport, transport)
        self.assertIs(bundle.streaming, streaming)
        self.assertIs(bundle.loader, loader)
        self.assertIs(bundle.storer, storer)
        self.assertIs(bundle.workspace, workspace)
        self.assertIs(bundle.streamer, controller)


if __name__ == '__main__':
    main()
