# -*- coding: UTF-8 -*-

'''
Module
    registry.py
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
    Encapsulates core scarajectory components for simplification of scarajectory bundle.
'''

from __future__ import annotations

from ats_utilities.base.setup.bundle import BaseBundle

from scarajectory.core.service.iservice import IService
from scarajectory.core.service.itrajectory_streamer import ITrajectoryStreamer
from scarajectory.infrastructure.gui.igui import IGUI
from scarajectory.infrastructure.cli.icli import ICLI
from scarajectory.setup.bundle import SCARAjectoryBundle
from scarajectory.setup.validator import SCARAjectoryBundleValidator
from scarajectory.setup.keys import SCARAjectoryBundleKeys
from scarajectory.setup.dependencies import SCARAjectoryBundleDependencies
from scarajectory.setup.dep_validator import SCARAjectoryBundleDependenciesValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SCARAjectoryBundleRegistry:
    '''
        Encapsulates core scarajectory components for simplification of scarajectory bundle.

        It defines:

            :methods:
                | create_bundle - Creates the scarajectory bundle.
                | get_version - Returns the registry version.
    '''

    @classmethod
    def create_bundle(cls, dependencies: SCARAjectoryBundleDependencies) -> SCARAjectoryBundle:
        '''
            Creates the scarajectory bundle.

            :param dependencies: The scarajectory bundle dependencies.
            :return: The scarajectory bundle.
            :exceptions:
                | ATSValueError: The dependencies or bundle must be provided and valid.
                | ATSTypeError: The dependencies or bundle attributes must match types.
        '''
        SCARAjectoryBundleDependenciesValidator.validate(dependencies)

        base: BaseBundle | None = dependencies.get(SCARAjectoryBundleKeys.DEPENDENCY_BASE) if dependencies else None
        service: IService | None = dependencies.get(SCARAjectoryBundleKeys.DEPENDENCY_SERVICE) if dependencies else None
        gui: IGUI | None = dependencies.get(SCARAjectoryBundleKeys.DEPENDENCY_GUI) if dependencies else None
        streamer: ITrajectoryStreamer | None = dependencies.get(SCARAjectoryBundleKeys.DEPENDENCY_STREAMER) if dependencies else None
        cli: ICLI | None = dependencies.get(SCARAjectoryBundleKeys.DEPENDENCY_CLI) if dependencies else None

        bundle: SCARAjectoryBundle = SCARAjectoryBundle(
            base=base, service=service, gui=gui, streamer=streamer, cli=cli
        )
        SCARAjectoryBundleValidator.validate(bundle)

        return bundle

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the registry version.

            :return: The registry version string.
            :exceptions: None.
        '''
        return __version__
