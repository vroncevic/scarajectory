# -*- coding: UTF-8 -*-

'''
Module
    scara_compiler_factory.py
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
    Factory instantiating and wiring ScaraCompiler with validators, linter, and compilers.
'''

from __future__ import annotations

from collections.abc import Sequence

from scarajectory.core.service.dsl.compiler.motion.arc_interpolator import ArcInterpolator
from scarajectory.core.service.dsl.compiler.primitive.control_command_compiler import ControlCommandCompiler
from scarajectory.core.service.dsl.compiler.motion.iarc_interpolator import IArcInterpolator
from scarajectory.core.service.dsl.compiler.primitive.iprimitive_compiler import IPrimitiveCompiler
from scarajectory.core.service.dsl.compiler.iscara_compiler import IScaraCompiler
from scarajectory.core.service.dsl.compiler.motion.motion_command_compiler_factory import MotionCommandCompilerFactory
from scarajectory.core.service.dsl.compiler.scara_compiler import ScaraCompiler
from scarajectory.core.service.trajectory.plan.trajectory_plan_factory import TrajectoryPlanFactory
from scarajectory.core.service.trajectory.plan.itrajectory_plan_factory import ITrajectoryPlanFactory
from scarajectory.core.service.dsl.compiler.primitive.state_command_compiler import StateCommandCompiler
from scarajectory.core.service.dsl.compiler.primitive.tool_command_compiler import ToolCommandCompiler
from scarajectory.core.service.dsl.linter.iscara_linter import IScaraLinter
from scarajectory.core.service.dsl.linter.scara_linter_factory import ScaraLinterFactory
from scarajectory.core.service.dsl.macro.frame_macro_expander import FrameMacroExpander
from scarajectory.core.service.dsl.macro.imacro_expander import IMacroExpander
from scarajectory.core.service.dsl.macro.jump_macro_expander import JumpMacroExpander
from scarajectory.core.service.dsl.macro.pallet_macro_expander import PalletMacroExpander
from scarajectory.core.service.dsl.macro.tangent_macro_expander import TangentMacroExpander
from scarajectory.core.service.trajectory.validation.itrajectory_validator import ITrajectoryValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaraCompilerFactory:
    '''
        Factory providing wired IScaraCompiler instances.

        It defines:

            :methods:
                | create - Builds and wires ScaraCompiler with collaborators.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        validator: ITrajectoryValidator,
    ) -> IScaraCompiler:
        '''
            Builds and wires ScaraCompiler with internal collaborators.

            :param validator: Injected ITrajectoryValidator instance from outside domain.
            :return: IScaraCompiler structural protocol instance.
            :exceptions: None.
        '''
        active_linter: IScaraLinter = ScaraLinterFactory.create()
        active_tangent: TangentMacroExpander = TangentMacroExpander()
        active_interpolator: IArcInterpolator = ArcInterpolator()
        active_motion = MotionCommandCompilerFactory.create_with_helpers(
            tangent_helper=active_tangent,
            arc_interpolator=active_interpolator,
        )

        active_expanders: tuple[IMacroExpander, ...] = (
            JumpMacroExpander(),
            FrameMacroExpander(),
            PalletMacroExpander(),
            active_tangent,
        )

        active_compilers: tuple[IPrimitiveCompiler, ...] = (
            StateCommandCompiler(),
            ToolCommandCompiler(),
            ControlCommandCompiler(),
            active_motion,
        )

        return ScaraCompiler(
            validator=validator,
            linter=active_linter,
            macro_expanders=active_expanders,
            primitive_compilers=active_compilers,
            plan_factory=TrajectoryPlanFactory(),
        )

    @classmethod
    def create_with_compilers(
        cls,
        *,
        validator: ITrajectoryValidator,
        primitive_compilers: Sequence[IPrimitiveCompiler],
    ) -> IScaraCompiler:
        '''
            Builds ScaraCompiler with injected primitive compilers and internal domain components.

            :param validator: Injected ITrajectoryValidator instance.
            :param primitive_compilers: Sequence of IPrimitiveCompiler components.
            :return: IScaraCompiler structural protocol instance.
            :exceptions: None.
        '''
        active_linter: IScaraLinter = ScaraLinterFactory.create()
        active_tangent: TangentMacroExpander = TangentMacroExpander()
        active_expanders: tuple[IMacroExpander, ...] = (
            JumpMacroExpander(),
            FrameMacroExpander(),
            PalletMacroExpander(),
            active_tangent,
        )

        return ScaraCompiler(
            validator=validator,
            linter=active_linter,
            macro_expanders=active_expanders,
            primitive_compilers=tuple(primitive_compilers),
            plan_factory=TrajectoryPlanFactory(),
        )

    @classmethod
    def create_with_collaborators(
        cls,
        *,
        validator: ITrajectoryValidator,
        primitive_compilers: Sequence[IPrimitiveCompiler],
        macro_expanders: Sequence[IMacroExpander],
        linter: IScaraLinter,
        plan_factory: ITrajectoryPlanFactory,
    ) -> IScaraCompiler:
        '''
            Builds ScaraCompiler with explicitly injected custom collaborators.

            :param validator: Injected ITrajectoryValidator instance.
            :param primitive_compilers: Sequence of IPrimitiveCompiler components.
            :param macro_expanders: Sequence of IMacroExpander components.
            :param linter: IScaraLinter instance.
            :param plan_factory: ITrajectoryPlanFactory instance.
            :return: IScaraCompiler structural protocol instance.
            :exceptions: None.
        '''
        return ScaraCompiler(
            validator=validator,
            linter=linter,
            macro_expanders=tuple(macro_expanders),
            primitive_compilers=tuple(primitive_compilers),
            plan_factory=plan_factory,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
