# -*- coding: UTF-8 -*-

'''
Module
    renderer_test.py
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
    Unit tests for decomposed CanvasRenderer and its specialized sub-renderers.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.service.kinematics.dependencies import KinematicsDependencies
from scaralang.core.service.kinematics.factory import KinematicsFactory
from scaralang.core.service.kinematics.profile.default_scara_profile import DefaultScaraProfile
from scaralang.core.service.trajectory.validation.dependencies import ValidationDependencies
from scaralang.core.service.trajectory.validation.factory import ValidationFactory

from scarajectory.core.model.trajectory.waypoint import TrajectoryWaypoint
from scarajectory.core.service.trajectory.plan.observer.factory import ObserverFactory
from scarajectory.core.service.trajectory.plan.selection.dependencies import SelectionDependencies
from scarajectory.core.service.trajectory.plan.selection.factory import SelectionFactory
from scarajectory.core.service.trajectory.plan.store.dependencies import StoreDependencies
from scarajectory.core.service.trajectory.plan.store.factory import StoreFactory
from scarajectory.infrastructure.gui.canvas.renderer.preview.renderer import CanvasPreviewRenderer

from scarajectory.infrastructure.gui.canvas.renderer.renderer import CanvasRenderer
from scarajectory.infrastructure.gui.canvas.renderer.trajectory.bundle import TrajectoryRenderBundle
from scarajectory.infrastructure.gui.canvas.renderer.trajectory.renderer import CanvasTrajectoryRenderer
from scarajectory.infrastructure.gui.canvas.transform.transform import ViewportTransform
from scarajectory.infrastructure.gui.model.canvas_tool_mode import CanvasToolMode
from scarajectory.infrastructure.scaralang.boundary.factory import WorkspaceBoundaryAdapterFactory
from scarajectory.infrastructure.scaralang.validation.dependencies import TrajectoryValidationDependencies
from scarajectory.infrastructure.scaralang.validation.factory import TrajectoryValidationAdapterFactory


__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MockCanvas:
    '''
        Mock Tkinter canvas recording draw commands for headless testing.

        It defines:

            :attributes:
                | width - Canvas width.
                | height - Canvas height.
                | lines - Recorded lines.
                | ovals - Recorded ovals.
                | texts - Recorded texts.
                | polygons - Recorded polygons.
                | rectangles - Recorded rectangles.
            :methods:
                | __init__ - Initializes mock canvas.
                | winfo_width - Returns canvas width.
                | winfo_height - Returns canvas height.
                | create_line - Records line creation.
                | create_oval - Records oval creation.
                | create_text - Records text creation.
                | create_polygon - Records polygon creation.
                | create_rectangle - Records rectangle creation.
    '''

    def __init__(self, width: int = 800, height: int = 600) -> None:
        '''
            Initializes mock canvas with dimensions.

            :param width: Canvas width integer.
            :param height: Canvas height integer.
            :exceptions: None.
        '''
        self.width = width
        self.height = height
        self.lines: list[tuple[tuple[float, ...], dict[str, object]]] = []
        self.ovals: list[tuple[tuple[float, ...], dict[str, object]]] = []
        self.texts: list[tuple[tuple[float, ...], dict[str, object]]] = []
        self.polygons: list[tuple[tuple[float, ...], dict[str, object]]] = []
        self.rectangles: list[tuple[tuple[float, ...], dict[str, object]]] = []

    def winfo_width(self) -> int:
        '''
            Returns mock canvas width.

            :return: Canvas width.
            :exceptions: None.
        '''
        return self.width

    def winfo_height(self) -> int:
        '''
            Returns mock canvas height.

            :return: Canvas height.
            :exceptions: None.
        '''
        return self.height

    def create_line(self, *args: float, **kwargs: object) -> int:
        '''
            Records line draw call.

            :param args: Coordinates.
            :param kwargs: Options.
            :return: Unique index.
            :exceptions: None.
        '''
        self.lines.append((args, kwargs))
        return len(self.lines)

    def create_oval(self, *args: float, **kwargs: object) -> int:
        '''
            Records oval draw call.

            :param args: Coordinates.
            :param kwargs: Options.
            :return: Unique index.
            :exceptions: None.
        '''
        self.ovals.append((args, kwargs))
        return len(self.ovals)

    def create_text(self, *args: float, **kwargs: object) -> int:
        '''
            Records text draw call.

            :param args: Coordinates.
            :param kwargs: Options.
            :return: Unique index.
            :exceptions: None.
        '''
        self.texts.append((args, kwargs))
        return len(self.texts)

    def create_polygon(self, *args: float, **kwargs: object) -> int:
        '''
            Records polygon draw call.

            :param args: Coordinates.
            :param kwargs: Options.
            :return: Unique index.
            :exceptions: None.
        '''
        self.polygons.append((args, kwargs))
        return len(self.polygons)

    def create_rectangle(self, *args: float, **kwargs: object) -> int:
        '''
            Records rectangle draw call.

            :param args: Coordinates.
            :param kwargs: Options.
            :return: Unique index.
            :exceptions: None.
        '''
        self.rectangles.append((args, kwargs))
        return len(self.rectangles)


class TestCanvasRenderer(TestCase):
    '''
        Test cases validating CanvasRenderer facade and sub-renderers.

        It defines:

            :methods:
                | setUp - Initializes fixtures for mock canvas, viewport, plan.
                | test_canvas_background_renderer - Tests background layers.
                | test_canvas_trajectory_renderer - Tests trajectory lines.
                | test_canvas_preview_renderer - Tests CAD tool previews.
                | test_canvas_renderer_facade - Tests facade delegation.
                | test_renderer_get_version - Tests CanvasRenderer get_version.
    '''

    def setUp(self) -> None:
        '''
            Initializes fixtures for mock canvas, viewport, plan, validator.

            :exceptions: None.
        '''
        self.canvas = MockCanvas()
        self.vp = ViewportTransform()
        self.bounds = DefaultScaraProfile.create_bounds()
        kinematics_provides = KinematicsFactory.create(
            dependencies=KinematicsDependencies(
                bounds=self.bounds,
                dls_config=DefaultScaraProfile.create_dls_config(),
            )
        )
        validation_provides = ValidationFactory.create(
            dependencies=ValidationDependencies(
                workspace=kinematics_provides.workspace,
                envelope=kinematics_provides.envelope,
            )
        )
        self.validator = TrajectoryValidationAdapterFactory.create(
            dependencies=TrajectoryValidationDependencies(
                workspace_envelope=kinematics_provides.envelope,
                waypoint_validator=validation_provides.waypoint,
                plan_validator=validation_provides.plan,
            )
        )
        store_provides = StoreFactory.create(
            StoreDependencies(initial_waypoints=())
        )
        self.store = store_provides.waypoint_store
        observer_provides = ObserverFactory.create()
        selection_provides = SelectionFactory.create(
            dependencies=SelectionDependencies(
                waypoint_store=self.store,
                plan_observer_dispatcher=observer_provides.plan_observer_dispatcher,
                initial_index=0,
            )
        )
        self.selection = selection_provides.plan_selection_coordinator
        self.boundary_adapter = WorkspaceBoundaryAdapterFactory.create()

    def test_canvas_background_renderer(self) -> None:
        '''
            Tests background polar grid and workspace limits drawing.

            :exceptions: None.
        '''
        CanvasRenderer.draw_background(
            self.canvas, self.vp, self.validator, self.boundary_adapter
        )



        self.assertGreater(len(self.canvas.lines), 0)
        self.assertGreater(len(self.canvas.ovals), 0)
        self.assertGreater(len(self.canvas.texts), 0)
        self.assertEqual(len(self.canvas.polygons), 1)

    def test_canvas_trajectory_renderer(self) -> None:
        '''
            Tests trajectory lines, nodes, and selection ring drawing.

            :exceptions: None.
        '''
        self.store.replace([
            TrajectoryWaypoint(x=100.0, y=100.0, z=0.0, speed=50.0, phi=0.0, name='', command=''),
            TrajectoryWaypoint(x=150.0, y=120.0, z=0.0, speed=50.0, phi=0.0, name='', command=''),
        ])
        self.selection.set_selected_index(0)

        bundle = TrajectoryRenderBundle(
            store=self.store, selection=self.selection, validator=self.validator
        )
        CanvasTrajectoryRenderer.draw_trajectory(
            self.canvas, self.vp, bundle
        )

        self.assertEqual(len(self.canvas.lines), 1)
        self.assertEqual(len(self.canvas.ovals), 3)
        self.assertEqual(len(self.canvas.texts), 2)

    def test_canvas_preview_renderer(self) -> None:
        '''
            Tests CAD tool preview geometries for circle, rectangle, and line.

            :exceptions: None.
        '''
        drag_pts: tuple[tuple[float, float], tuple[float, float]] = (
            (50.0, 50.0), (100.0, 100.0)
        )

        CanvasPreviewRenderer.draw_preview(
            self.canvas, self.vp, CanvasToolMode.CIRCLE, drag_pts
        )
        self.assertGreater(len(self.canvas.ovals), 0)

        CanvasPreviewRenderer.draw_preview(
            self.canvas, self.vp, CanvasToolMode.RECTANGLE, drag_pts
        )
        self.assertGreater(len(self.canvas.rectangles), 0)

        CanvasPreviewRenderer.draw_preview(
            self.canvas, self.vp, CanvasToolMode.LINE, drag_pts
        )
        self.assertGreater(len(self.canvas.lines), 0)

        CanvasPreviewRenderer.draw_preview(
            self.canvas, self.vp, CanvasToolMode.FREEHAND, drag_pts
        )

    def test_canvas_renderer_facade(self) -> None:
        '''
            Tests that CanvasRenderer facade delegates calls to all 3.

            :exceptions: None.
        '''
        self.store.replace([
            TrajectoryWaypoint(x=120.0, y=80.0, z=0.0, speed=50.0, phi=0.0, name='', command='')
        ])

        bundle = TrajectoryRenderBundle(
            store=self.store, selection=self.selection, validator=self.validator
        )
        CanvasRenderer.draw_background(
            self.canvas, self.vp, self.validator, self.boundary_adapter
        )

        CanvasRenderer.draw_trajectory(self.canvas, self.vp, bundle)

        CanvasRenderer.draw_preview(
            self.canvas,
            self.vp,
            CanvasToolMode.CIRCLE,
            ((0.0, 0.0), (50.0, 50.0))
        )

        self.assertGreater(len(self.canvas.lines), 0)
        self.assertGreater(len(self.canvas.ovals), 0)
        self.assertGreater(len(self.canvas.texts), 0)
        self.assertGreater(len(self.canvas.polygons), 0)

    def test_renderer_get_version(self) -> None:
        '''
            Tests that CanvasRenderer get_version returns string.

            :exceptions: None.
        '''
        version: str = CanvasRenderer.get_version()
        self.assertIsInstance(version, str)
        self.assertEqual(version, '1.0.3')


if __name__ == '__main__':
    main()
