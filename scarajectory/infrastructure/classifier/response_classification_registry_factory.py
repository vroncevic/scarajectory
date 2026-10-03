# -*- coding: UTF-8 -*-

'''
Module
    response_classification_registry_factory.py
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
    Factory constructing populated ResponseClassificationRegistry instances.
'''

from __future__ import annotations

from scarajectory.infrastructure.classifier.response_classification_registry import ResponseClassificationRegistry
from scarajectory.infrastructure.classifier.response_classification_rule import ResponseClassificationRule

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ResponseClassificationRegistryFactory:
    '''
        Factory providing configured ResponseClassificationRegistry instances.

        It defines:

            :methods:
                | create - Constructs registry populated with protocol rules.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls) -> ResponseClassificationRegistry:
        '''
            Constructs registry populated with standard protocol rules.

            :return: Populated ResponseClassificationRegistry instance.
            :exceptions: None.
        '''
        registry = ResponseClassificationRegistry()
        rules: list[ResponseClassificationRule] = [
            ResponseClassificationRule(
                'ACK', lambda s: s.startswith(('<RESP:ACK', '<ACK'))
            ),
            ResponseClassificationRule(
                'CONFIG', lambda s: s.startswith(('<RESP:CONFIG', '<CONFIG'))
            ),
            ResponseClassificationRule(
                'ELBOW', lambda s: s.startswith(('<RESP:ELBOW', '<ELBOW'))
            ),
            ResponseClassificationRule(
                'NACK',
                lambda s: s.startswith(('<RESP:NACK', '<NACK')),
                is_success=False,
            ),
            ResponseClassificationRule(
                'DONE',
                lambda s: 'MOVE_DONE' in s or s == '<DONE>',
                preserve_clean_msg=True,
            ),
            ResponseClassificationRule(
                'MOVE_FAILED',
                lambda s: 'MOVE_FAILED' in s,
                is_success=False,
            ),
            ResponseClassificationRule(
                'MOVE_START', lambda s: 'MOVE_START' in s
            ),
            ResponseClassificationRule(
                'TELEM', lambda s: s.startswith('<TELEM')
            ),
            ResponseClassificationRule(
                'FULL',
                lambda s: 'BUFFER_FULL' in s or s == '<FULL>',
                is_success=False,
                preserve_clean_msg=True,
            ),
            ResponseClassificationRule(
                'ERR',
                lambda s: 'ERR' in s or s.startswith('<ERR'),
                is_success=False,
                preserve_clean_msg=True,
            ),
            ResponseClassificationRule(
                'HOMED', lambda s: 'HOMED_SUCCESS' in s
            ),
            ResponseClassificationRule(
                'HOMED_FAIL',
                lambda s: 'HOMED_FAIL' in s or 'HOMING_FAILED' in s,
                is_success=False,
            ),
            ResponseClassificationRule(
                'STATUS', lambda s: s.startswith(('<STATUS', '<RESP:STATUS'))
            ),
            ResponseClassificationRule(
                'POS', lambda s: s.startswith(('<POS', '<RESP:POS'))
            ),
        ]
        for rule in rules:
            registry.register_rule(rule)

        return registry

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
