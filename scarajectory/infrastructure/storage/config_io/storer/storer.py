# -*- coding: UTF-8 -*-

'''
Module
    storer.py
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
    Dedicated configuration storer adapter encapsulating ATS Storer operations.
'''

from __future__ import annotations

from typing import Final

from ats_utilities.config_io.setup.factory import ConfigIOBundleFactory
from ats_utilities.config_io.setup.options import ConfigIOBundleOptions
from ats_utilities.config_io.storer.engine import Storer
from ats_utilities.context.bundle import ContextBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConfigStorer:
    '''
        Adapter persisting configuration dictionaries into files via ATS Storer.

        It defines:

            :attributes:
                | _context - The ATS ContextBundle for configuration I/O operations.
            :methods:
                | __init__ - Initializes storer with injected ATS ContextBundle.
                | store - Persists configuration content to target destination file.
                | get_version - Returns component version string.
    '''

    _context: ContextBundle

    def __init__(self, context_bundle: ContextBundle) -> None:
        '''
            Initializes storer adapter with injected context bundle.

            :param context_bundle: ATS ContextBundle instance.
            :exceptions: None.
        '''
        self._context: Final[ContextBundle] = context_bundle

    def store(
        self,
        filepath: str,
        data: dict[str, object]
    ) -> bool:
        '''
            Stores configuration dictionary into destination file path.

            :param filepath: Target destination file path.
            :param data: Dictionary containing configuration content.
            :return: True if storage succeeded, False otherwise.
            :exceptions: None.
        '''
        bundle = ConfigIOBundleFactory.create_bundle(
            ConfigIOBundleOptions(
                file_path=filepath,
                context_bundle=self._context,
            )
        )
        storer = Storer(bundle)
        storer.store_configuration(data)

        return True

    def get_version(self) -> str:
        '''
            Returns component version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
