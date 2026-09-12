# -*- coding: UTF-8 -*-

'''
Module
    scara_compiler.py
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
    Implementation of IScaraCompiler transforming SCARA DSL programs into validated trajectory plans.
'''

from __future__ import annotations

from collections.abc import Sequence

from scarajectory.core.model.dsl.ast.iscara_instruction import IScaraInstruction
from scarajectory.core.model.dsl.ast.iscara_program import IScaraProgram
from scarajectory.core.model.dsl.diagnostic.scara_diagnostic import ScaraDiagnostic
from scarajectory.core.model.dsl.diagnostic.scara_diagnostic_severity import (
    ScaraDiagnosticSeverity,
)
from scarajectory.core.model.kinematics.scara_bounds import ScaraBounds
from scarajectory.core.model.trajectory.trajectory_plan import TrajectoryPlan
from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.core.service.dsl.compiler.arc_interpolator import (
    ArcInterpolator,
)
from scarajectory.core.service.dsl.compiler.control_command_compiler import (
    ControlCommandCompiler,
)
from scarajectory.core.service.dsl.compiler.iarc_interpolator import (
    IArcInterpolator,
)
from scarajectory.core.service.dsl.compiler.iprimitive_compiler import (
    IPrimitiveCompiler,
)
from scarajectory.core.service.dsl.compiler.motion_command_compiler import (
    MotionCommandCompiler,
)
from scarajectory.core.service.dsl.compiler.scara_compiler_context import (
    ScaraCompilerContext,
)
from scarajectory.core.service.dsl.compiler.state_command_compiler import (
    StateCommandCompiler,
)
from scarajectory.core.service.dsl.compiler.tool_command_compiler import (
    ToolCommandCompiler,
)
from scarajectory.core.service.dsl.linter.iscara_linter import IScaraLinter
from scarajectory.core.service.dsl.linter.scara_linter import ScaraLinter
from scarajectory.core.service.dsl.macro.frame_macro_expander import (
    FrameMacroExpander,
)
from scarajectory.core.service.dsl.macro.imacro_expander import IMacroExpander
from scarajectory.core.service.dsl.macro.jump_macro_expander import JumpMacroExpander
from scarajectory.core.service.dsl.macro.pallet_macro_expander import (
    PalletMacroExpander,
)
from scarajectory.core.service.dsl.macro.tangent_macro_expander import (
    TangentMacroExpander,
)
from scarajectory.core.service.trajectory.itrajectory_validator import (
    ITrajectoryValidator,
)
from scarajectory.core.service.trajectory.trajectory_validator import (
    TrajectoryValidator,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaraCompiler:
    '''
        Compiler orchestrator coordinating macro expansion, arc interpolation, and kinematic validation.

        It defines:

            :attributes:
                | _macro_expanders - Tuple of registered IMacroExpander plugins.
                | _validator - Kinematic reachability validator.
                | _tangent_helper - Helper calculating heading angles.
                | _arc_interpolator - Dedicated circular arc interpolator.
                | _linter - Static analysis and safety linter.
                | _primitive_compilers - Tuple of registered IPrimitiveCompiler components.
            :methods:
                | __init__ - Initializes compiler with optional custom expanders, validator, interpolator, linter, and compilers.
                | compile - Compiles IScaraProgram into validated TrajectoryPlan.
                | lint - Lints IScaraProgram and returns diagnostic findings.
    '''

    def __init__(
        self,
        *,
        macro_expanders: Sequence[IMacroExpander] | None = None,
        validator: ITrajectoryValidator | None = None,
        arc_interpolator: IArcInterpolator | None = None,
        linter: IScaraLinter | None = None,
        primitive_compilers: Sequence[IPrimitiveCompiler] | None = None,
    ) -> None:
        '''
            Initializes ScaraCompiler with injected components.

            :param macro_expanders: Optional custom sequence of IMacroExpander components.
            :param validator: Optional ITrajectoryValidator instance.
            :param arc_interpolator: Optional IArcInterpolator component.
            :param linter: Optional IScaraLinter component.
            :param primitive_compilers: Optional custom sequence of IPrimitiveCompiler components.
            :exceptions: None.
        '''
        if macro_expanders is not None:
            self._macro_expanders: tuple[IMacroExpander, ...] = tuple(
                macro_expanders
            )
        else:
            self._macro_expanders = (
                JumpMacroExpander(),
                FrameMacroExpander(),
                PalletMacroExpander(),
                TangentMacroExpander(),
            )
        self._validator: ITrajectoryValidator = (
            validator if validator is not None else TrajectoryValidator()
        )
        self._tangent_helper: TangentMacroExpander = TangentMacroExpander()
        self._arc_interpolator: IArcInterpolator = (
            arc_interpolator
            if arc_interpolator is not None
            else ArcInterpolator()
        )
        self._linter: IScaraLinter = (
            linter if linter is not None else ScaraLinter()
        )

        if primitive_compilers is not None:
            self._primitive_compilers: tuple[IPrimitiveCompiler, ...] = tuple(
                primitive_compilers
            )
        else:
            self._primitive_compilers = (
                StateCommandCompiler(),
                ToolCommandCompiler(),
                ControlCommandCompiler(),
                MotionCommandCompiler(
                    arc_interpolator=self._arc_interpolator,
                    tangent_helper=self._tangent_helper,
                ),
            )

    def lint(
        self,
        *,
        program: IScaraProgram,
    ) -> tuple[ScaraDiagnostic, ...]:
        '''
            Lints a SCARA DSL program and returns diagnostic warnings and errors.

            :param program: Parsed IScaraProgram AST root.
            :return: Tuple of ScaraDiagnostic findings.
            :exceptions: None.
        '''
        return self._linter.lint(program=program)

    def compile(
        self,
        *,
        program: IScaraProgram,
        bounds: ScaraBounds | None = None,
    ) -> TrajectoryPlan:
        '''
            Compiles a SCARA DSL program into an executable and validated TrajectoryPlan.

            :param program: Parsed IScaraProgram AST root.
            :param bounds: Optional kinematic boundary constraints.
            :return: Validated TrajectoryPlan instance.
            :exceptions: ValueError if static analysis or kinematic validation fails.
        '''
        diagnostics = self.lint(program=program)
        errors = [
            d for d in diagnostics
            if d.severity == ScaraDiagnosticSeverity.ERROR
        ]
        if errors:
            err_details = '; '.join(d.format_report() for d in errors)
            raise ValueError(
                f'Compilation aborted due to static analysis errors: {err_details}'
            )

        context = ScaraCompilerContext()
        waypoints: list[Waypoint] = []
        for inst in program.instructions:
            expanded = False
            for expander in self._macro_expanders:
                if expander.can_expand(instruction=inst):
                    for new_inst in expander.expand(
                        instruction=inst, context=context
                    ):
                        self._process_primitive(
                            instruction=new_inst,
                            context=context,
                            waypoints=waypoints,
                        )
                    expanded = True
                    break

            if not expanded:
                self._process_primitive(
                    instruction=inst,
                    context=context,
                    waypoints=waypoints,
                )

        plan = TrajectoryPlan()
        plan.set_waypoints(waypoints)

        active_bounds = bounds if bounds is not None else ScaraBounds()
        validator = (
            TrajectoryValidator(bounds=active_bounds)
            if bounds is not None
            else self._validator
        )
        is_valid, messages = validator.validate_plan(plan=plan)

        if not is_valid:
            err_msg = '; '.join(messages)
            raise ValueError(
                f'Compilation failed kinematic validation: {err_msg}'
            )

        return plan

    def _process_primitive(
        self,
        *,
        instruction: IScaraInstruction,
        context: ScaraCompilerContext,
        waypoints: list[Waypoint],
    ) -> None:
        '''
            Processes primitive non-macro instructions by delegating to specialized compilers.

            :param instruction: Primitive instruction node.
            :param context: Stateful compiler context.
            :param waypoints: Accumulator list of compiled Waypoint instances.
            :exceptions: None.
        '''
        for compiler in self._primitive_compilers:
            if compiler.can_compile(instruction=instruction):
                compiler.compile(
                    instruction=instruction,
                    context=context,
                    waypoints=waypoints,
                )
                return
