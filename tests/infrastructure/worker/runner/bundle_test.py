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
    Unit tests for RunnerBundle parameter object.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scaracom.bridge.transceiver.ibyte_sender import IByteSender

from scarajectory.core.model.streaming.pacing_config import StreamPacingConfig
from scarajectory.core.service.streaming.observer.idispatcher import IStreamObserverDispatcher
from scarajectory.infrastructure.pacing.provides import PacingProvides
from scarajectory.infrastructure.packet.istrategy import IPacketStrategy
from scarajectory.infrastructure.state.imachine import IStreamStateMachine
from scarajectory.infrastructure.worker.parser.bundle import ParserBundle
from scarajectory.infrastructure.worker.runner.bundle import RunnerBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class RunnerBundleTestCase(TestCase):
    '''
        Unit tests for RunnerBundle.

        It defines:

            :methods:
                | test_bundle_fields - Validates attributes assignment.
    '''

    def test_bundle_fields(self) -> None:
        '''
            Validates correct assignment of bundle properties.

            :exceptions: None.
        '''
        mock_pacing = MagicMock(spec=PacingProvides)
        mock_strategy = MagicMock(spec=IPacketStrategy)
        mock_sender = MagicMock(spec=IByteSender)
        mock_state = MagicMock(spec=IStreamStateMachine)
        mock_dispatcher = MagicMock(spec=IStreamObserverDispatcher)
        mock_config = MagicMock(spec=StreamPacingConfig)
        mock_parser = MagicMock(spec=ParserBundle)

        bundle = RunnerBundle(
            pacing_bundle=mock_pacing,
            packet_strategy=mock_strategy,
            byte_sender=mock_sender,
            state_controller=mock_state,
            observer_dispatcher=mock_dispatcher,
            pacing_config=mock_config,
            parser_bundle=mock_parser,
        )

        self.assertIs(bundle.pacing_bundle, mock_pacing)
        self.assertIs(bundle.packet_strategy, mock_strategy)
        self.assertIs(bundle.byte_sender, mock_sender)
        self.assertIs(bundle.state_controller, mock_state)
        self.assertIs(bundle.observer_dispatcher, mock_dispatcher)
        self.assertIs(bundle.pacing_config, mock_config)
        self.assertIs(bundle.parser_bundle, mock_parser)


if __name__ == '__main__':
    main()
