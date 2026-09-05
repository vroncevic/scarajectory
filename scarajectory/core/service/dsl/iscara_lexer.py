# -*- coding: UTF-8 -*-

'''
Module
    iscara_lexer.py
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
    Defines structural runtime-checkable protocol IScaraLexer for SCARA DSL lexical analysis.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scarajectory.core.model.dsl.scara_token import ScaraToken

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IScaraLexer(Protocol):
    '''
        Structural protocol defining contract for SCARA DSL source text tokenization.

        It defines:

            :attributes:
                | None.
            :methods:
                | tokenize - Tokenizes raw source code into an immutable tuple of lexical tokens.
    '''

    def tokenize(self, *, source: str) -> tuple[ScaraToken, ...]:
        '''
            Tokenizes source text into a tuple of ScaraToken instances.

            :param source: Raw source code string.
            :return: Immutable tuple of ScaraToken tokens.
        '''
        ...
