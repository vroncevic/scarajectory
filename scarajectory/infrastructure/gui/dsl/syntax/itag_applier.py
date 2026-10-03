# -*- coding: UTF-8 -*-

'''
Module
    itag_applier.py
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
    Interface contract for applying syntax highlighting tags to text widgets.
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
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IDslTagApplier(Protocol):
    '''
        Interface defining contract for syntax highlighting tag configuration and application.

        It defines:

            :methods:
                | configure_styles - Configures syntax color tags on widget.
                | apply_tokens - Clears previous tags and applies token spans.
    '''

    def configure_styles(self, text_widget: Text) -> None:
        '''
            Configures syntax color tags on the target Tkinter Text widget.

            :param text_widget: Target text widget to format.
            :exceptions: None.
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
            :exceptions: None.
        '''
