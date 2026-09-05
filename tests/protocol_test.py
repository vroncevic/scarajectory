# -*- coding: UTF-8 -*-

'''
Module
    protocol_test.py
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
    Unit tests for CommandFormatter and ProtocolParser communication protocol.
'''

from __future__ import annotations

import os
import sys
import unittest

pkg_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if pkg_dir not in sys.path:
    sys.path.insert(0, pkg_dir)

from scarajectory.core.model.waypoint import Waypoint
from scarajectory.infrastructure.communication.protocol.command_formatter import CommandFormatter
from scarajectory.infrastructure.communication.protocol.protocol_parser import ProtocolParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestProtocol(unittest.TestCase):
    '''
        Test cases for ASCII serial protocol formatting and parsing.

        It defines:

            :methods:
                | test_command_formatting - Tests formatting commands to controller.
                | test_response_ack_parsing - Tests parsing ACK response messages.
                | test_protocol_status_helpers - Tests status check helper methods.
    '''

    def test_command_formatting(self) -> None:
        '''
            Tests generation of ASCII command strings.

            :exceptions: None.
        '''
        self.assertEqual(CommandFormatter.format_enable(), '<CMD:ENABLE>')
        self.assertEqual(CommandFormatter.format_disable(), '<CMD:DISABLE>')
        self.assertEqual(CommandFormatter.format_home(), '<CMD:HOME>')
        self.assertEqual(CommandFormatter.format_status(), '<CMD:STATUS>')
        self.assertEqual(CommandFormatter.format_jog('X', 10.0), '<CMD:JOG#X#10.0>')

        pt = Waypoint(x=120.5, y=80.25, z=15.0, phi=0.0, speed=40.0)
        self.assertEqual(CommandFormatter.format_move(pt), '<pt#120.50#80.25#15.00#0.00#40.0#end>')

    def test_response_ack_parsing(self) -> None:
        '''
            Tests parsing controller ACK responses.

            :exceptions: None.
        '''
        resp = ProtocolParser.parse_response('<RESP:ACK#QUEUE=3>')
        self.assertEqual(resp.response_type, 'ACK')
        self.assertEqual(resp.queue_depth, 3)
        self.assertTrue(resp.is_success)

        err_resp = ProtocolParser.parse_response('<RESP:ERR#OUT_OF_BOUNDS>')
        self.assertEqual(err_resp.response_type, 'ERR')
        self.assertFalse(err_resp.is_success)

    def test_protocol_status_helpers(self) -> None:
        '''
            Tests helper methods for detecting move completion and buffer saturation.

            :exceptions: None.
        '''
        self.assertTrue(ProtocolParser.is_move_done('<RESP:MOVE_DONE>'))
        self.assertFalse(ProtocolParser.is_move_done('<RESP:ACK#QUEUE=1>'))
        self.assertTrue(ProtocolParser.is_error('<RESP:ERR#COLLISION>'))
        self.assertFalse(ProtocolParser.is_error('<RESP:ACK>'))

    def test_tool_command_formatting(self) -> None:
        '''
            Tests formatting of tool, wait, and override commands.
        '''
        self.assertEqual(CommandFormatter.format_pump(True), '<CMD:PUMP#1>')
        self.assertEqual(CommandFormatter.format_pump(False), '<CMD:PUMP#0>')
        self.assertEqual(CommandFormatter.format_valve(True), '<CMD:VALVE#1>')
        self.assertEqual(CommandFormatter.format_valve(False), '<CMD:VALVE#0>')
        self.assertEqual(CommandFormatter.format_wait(250), '<CMD:WAIT#250>')
        self.assertEqual(CommandFormatter.format_override(75), '<CMD:OVERRIDE#75>')

    def test_action_done_helpers(self) -> None:
        '''
            Tests detection of action completion responses and homing status.
        '''
        self.assertTrue(ProtocolParser.is_action_done('<RESP:ACK#WAIT_DONE#MS=200>'))
        self.assertTrue(ProtocolParser.is_action_done('<RESP:ACK#PUMP_ON>'))
        self.assertTrue(ProtocolParser.is_action_done('<RESP:ACK#VALVE_OFF>'))
        self.assertTrue(ProtocolParser.is_action_done('<RESP:HOMED_SUCCESS#X=0#Y=0#Z=0#PHI=0>'))
        self.assertTrue(ProtocolParser.is_complete('<RESP:ACK#WAIT_DONE#MS=200>'))
        self.assertTrue(ProtocolParser.is_complete('<RESP:MOVE_DONE#X=100#Y=50>'))
        self.assertFalse(ProtocolParser.is_action_done('<RESP:ACK#QUEUE=2>'))
        self.assertFalse(ProtocolParser.is_action_done('<RESP:ACK#HOMING_STARTED>'))

        self.assertTrue(ProtocolParser.is_homed_success('<RESP:HOMED_SUCCESS#X=0#Y=0#Z=0#PHI=0>'))
        self.assertFalse(ProtocolParser.is_homed_success('<RESP:HOMING_FAILED>'))

        self.assertTrue(ProtocolParser.is_homing_failed('<RESP:HOMING_FAILED>'))
        self.assertTrue(ProtocolParser.is_homing_failed('<RESP:HOMED_FAIL>'))
        self.assertFalse(ProtocolParser.is_homing_failed('<RESP:HOMED_SUCCESS#X=0#Y=0#Z=0#PHI=0>'))

        self.assertTrue(ProtocolParser.is_error('<RESP:HOMING_FAILED>'))
        fail_resp = ProtocolParser.parse_response('<RESP:HOMING_FAILED>')
        self.assertFalse(fail_resp.is_success)
        self.assertEqual(fail_resp.response_type, 'HOMED_FAIL')


if __name__ == '__main__':
    unittest.main()
