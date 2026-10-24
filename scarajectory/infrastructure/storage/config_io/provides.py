# -*- coding: UTF-8 -*-

'''
Module
    provides.py
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
    Provides container exposing configuration I/O loader and storer interfaces.
'''

from __future__ import annotations

from dataclasses import dataclass

from scarajectory.infrastructure.storage.config_io.loader.iloader import IConfigLoader
from scarajectory.infrastructure.storage.config_io.storer.istorer import IConfigStorer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True)
class ConfigIOProvides:
    '''
        Immutable container providing configuration loader and storer interfaces.

        It defines:

            :attributes:
                | config_loader - Injected IConfigLoader protocol instance.
                | config_storer - Injected IConfigStorer protocol instance.
    '''

    config_loader: IConfigLoader
    config_storer: IConfigStorer
