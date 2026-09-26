# -*- coding: UTF-8 -*-

'''
Module
    arc_move_compiler_factory.py
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
    Factory for instantiating ArcMoveCompiler components with dependency injection.
'''

from __future__ import annotations

from scarajectory.core.service.dsl.compiler.motion.iarc_interpolator import IArcInterpolator
from scarajectory.core.service.dsl.compiler.motion.arc_interpolator import ArcInterpolator
from scarajectory.core.service.dsl.compiler.motion.arc_move_compiler import ArcMoveCompiler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ArcMoveCompilerFactory:
    '''
        Factory providing creation of ArcMoveCompiler instances.

        It defines:

            :methods:
                | create - Instantiates ArcMoveCompiler with internal ArcInterpolator.
                | create_with_interpolator - Instantiates ArcMoveCompiler with injected arc interpolator.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls) -> ArcMoveCompiler:
        '''
            Creates ArcMoveCompiler instance with internal ArcInterpolator.

            :return: Configured ArcMoveCompiler instance.
            :exceptions: None.
        '''
        return ArcMoveCompiler(arc_interpolator=ArcInterpolator())

    @classmethod
    def create_with_interpolator(
        cls,
        *,
        arc_interpolator: IArcInterpolator,
    ) -> ArcMoveCompiler:
        '''
            Creates ArcMoveCompiler instance with injected interpolator.

            :param arc_interpolator: IArcInterpolator instance.
            :return: Configured ArcMoveCompiler instance.
            :exceptions: None.
        '''
        return ArcMoveCompiler(arc_interpolator=arc_interpolator)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__


