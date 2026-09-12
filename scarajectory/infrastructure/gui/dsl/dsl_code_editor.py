# -*- coding: UTF-8 -*-

'''
Module
    dsl_code_editor.py
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

from tkinter import (
    BOTH, END, Event, Misc, RIGHT, VERTICAL, Widget, Y, Text,
)
from tkinter.ttk import Frame, Scrollbar
from typing import Final

from scarajectory.infrastructure.gui.dsl.dsl_syntax_highlighter import DslSyntaxHighlighter

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
                | _txt_editor - Inner multi-line Text widget.
                | _highlighter - Syntax highlighter instance.
            :methods:
                | __init__ - Initializes the editor container and binds syntax highlighter.
                | get_text - Returns full contents of the editor buffer.
                | set_text - Replaces editor buffer with provided text.
                | clear - Clears all text in the editor.
                | highlight - Triggers manual syntax highlighting refresh.
    '''

    _txt_editor: Text
    _highlighter: DslSyntaxHighlighter

    def __init__(self, parent: Widget, **kwargs: object) -> None:
        '''
            Initializes the editor container and binds syntax highlighter.

            :param parent: Parent container widget.
            :exceptions: None.
        '''
        super().__init__(parent, **kwargs)

        scroll_y = Scrollbar(self, orient=VERTICAL)
        scroll_y.pack(side=RIGHT, fill=Y)

        self._txt_editor = Text(
            self,
            width=1,
            bg='#14161a',
            fg='#abb2bf',
            insertbackground='#61afef',
            font=('DejaVu Sans Mono', 9),
            wrap='none',
            yscrollcommand=scroll_y.set,
            undo=True,
        )
        self._txt_editor.pack(fill=BOTH, expand=True)
        scroll_y.config(command=self._txt_editor.yview)

        self._highlighter: Final[DslSyntaxHighlighter] = DslSyntaxHighlighter(self._txt_editor)
        self._txt_editor.bind('<KeyRelease>', self._on_key_release)

    def _on_key_release(self, _event: Event[Misc]) -> None:
        '''
            Refreshes syntax highlighting on keystrokes.

            :param _event: Tkinter event.
            :exceptions: None.
        '''
        self._highlighter.highlight(self._txt_editor)

    def get_text(self) -> str:
        '''
            Returns full contents of the editor buffer.

            :return: Code string.
            :exceptions: None.
        '''
        return self._txt_editor.get('1.0', END)

    def set_text(self, content: str) -> None:
        '''
            Replaces editor buffer with provided text and refreshes highlighting.

            :param content: Source code string.
            :exceptions: None.
        '''
        self._txt_editor.delete('1.0', END)
        self._txt_editor.insert(END, content)
        self._highlighter.highlight(self._txt_editor)

    def clear(self) -> None:
        '''
            Clears all text in the editor.

            :exceptions: None.
        '''
        self._txt_editor.delete('1.0', END)

    def highlight(self) -> None:
        '''
            Triggers manual syntax highlighting refresh.

            :exceptions: None.
        '''
        self._highlighter.highlight(self._txt_editor)
