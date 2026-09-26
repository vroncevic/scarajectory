# -*- coding: UTF-8 -*-

'''
Module
    scara_linter_factory.py
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
    Factory instantiating and wiring ScaraLinter with static analysis rules.
'''

from __future__ import annotations

from collections.abc import Sequence

from scarajectory.core.service.dsl.linter.iscara_linter import IScaraLinter
from scarajectory.core.service.dsl.linter.rules.iscara_lint_rule import IScaraLintRule
from scarajectory.core.service.dsl.linter.rules.motion_lint_rule import MotionLintRule
from scarajectory.core.service.dsl.linter.rules.pneumatic_lint_rule import PneumaticLintRule
from scarajectory.core.service.dsl.linter.rules.state_lint_rule import StateLintRule
from scarajectory.core.service.dsl.linter.rules.timing_lint_rule import TimingLintRule
from scarajectory.core.service.dsl.linter.scara_linter import ScaraLinter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaraLinterFactory:
    '''
        Factory providing wired IScaraLinter instances.

        It defines:

            :methods:
                | create - Builds and wires ScaraLinter with static analysis rules.
                | create_with_rules - Builds ScaraLinter with explicit custom rules.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls) -> IScaraLinter:
        '''
            Builds and wires ScaraLinter with default static analysis rules.

            :return: IScaraLinter structural protocol instance.
            :exceptions: None.
        '''
        return ScaraLinter(
            rules=(
                StateLintRule(),
                MotionLintRule(),
                PneumaticLintRule(),
                TimingLintRule(),
            )
        )

    @classmethod
    def create_with_rules(cls, *, rules: Sequence[IScaraLintRule]) -> IScaraLinter:
        '''
            Builds ScaraLinter with explicit custom rules.

            :param rules: Explicit sequence of IScaraLintRule components.
            :return: IScaraLinter structural protocol instance.
            :exceptions: None.
        '''
        return ScaraLinter(rules=rules)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
