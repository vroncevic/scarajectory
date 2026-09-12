# -*- coding: UTF-8 -*-

'''
Module
    iscara_dsl_service.py
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
    Defines interface IScaraDslService coordinating high-level SCARA DSL compilation and export.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scarajectory.core.service.dsl.iscara_dsl_compiler import IScaraDslCompiler
from scarajectory.core.service.dsl.iscara_dsl_validator import IScaraDslValidator
from scarajectory.core.service.dsl.iscara_plan_exporter_service import (
    IScaraPlanExporterService,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IScaraDslService(
    IScaraDslCompiler,
    IScaraDslValidator,
    IScaraPlanExporterService,
    Protocol,
):
    '''
        High-level composite orchestration service protocol for SCARA DSL processing.

        Combines compilation, validation, linting, and trajectory plan export contracts.
    '''

