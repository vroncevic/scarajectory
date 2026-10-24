# -*- coding: UTF-8 -*-

'''
Module
    ipresenter_test.py
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
    Unit testing for ICanvasSettingsPresenter protocol conformance.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.infrastructure.gui.canvas.settings.ipresenter import ICanvasSettingsPresenter
from scarajectory.infrastructure.gui.model.canvas_settings import CanvasSettings

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConformingPresenterStub:
    '''
        Conforming stub implementation satisfying ICanvasSettingsPresenter.

        It defines:

            :methods:
                | update_settings - Updates settings.
                | settings - Returns settings.
    '''

    def update_settings(self, settings: CanvasSettings) -> None:
        '''
            Updates settings.

            :param settings: CanvasSettings instance.
            :exceptions: None.
        '''
        del settings

    @property
    def settings(self) -> CanvasSettings:
        '''
            Returns settings.

            :return: CanvasSettings instance.
            :exceptions: None.
        '''
        return CanvasSettings(
            default_z=10.0,
            default_speed=50.0,
            enforce_deadzone=True,
        )


class NonConformingPresenterStub:
    '''
        Non-conforming stub missing settings property.

        It defines:

            :methods:
                | update_settings - Updates settings.
                | validate - Dummy validation method.
    '''

    def update_settings(self, settings: CanvasSettings) -> None:
        '''
            Updates settings.

            :param settings: CanvasSettings instance.
            :exceptions: None.
        '''
        del settings

    def validate(self) -> bool:
        '''
            Dummy validation method.

            :return: True.
            :exceptions: None.
        '''
        return True


class TestICanvasSettingsPresenter(TestCase):
    '''
        Unit tests validating structural protocol runtime checks for ICanvasSettingsPresenter.

        It defines:

            :methods:
                | test_protocol_conformance_success - Verifies conforming stub satisfies protocol.
                | test_protocol_conformance_failure - Verifies non-conforming stub fails protocol.
    '''

    def test_protocol_conformance_success(self) -> None:
        '''
            Verifies conforming stub satisfies ICanvasSettingsPresenter protocol.

            :exceptions: None.
        '''
        stub = ConformingPresenterStub()
        self.assertIsInstance(stub, ICanvasSettingsPresenter)

    def test_protocol_conformance_failure(self) -> None:
        '''
            Verifies non-conforming stub fails ICanvasSettingsPresenter protocol check.

            :exceptions: None.
        '''
        incomplete = NonConformingPresenterStub()
        self.assertNotIsInstance(incomplete, ICanvasSettingsPresenter)


if __name__ == '__main__':
    main()
