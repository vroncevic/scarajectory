# -*- coding: UTF-8 -*-

'''
Module
    config_io_factory.py
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
    Dedicated factory constructing ATS Loader and Storer instances for configuration I/O.
'''

from __future__ import annotations

from os.path import exists
from typing import Final

from ats_utilities.config_io.loader.engine import Loader
from ats_utilities.config_io.setup.factory import ConfigIOBundleFactory
from ats_utilities.config_io.setup.keys import ConfigIOBundleKeys
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


class ConfigIOFactory:
    '''
        Factory constructing Loader and Storer components bound to an ATS ContextBundle.

        It defines:

            :attributes:
                | _context - The ATS ContextBundle for configuration I/O operations.
            :methods:
                | __init__ - Initializes factory with injected ATS ContextBundle.
                | create_loader - Constructs ATS Loader for given file path.
                | create_storer - Constructs ATS Storer for given file path.
                | create_validated_loader - Constructs validated ATS Loader with JSON schema.
                | create - Factory class method creating ConfigIOFactory instance.
                | get_version - Returns factory version string.
    '''

    _context: ContextBundle

    def __init__(self, context_bundle: ContextBundle) -> None:
        '''
            Initializes factory with injected context bundle.

            :param context_bundle: ATS ContextBundle instance.
            :exceptions: None.
        '''
        self._context: Final[ContextBundle] = context_bundle

    def create_loader(self, filepath: str) -> Loader:
        '''
            Constructs ATS Loader for specified file path.

            :param filepath: Target file path.
            :return: Instantiated Loader object.
            :exceptions: None.
        '''
        bundle = ConfigIOBundleFactory.create_bundle(
            ConfigIOBundleOptions(
                file_path=filepath,
                context_bundle=self._context,
            )
        )
        return Loader(bundle)

    def create_storer(self, filepath: str) -> Storer:
        '''
            Constructs ATS Storer for specified file path.

            :param filepath: Target file path.
            :return: Instantiated Storer object.
            :exceptions: None.
        '''
        bundle = ConfigIOBundleFactory.create_bundle(
            ConfigIOBundleOptions(
                file_path=filepath,
                context_bundle=self._context,
            )
        )
        return Storer(bundle)

    def create_validated_loader(
        self,
        filepath: str,
        scheme_path: str,
    ) -> Loader:
        '''
            Constructs validated ATS Loader applying schema validation if available.

            :param filepath: Target configuration file path.
            :param scheme_path: Validation schema file path.
            :return: Instantiated Loader object with optional schema validation.
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
        return Loader(config_bundle)

    @classmethod
    def create(cls, context_bundle: ContextBundle) -> ConfigIOFactory:
        '''
            Factory creation method instantiating ConfigIOFactory.

            :param context_bundle: ATS ContextBundle instance.
            :return: ConfigIOFactory instance.
        '''
        return cls(context_bundle)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string.

            :return: Factory version string.
        '''
        return __version__
