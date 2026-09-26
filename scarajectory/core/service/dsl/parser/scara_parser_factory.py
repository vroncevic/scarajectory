# -*- coding: UTF-8 -*-

'''
Module
    scara_parser_factory.py
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
    Factory instantiating and wiring ScaraParser with tokenizer and command handlers.
'''

from __future__ import annotations

from collections.abc import Sequence

from scarajectory.core.service.dsl.lexer.iscara_lexer import IScaraLexer
from scarajectory.core.service.dsl.parser.commands.approach_retract_parser import ApproachRetractParser
from scarajectory.core.service.dsl.parser.commands.arc_command_parser import ArcCommandParser
from scarajectory.core.service.dsl.parser.commands.config_command_parser import ConfigCommandParser
from scarajectory.core.service.dsl.parser.commands.flow_command_parser import FlowCommandParser
from scarajectory.core.service.dsl.parser.commands.frame_command_parser import FrameCommandParser
from scarajectory.core.service.dsl.parser.commands.jog_command_parser import JogCommandParser
from scarajectory.core.service.dsl.parser.commands.jump_command_parser import JumpCommandParser
from scarajectory.core.service.dsl.parser.commands.motion_command_parser import MotionCommandParser
from scarajectory.core.service.dsl.parser.commands.pallet_command_parser import PalletCommandParser
from scarajectory.core.service.dsl.parser.commands.probe_command_parser import ProbeCommandParser
from scarajectory.core.service.dsl.parser.commands.tool_command_parser import ToolCommandParser
from scarajectory.core.service.dsl.parser.commands.tool_orient_command_parser import ToolOrientCommandParser
from scarajectory.core.service.dsl.parser.commands.zone_command_parser import ZoneCommandParser
from scarajectory.core.service.dsl.parser.icommand_parser import ICommandParser
from scarajectory.core.service.dsl.parser.iscara_parser import IScaraParser
from scarajectory.core.service.dsl.parser.scara_parser import ScaraParser
from scarajectory.core.service.dsl.ast.program_factory import ProgramFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaraParserFactory:
    '''
        Factory providing wired IScaraParser instances.

        It defines:

            :methods:
                | create - Builds and wires ScaraParser with tokenizer and default command handlers.
                | create_with_handlers - Builds ScaraParser with explicit custom command handlers.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls, *, lexer: IScaraLexer) -> IScaraParser:
        '''
            Builds and wires ScaraParser with injected tokenizer and default command handlers.

            :param lexer: Injected IScaraLexer instance.
            :return: IScaraParser structural protocol instance.
            :exceptions: None.
        '''
        return ScaraParser(
            lexer=lexer,
            handlers=(
                MotionCommandParser(),
                JumpCommandParser(),
                ArcCommandParser(),
                ApproachRetractParser(),
                ConfigCommandParser(),
                PalletCommandParser(),
                FrameCommandParser(),
                ToolCommandParser(),
                FlowCommandParser(),
                JogCommandParser(),
                ProbeCommandParser(),
                ZoneCommandParser(),
                ToolOrientCommandParser(),
            ),
            program_factory=ProgramFactory(),
        )

    @classmethod
    def create_with_handlers(cls, *, lexer: IScaraLexer, handlers: Sequence[ICommandParser]) -> IScaraParser:
        '''
            Builds and wires ScaraParser with injected tokenizer and explicit custom command handlers.

            :param lexer: Injected IScaraLexer instance.
            :param handlers: Explicit sequence of custom ICommandParser handlers.
            :return: IScaraParser structural protocol instance.
            :exceptions: None.
        '''
        return ScaraParser(lexer=lexer, handlers=handlers, program_factory=ProgramFactory())

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
