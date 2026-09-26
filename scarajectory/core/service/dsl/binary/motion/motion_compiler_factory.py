# -*- coding: UTF-8 -*-

'''
Module
    motion_compiler_factory.py
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
    Factory for instantiating IMotionCompiler implementations with pure DI.
'''

from __future__ import annotations

from scarajectory.core.service.communication.protocol.ibinary_frame_builder import IBinaryFrameBuilder
from scarajectory.core.service.dsl.binary.motion.imotion_compiler import IMotionCompiler
from scarajectory.core.service.dsl.binary.motion.motion_compiler import MotionCompiler
from scarajectory.core.service.dsl.binary.step.istep_discretizer import IStepDiscretizer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MotionCompilerFactory:
    '''
        Factory providing creation of IMotionCompiler implementations.

        It defines:

            :methods:
                | create - Creates an IMotionCompiler instance via pure DI.
    '''

    @classmethod
    def create(cls, *, discretizer: IStepDiscretizer, frame_builder: IBinaryFrameBuilder) -> IMotionCompiler:
        '''
            Instantiates MotionCompiler with strictly injected collaborators.

            :param discretizer: Injected IStepDiscretizer instance.
            :param frame_builder: Injected IBinaryFrameBuilder instance.
            :return: Configured IMotionCompiler protocol instance.
            :exceptions: None.
        '''
        return MotionCompiler(discretizer=discretizer, frame_builder=frame_builder)
