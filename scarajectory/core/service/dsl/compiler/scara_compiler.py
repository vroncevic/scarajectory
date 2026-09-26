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

from scarajectory.core.model.dsl.ast.instruction import Instruction
from scarajectory.core.model.dsl.ast.program import Program
from scarajectory.core.model.dsl.diagnostic.diagnostic import Diagnostic
from scarajectory.core.model.dsl.diagnostic.diagnostic_severity import DiagnosticSeverity
from scarajectory.core.service.trajectory.plan.itrajectory_plan import ITrajectoryPlan
from scarajectory.core.service.trajectory.plan.itrajectory_plan_factory import ITrajectoryPlanFactory
from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.core.service.dsl.compiler.primitive.iprimitive_compiler import IPrimitiveCompiler
from scarajectory.core.service.dsl.compiler.scara_compiler_context import ScaraCompilerContext
from scarajectory.core.service.dsl.diagnostic.scara_diagnostic_formatter import ScaraDiagnosticFormatter
from scarajectory.core.service.dsl.linter.iscara_linter import IScaraLinter
from scarajectory.core.service.dsl.macro.imacro_expander import IMacroExpander
from scarajectory.core.service.trajectory.validation.itrajectory_validator import ITrajectoryValidator

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
                | _linter - Static analysis and safety linter.
                | _primitive_compilers - Tuple of registered IPrimitiveCompiler components.
            :methods:
                | __init__ - Initializes compiler with injected collaborators.
                | compile - Compiles Program into validated TrajectoryPlan.
                | lint - Lints Program and returns diagnostic findings.
    '''

    def __init__(
        self,
        *,
        validator: ITrajectoryValidator,
        linter: IScaraLinter,
        plan_factory: ITrajectoryPlanFactory,
        macro_expanders: Sequence[IMacroExpander],
        primitive_compilers: Sequence[IPrimitiveCompiler],
    ) -> None:
        '''
            Initializes ScaraCompiler with injected components.

            :param validator: Injected ITrajectoryValidator instance.
            :param linter: Injected IScaraLinter component.
            :param plan_factory: Injected ITrajectoryPlanFactory component.
            :param macro_expanders: Sequence of IMacroExpander components.
            :param primitive_compilers: Sequence of IPrimitiveCompiler components.
            :exceptions: None.
        '''
        self._validator: ITrajectoryValidator = validator
        self._linter: IScaraLinter = linter
        self._plan_factory: ITrajectoryPlanFactory = plan_factory
        self._macro_expanders: tuple[IMacroExpander, ...] = tuple(
            macro_expanders
        )
        self._primitive_compilers: tuple[IPrimitiveCompiler, ...] = tuple(
            primitive_compilers
        )

    def lint(self, *, program: Program) -> tuple[Diagnostic, ...]:
        '''
            Lints a SCARA DSL program and returns diagnostic warnings and errors.

            :param program: Parsed Program AST root.
            :return: Tuple of Diagnostic findings.
            :exceptions: None.
        '''
        return self._linter.lint(program=program)

    def compile(self, *, program: Program) -> ITrajectoryPlan:
        '''
            Compiles a SCARA DSL program into an executable and validated ITrajectoryPlan.

            :param program: Parsed Program AST root.
            :return: Validated ITrajectoryPlan instance.
            :exceptions: ValueError if static analysis or kinematic validation fails.
        '''
        diagnostics = self.lint(program=program)
        errors = [
            d for d in diagnostics
            if d.severity == DiagnosticSeverity.ERROR
        ]
        if errors:
            err_details = '; '.join(
                ScaraDiagnosticFormatter.format_report(diagnostic=d)
                for d in errors
            )
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

        plan = self._plan_factory.create()
        plan.set_waypoints(waypoints)

        is_valid, messages = self._validator.validate_plan(plan=plan)

        if not is_valid:
            err_msg = '; '.join(messages)
            raise ValueError(
                f'Compilation failed kinematic validation: {err_msg}'
            )

        return plan

    def _process_primitive(
        self,
        *,
        instruction: Instruction,
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
