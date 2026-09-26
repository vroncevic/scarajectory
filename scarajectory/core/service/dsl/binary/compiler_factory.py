# -*- coding: UTF-8 -*-

'''
Module
    compiler_factory.py
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
    Factory assembling and wiring the Compiler service tree with pure DI.
'''

from __future__ import annotations

from scarajectory.core.service.dsl.binary.compiler import Compiler
from scarajectory.core.service.dsl.binary.icompiler import ICompiler
from scarajectory.core.service.dsl.binary.command.icommand_compiler import ICommandCompiler
from scarajectory.core.service.dsl.binary.motion.imotion_compiler import IMotionCompiler
from scarajectory.core.service.dsl.compiler.iscara_compiler import IScaraCompiler
from scarajectory.core.service.dsl.lexer.iscara_lexer import IScaraLexer
from scarajectory.core.service.dsl.parser.iscara_parser import IScaraParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CompilerFactory:
    '''
        Factory providing composite composition for Compiler using pure DI.

        It defines:

            :methods:
                | create - Wires injected component protocols into an ICompiler instance.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        lexer: IScaraLexer,
        parser: IScaraParser,
        compiler: IScaraCompiler,
        motion_compiler: IMotionCompiler,
        command_compiler: ICommandCompiler
    ) -> ICompiler:
        '''
            Builds and wires Compiler with injected component protocols.

            :param lexer: Injected IScaraLexer protocol instance.
            :param parser: Injected IScaraParser protocol instance.
            :param compiler: Injected IScaraCompiler protocol instance.
            :param motion_compiler: Injected IMotionCompiler protocol instance.
            :param command_compiler: Injected ICommandCompiler protocol instance.
            :return: Fully wired ICompiler protocol instance.
            :exceptions: None.
        '''
        return Compiler(
            lexer=lexer,
            parser=parser,
            compiler=compiler,
            motion_compiler=motion_compiler,
            command_compiler=command_compiler
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
