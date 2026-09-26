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

from os.path import abspath, dirname, join

from ats_utilities.base.setup.bundle import BaseBundle
from ats_utilities.base.setup.factory import BaseBundleFactory
from ats_utilities.base.setup.options import BaseBundleOptions
from ats_utilities.context.bundle import ContextBundle
from ats_utilities.context.factory import ContextBundleFactory

from scarajectory.infrastructure.settings.config_loader_factory import ScaraConfigLoaderFactory
from scarajectory.core.service.config.iscara_config_loader import IScaraConfigLoader
from scarajectory.core.model.kinematics.scara_bounds import ScaraBounds
from scarajectory.core.model.kinematics.transmission_parameters import TransmissionParameters
from scarajectory.core.service.trajectory.plan.trajectory_plan import TrajectoryPlan
from scarajectory.core.service.trajectory.plan.trajectory_plan_factory import TrajectoryPlanFactory
from scarajectory.core.service.kinematics.ikinematics_service import IKinematicsService
from scarajectory.core.service.kinematics.kinematics_service_factory import KinematicsServiceFactory
from scarajectory.core.service.trajectory.validation.itrajectory_validator import ITrajectoryValidator
from scarajectory.core.service.trajectory.validation.trajectory_validator_factory import TrajectoryValidatorFactory
from scarajectory.infrastructure.communication.preferences.connection_repository import ConnectionRepository
from scarajectory.infrastructure.communication.preferences.connection_repository_factory import ConnectionRepositoryFactory
from scarajectory.infrastructure.storage.plan_storage_service import PlanStorageService
from scarajectory.infrastructure.storage.plan_storage_service_factory import PlanStorageServiceFactory
from scaralang.core.service.dsl.iscara_dsl_service import IScaraDslService
from scaralang.core.service.dsl.scara_dsl_service_factory import ScaraDslServiceFactory
from scarajectory.core.service.engine import Service
from scarajectory.core.service.service_factory import ServiceFactory
from scarajectory.infrastructure.communication.transport.itransport import ITransport
from scarajectory.infrastructure.communication.transport.transport_factory import TransportFactory
from scarajectory.core.service.communication.stream.itrajectory_streamer import ITrajectoryStreamer
from scarajectory.infrastructure.communication.streamer.trajectory_streamer_factory import TrajectoryStreamerFactory
from scarajectory.infrastructure.gui.engine import ScarajectoryGUI
from scarajectory.infrastructure.gui.gui_factory import ScarajectoryGUIFactory
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
__version__ = '1.0.3'
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
                | resolve_bounds - Resolves and constructs ScaraBounds from JSON config and options.
                | create_bundle - Creates the scarajectory bundle with optional pre-configured options.
                | get_version - Returns the factory version.
    '''

    _info_file: str = join(
        dirname(dirname(abspath(__file__))),
        'infrastructure', 'config', 'scarajectory.cfg'
    )
    _geometry_config_file: str = join(
        dirname(dirname(abspath(__file__))),
        'infrastructure', 'config', 'scara_geometry.json'
    )
    _geometry_scheme_file: str = join(
        dirname(dirname(abspath(__file__))),
        'infrastructure', 'config', 'scheme.json'
    )

    @classmethod
    def resolve_bounds(cls) -> ScaraBounds:
        '''
            Resolves and constructs ScaraBounds from JSON configuration.

            :return: ScaraBounds domain model.
            :exceptions: None.
        '''
        loader: IScaraConfigLoader = ScaraConfigLoaderFactory.create()

        return loader.load_bounds()

    @classmethod
    def resolve_bounds_with_options(
        cls,
        options: SCARAjectoryBundleOptions,
    ) -> ScaraBounds:
        '''
            Resolves and constructs ScaraBounds from JSON configuration and options.

            :param options: Bundle configuration options.
            :return: ScaraBounds domain model.
            :exceptions: None.
        '''
        opts_dict: dict[str, object] = {}
        if SCARAjectoryBundleKeys.OPTION_L1 in options:
            opts_dict['l1'] = options[SCARAjectoryBundleKeys.OPTION_L1]
        if SCARAjectoryBundleKeys.OPTION_L2 in options:
            opts_dict['l2'] = options[SCARAjectoryBundleKeys.OPTION_L2]
        if SCARAjectoryBundleKeys.OPTION_Z_MIN in options:
            opts_dict['z_min'] = options[SCARAjectoryBundleKeys.OPTION_Z_MIN]
        if SCARAjectoryBundleKeys.OPTION_Z_MAX in options:
            opts_dict['z_max'] = options[SCARAjectoryBundleKeys.OPTION_Z_MAX]
        if SCARAjectoryBundleKeys.OPTION_MIN_SPEED in options:
            opts_dict['min_speed'] = options[SCARAjectoryBundleKeys.OPTION_MIN_SPEED]
        if SCARAjectoryBundleKeys.OPTION_MAX_SPEED in options:
            opts_dict['max_speed'] = options[SCARAjectoryBundleKeys.OPTION_MAX_SPEED]

        loader: IScaraConfigLoader = ScaraConfigLoaderFactory.create()

        if opts_dict:
            return loader.load_bounds_with_options(options=opts_dict)

        return loader.load_bounds()

    @classmethod
    def create_bundle(cls) -> SCARAjectoryBundle:
        '''
            Creates the scarajectory bundle with default options.

            :return: The scarajectory bundle.
            :exceptions: None.
        '''
        info_file: str = cls._info_file
        base_bundle: BaseBundle = BaseBundleFactory.create_bundle(
            options=BaseBundleOptions(
                info_file=info_file,
                use_generator=False,
                context_bundle=ContextBundleFactory.create_bundle(),
            )
        )
        context_bundle: ContextBundle = base_bundle.context_bundle
        connection_repo: ConnectionRepository = ConnectionRepositoryFactory.create(
            context_bundle=context_bundle
        )

        loader: IScaraConfigLoader = ScaraConfigLoaderFactory.create()
        bounds: ScaraBounds = cls.resolve_bounds()
        transmission: TransmissionParameters = loader.load_transmission()
        kinematics: IKinematicsService = KinematicsServiceFactory.create(
            bounds=bounds,
        )
        validator: ITrajectoryValidator = TrajectoryValidatorFactory.create(
            kinematics=kinematics,
        )
        transport: ITransport = TransportFactory.create_default_transport()
        streamer: ITrajectoryStreamer = TrajectoryStreamerFactory.create(
            transport=transport
        )
        storage: PlanStorageService = PlanStorageServiceFactory.create_with_context(
            context_bundle=context_bundle
        )
        plan: TrajectoryPlan = TrajectoryPlanFactory.create()
        dsl_service: IScaraDslService = ScaraDslServiceFactory.create(
            validator=validator,
            kinematics=kinematics,
            transmission=transmission,
        )
        service: Service = ServiceFactory.create(
            validator=validator,
            streamer=streamer,
            storage=storage,
            plan=plan,
            dsl_service=dsl_service,
        )
        gui: ScarajectoryGUI = ScarajectoryGUIFactory.create(
            service=service,
            connection_repository=connection_repo,
        )
        cli_bundle: CLIBundle = CLIBundleFactory.create_bundle(
            options=CLIBundleOptions(
                service=service,
                parser=base_bundle.option_manager,
                gui=gui,
            )
        )
        cli: CLI = CLI(bundle=cli_bundle)

        return SCARAjectoryBundleRegistry.create_bundle(
            dependencies=SCARAjectoryBundleDependencies(
                base=base_bundle,
                service=service,
                gui=gui,
                streamer=streamer,
                cli=cli,
            )
        )

    @classmethod
    def create_bundle_with_options(
        cls,
        options: SCARAjectoryBundleOptions,
    ) -> SCARAjectoryBundle:
        '''
            Creates the scarajectory bundle with pre-configured options.

            :param options: Pre-configured options for the bundle.
            :return: The scarajectory bundle.
            :exceptions:
                | ATSValueError: The options or dependencies must be valid.
                | ATSTypeError: The options or dependencies must match types.
        '''
        SCARAjectoryBundleOptionsValidator.validate(options)

        info_file: str = (
            options[SCARAjectoryBundleKeys.OPTION_INFO_FILE]
            if SCARAjectoryBundleKeys.OPTION_INFO_FILE in options
            else cls._info_file
        )

        base_bundle: BaseBundle = BaseBundleFactory.create_bundle(
            options=BaseBundleOptions(
                info_file=info_file,
                use_generator=False,
                context_bundle=ContextBundleFactory.create_bundle(),
            )
        )
        context_bundle: ContextBundle = base_bundle.context_bundle
        connection_repo: ConnectionRepository = ConnectionRepositoryFactory.create(
            context_bundle=context_bundle
        )

        loader: IScaraConfigLoader = ScaraConfigLoaderFactory.create()
        bounds: ScaraBounds = cls.resolve_bounds_with_options(options=options)
        transmission: TransmissionParameters = loader.load_transmission()
        kinematics: IKinematicsService = KinematicsServiceFactory.create(
            bounds=bounds,
        )
        validator: ITrajectoryValidator = TrajectoryValidatorFactory.create(
            kinematics=kinematics,
        )
        transport: ITransport = TransportFactory.create_default_transport()
        streamer: ITrajectoryStreamer = TrajectoryStreamerFactory.create(
            transport=transport
        )
        storage: PlanStorageService = PlanStorageServiceFactory.create_with_context(
            context_bundle=context_bundle
        )
        plan: TrajectoryPlan = TrajectoryPlanFactory.create()
        dsl_service: IScaraDslService = ScaraDslServiceFactory.create(
            validator=validator,
            kinematics=kinematics,
            transmission=transmission,
        )
        service: Service = ServiceFactory.create(
            validator=validator,
            streamer=streamer,
            storage=storage,
            plan=plan,
            dsl_service=dsl_service,
        )
        gui: ScarajectoryGUI = ScarajectoryGUIFactory.create(
            service=service,
            connection_repository=connection_repo,
        )

        cli_bundle: CLIBundle = CLIBundleFactory.create_bundle(
            options=CLIBundleOptions(
                service=service,
                parser=base_bundle.option_manager,
                gui=gui,
            )
        )

        cli: CLI = CLI(bundle=cli_bundle)

        return SCARAjectoryBundleRegistry.create_bundle(
            dependencies=SCARAjectoryBundleDependencies(
                base=base_bundle,
                service=service,
                gui=gui,
                streamer=streamer,
                cli=cli,
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
