# -*- coding: UTF-8 -*-

'''
Module
    factory.py
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
    Factory responsible for assembling bounds subsystem.
'''

from __future__ import annotations

from scarajectory.infrastructure.settings.bounds.dependencies import BoundsDependencies
from scarajectory.infrastructure.settings.bounds.loader.dependencies import LoaderDependencies
from scarajectory.infrastructure.settings.bounds.loader.factory import BoundsLoaderFactory
from scarajectory.infrastructure.settings.bounds.loader.provides import LoaderProvides
from scarajectory.infrastructure.settings.bounds.parser.factory import BoundsParserFactory
from scarajectory.infrastructure.settings.bounds.parser.provides import ParserProvides
from scarajectory.infrastructure.settings.bounds.provides import BoundsProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BoundsFactory:
    '''
        Factory responsible for assembling bounds subsystem.

        It defines:

            :methods:
                | create - Assembles and wires bounds subsystem returning BoundsProvides.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls, dependencies: BoundsDependencies) -> BoundsProvides:
        '''
            Assembles and wires bounds subsystem returning BoundsProvides.

            :param dependencies: BoundsDependencies parameter bundle.
            :return: BoundsProvides container holding configured bounds components.
            :exceptions: None.
        '''
        parser_provides: ParserProvides = BoundsParserFactory.create()
        loader_provides: LoaderProvides = BoundsLoaderFactory.create(
            LoaderDependencies(
                settings_reader=dependencies.settings_reader,
                bounds_parser=parser_provides.bounds_parser,
            )
        )

        return BoundsProvides(
            bounds_loader=loader_provides.bounds_loader,
            bounds_parser=parser_provides.bounds_parser,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
