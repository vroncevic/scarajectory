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
    Unit tests for ParserBundle dataclass.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scaralang.core.service.protocol.iparser import IBinaryFrameParser
from scaralang.core.service.protocol.iresponse_unpacker import IBinaryResponsePayloadUnpacker

from scarajectory.infrastructure.worker.parser.bundle import ParserBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ParserBundleTestCase(TestCase):
    '''
        Tests ParserBundle initialization and property access.

        It defines:

            :methods:
                | test_parser_bundle_instantiation - Verifies valid instantiation.
    '''

    def test_parser_bundle_instantiation(self) -> None:
        '''
            Verifies valid instantiation and attribute assignments.

            :exceptions: None.
        '''
        mock_parser = MagicMock(spec=IBinaryFrameParser)
        mock_unpacker = MagicMock(spec=IBinaryResponsePayloadUnpacker)
        bundle = ParserBundle(
            frame_parser=mock_parser,
            response_unpacker=mock_unpacker,
        )
        self.assertIs(bundle.frame_parser, mock_parser)
        self.assertIs(bundle.response_unpacker, mock_unpacker)


if __name__ == '__main__':
    main()
