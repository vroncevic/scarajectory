# -*- coding: UTF-8 -*-

'''
Module
    iapplier.py
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
    Defines structural protocol IDslTagApplier for syntax tag styling.
'''

from __future__ import annotations

from collections.abc import Sequence
from tkinter import Text
from typing import Protocol, runtime_checkable

from scarajectory.infrastructure.gui.dsl.syntax.token import SyntaxToken

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IDslTagApplier(Protocol):
    '''
        Structural protocol defining syntax tag application on Tkinter Text.

        It defines:

            :methods:
                | configure_styles - Configures syntax color tags on widget.
                | apply_tokens - Clears old tags and applies token spans.
                | get_version - Returns tag applier component version string.
    '''

    def configure_styles(self, text_widget: Text) -> None:
        '''
            Configures syntax color tags on the target Tkinter Text widget.

            :param text_widget: Target text widget to format.
        '''

    def apply_tokens(
        self,
        text_widget: Text,
        tokens: Sequence[SyntaxToken],
        tags_to_clear: Sequence[str],
    ) -> None:
        '''
            Clears previous syntax tags and applies computed token spans.

            :param text_widget: Target Tkinter Text widget.
            :param tokens: Sequence of SyntaxToken spans to apply.
            :param tags_to_clear: Sequence of tag names to remove prior.
        '''

    def get_version(self) -> str:
        '''
            Returns tag applier component version string.

            :return: Semantic version string.
        '''
