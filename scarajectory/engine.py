# -*- coding: UTF-8 -*-

'''
Module
    engine.py
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
    Engine orchestrating the initialization and execution of scarajectory.
'''

from __future__ import annotations

from logging import INFO, ERROR
from sys import stdout

from ats_utilities.base.engine import Base
from ats_utilities.logger.ilogger import ILogger
from ats_utilities.exceptions import ATSValueError, ATSTypeError

from scarajectory.setup.bundle import SCARAjectoryBundle
from scarajectory.setup.validator import SCARAjectoryBundleValidator
from scarajectory.core.service.iservice import IService
from scarajectory.infrastructure.gui.igui import IGUI

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SCARAjectory(Base):
    '''
        Engine orchestrating the initialization and execution of scarajectory.

        It defines:

            :attributes:
                | _is_initialized - Flag indicating whether engine is initialized.
                | _logger - Logger for recording application events.
                | _gui - GUI presentation adapter.
                | _service - Trajectory domain service.
            :methods:
                | __init__ - Initializes the engine with bundle dependencies.
                | process - Executes the main application loop.
    '''

    _is_initialized: bool
    _logger: ILogger
    _gui: IGUI
    _service: IService

    def __init__(self, bundle: SCARAjectoryBundle) -> None:
        '''
            Initializes the scarajectory engine with adapters and services.

            :param bundle: SCARAjectoryBundle containing components.
            :exceptions: None.
        '''
        self._is_initialized = False

        try:
            SCARAjectoryBundleValidator.validate(bundle)
            super().__init__(bundle.base)

            self._gui = bundle.gui
            self._service = bundle.service

            self._is_initialized = all(
                component.is_initialized() for component in [
                    bundle.base.option_manager,
                    bundle.service,
                    self._gui
                ] if component
            )

            self._logger = self.get_context().logger
            self._logger.write_log(INFO, '✅ scarajectory: engine initialized successfully!')

        except (ATSValueError, ATSTypeError) as exc:
            stdout.write(f'❌ scarajectory: {exc}!\n')

        except Exception as exc:
            stdout.write(f'❌ scarajectory unexpected exception: {exc}!\n')

    def process(self, verbose: bool = False) -> bool:
        '''
            Launches the SCARAjectory GUI studio.

            :param verbose: Enable verbose logging.
            :return: True if executed successfully, False otherwise.
            :exceptions: None.
        '''
        try:
            if self.is_initialized():
                self._logger.write_log(INFO, '🔥 Launching SCARAjectory Motion Studio GUI...')
                self._gui.start()
                self._logger.write_log(INFO, '✅ SCARAjectory: application exiting successfully!')
                return True

            self._logger.write_log(ERROR, '❌ scarajectory: engine not initialized!')
            return False

        except (ATSValueError, ATSTypeError) as exc:
            self._logger.write_log(ERROR, f'❌ scarajectory: {exc}!')
            return False

        except Exception as exc:
            self._logger.write_log(ERROR, f'❌ scarajectory unexpected exception: {exc}!')
            return False
