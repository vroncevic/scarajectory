# -*- coding: UTF-8 -*-

'''
Module
    scara_dsl_service_factory.py
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
    Root factory for the SCARA DSL subsystem wiring lexer, parser, compiler, and binary pipeline.
'''

from __future__ import annotations

from scarajectory.core.model.kinematics.transmission_parameters import TransmissionParameters
from scarajectory.core.service.communication.protocol.ibinary_frame_builder import IBinaryFrameBuilder
from scarajectory.core.service.dsl.binary.command.command_compiler_factory import CommandCompilerFactory
from scarajectory.core.service.dsl.binary.compiler_factory import CompilerFactory
from scarajectory.core.service.dsl.binary.command.icommand_compiler import ICommandCompiler
from scarajectory.core.service.dsl.binary.icompiler import ICompiler
from scarajectory.core.service.dsl.binary.motion.imotion_compiler import IMotionCompiler
from scarajectory.core.service.dsl.binary.step.istep_discretizer import IStepDiscretizer
from scarajectory.core.service.dsl.binary.motion.motion_compiler_factory import MotionCompilerFactory
from scarajectory.core.service.dsl.binary.step.step_discretizer_factory import StepDiscretizerFactory
from scarajectory.core.service.dsl.compiler.iscara_compiler import IScaraCompiler
from scarajectory.core.service.dsl.compiler.scara_compiler_factory import ScaraCompilerFactory
from scarajectory.core.service.dsl.exporter.iscara_plan_exporter import IScaraPlanExporter
from scarajectory.core.service.dsl.exporter.scara_plan_exporter_factory import ScaraPlanExporterFactory
from scarajectory.core.service.dsl.iscara_dsl_service import IScaraDslService
from scarajectory.core.service.dsl.lexer.iscara_lexer import IScaraLexer
from scarajectory.core.service.dsl.lexer.scara_lexer_factory import ScaraLexerFactory
from scarajectory.core.service.dsl.parser.iscara_parser import IScaraParser
from scarajectory.core.service.dsl.parser.scara_parser_factory import ScaraParserFactory
from scarajectory.core.service.dsl.scara_dsl_service import ScaraDslService
from scarajectory.core.service.kinematics.ikinematics_service import IKinematicsService
from scarajectory.core.service.trajectory.validation.itrajectory_validator import ITrajectoryValidator
from scarajectory.infrastructure.communication.protocol.binary.builder.binary_frame_builder_factory import BinaryFrameBuilderFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaraDslServiceFactory:
    '''
        Factory providing composite composition for ScaraDslService using explicit sub-factory DI.

        It defines:

            :methods:
                | create - Wires child factories and returns an IScaraDslService instance.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        validator: ITrajectoryValidator,
        kinematics: IKinematicsService,
        transmission: TransmissionParameters
    ) -> IScaraDslService:
        '''
            Builds and wires ScaraDslService performing explicit DI into child sub-factories.

            :param validator: Injected ITrajectoryValidator protocol instance.
            :param kinematics: Injected IKinematicsService protocol instance.
            :param transmission: Injected TransmissionParameters domain model.
            :return: Fully wired IScaraDslService protocol instance.
            :exceptions: None.
        '''
        active_lexer: IScaraLexer = ScaraLexerFactory.create()
        active_parser: IScaraParser = ScaraParserFactory.create(lexer=active_lexer)
        active_compiler: IScaraCompiler = ScaraCompilerFactory.create(validator=validator)
        active_exporter: IScaraPlanExporter = ScaraPlanExporterFactory.create()
        active_discretizer: IStepDiscretizer = StepDiscretizerFactory.create(
            kinematics=kinematics, transmission=transmission
        )
        active_frame_builder: IBinaryFrameBuilder = (BinaryFrameBuilderFactory.create())
        active_motion_compiler: IMotionCompiler = MotionCompilerFactory.create(
            discretizer=active_discretizer, frame_builder=active_frame_builder
        )
        active_command_compiler: ICommandCompiler = CommandCompilerFactory.create(
            frame_builder=active_frame_builder
        )
        active_binary_compiler: ICompiler = CompilerFactory.create(
            lexer=active_lexer,
            parser=active_parser,
            compiler=active_compiler,
            motion_compiler=active_motion_compiler,
            command_compiler=active_command_compiler
        )

        return ScaraDslService(
            lexer=active_lexer,
            parser=active_parser,
            compiler=active_compiler,
            exporter=active_exporter,
            binary_compiler=active_binary_compiler
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
