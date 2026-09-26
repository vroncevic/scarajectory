# -*- coding: UTF-8 -*-
from __future__ import annotations

from math import cos, pi, sin
from typing import Final

from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.core.service.trajectory.discretization.iwaypoint_factory import IWaypointFactory

class ShapeDiscretizer:
    def __init__(self, *, waypoint_factory: IWaypointFactory) -> None:
        self._waypoint_factory: Final[IWaypointFactory] = waypoint_factory

    def discretize_line(
        self,
        p1: tuple[float, float],
        p2: tuple[float, float],
        *,
        z: float,
        speed: float,
    ) -> list[Waypoint]:
        return [
            self._waypoint_factory.create(x=p1[0], y=p1[1], z=z, speed=speed),
            self._waypoint_factory.create(x=p2[0], y=p2[1], z=z, speed=speed),
        ]

    def discretize_circle(
        self,
        center: tuple[float, float],
        radius: float,
        steps: int,
        *,
        z: float,
        speed: float,
    ) -> list[Waypoint]:
        pts: list[Waypoint] = []
        for i in range(steps + 1):
            angle: float = 2.0 * pi * (i / steps)
            px: float = center[0] + radius * cos(angle)
            py: float = center[1] + radius * sin(angle)
            pts.append(self._waypoint_factory.create(x=px, y=py, z=z, speed=speed))
        return pts

    def discretize_rectangle(
        self,
        p1: tuple[float, float],
        p2: tuple[float, float],
        *,
        z: float,
        speed: float,
    ) -> list[Waypoint]:
        return [
            self._waypoint_factory.create(x=p1[0], y=p1[1], z=z, speed=speed),
            self._waypoint_factory.create(x=p2[0], y=p1[1], z=z, speed=speed),
            self._waypoint_factory.create(x=p2[0], y=p2[1], z=z, speed=speed),
            self._waypoint_factory.create(x=p1[0], y=p2[1], z=z, speed=speed),
            self._waypoint_factory.create(x=p1[0], y=p1[1], z=z, speed=speed),
        ]
