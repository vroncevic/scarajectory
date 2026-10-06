# -*- coding: UTF-8 -*-

'''
Module
    code_editor_factory.py
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
    Factory service constructing DslCodeEditor instances.
'''

from __future__ import annotations

from tkinter import Widget

from scarajectory.infrastructure.gui.dsl.code_editor import DslCodeEditor
from scarajectory.infrastructure.gui.dsl.syntax.highlighter_factory import DslSyntaxHighlighterFactory
from scarajectory.infrastructure.gui.dsl.syntax.ihighlighter import IDslSyntaxHighlighter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DslCodeEditorFactory:
    '''
        Factory providing creation of DslCodeEditor instances.

        It defines:

            :methods:
                | create - Constructs DslCodeEditor with explicit highlighter.
                | create_default - Constructs DslCodeEditor with default highlighter.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        parent: Widget,
        *,
        highlighter: IDslSyntaxHighlighter,
    ) -> DslCodeEditor:
        '''
            Constructs DslCodeEditor with explicit highlighter.

            :param parent: Parent container widget.
            :param highlighter: Required IDslSyntaxHighlighter strategy.
            :return: Configured DslCodeEditor instance.
            :exceptions: None.
        '''
        return DslCodeEditor(parent, highlighter=highlighter)

    @classmethod
    def create_default(cls, parent: Widget) -> DslCodeEditor:
        '''
            Constructs DslCodeEditor with default highlighter.

            :param parent: Parent container widget.
            :return: Configured DslCodeEditor instance.
            :exceptions: None.
        '''
        highlighter: IDslSyntaxHighlighter = DslSyntaxHighlighterFactory.create_default()

        return cls.create(parent, highlighter=highlighter)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
