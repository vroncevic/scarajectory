# -*- coding: UTF-8 -*-

'''
Module
    applier.py
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

from collections.abc import Sequence
from tkinter import END, Text
from typing import ClassVar

from scarajectory.infrastructure.gui.dsl.syntax.token import SyntaxToken

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DslTagApplier:
    '''
        UI helper applying syntax token formatting tags to Tkinter Text widgets.

        It defines:

            :attributes:
                | TAG_COMMENT - Tag category name for comments.
                | TAG_COMMAND - Tag category name for commands.
                | TAG_KEYWORD - Tag category name for keywords.
                | TAG_PARAM - Tag category name for parameters.
                | TAG_NUMBER - Tag category name for numbers.
                | COLOR_COMMENT - Color hex string for comments.
                | COLOR_COMMAND - Color hex string for commands.
                | COLOR_KEYWORD - Color hex string for keywords.
                | COLOR_PARAM - Color hex string for parameters.
                | COLOR_NUMBER - Color hex string for numbers.
                | FONT_FAMILY - Monospace font family name.
                | FONT_SIZE - Standard font size in points.
                | START_INDEX - Text buffer start position.
            :methods:
                | __init__ - Initializes the tag applier instance.
                | configure_styles - Configures syntax color tags on widget.
                | apply_tokens - Clears old tags and applies token spans.
                | get_version - Returns tag applier component version string.
    '''

    TAG_COMMENT: ClassVar[str] = 'dsl_comment'
    TAG_COMMAND: ClassVar[str] = 'dsl_command'
    TAG_KEYWORD: ClassVar[str] = 'dsl_keyword'
    TAG_PARAM: ClassVar[str] = 'dsl_param'
    TAG_NUMBER: ClassVar[str] = 'dsl_number'

    COLOR_COMMENT: ClassVar[str] = '#5c6370'
    COLOR_COMMAND: ClassVar[str] = '#61afef'
    COLOR_KEYWORD: ClassVar[str] = '#c678dd'
    COLOR_PARAM: ClassVar[str] = '#e5c07b'
    COLOR_NUMBER: ClassVar[str] = '#98c379'

    FONT_FAMILY: ClassVar[str] = 'DejaVu Sans Mono'
    FONT_SIZE: ClassVar[int] = 9
    START_INDEX: ClassVar[str] = '1.0'

    def __init__(self) -> None:
        '''
            Initializes the tag applier instance.

            :exceptions: None.
        '''

    def configure_styles(self, text_widget: Text) -> None:
        '''
            Configures syntax color tags on the target Tkinter Text widget.

            :param text_widget: Target text widget to format.
            :exceptions: None.
        '''
        text_widget.tag_configure(
            self.TAG_COMMENT,
            foreground=self.COLOR_COMMENT,
            font=(self.FONT_FAMILY, self.FONT_SIZE, 'italic'),
        )
        text_widget.tag_configure(
            self.TAG_COMMAND,
            foreground=self.COLOR_COMMAND,
            font=(self.FONT_FAMILY, self.FONT_SIZE, 'bold'),
        )
        text_widget.tag_configure(
            self.TAG_KEYWORD,
            foreground=self.COLOR_KEYWORD,
            font=(self.FONT_FAMILY, self.FONT_SIZE, 'bold'),
        )
        text_widget.tag_configure(
            self.TAG_PARAM,
            foreground=self.COLOR_PARAM,
            font=(self.FONT_FAMILY, self.FONT_SIZE),
        )
        text_widget.tag_configure(
            self.TAG_NUMBER,
            foreground=self.COLOR_NUMBER,
            font=(self.FONT_FAMILY, self.FONT_SIZE),
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
            :exceptions: None.
        '''
        for tag in tags_to_clear:
            text_widget.tag_remove(tag, self.START_INDEX, END)

        for tok in tokens:
            text_widget.tag_add(tok.tag, tok.start_idx, tok.end_idx)

    def get_version(self) -> str:
        '''
            Returns tag applier component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
