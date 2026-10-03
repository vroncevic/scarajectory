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
from scaralang.core.model.kinematics.scara_bounds import ScaraBounds
from scarajectory.core.service.settings.iscara_bounds_loader import IScaraBoundsLoader
from scarajectory.infrastructure.settings.bounds.scara_bounds_loader_factory import ScaraBoundsLoaderFactory
from scarajectory.infrastructure.settings.settings_reader import SettingsReader
from scarajectory.infrastructure.settings.settings_reader_factory import SettingsReaderFactory
from scarajectory.setup.assembly.app_core_assembler import AppCoreAssembler
from scarajectory.setup.assembly.app_core_bundle import AppCoreBundle
from scarajectory.setup.assembly.app_presentation_assembler import AppPresentationAssembler
from scarajectory.setup.assembly.app_runtime_assembler import AppRuntimeAssembler
from scarajectory.setup.assembly.app_runtime_bundle import AppRuntimeBundle
from scarajectory.setup.bundle import SCARAjectoryBundle
from scarajectory.setup.keys import SCARAjectoryBundleKeys
from scarajectory.setup.opt_validator import SCARAjectoryBundleOptionsValidator
from scarajectory.setup.options import SCARAjectoryBundleOptions
from scarajectory.setup.pipeline.plan_pipeline_builder import PlanPipelineBuilder
from scarajectory.setup.pipeline.plan_pipeline_bundle import PlanPipelineBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SCARAjectoryBundleFactory:
    '''
        Factory for creating the scarajectory bundle.

        It defines:

            :attributes:
                | _info_file - Path to the scarajectory info file.
            :methods:
                | resolve_bounds - Resolves ScaraBounds from config.
                | resolve_bounds_with_options - Resolves bounds from options.
                | create_bundle - Creates scarajectory bundle with defaults.
                | create_bundle_with_options - Creates bundle with options.
                | get_version - Returns the factory version string.
    '''

    _info_file: str = join(
        dirname(dirname(abspath(__file__))),
        'infrastructure', 'config', 'scarajectory.cfg'
    )

    @classmethod
    def resolve_bounds(cls) -> ScaraBounds:
        '''
            Resolves and constructs ScaraBounds from JSON configuration.

            :return: ScaraBounds domain model.
            :exceptions: None.
        '''
        return cls.resolve_bounds_with_options(
            options=SCARAjectoryBundleOptions({}),
            context_bundle=ContextBundleFactory.create_bundle(),
        )

    @classmethod
    def resolve_bounds_with_options(
        cls,
        options: SCARAjectoryBundleOptions,
        context_bundle: ContextBundle,
    ) -> ScaraBounds:
        '''
            Resolves ScaraBounds from JSON configuration and options.

            :param options: Bundle configuration options.
            :param context_bundle: Shared ATS ContextBundle instance.
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
            opts_dict['min_speed'] = options[
                SCARAjectoryBundleKeys.OPTION_MIN_SPEED
            ]
        if SCARAjectoryBundleKeys.OPTION_MAX_SPEED in options:
            opts_dict['max_speed'] = options[
                SCARAjectoryBundleKeys.OPTION_MAX_SPEED
            ]

        reader: SettingsReader = SettingsReaderFactory.create_with_context(
            context_bundle=context_bundle
        )
        loader: IScaraBoundsLoader = ScaraBoundsLoaderFactory.create_with_reader(
            reader=reader
        )

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
        return cls.create_bundle_with_options(
            options=SCARAjectoryBundleOptions({})
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
                | ATSTypeError:  The options or dependencies must match types.
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
        bounds: ScaraBounds = cls.resolve_bounds_with_options(
            options=options,
            context_bundle=base_bundle.context_bundle,
        )
        core_bundle: AppCoreBundle = AppCoreAssembler.assemble(
            bounds=bounds,
            context_bundle=base_bundle.context_bundle,
        )
        runtime_bundle: AppRuntimeBundle = AppRuntimeAssembler.assemble(
            context_bundle=base_bundle.context_bundle
        )
        plan_bundle: PlanPipelineBundle = PlanPipelineBuilder.build()

        return AppPresentationAssembler.assemble(
            base_bundle=base_bundle,
            core_bundle=core_bundle,
            runtime_bundle=runtime_bundle,
            plan_bundle=plan_bundle,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: The factory version string.
            :exceptions: None.
        '''
        return __version__
