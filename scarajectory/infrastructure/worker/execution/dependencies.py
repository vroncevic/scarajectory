# -*- coding: UTF-8 -*-

'''
Module
    dependencies.py
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
    Parameter bundle dependencies for StreamExecutionWorker component.
'''

from __future__ import annotations

from dataclasses import dataclass

from scarajectory.infrastructure.worker.holder import StreamSessionHolder
from scarajectory.infrastructure.worker.runner.irunner import IStreamLoopRunner
from scarajectory.infrastructure.worker.thread.icoordinator import IWorkerThreadCoordinator

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True)
class ExecutionWorkerDependencies:
    '''
        Parameter bundle encapsulating external collaborators for StreamExecutionWorker.

        It defines:

            :attributes:
                | loop_runner - Injected IStreamLoopRunner instance.
                | coordinator - Injected IWorkerThreadCoordinator instance.
                | session_holder - Injected StreamSessionHolder instance.
    '''

    loop_runner: IStreamLoopRunner
    coordinator: IWorkerThreadCoordinator
    session_holder: StreamSessionHolder
