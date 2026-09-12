# -*- coding: UTF-8 -*-

'''
Module
    emulator_launcher.py
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

from os import environ
from pathlib import Path
from subprocess import Popen
from sys import executable
from tempfile import NamedTemporaryFile

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
        External process launcher adapter for SCARAEmu digital twin preview.

        It defines:

            :methods:
                | launch_preview - Exports script to temporary file and spawns SCARAEmu background process.
    '''

    def launch_preview(self, *, dsl_code: str) -> tuple[bool, str]:
        '''
            Exports script to temporary file and spawns SCARAEmu background process.

            :param dsl_code: SCARA DSL source text to preview.
            :return: Tuple of (success_boolean, status_or_error_message).
            :exceptions: None.
        '''
        code: str = dsl_code.strip()

        if not code:
            return False, 'DSL editor is empty. Nothing to preview.'

        candidate_dirs: list[Path] = [
            Path(__file__).resolve().parents[6] / 'scaraemu' / 'github' / 'scaraemu',
            Path('/data/dev/python/3_tools/scaraemu/github/scaraemu'),
        ]
        emu_dir: Path | None = next(
            (d for d in candidate_dirs if (d / 'main.py').is_file()),
            None,
        )

        if not emu_dir:
            return False, 'SCARAEmu directory with main.py not found.'

        try:
            with NamedTemporaryFile(
                mode='w', suffix='.scara', delete=False, encoding='utf-8'
            ) as tmp:
                tmp.write(code)
                tmp_path: str = tmp.name

            cmd: list[str] = [
                executable,
                str(emu_dir / 'main.py'),
                'emulator',
                '--file',
                tmp_path,
            ]
            env: dict[str, str] = dict(environ)
            env['PYTHONPATH'] = f"{emu_dir}:{env.get('PYTHONPATH', '')}"
            Popen(cmd, cwd=str(emu_dir), env=env)

            return True, f'🚀 Launched SCARAEmu preview with {tmp_path}'

        except OSError as exc:
            return False, f'[ERR]: Failed to launch SCARAEmu: {exc}'
