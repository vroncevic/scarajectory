# -*- coding: UTF-8 -*-

'''
Module
    iconfig_io_factory_test.py
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
    Unit testing for IConfigIOFactory protocol specification.
'''

from __future__ import annotations

from typing import Any, Mapping
from unittest import TestCase, main

from ats_utilities.context.bundle import ContextBundle
from ats_utilities.context.factory import ContextBundleFactory

from scarajectory.infrastructure.storage.config_io.iconfig_io_factory import IConfigIOFactory
from scarajectory.infrastructure.storage.config_io.iconfig_loader import IConfigLoader
from scarajectory.infrastructure.storage.config_io.iconfig_storer import IConfigStorer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StubLoader:
    '''Structural test stub for IConfigLoader.'''

    def __init__(self, context: ContextBundle) -> None:
        self.context = context

    def get_context(self) -> ContextBundle:
        '''Returns context.'''
        return self.context

    def load_configuration(self) -> dict[str, object]:
        '''Loads configuration.'''
        return {}


class StubStorer:
    '''Structural test stub for IConfigStorer.'''

    def __init__(self, context: ContextBundle) -> None:
        self.context = context

    def get_context(self) -> ContextBundle:
        '''Returns context.'''
        return self.context

    def store_configuration(self, config: Mapping[str, Any]) -> bool:
        '''Stores configuration.'''
        _ = config
        return True


class ConformingConfigIOFactoryStub:
    '''Conforming stub implementation satisfying IConfigIOFactory.'''

    def __init__(self, context: ContextBundle) -> None:
        self.context = context

    def create_loader(self, filepath: str) -> IConfigLoader:
        '''Constructs loader.'''
        _ = filepath
        return StubLoader(self.context)

    def create_storer(self, filepath: str) -> IConfigStorer:
        '''Constructs storer.'''
        _ = filepath
        return StubStorer(self.context)

    def create_validated_loader(
        self, filepath: str, scheme_path: str
    ) -> IConfigLoader:
        '''Constructs validated loader.'''
        _ = (filepath, scheme_path)
        return StubLoader(self.context)


class NonConformingConfigIOFactoryStub:
    '''Non-conforming stub missing create_storer method.'''

    def __init__(self, context: ContextBundle) -> None:
        self.context = context

    def create_loader(self, filepath: str) -> IConfigLoader:
        '''Constructs loader.'''
        _ = filepath
        return StubLoader(self.context)

    def get_version(self) -> str:
        '''Returns version string.'''
        return '1.0.0'


class ConfigIOFactoryProtocolTestCase(TestCase):
    '''Unit tests validating structural protocol runtime checks for IConfigIOFactory.'''

    def test_protocol_conformance_success(self) -> None:
        '''Verifies conforming stub satisfies IConfigIOFactory protocol.'''
        context = ContextBundleFactory.create_bundle()
        stub = ConformingConfigIOFactoryStub(context)
        self.assertIsInstance(stub, IConfigIOFactory)

    def test_protocol_conformance_failure(self) -> None:
        '''Verifies non-conforming stub fails IConfigIOFactory protocol check.'''
        context = ContextBundleFactory.create_bundle()
        incomplete = NonConformingConfigIOFactoryStub(context)
        self.assertNotIsInstance(incomplete, IConfigIOFactory)


if __name__ == '__main__':
    main()
