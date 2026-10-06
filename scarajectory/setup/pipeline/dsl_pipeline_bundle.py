# -*- coding: UTF-8 -*-

'''
Module
    dsl_pipeline_bundle.py
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
    Bundle containing fine-grained SCARA DSL pipeline role services.
'''

from __future__ import annotations

from dataclasses import dataclass

from scaralang.core.service.compiler.iscara_compiler import IScaraCompiler
from scaralang.core.service.compiler.plan.iscara_plan_compiler import IScaraPlanCompiler
from scaralang.core.service.decompiler.iscara_decompiler import IScaraDecompiler
from scaralang.core.service.exporter.scara.iscara_plan_exporter import IScaraPlanExporter
from scaralang.core.service.linter.script.iscara_dsl_validator import IScaraDslValidator
from scarajectory.setup.pipeline.dsl_diagnostic_bundle import DslDiagnosticBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(slots=True, frozen=True, kw_only=True)
class DslPipelineBundle:
    '''
        Bundle containing fine-grained SCARA DSL pipeline role services.

        It defines:

            :attributes:
                | compiler - SCARA wire and binary compiler service interface instance.
                | decompiler - Binary program decompilation service interface instance.
                | plan_compiler - SCARA trajectory plan compiler service interface instance.
                | plan_exporter - SCARA trajectory plan export service interface instance.
                | validator - SCARA DSL script validation and linting service interface instance.
                | diagnostics - SCARA DSL diagnostic and error handler services bundle.
    '''

    compiler: IScaraCompiler
    decompiler: IScaraDecompiler
    plan_compiler: IScaraPlanCompiler
    plan_exporter: IScaraPlanExporter
    validator: IScaraDslValidator
    diagnostics: DslDiagnosticBundle
