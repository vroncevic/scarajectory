# -*- coding: UTF-8 -*-

'''
Module
    launcher.py
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
    Concrete implementation of external SCARAEmu emulator launcher adapter.
'''

from __future__ import annotations

from os import P_NOWAIT, spawnve
from sys import executable
from tempfile import NamedTemporaryFile
from typing import ClassVar, Final

from scarajectory.infrastructure.gui.emulator.locator.ilocator import IEmulatorLocator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class EmulatorLauncher:
    '''
        Defines class EmulatorLauncher implementing IEmulatorLauncher contract structurally.
        External process launcher adapter for SCARAEmu digital twin preview.

        It defines:

            :constants:
                | FILE_MODE - File open mode for temporary script creation.
                | FILE_SUFFIX - File extension suffix for temporary SCARA DSL scripts.
                | FILE_ENCODING - Text encoding for temporary SCARA DSL script files.
                | DELETE_ON_CLOSE - Flag controlling temporary file deletion on descriptor close.
                | MSG_EMPTY_CODE - Status message returned when input DSL code is blank.
                | MSG_UNAVAILABLE - Error message returned when emulator target is not found.
                | MSG_LAUNCH_SUCCESS - Template for successful launch status message.
                | MSG_LAUNCH_FAILURE - Template for process launch failure error message.
            :attributes:
                | _locator - Injected IEmulatorLocator protocol collaborator.
            :methods:
                | __init__ - Initializes EmulatorLauncher with locator collaborator.
                | is_available - Checks if external emulator executable or script is available.
                | launch_preview - Exports script to temporary file and spawns SCARAEmu background process.
                | get_version - Returns launcher version string.
    '''

    FILE_MODE: ClassVar[str] = 'w'
    FILE_SUFFIX: ClassVar[str] = '.scara'
    FILE_ENCODING: ClassVar[str] = 'utf-8'
    DELETE_ON_CLOSE: ClassVar[bool] = False

    MSG_EMPTY_CODE: ClassVar[str] = 'DSL editor is empty. Nothing to preview.'
    MSG_UNAVAILABLE: ClassVar[str] = (
        'SCARAEmu executable or main.py not found on system.'
    )
    MSG_LAUNCH_SUCCESS: ClassVar[str] = '🚀 Launched SCARAEmu preview with {path}'
    MSG_LAUNCH_FAILURE: ClassVar[str] = '[ERR]: Failed to launch SCARAEmu: {exc}'

    _locator: IEmulatorLocator

    def __init__(self, *, locator: IEmulatorLocator) -> None:
        '''
            Initializes EmulatorLauncher with injected locator collaborator.

            :param locator: Injected IEmulatorLocator instance.
            :exceptions: None.
        '''
        self._locator: Final[IEmulatorLocator] = locator

    def is_available(self) -> bool:
        '''
            Checks if external emulator executable or script is available on the system.

            :return: True if SCARAEmu executable exists, False otherwise.
            :exceptions: None.
        '''
        return self._locator.is_available()

    def launch_preview(self, *, dsl_code: str) -> tuple[bool, str]:
        '''
            Exports script to temporary file and spawns SCARAEmu background process.

            :param dsl_code: SCARA DSL source text to preview.
            :return: Tuple of (success_boolean, status_or_error_message).
            :exceptions: None.
        '''
        code: str = dsl_code.strip()
        if not code:
            return False, self.MSG_EMPTY_CODE

        if not self._locator.is_available():
            return False, self.MSG_UNAVAILABLE

        try:
            with NamedTemporaryFile(
                mode=self.FILE_MODE,
                suffix=self.FILE_SUFFIX,
                delete=self.DELETE_ON_CLOSE,
                encoding=self.FILE_ENCODING,
            ) as tmp:
                tmp.write(code)
                tmp_path: str = tmp.name

            cmd: list[str] = self._locator.build_command(file_path=tmp_path)
            env: dict[str, str] = self._locator.build_environment()
            spawnve(P_NOWAIT, executable, cmd, env)

            return True, self.MSG_LAUNCH_SUCCESS.format(path=tmp_path)

        except OSError as exc:
            return False, self.MSG_LAUNCH_FAILURE.format(exc=exc)

    def get_version(self) -> str:
        '''
            Returns launcher version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
