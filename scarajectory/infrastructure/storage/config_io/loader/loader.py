# -*- coding: UTF-8 -*-

'''
Module
    loader.py
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
    Dedicated configuration loader adapter encapsulating ATS Loader operations.
'''

from __future__ import annotations

from os.path import exists
from typing import Final

from ats_utilities.config_io.loader.engine import Loader
from ats_utilities.config_io.setup.factory import ConfigIOBundleFactory
from ats_utilities.config_io.setup.keys import ConfigIOBundleKeys
from ats_utilities.config_io.setup.options import ConfigIOBundleOptions
from ats_utilities.context.bundle import ContextBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConfigLoader:
    '''
        Adapter loading configuration files and applying optional schema validation.

        It defines:

            :attributes:
                | _context - The ATS ContextBundle for configuration I/O operations.
            :methods:
                | __init__ - Initializes loader with injected ATS ContextBundle.
                | load - Loads and deserializes configuration content from file.
                | load_validated - Loads configuration with optional JSON schema validation.
    '''

    _context: ContextBundle

    def __init__(self, context_bundle: ContextBundle) -> None:
        '''
            Initializes loader adapter with injected context bundle.

            :param context_bundle: ATS ContextBundle instance.
            :exceptions: None.
        '''
        self._context: Final[ContextBundle] = context_bundle

    def load(self, filepath: str) -> dict[str, object]:
        '''
            Loads configuration from file path and returns structured dictionary.

            :param filepath: Target file path.
            :return: Dictionary containing parsed configuration key-value mappings.
            :exceptions: None.
        '''
        bundle = ConfigIOBundleFactory.create_bundle(
            ConfigIOBundleOptions(
                file_path=filepath,
                context_bundle=self._context,
            )
        )
        loader = Loader(bundle)

        return loader.load_configuration()

    def load_validated(
        self,
        filepath: str,
        scheme_path: str
    ) -> dict[str, object]:
        '''
            Loads configuration and validates against specified JSON schema.

            :param filepath: Target configuration file path.
            :param scheme_path: Validation schema file path.
            :return: Dictionary containing validated configuration.
            :exceptions: None.
        '''
        opts: dict[str, object] = {
            ConfigIOBundleKeys.OPTION_FILE_PATH: filepath,
            ConfigIOBundleKeys.OPTION_CONTEXT_BUNDLE: self._context,
        }

        if exists(scheme_path):
            scheme_bundle = ConfigIOBundleFactory.create_bundle(
                ConfigIOBundleOptions({
                    ConfigIOBundleKeys.OPTION_FILE_PATH: scheme_path,
                    ConfigIOBundleKeys.OPTION_CONTEXT_BUNDLE: self._context,
                })
            )
            scheme: object = Loader(scheme_bundle).load_configuration()

            if bool(scheme):
                opts[ConfigIOBundleKeys.OPTION_SCHEME] = scheme

        config_bundle = ConfigIOBundleFactory.create_bundle(
            ConfigIOBundleOptions(opts)
        )
        loader = Loader(config_bundle)

        return loader.load_configuration()
