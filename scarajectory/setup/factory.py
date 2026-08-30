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
    Factory for creating the scarajectory bundle.
'''

from __future__ import annotations

from ats_utilities.base.setup.factory import BaseBundleFactory
from ats_utilities.base.setup.bundle import BaseBundle
from ats_utilities.base.setup.options import BaseBundleOptions
from ats_utilities.context.bundle import ContextBundle
from ats_utilities.context.factory import ContextBundleFactory

from scarajectory.core.model.scara_bounds_dto import ScaraBoundsDTO
from scarajectory.core.service.trajectory_validator import TrajectoryValidator
from scarajectory.core.service.serial_streamer import SerialStreamer
from scarajectory.core.service.engine import Service
from scarajectory.infrastructure.gui.engine import ScarajectoryGUI
from scarajectory.setup.bundle import SCARAjectoryBundle
from scarajectory.setup.options import SCARAjectoryBundleOptions
from scarajectory.setup.registry import SCARAjectoryBundleRegistry
from scarajectory.setup.dependencies import SCARAjectoryBundleDependencies
from scarajectory.setup.opt_validator import SCARAjectoryBundleOptionsValidator
from scarajectory.setup.keys import SCARAjectoryBundleKeys

__author__: str = 'Vladimir Roncevic'
__copyright__: str = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__: list[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__: str = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__: str = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SCARAjectoryBundleFactory:
    '''
        Factory for creating the scarajectory bundle.

        It defines:

            :attributes:
                | _info_file - Path to the scarajectory info file.
            :methods:
                | create_bundle - Creates the scarajectory bundle with optional pre-configured options.
                | get_version - Returns the factory version.
    '''

    _info_file: str = 'scarajectory/infrastructure/config/scarajectory.cfg'

    @classmethod
    def create_bundle(cls, options: SCARAjectoryBundleOptions | None = None) -> SCARAjectoryBundle:
        '''
            Creates the scarajectory bundle with optional pre-configured options.

            :param options: Optional pre-configured options for the bundle.
            :return: The scarajectory bundle.
            :exceptions:
                | ATSValueError: The options or dependencies must be valid.
                | ATSTypeError: The options or dependencies must match types.
        '''
        if options is not None:
            SCARAjectoryBundleOptionsValidator.validate(options)

        info_file: str = options.get(SCARAjectoryBundleKeys.OPTION_INFO_FILE) if options else cls._info_file

        context_bundle: ContextBundle = ContextBundleFactory.create_bundle()

        base_bundle: BaseBundle = BaseBundleFactory.create_bundle(
            options=BaseBundleOptions(
                info_file=info_file,
                use_generator=False,
                context_bundle=context_bundle
            )
        )

        bounds: ScaraBoundsDTO = ScaraBoundsDTO(l1=150.0, l2=120.0, z_min=0.0, z_max=100.0)
        validator: TrajectoryValidator = TrajectoryValidator(bounds=bounds)
        streamer: SerialStreamer = SerialStreamer()
        service: Service = Service(validator=validator, streamer=streamer)
        gui: ScarajectoryGUI = ScarajectoryGUI(service=service)

        if options and SCARAjectoryBundleKeys.OPTION_FILE_PATH in options:
            plan_path: str = options[SCARAjectoryBundleKeys.OPTION_FILE_PATH]
            if plan_path:
                gui.load_file(plan_path)

        return SCARAjectoryBundleRegistry.create_bundle(
            dependencies=SCARAjectoryBundleDependencies(
                base=base_bundle,
                service=service,
                gui=gui,
                streamer=streamer
            )
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version.

            :return: The factory version string.
            :exceptions: None.
        '''
        return __version__
