# -*- coding: UTF-8 -*-

'''
Module
    dep_validator.py
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
    Validator for the scarajectory bundle dependencies.
'''

from __future__ import annotations

from collections.abc import Mapping
from ats_utilities.exceptions import ATSValueError, ATSTypeError
from ats_utilities.validation.check_type import istype
from ats_utilities.validation.check_value import not_none

from scarajectory.setup.dependencies import SCARAjectoryBundleDependencies
from scarajectory.setup.keys import SCARAjectoryBundleKeys

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SCARAjectoryBundleDependenciesValidator:
    '''
        Validator for the scarajectory bundle dependencies.

        It defines:

            :methods:
                | validate - Validates the scarajectory bundle dependencies.
                | is_valid - Checks if the scarajectory bundle dependencies are valid.
    '''

    @classmethod
    def validate(cls, dependencies: SCARAjectoryBundleDependencies) -> None:
        '''
            Validates the scarajectory bundle dependencies.

            :param dependencies: The scarajectory bundle dependencies to be validated.
            :exceptions:
                | ATSValueError: The dependencies must be provided.
                | ATSTypeError: The dependencies must be a Mapping and match expected types.
        '''
        ctx: str = 'scarajectory_bundle_dependencies_validator::validate(...)'
        msg_deps_none: str = 'the scarajectory bundle dependencies must be provided'
        msg_deps_istype: str = 'the scarajectory bundle dependencies must be a Mapping'

        not_none(dependencies, ctx, msg_deps_none)
        istype(dependencies, Mapping, ctx, msg_deps_istype)

        for attr_name, expected_type in SCARAjectoryBundleKeys.get_dependency_to_type().items():
            msg_attr_none: str = f'the {attr_name.replace("_", " ")} must be provided'
            msg_attr_istype: str = f'the {attr_name.replace("_", " ")} must be an instance of {expected_type.__name__}'

            attribute = dependencies.get(attr_name)

            not_none(attribute, ctx, msg_attr_none)
            istype(attribute, expected_type, ctx, msg_attr_istype)

    @classmethod
    def is_valid(cls, dependencies: SCARAjectoryBundleDependencies) -> bool:
        '''
            Checks if the scarajectory bundle dependencies are valid.

            :param dependencies: The scarajectory bundle dependencies to check.
            :return: True if valid, False otherwise.
            :exceptions: None.
        '''
        try:
            cls.validate(dependencies)
            return True
        except (ATSValueError, ATSTypeError):
            return False
