# -*- coding: UTF-8 -*-

'''
Module
    iconfig_loader_test.py
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
    Unit testing for IConfigLoader protocol specification.
'''

from __future__ import annotations

from unittest import TestCase, main

from ats_utilities.context.bundle import ContextBundle
from ats_utilities.context.factory import ContextBundleFactory

from scarajectory.infrastructure.storage.config_io.iconfig_loader import IConfigLoader

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConformingConfigLoaderStub:
    '''Conforming stub implementation satisfying IConfigLoader.'''

    def __init__(self, context_bundle: ContextBundle) -> None:
        self.context = context_bundle

    def get_context(self) -> ContextBundle:
        '''Returns context bundle.'''
        return self.context

    def load_configuration(self) -> dict[str, object]:
        '''Loads configuration.'''
        return {'key': 'value'}


class NonConformingConfigLoaderStub:
    '''Non-conforming stub missing load_configuration method.'''

    def __init__(self, context_bundle: ContextBundle) -> None:
        self.context = context_bundle

    def get_context(self) -> ContextBundle:
        '''Returns context bundle.'''
        return self.context

    def get_version(self) -> str:
        '''Returns version string.'''
        return '1.0.0'


class ConfigLoaderTestCase(TestCase):
    '''Unit tests validating structural protocol runtime checks for IConfigLoader.'''

    def test_protocol_conformance_success(self) -> None:
        '''Verifies conforming stub satisfies IConfigLoader protocol.'''
        context = ContextBundleFactory.create_bundle()
        stub = ConformingConfigLoaderStub(context)
        self.assertIsInstance(stub, IConfigLoader)

    def test_protocol_conformance_failure(self) -> None:
        '''Verifies non-conforming stub fails IConfigLoader protocol check.'''
        context = ContextBundleFactory.create_bundle()
        incomplete = NonConformingConfigLoaderStub(context)
        self.assertNotIsInstance(incomplete, IConfigLoader)


if __name__ == '__main__':
    main()
