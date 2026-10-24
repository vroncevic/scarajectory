# -*- coding: UTF-8 -*-

'''
Module
    iparser_test.py
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
    Unit testing for IScaraBoundsParser protocol conformance.
'''

from __future__ import annotations

from collections.abc import Mapping
from unittest import TestCase, main

from scarajectory.infrastructure.settings.bounds.parser.factory import BoundsParserFactory
from scarajectory.infrastructure.settings.bounds.parser.iparser import IScaraBoundsParser
from scarajectory.infrastructure.settings.bounds.parser.provides import ParserProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConformingBoundsParserStub:
    '''Conforming stub implementation satisfying IScaraBoundsParser protocol.'''

    def parse_geometry(
        self, *, options: Mapping[str, object], cfg: Mapping[str, float]
    ) -> dict[str, float]:
        '''Parses geometry.'''
        _ = (options, cfg)
        return {'l1': 150.0}

    def parse_motion(
        self, *, options: Mapping[str, object], cfg: Mapping[str, float]
    ) -> dict[str, float]:
        '''Parses motion.'''
        _ = (options, cfg)
        return {'min_speed': 1.0}

    def parse_joints(
        self, *, options: Mapping[str, object], cfg: Mapping[str, float]
    ) -> dict[str, float]:
        '''Parses joints.'''
        _ = (options, cfg)
        return {'j1_min_rad': -2.6}

    def parse_singularities(
        self, *, options: Mapping[str, object], cfg: Mapping[str, float]
    ) -> dict[str, float]:
        '''Parses singularities.'''
        _ = (options, cfg)
        return {'singularity_outer_margin_mm': 3.0}


class IncompleteBoundsParserStub:
    '''Non-conforming stub implementation missing parse_singularities.'''

    def parse_geometry(
        self, *, options: Mapping[str, object], cfg: Mapping[str, float]
    ) -> dict[str, float]:
        '''Parses geometry.'''
        _ = (options, cfg)
        return {}

    def other_action(self) -> None:
        '''Dummy method to satisfy method count.'''


class ScaraBoundsParserProtocolTestCase(TestCase):
    '''
        Tests IScaraBoundsParser runtime checkable protocol conformance.

        It defines:

            :methods:
                | test_protocol_conformance_success - Verifies conforming class passes check.
                | test_protocol_conformance_failure - Verifies non-conforming class fails check.
                | test_parser_conformance - Verifies concrete ScaraBoundsParser satisfies it.
    '''

    def test_protocol_conformance_success(self) -> None:
        '''Verifies compliant class satisfies IScaraBoundsParser protocol.'''
        stub = ConformingBoundsParserStub()
        self.assertIsInstance(stub, IScaraBoundsParser)

    def test_protocol_conformance_failure(self) -> None:
        '''Verifies non-compliant class fails IScaraBoundsParser protocol check.'''
        stub = IncompleteBoundsParserStub()
        self.assertNotIsInstance(stub, IScaraBoundsParser)

    def test_parser_conformance(self) -> None:
        '''Verifies concrete parser structurally satisfies IScaraBoundsParser.'''
        provides: ParserProvides = BoundsParserFactory.create()
        self.assertIsInstance(provides.bounds_parser, IScaraBoundsParser)


if __name__ == '__main__':
    main()
