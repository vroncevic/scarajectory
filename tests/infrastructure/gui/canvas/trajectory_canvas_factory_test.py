# -*- coding: UTF-8 -*-

'''
Module
    trajectory_canvas_factory_test.py
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
    Unit tests for TrajectoryCanvasFactory assembly service.
'''

from __future__ import annotations

from tkinter import Tk
from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.canvas.bundle import CanvasBundle
from scarajectory.infrastructure.gui.canvas.trajectory_canvas import TrajectoryCanvas
from scarajectory.infrastructure.gui.canvas.trajectory_canvas_factory import TrajectoryCanvasFactory
from scarajectory.infrastructure.gui.model.canvas_settings import CanvasSettings

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestTrajectoryCanvasFactory(TestCase):
    '''
        Test cases verifying TrajectoryCanvasFactory construction logic.
    '''

    root: Tk

    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Tk()
        cls.root.withdraw()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.root.destroy()

    def test_create(self) -> None:
        '''
            Verifies factory creates and wires TrajectoryCanvas instance.
        '''
        mock_dispatcher = MagicMock()
        mock_validator = MagicMock()
        mock_validator.r_max = 350.0
        mock_validator.r_min = 50.0
        settings = CanvasSettings(
            default_z=20.0,
            default_speed=50.0,
            enforce_deadzone=True,
        )
        bundle = CanvasBundle(
            store=MagicMock(),
            selection=MagicMock(),
            mutation=MagicMock(),
            dispatcher=mock_dispatcher,
            validator=mock_validator,
            settings=settings,
        )
        canvas = TrajectoryCanvasFactory.create(self.root, bundle=bundle)
        self.assertIsInstance(canvas, TrajectoryCanvas)
        self.assertIsNotNone(canvas.navigator)
        self.assertIsNotNone(canvas.status_presenter)
        mock_dispatcher.add_observer.assert_called_once()
        canvas.destroy()

    def test_get_version(self) -> None:
        '''
            Verifies factory version string retrieval.
        '''
        version = TrajectoryCanvasFactory.get_version()
        self.assertIsInstance(version, str)
        self.assertTrue(len(version) > 0)


if __name__ == '__main__':
    main()
