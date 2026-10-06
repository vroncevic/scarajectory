# -*- coding: UTF-8 -*-

'''
Module
    highlighter.py
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
    Syntax highlighter coordinator delegating tokenization and tag styling.
'''

from __future__ import annotations

from tkinter import END, Text
from typing import Final

from scarajectory.infrastructure.gui.dsl.syntax.itag_applier import IDslTagApplier
from scarajectory.infrastructure.gui.dsl.syntax.itokenizer import IDslSyntaxTokenizer
from scarajectory.infrastructure.gui.dsl.syntax.token import SyntaxToken

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DslSyntaxHighlighter:
    '''
        Syntax highlighting coordinator combining token scanning and styling.

        It defines:

            :attributes:
                | _tokenizer - IDslSyntaxTokenizer strategy.
                | _tag_applier - IDslTagApplier formatting helper.
            :methods:
                | __init__ - Initializes syntax highlighter with injected collaborators.
                | configure_styles - Configures syntax color tags on widget.
                | highlight - Performs syntax color update on text widget.
                | get_version - Returns component version string.
    '''

    _tokenizer: IDslSyntaxTokenizer
    _tag_applier: IDslTagApplier

    def __init__(
        self,
        *,
        tokenizer: IDslSyntaxTokenizer,
        tag_applier: IDslTagApplier,
    ) -> None:
        '''
            Initializes syntax highlighter with injected tokenizer and tag applier.

            :param tokenizer: Required IDslSyntaxTokenizer strategy.
            :param tag_applier: Required IDslTagApplier formatting helper.
            :exceptions: None.
        '''
        self._tokenizer: Final[IDslSyntaxTokenizer] = tokenizer
        self._tag_applier: Final[IDslTagApplier] = tag_applier

    def configure_styles(self, text_widget: Text) -> None:
        '''
            Configures syntax color tags on the target Tkinter Text widget.

            :param text_widget: Target text widget to format.
            :exceptions: None.
        '''
        self._tag_applier.configure_styles(text_widget)

    def highlight(self, text_widget: Text) -> None:
        '''
            Performs complete syntax color update on text widget contents.

            :param text_widget: Target text widget.
            :exceptions: None.
        '''
        content: str = text_widget.get('1.0', END)
        tokens: tuple[SyntaxToken, ...] = self._tokenizer.tokenize(content)
        self._tag_applier.apply_tokens(
            text_widget, tokens, self._tokenizer.get_supported_tags()
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns component version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
