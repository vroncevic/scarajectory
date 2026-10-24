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
    Factory responsible for assembling settings subsystem.
'''

from __future__ import annotations

from scarajectory.infrastructure.settings.bounds.dependencies import BoundsDependencies
from scarajectory.infrastructure.settings.bounds.factory import BoundsFactory
from scarajectory.infrastructure.settings.bounds.provides import BoundsProvides
from scarajectory.infrastructure.settings.dependencies import SettingsDependencies
from scarajectory.infrastructure.settings.provides import SettingsProvides
from scarajectory.infrastructure.settings.reader.dependencies import ReaderDependencies
from scarajectory.infrastructure.settings.reader.factory import ReaderFactory
from scarajectory.infrastructure.settings.reader.provides import ReaderProvides
from scarajectory.infrastructure.settings.transmission.dependencies import TransmissionDependencies
from scarajectory.infrastructure.settings.transmission.factory import TransmissionFactory
from scarajectory.infrastructure.settings.transmission.provides import TransmissionProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SettingsFactory:
    '''
        Factory responsible for assembling settings subsystem.

        It defines:

            :methods:
                | create - Assembles and wires settings subsystem returning SettingsProvides.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        dependencies: SettingsDependencies
    ) -> SettingsProvides:
        '''
            Assembles and wires settings subsystem returning SettingsProvides.

            :param dependencies: SettingsDependencies parameter bundle.
            :return: SettingsProvides container holding configured components.
            :exceptions: None.
        '''
        reader_provides: ReaderProvides = ReaderFactory.create(
            ReaderDependencies(
                config_loader=dependencies.config_loader,
                config_path=dependencies.config_path,
                scheme_path=dependencies.scheme_path,
            )
        )
        bounds_provides: BoundsProvides = BoundsFactory.create(
            BoundsDependencies(settings_reader=reader_provides.settings_reader)
        )
        trans_provides: TransmissionProvides = TransmissionFactory.create(
            TransmissionDependencies(settings_reader=reader_provides.settings_reader)
        )

        return SettingsProvides(
            settings_reader=reader_provides.settings_reader,
            bounds_provides=bounds_provides,
            transmission_provides=trans_provides,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
