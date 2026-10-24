# -*- coding: UTF-8 -*-

'''
Module
    locator.py
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
    Discovers, validates, and builds execution commands for SCARAEmu emulator target.
'''

from __future__ import annotations

from json import loads as json_loads
from os import environ
from os.path import abspath, dirname, exists, isdir, isfile, join
from pathlib import Path
from shutil import which
from sys import executable
from typing import ClassVar

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class EmulatorLocator:
    '''
        Discovers, validates, and builds execution commands for SCARAEmu emulator target.

        It defines:

            :constants:
                | TARGET_BINARY - Identifier for binary executable execution target.
                | TARGET_SCRIPT - Identifier for Python script execution target.
                | TARGET_NONE - Identifier when no valid execution target is found.
                | ENV_TOOL_PATH - Environment variable key specifying tool path.
                | ENV_MAIN_MODULE - Environment variable key specifying main module name.
                | ENV_PYTHONPATH - Environment variable key for Python search path.
                | CONFIG_KEY_TOOL_PATH - Configuration key for tool path in settings JSON.
                | CONFIG_KEY_MAIN_MODULE - Configuration key for main module in settings JSON.
                | DEFAULT_MAIN_MODULE - Default main entry script filename.
                | EXECUTABLE_NAME - Standard console script executable name.
                | COMMAND_EMULATOR - SCARAEmu CLI sub-command name.
                | OPTION_FILE - SCARAEmu CLI trajectory file option flag.
                | PYTHON_EXT - Python source file extension.
                | USER_CONFIG_DIR - Per-user dot-directory name under user home.
                | CONFIG_FILE_NAME - Default configuration file name.
                | FILE_READ_MODE - File reading mode string.
                | CONFIG_ENCODING - Text encoding for configuration JSON file.
                | DEV_REL_PARTS - Relative path components to adjacent dev tool repository.
                | DEFAULT_CONFIG_PATH - Default absolute path to scaraemu.json configuration.
            :attributes:
                | _config_path - Path to scaraemu.json configuration file.
            :methods:
                | __init__ - Initializes EmulatorLocator with configuration path.
                | resolve_target - Resolves target type and path across environment, config, PATH, and dev fallback.
                | is_available - Checks if external emulator executable or script is available.
                | build_command - Builds executable command list for spawning emulator process.
                | build_environment - Builds environment dictionary for external process.
                | get_version - Returns locator version string.
    '''

    TARGET_BINARY: ClassVar[str] = 'binary'
    TARGET_SCRIPT: ClassVar[str] = 'script'
    TARGET_NONE: ClassVar[str] = 'none'

    ENV_TOOL_PATH: ClassVar[str] = 'SCARAEMU_PATH'
    ENV_MAIN_MODULE: ClassVar[str] = 'SCARAEMU_MAIN'
    ENV_PYTHONPATH: ClassVar[str] = 'PYTHONPATH'

    CONFIG_KEY_TOOL_PATH: ClassVar[str] = 'tool_path'
    CONFIG_KEY_MAIN_MODULE: ClassVar[str] = 'main_module'
    DEFAULT_MAIN_MODULE: ClassVar[str] = 'main.py'
    EXECUTABLE_NAME: ClassVar[str] = 'scaraemu'
    COMMAND_EMULATOR: ClassVar[str] = 'emulator'
    OPTION_FILE: ClassVar[str] = '--file'
    PYTHON_EXT: ClassVar[str] = '.py'

    USER_CONFIG_DIR: ClassVar[str] = '.scarajectory'
    CONFIG_FILE_NAME: ClassVar[str] = 'scaraemu.json'
    FILE_READ_MODE: ClassVar[str] = 'r'
    CONFIG_ENCODING: ClassVar[str] = 'utf-8'

    DEV_REL_PARTS: ClassVar[tuple[str, ...]] = (
        'scaraemu', 'github', 'scaraemu'
    )

    DEFAULT_CONFIG_PATH: ClassVar[str] = join(
        dirname(dirname(dirname(dirname(abspath(__file__))))),
        'config',
        'scaraemu.json',
    )

    _config_path: str

    def __init__(self, *, config_path: str) -> None:
        '''
            Initializes EmulatorLocator with configuration path.

            :param config_path: Path to scaraemu.json configuration file.
            :exceptions: None.
        '''
        self._config_path = config_path

    def resolve_target(self) -> tuple[str, str]:
        '''
            Resolves target type and path across environment, config, PATH, and dev fallback.

            :return: Tuple of target type (binary, script, or none) and target path string.
            :exceptions: None.
        '''
        target_type: str = self.TARGET_NONE
        target_path: str = ''

        env_path: str = environ.get(self.ENV_TOOL_PATH, '').strip()
        if env_path and isdir(env_path) and isfile(join(env_path, self.DEFAULT_MAIN_MODULE)):
            target_type = self.TARGET_SCRIPT
            target_path = join(env_path, self.DEFAULT_MAIN_MODULE)
        elif env_path and isfile(env_path):
            target_type = (
                self.TARGET_SCRIPT if env_path.endswith(self.PYTHON_EXT)
                else self.TARGET_BINARY
            )
            target_path = env_path

        if target_type == self.TARGET_NONE:
            user_cfg = join(str(Path.home()), self.USER_CONFIG_DIR, self.CONFIG_FILE_NAME)
            cfg_path = user_cfg if exists(user_cfg) else self._config_path
            if exists(cfg_path):
                with open(cfg_path, mode=self.FILE_READ_MODE, encoding=self.CONFIG_ENCODING) as f:
                    raw_cfg = json_loads(f.read())
                if isinstance(raw_cfg, dict):
                    cfg_tool = str(raw_cfg.get(self.CONFIG_KEY_TOOL_PATH, '')).strip()
                    cfg_main = str(raw_cfg.get(self.CONFIG_KEY_MAIN_MODULE, '')).strip() or self.DEFAULT_MAIN_MODULE
                    if cfg_tool and isdir(cfg_tool) and isfile(join(cfg_tool, cfg_main)):
                        target_type = self.TARGET_SCRIPT
                        target_path = join(cfg_tool, cfg_main)
                    elif cfg_tool and isfile(cfg_tool):
                        target_type = (
                            self.TARGET_SCRIPT if cfg_tool.endswith(self.PYTHON_EXT)
                            else self.TARGET_BINARY
                        )
                        target_path = cfg_tool

        if target_type == self.TARGET_NONE:
            system_bin = which(self.EXECUTABLE_NAME)
            if system_bin:
                target_type = self.TARGET_BINARY
                target_path = system_bin

        if target_type == self.TARGET_NONE:
            ancestor = dirname(dirname(dirname(dirname(dirname(dirname(dirname(abspath(__file__))))))))
            dev_candidate = join(ancestor, *self.DEV_REL_PARTS, self.DEFAULT_MAIN_MODULE)
            if isfile(dev_candidate):
                target_type = self.TARGET_SCRIPT
                target_path = dev_candidate

        return target_type, target_path

    def is_available(self) -> bool:
        '''
            Checks if external emulator executable or script is available.

            :return: True if available, False otherwise.
            :exceptions: None.
        '''
        target_type, _ = self.resolve_target()
        return target_type != self.TARGET_NONE

    def build_command(self, *, file_path: str) -> list[str]:
        '''
            Builds executable command list for spawning emulator process.

            :param file_path: Path to trajectory plan file to preview.
            :return: Subprocess command arguments list.
            :exceptions: None.
        '''
        target_type, target_path = self.resolve_target()
        if target_type == self.TARGET_BINARY:
            return [target_path, self.COMMAND_EMULATOR, self.OPTION_FILE, file_path]
        if target_type == self.TARGET_SCRIPT:
            return [executable, target_path, self.COMMAND_EMULATOR, self.OPTION_FILE, file_path]
        return []

    def build_environment(self) -> dict[str, str]:
        '''
            Builds environment dictionary for external process.

            :return: Environment variables mapping.
            :exceptions: None.
        '''
        env: dict[str, str] = dict(environ)
        target_type, target_path = self.resolve_target()
        if target_type == self.TARGET_SCRIPT:
            script_dir: str = dirname(target_path)
            existing: str = env.get(self.ENV_PYTHONPATH, '')
            env[self.ENV_PYTHONPATH] = (
                f'{script_dir}:{existing}' if existing else script_dir
            )
        return env

    def get_version(self) -> str:
        '''
            Returns locator version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
