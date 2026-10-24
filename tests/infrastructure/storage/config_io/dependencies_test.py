# -*- coding: UTF-8 -*-

'''
Module
    dependencies_test.py
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
    Unit testing for ConfigIODependencies parameter bundle dataclass.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main

from ats_utilities.context.bundle import ContextBundle
from ats_utilities.context.factory import ContextBundleFactory

from scarajectory.infrastructure.storage.config_io.dependencies import ConfigIODependencies

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConfigIODependenciesTestCase(TestCase):
    '''Unit tests validating ConfigIODependencies parameter bundle.'''

    def test_explicit_dependencies(self) -> None:
        '''Verifies construction with explicit context bundle.'''
        context = ContextBundleFactory.create_bundle()
        deps = ConfigIODependencies(context_bundle=context)
        self.assertIsInstance(deps.context_bundle, ContextBundle)
        self.assertIs(deps.context_bundle, context)

    def test_immutable_bundle(self) -> None:
        '''Verifies parameter bundle immutability.'''
        context = ContextBundleFactory.create_bundle()
        deps = ConfigIODependencies(context_bundle=context)
        with self.assertRaises(FrozenInstanceError):
            deps.context_bundle = context


if __name__ == '__main__':
    main()
