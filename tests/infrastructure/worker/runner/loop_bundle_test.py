# -*- coding: UTF-8 -*-

'''
Module
    loop_bundle_test.py
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
    Unit tests for LoopRunnerBundle parameter object.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scaralang.core.service.protocol.iparser import IBinaryFrameParser

from scarajectory.core.model.streaming.pacing_config import StreamPacingConfig
from scarajectory.infrastructure.worker.dispatcher.idispatcher import IStepDispatcher
from scarajectory.infrastructure.worker.drainer.idrainer import IQueueDrainer
from scarajectory.infrastructure.worker.handler.ihandler import IStreamFrameHandler
from scarajectory.infrastructure.worker.runner.loop_bundle import LoopRunnerBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class LoopRunnerBundleTestCase(TestCase):
    '''
        Unit tests for LoopRunnerBundle.

        It defines:

            :methods:
                | test_loop_bundle_fields - Validates attributes assignment.
    '''

    def test_loop_bundle_fields(self) -> None:
        '''
            Validates correct assignment of loop bundle properties.

            :exceptions: None.
        '''
        mock_disp = MagicMock(spec=IStepDispatcher)
        mock_drain = MagicMock(spec=IQueueDrainer)
        mock_parser = MagicMock(spec=IBinaryFrameParser)
        mock_handler = MagicMock(spec=IStreamFrameHandler)
        mock_config = MagicMock(spec=StreamPacingConfig)

        bundle = LoopRunnerBundle(
            step_dispatcher=mock_disp,
            queue_drainer=mock_drain,
            frame_parser=mock_parser,
            frame_handler=mock_handler,
            pacing_config=mock_config,
        )

        self.assertIs(bundle.step_dispatcher, mock_disp)
        self.assertIs(bundle.queue_drainer, mock_drain)
        self.assertIs(bundle.frame_parser, mock_parser)
        self.assertIs(bundle.frame_handler, mock_handler)
        self.assertIs(bundle.pacing_config, mock_config)


if __name__ == '__main__':
    main()
