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

import os
import json
from typing import Any

from ats_utilities.base.setup.factory import BaseBundleFactory
from ats_utilities.base.setup.bundle import BaseBundle
from ats_utilities.base.setup.options import BaseBundleOptions
from ats_utilities.context.bundle import ContextBundle
from ats_utilities.context.factory import ContextBundleFactory
from ats_utilities.config_io.processor.json_processor import JSONProcessor

from scarajectory.core.model.scara_bounds import ScaraBounds
from scarajectory.core.model.trajectory_plan import TrajectoryPlan
from scarajectory.core.service.trajectory_validator import TrajectoryValidator
from scarajectory.core.service.plan_storage_service import PlanStorageService
from scarajectory.core.service.engine import Service
from scarajectory.infrastructure.communication.transport.serial_transport import SerialTransport
from scarajectory.infrastructure.communication.serial_streamer import SerialStreamer
from scarajectory.infrastructure.gui.engine import ScarajectoryGUI
from scarajectory.infrastructure.cli.engine import CLI
from scarajectory.infrastructure.cli.setup.bundle import CLIBundle
from scarajectory.infrastructure.cli.setup.options import CLIBundleOptions
from scarajectory.infrastructure.cli.setup.factory import CLIBundleFactory
from scarajectory.setup.bundle import SCARAjectoryBundle
from scarajectory.setup.options import SCARAjectoryBundleOptions
from scarajectory.setup.registry import SCARAjectoryBundleRegistry
from scarajectory.setup.dependencies import SCARAjectoryBundleDependencies
from scarajectory.setup.opt_validator import SCARAjectoryBundleOptionsValidator
from scarajectory.setup.keys import SCARAjectoryBundleKeys

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SCARAjectoryBundleFactory:
    '''
        Factory for creating the scarajectory bundle.

        It defines:

            :attributes:
                | _info_file - Path to the scarajectory info file.
                | _geometry_config_file - Path to default robot geometry config file.
                | _geometry_scheme_file - Path to robot geometry validation scheme.
            :methods:
                | _resolve_bounds - Resolves and constructs ScaraBounds from JSON config and options.
                | create_bundle - Creates the scarajectory bundle with optional pre-configured options.
                | get_version - Returns the factory version.
    '''

    _info_file: str = 'scarajectory/infrastructure/config/scarajectory.cfg'
    _geometry_config_file: str = 'scarajectory/infrastructure/config/scara_geometry.json'
    _geometry_scheme_file: str = 'scarajectory/infrastructure/config/scheme.json'

    @classmethod
    def _resolve_bounds(cls, options: SCARAjectoryBundleOptions | None = None) -> ScaraBounds:
        '''
            Resolves and constructs ScaraBounds from JSON configuration and options.

            :param options: Optional bundle configuration options.
            :return: ScaraBounds domain model.
            :exceptions: None.
        '''
        config_path: str = cls._geometry_config_file
        if options and SCARAjectoryBundleKeys.OPTION_ROBOT_CONFIG in options:
            config_path = str(options[SCARAjectoryBundleKeys.OPTION_ROBOT_CONFIG])

        config_data: dict[str, Any] = {}

        if os.path.exists(config_path) and os.path.exists(cls._geometry_scheme_file):
            try:
                with open(cls._geometry_scheme_file, 'r', encoding='utf-8') as sf:
                    scheme = json.load(sf)

                processor: JSONProcessor = JSONProcessor(scheme=scheme)

                with open(config_path, 'r', encoding='utf-8') as cf:
                    if processor.deserialize(cf.read()) and processor.validate_by_scheme():
                        config_data = processor.to_dict()

            except (OSError, json.JSONDecodeError):
                config_data = {}

        l1: float = (
            float(options[SCARAjectoryBundleKeys.OPTION_L1])
            if options and SCARAjectoryBundleKeys.OPTION_L1 in options
            else float(config_data.get('l1', 150.0))
        )
        l2: float = (
            float(options[SCARAjectoryBundleKeys.OPTION_L2])
            if options and SCARAjectoryBundleKeys.OPTION_L2 in options
            else float(config_data.get('l2', 120.0))
        )
        z_min: float = (
            float(options[SCARAjectoryBundleKeys.OPTION_Z_MIN])
            if options and SCARAjectoryBundleKeys.OPTION_Z_MIN in options
            else float(config_data.get('z_min', 0.0))
        )
        z_max: float = (
            float(options[SCARAjectoryBundleKeys.OPTION_Z_MAX])
            if options and SCARAjectoryBundleKeys.OPTION_Z_MAX in options
            else float(config_data.get('z_max', 100.0))
        )
        min_speed: float = (
            float(options[SCARAjectoryBundleKeys.OPTION_MIN_SPEED])
            if options and SCARAjectoryBundleKeys.OPTION_MIN_SPEED in options
            else float(config_data.get('min_speed', 1.0))
        )
        max_speed: float = (
            float(options[SCARAjectoryBundleKeys.OPTION_MAX_SPEED])
            if options and SCARAjectoryBundleKeys.OPTION_MAX_SPEED in options
            else float(config_data.get('max_speed', 100.0))
        )

        return ScaraBounds(
            l1=l1,
            l2=l2,
            z_min=z_min,
            z_max=z_max,
            min_speed=min_speed,
            max_speed=max_speed
        )

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

        info_file: str = (
            options[SCARAjectoryBundleKeys.OPTION_INFO_FILE]
            if options and SCARAjectoryBundleKeys.OPTION_INFO_FILE in options
            else cls._info_file
        )

        context_bundle: ContextBundle = ContextBundleFactory.create_bundle()

        base_bundle: BaseBundle = BaseBundleFactory.create_bundle(
            options=BaseBundleOptions(
                info_file=info_file,
                use_generator=False,
                context_bundle=context_bundle
            )
        )

        bounds: ScaraBounds = cls._resolve_bounds(options=options)
        validator: TrajectoryValidator = TrajectoryValidator(bounds=bounds)
        transport: SerialTransport = SerialTransport()
        streamer: SerialStreamer = SerialStreamer(transport=transport)
        storage: PlanStorageService = PlanStorageService()
        plan: TrajectoryPlan = TrajectoryPlan()
        service: Service = Service(validator=validator, streamer=streamer, storage=storage, plan=plan)
        gui: ScarajectoryGUI = ScarajectoryGUI(service=service)

        cli_bundle: CLIBundle = CLIBundleFactory.create_bundle(
            options=CLIBundleOptions(
                service=service,
                parser=base_bundle.option_manager,
                gui=gui
            )
        )

        cli: CLI = CLI(cli_bundle)

        return SCARAjectoryBundleRegistry.create_bundle(
            dependencies=SCARAjectoryBundleDependencies(
                base=base_bundle,
                service=service,
                gui=gui,
                streamer=streamer,
                cli=cli
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
