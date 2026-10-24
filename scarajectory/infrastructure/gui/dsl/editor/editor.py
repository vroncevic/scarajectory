# -*- coding: UTF-8 -*-

'''
Module
    editor.py
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
    Syntax-highlighted multi-line code editor component for SCARA DSL scripts.
'''

from __future__ import annotations

from tkinter import BOTH, END, RIGHT, VERTICAL, Text, Widget, Y
from tkinter.ttk import Frame, Scrollbar
from typing import ClassVar, Final

from scarajectory.infrastructure.gui.dsl.syntax.highlighter.ihighlighter import IDslSyntaxHighlighter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DslCodeEditor(Frame):
    '''
        Scrolled multi-line text editor with integrated syntax highlighting and undo/redo support.

        It defines:

            :attributes:
                | COLOR_BG - Background color hex string.
                | COLOR_FG - Foreground color hex string.
                | COLOR_CURSOR - Insertion cursor color hex string.
                | FONT_FAMILY - Monospace editor font family.
                | FONT_SIZE - Standard editor font size in points.
                | START_INDEX - Text buffer start position.
                | EVENT_KEY - Tkinter key release event sequence string.
                | WRAP_MODE - Editor text line wrap mode.
                | _txt_editor - Inner multi-line Text widget.
                | _highlighter - IDslSyntaxHighlighter strategy.
            :methods:
                | __init__ - Initializes the editor container and binds syntax highlighter.
                | get_text - Returns full contents of the editor buffer.
                | set_text - Replaces editor buffer with provided text.
                | clear - Clears all text in the editor.
                | highlight - Triggers manual syntax highlighting refresh.
                | get_version - Returns editor component version string.
    '''

    COLOR_BG: ClassVar[str] = '#14161a'
    COLOR_FG: ClassVar[str] = '#abb2bf'
    COLOR_CURSOR: ClassVar[str] = '#61afef'
    FONT_FAMILY: ClassVar[str] = 'DejaVu Sans Mono'
    FONT_SIZE: ClassVar[int] = 9
    START_INDEX: ClassVar[str] = '1.0'
    EVENT_KEY: ClassVar[str] = '<KeyRelease>'
    WRAP_MODE: ClassVar[str] = 'none'

    _txt_editor: Text
    _highlighter: IDslSyntaxHighlighter

    def __init__(
        self,
        parent: Widget,
        *,
        highlighter: IDslSyntaxHighlighter,
    ) -> None:
        '''
            Initializes the editor container and binds syntax highlighter.

            :param parent: Parent container widget.
            :param highlighter: Required IDslSyntaxHighlighter strategy.
            :exceptions: None.
        '''
        super().__init__(parent)

        scroll_y = Scrollbar(self, orient=VERTICAL)
        scroll_y.pack(side=RIGHT, fill=Y)

        self._txt_editor = Text(
            self,
            width=1,
            bg=self.COLOR_BG,
            fg=self.COLOR_FG,
            insertbackground=self.COLOR_CURSOR,
            font=(self.FONT_FAMILY, self.FONT_SIZE),
            wrap=self.WRAP_MODE,
            yscrollcommand=scroll_y.set,
            undo=True,
        )
        self._txt_editor.pack(fill=BOTH, expand=True)
        scroll_y.config(command=self._txt_editor.yview)

        self._highlighter: Final[IDslSyntaxHighlighter] = highlighter
        self._highlighter.configure_styles(self._txt_editor)
        self._txt_editor.bind(self.EVENT_KEY, lambda _e: self.highlight())

    def get_text(self) -> str:
        '''
            Returns full contents of the editor buffer.

            :return: Code string.
            :exceptions: None.
        '''
        return self._txt_editor.get(self.START_INDEX, END)

    def set_text(self, content: str) -> None:
        '''
            Replaces editor buffer with provided text and refreshes highlighting.

            :param content: Source code string.
            :exceptions: None.
        '''
        self._txt_editor.delete(self.START_INDEX, END)
        self._txt_editor.insert(END, content)
        self._highlighter.highlight(self._txt_editor)

    def clear(self) -> None:
        '''
            Clears all text in the editor.

            :exceptions: None.
        '''
        self._txt_editor.delete(self.START_INDEX, END)

    def highlight(self) -> None:
        '''
            Triggers manual syntax highlighting refresh.

            :exceptions: None.
        '''
        self._highlighter.highlight(self._txt_editor)

    def get_version(self) -> str:
        '''
            Returns editor component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
