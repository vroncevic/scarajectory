# -*- coding: UTF-8 -*-

'''
Module
    parameter_extractor.py
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
    Utility service extracting key-value and positional parameters from DSL token slices.
'''

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from scarajectory.core.model.dsl.scara_token import ScaraToken
from scarajectory.core.model.dsl.scara_token_type import ScaraTokenType

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ParameterExtractor:
    '''
        Helper utility extracting key-value pairs and typed numerical literals from tokens.

        It defines:

            :attributes:
                | None.
            :methods:
                | extract_key_values - Parses key=value pairs and positional parameters into dictionary.
                | parse_token_value - Converts token string literal to typed float, int, or str.
    '''

    @staticmethod
    def extract_key_values(*, tokens: Sequence[ScaraToken]) -> dict[str, Any]:
        '''
            Extracts key-value pairs (e.g. X=150.0 Y=80.0) from a sequence of tokens.

            :param tokens: Token slice following command keyword.
            :return: Dictionary of parsed parameter names and typed values.
        '''
        params: dict[str, Any] = {}
        idx = 0
        n = len(tokens)

        while idx < n:
            tok = tokens[idx]
            if (
                idx + 2 < n
                and tokens[idx + 1].token_type == ScaraTokenType.EQUALS
            ):
                key = tok.value.upper()
                val_tok = tokens[idx + 2]
                params[key] = ParameterExtractor.parse_token_value(token=val_tok)
                idx += 3
            else:
                key = tok.value.upper()
                if idx + 1 < n and tokens[idx + 1].token_type in (
                    ScaraTokenType.NUMBER,
                    ScaraTokenType.STRING,
                    ScaraTokenType.IDENTIFIER,
                ):
                    params[key] = ParameterExtractor.parse_token_value(
                        token=tokens[idx + 1]
                    )
                    idx += 2
                else:
                    params[key] = True
                    idx += 1
        return params

    @staticmethod
    def parse_token_value(*, token: ScaraToken) -> Any:
        '''
            Converts token string literal to float, int or string.

            :param token: ScaraToken instance.
            :return: Float, int, or string literal.
        '''
        if token.token_type == ScaraTokenType.NUMBER:
            if '.' in token.value or 'e' in token.value or 'E' in token.value:
                return float(token.value)
            return int(token.value)
        return token.value
