# -*- coding: UTF-8 -*-

'''
Module
    command_formatter.py
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
    Unified serial packet encoder and command formatter for SCARA microcontroller.
'''

from __future__ import annotations

from scarajectory.infrastructure.communication.protocol.ascii.formatter.motion_command_formatter import MotionCommandFormatter
from scarajectory.infrastructure.communication.protocol.ascii.formatter.jog_command_formatter import JogCommandFormatter
from scarajectory.infrastructure.communication.protocol.ascii.formatter.query_command_formatter import QueryCommandFormatter
from scarajectory.infrastructure.communication.protocol.ascii.formatter.system_command_formatter import SystemCommandFormatter
from scarajectory.infrastructure.communication.protocol.ascii.formatter.config_command_formatter import ConfigCommandFormatter
from scarajectory.infrastructure.communication.protocol.ascii.formatter.tool_command_formatter import ToolCommandFormatter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CommandFormatter(
    MotionCommandFormatter,
    JogCommandFormatter,
    QueryCommandFormatter,
    SystemCommandFormatter,
    ConfigCommandFormatter,
    ToolCommandFormatter
):
    '''
        Unified serial packet encoder combining motion, jog, query, system,
        configuration and tool commands.

        Inherits motion formatting methods from MotionCommandFormatter,
        jog formatting methods from JogCommandFormatter,
        query formatting methods from QueryCommandFormatter,
        system lifecycle methods from SystemCommandFormatter,
        configuration formatting methods from ConfigCommandFormatter,
        and actuator/tool/wait/override methods from ToolCommandFormatter.
    '''
