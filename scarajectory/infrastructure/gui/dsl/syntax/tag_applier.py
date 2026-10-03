# -*- coding: UTF-8 -*-

'''
Module
    tag_applier.py
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
    UI helper applying syntax token formatting tags to Tkinter Text widgets.
'''

from __future__ import annotations

from tkinter import END, Text
from typing import Sequence

from scarajectory.infrastructure.gui.dsl.syntax.token import SyntaxToken

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DslTagApplier:
    '''
        UI helper applying syntax token formatting tags to Tkinter Text.

        It defines:

            :methods:
                | configure_styles - Configures syntax color tags on widget.
                | apply_tokens - Clears old tags and applies token spans.
    '''

    def configure_styles(self, text_widget: Text) -> None:
        '''
            Configures syntax color tags on the target Tkinter Text widget.

            :param text_widget: Target text widget to format.
        '''
        text_widget.tag_configure(
            'dsl_comment',
            foreground='#5c6370',
            font=('DejaVu Sans Mono', 9, 'italic'),
        )
        text_widget.tag_configure(
            'dsl_command',
            foreground='#61afef',
            font=('DejaVu Sans Mono', 9, 'bold'),
        )
        text_widget.tag_configure(
            'dsl_keyword',
            foreground='#c678dd',
            font=('DejaVu Sans Mono', 9, 'bold'),
        )
        text_widget.tag_configure(
            'dsl_param',
            foreground='#e5c07b',
            font=('DejaVu Sans Mono', 9),
        )
        text_widget.tag_configure(
            'dsl_number',
            foreground='#98c379',
            font=('DejaVu Sans Mono', 9),
        )

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
        for tag in tags_to_clear:
            text_widget.tag_remove(tag, '1.0', END)

        for tok in tokens:
            text_widget.tag_add(tok.tag, tok.start_idx, tok.end_idx)
