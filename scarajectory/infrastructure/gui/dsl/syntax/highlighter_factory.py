# -*- coding: UTF-8 -*-

'''
Module
    highlighter_factory.py
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
    Factory service constructing DslSyntaxHighlighter instances.
'''

from __future__ import annotations

from scarajectory.infrastructure.gui.dsl.syntax.highlighter import DslSyntaxHighlighter
from scarajectory.infrastructure.gui.dsl.syntax.itag_applier import IDslTagApplier
from scarajectory.infrastructure.gui.dsl.syntax.itokenizer import IDslSyntaxTokenizer
from scarajectory.infrastructure.gui.dsl.syntax.tag_applier_factory import DslTagApplierFactory
from scarajectory.infrastructure.gui.dsl.syntax.tokenizer_factory import DslSyntaxTokenizerFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DslSyntaxHighlighterFactory:
    '''
        Factory providing creation of DslSyntaxHighlighter instances.

        It defines:

            :methods:
                | create - Constructs DslSyntaxHighlighter with explicit collaborators.
                | create_default - Constructs DslSyntaxHighlighter with default collaborators.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        tokenizer: IDslSyntaxTokenizer,
        tag_applier: IDslTagApplier,
    ) -> DslSyntaxHighlighter:
        '''
            Constructs DslSyntaxHighlighter with explicit collaborators.

            :param tokenizer: Required IDslSyntaxTokenizer strategy.
            :param tag_applier: Required IDslTagApplier formatting helper.
            :return: Configured DslSyntaxHighlighter instance.
            :exceptions: None.
        '''
        return DslSyntaxHighlighter(
            tokenizer=tokenizer,
            tag_applier=tag_applier,
        )

    @classmethod
    def create_default(cls) -> DslSyntaxHighlighter:
        '''
            Constructs DslSyntaxHighlighter with default collaborators.

            :return: Configured DslSyntaxHighlighter instance.
            :exceptions: None.
        '''
        return cls.create(
            tokenizer=DslSyntaxTokenizerFactory.create(),
            tag_applier=DslTagApplierFactory.create(),
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
