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

from os.path import abspath, dirname
from sys import path
from unittest import TestCase, main

pkg_dir = dirname(dirname(abspath(__file__)))
if pkg_dir not in path:
    path.insert(0, pkg_dir)

from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.infrastructure.communication.protocol.ascii.formatter.command_formatter import CommandFormatter
from scarajectory.infrastructure.communication.protocol.ascii.formatter.jog_command_formatter import JogCommandFormatter
from scarajectory.infrastructure.communication.protocol.ascii.formatter.motion_command_formatter import MotionCommandFormatter
from scarajectory.infrastructure.communication.protocol.ascii.formatter.query_command_formatter import QueryCommandFormatter
from scarajectory.infrastructure.communication.protocol.ascii.formatter.system_command_formatter import SystemCommandFormatter
from scarajectory.infrastructure.communication.protocol.ascii.parser.protocol_parser import ProtocolParser
from scarajectory.infrastructure.communication.protocol.ascii.parser.protocol_status_classifier import ProtocolStatusClassifier
from scarajectory.infrastructure.communication.protocol.ascii.parser.response_parser import ResponseParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestProtocol(TestCase):
    '''
        Test cases for ASCII serial protocol formatting and parsing.

        It defines:

            :methods:
                | test_command_formatting - Tests formatting commands to controller.
                | test_jog_command_formatting - Tests manual axis jog formatting.
                | test_query_command_formatting - Tests query command formatting.
                | test_system_command_formatting - Tests lifecycle and safety formatting.
                | test_motion_command_formatting - Tests trajectory and program formatting.
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

        pt = Waypoint(x=120.5, y=80.25, z=15.0, phi=0.0, speed=40.0, name='', command='')
        self.assertEqual(CommandFormatter.format_move(pt), '<pt#120.50#80.25#15.00#0.00#40.0#end>')

    def test_jog_command_formatting(self) -> None:
        '''
            Tests manual axis jog step command formatting.

            :exceptions: None.
        '''
        self.assertEqual(JogCommandFormatter.format_jog('x', 5.0), '<CMD:JOG#X#5.0>')
        self.assertEqual(JogCommandFormatter.format_jog('Y', -2.5), '<CMD:JOG#Y#-2.5>')
        self.assertEqual(CommandFormatter.format_jog('z', 10.0), '<CMD:JOG#Z#10.0>')

    def test_query_command_formatting(self) -> None:
        '''
            Tests position and kinematics query command formatting.

            :exceptions: None.
        '''
        self.assertEqual(QueryCommandFormatter.format_getpos(), '<CMD:GETPOS>')
        self.assertEqual(QueryCommandFormatter.format_get_elbow(), '<CMD:GET_ELBOW>')
        self.assertEqual(QueryCommandFormatter.format_set_elbow(True), '<CMD:SET_ELBOW#LEFT>')
        self.assertEqual(QueryCommandFormatter.format_set_elbow(False), '<CMD:SET_ELBOW#RIGHT>')
        self.assertEqual(CommandFormatter.format_getpos(), '<CMD:GETPOS>')
        self.assertEqual(CommandFormatter.format_get_elbow(), '<CMD:GET_ELBOW>')
        self.assertEqual(CommandFormatter.format_set_elbow(True), '<CMD:SET_ELBOW#LEFT>')

    def test_system_command_formatting(self) -> None:
        '''
            Tests power lifecycle, safety and stream execution commands.

            :exceptions: None.
        '''
        self.assertEqual(SystemCommandFormatter.format_enable(), '<CMD:ENABLE>')
        self.assertEqual(SystemCommandFormatter.format_disable(), '<CMD:DISABLE>')
        self.assertEqual(SystemCommandFormatter.format_estop(), '<CMD:ESTOP>')
        self.assertEqual(SystemCommandFormatter.format_status(), '<CMD:STATUS>')
        self.assertEqual(SystemCommandFormatter.format_pause(), '<CMD:PAUSE>')
        self.assertEqual(SystemCommandFormatter.format_resume(), '<CMD:RESUME>')
        self.assertEqual(CommandFormatter.format_estop(), '<CMD:ESTOP>')
        self.assertEqual(CommandFormatter.format_pause(), '<CMD:PAUSE>')
        self.assertEqual(CommandFormatter.format_resume(), '<CMD:RESUME>')

    def test_motion_command_formatting(self) -> None:
        '''
            Tests trajectory motion, packet encoding and program stream formatting.

            :exceptions: None.
        '''
        self.assertEqual(MotionCommandFormatter.format_home(), '<CMD:HOME>')

        pt_normal = Waypoint(x=10.0, y=20.0, z=5.0, phi=0.0, speed=25.0, name='', command='')
        self.assertEqual(
            MotionCommandFormatter.format_waypoint_packet(pt_normal),
            '<pt#10.00#20.00#5.00#25.0#end>'
        )

        pt_phi = Waypoint(x=10.0, y=20.0, z=5.0, phi=45.0, speed=25.0, name='', command='')
        self.assertEqual(
            MotionCommandFormatter.format_waypoint_packet(pt_phi),
            '<pt#10.00#20.00#5.00#45.00#25.0#end>'
        )

        pt_custom = Waypoint(x=0.0, y=0.0, z=0.0, phi=0.0, speed=0.0, name='', command='<CMD:CUSTOM>')
        self.assertEqual(MotionCommandFormatter.format_move(pt_custom), '<CMD:CUSTOM>')
        self.assertEqual(MotionCommandFormatter.format_waypoint_packet(pt_custom), '<CMD:CUSTOM>')

        prog = MotionCommandFormatter.format_program([pt_normal, pt_phi], total_distance=100.5)
        self.assertIn('; Total Waypoints: 2', prog)
        self.assertIn('; Total Distance: 100.50 mm', prog)
        self.assertIn('<CMD:ENABLE>', prog)

        prog_nodist = CommandFormatter.format_program([pt_normal])
        self.assertNotIn('; Total Distance:', prog_nodist)

    def test_response_ack_parsing(self) -> None:
        '''
            Tests parsing controller ACK responses.

            :exceptions: None.
        '''
        resp = ProtocolParser.parse_response('<RESP:ACK#QUEUE=3>')
        self.assertEqual(resp.response_type, 'ACK')
        self.assertEqual(ProtocolParser.parse_queue_depth('<RESP:ACK#QUEUE=3>'), 3)
        self.assertIsNone(ProtocolParser.parse_queue_depth('<RESP:ERR#OUT_OF_BOUNDS>'))
        self.assertTrue(resp.is_success)

        resp_direct = ResponseParser.parse_response('<RESP:ACK#QUEUE=5>')
        self.assertEqual(resp_direct.response_type, 'ACK')
        self.assertEqual(ResponseParser.parse_queue_depth('<RESP:ACK#QUEUE=5>'), 5)

        cfg_resp = ResponseParser.parse_response('<RESP:CONFIG#R_MAX=300>')
        self.assertEqual(cfg_resp.response_type, 'CONFIG')

        elbow_resp = ResponseParser.parse_response('<RESP:ELBOW#LEFT>')
        self.assertEqual(elbow_resp.response_type, 'ELBOW')

        nack_resp = ResponseParser.parse_response('<RESP:NACK#INVALID>')
        self.assertEqual(nack_resp.response_type, 'NACK')
        self.assertFalse(nack_resp.is_success)

        err_resp = ProtocolParser.parse_response('<RESP:ERR#OUT_OF_BOUNDS>')
        self.assertEqual(err_resp.response_type, 'ERR')
        self.assertFalse(err_resp.is_success)

    def test_protocol_status_helpers(self) -> None:
        '''
            Tests helper methods for detecting move completion and buffer saturation.

            :exceptions: None.
        '''
        self.assertTrue(ProtocolParser.is_move_done('<RESP:MOVE_DONE>'))
        self.assertTrue(ProtocolStatusClassifier.is_move_done('<RESP:MOVE_DONE>'))
        self.assertFalse(ProtocolParser.is_move_done('<RESP:ACK#QUEUE=1>'))
        self.assertTrue(ProtocolParser.is_error('<RESP:ERR#COLLISION>'))
        self.assertTrue(ProtocolStatusClassifier.is_error('<RESP:ERR#COLLISION>'))
        self.assertFalse(ProtocolParser.is_error('<RESP:ACK>'))
        self.assertTrue(ProtocolStatusClassifier.is_buffer_full('<RESP:NACK#BUFFER_FULL>'))
        self.assertTrue(ProtocolStatusClassifier.is_move_failed('<RESP:MOVE_FAILED#KINEMATICS>'))
        self.assertTrue(ProtocolStatusClassifier.is_telemetry('<TELEM#X=10#Y=20>'))

    def test_protocol_parser_facade_methods(self) -> None:
        '''
            Tests get_version and is_valid_packet methods on ProtocolParser facade.
        '''
        self.assertEqual(ProtocolParser.get_version(), '1.0.3')
        self.assertTrue(ProtocolParser.is_valid_packet('<RESP:ACK>'))
        self.assertTrue(ProtocolParser.is_valid_packet('<>'))
        self.assertFalse(ProtocolParser.is_valid_packet('<INCOMPLETE'))
        self.assertFalse(ProtocolParser.is_valid_packet('GARBAGE>'))
        self.assertFalse(ProtocolParser.is_valid_packet(''))
        self.assertFalse(ProtocolParser.is_valid_packet('   '))

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
    main()
