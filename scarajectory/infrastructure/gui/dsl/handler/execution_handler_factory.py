# -*- coding: UTF-8 -*-

'''
Module
    execution_handler_factory.py
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
    Factory for instantiating DslEditorExecutionHandler instances.
'''

from __future__ import annotations

from scarajectory.infrastructure.gui.dsl.handler.execution_handler import DslEditorExecutionHandler
from scarajectory.infrastructure.gui.dsl.handler.execution_handler_bundle import ExecutionHandlerBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DslEditorExecutionHandlerFactory:
    '''
        Factory responsible for assembling DslEditorExecutionHandler instances.

        It defines:

            :methods:
                | create - Instantiates a DslEditorExecutionHandler with bundle.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        bundle: ExecutionHandlerBundle,
    ) -> DslEditorExecutionHandler:
        '''
            Instantiates a DslEditorExecutionHandler with collaborators bundle.

            :param bundle: Required ExecutionHandlerBundle container.
            :return: Fully configured DslEditorExecutionHandler.
            :exceptions: None.
        '''
        return DslEditorExecutionHandler(bundle=bundle)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
