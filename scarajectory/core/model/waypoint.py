# -*- coding: UTF-8 -*-

'''
Module
    waypoint.py
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
    Defines Waypoint data model representing a single 4-DOF motion target point.
'''

from __future__ import annotations

import math
from typing import NamedTuple

from scarajectory.core.model.point_dto import PointDTO

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class Waypoint(NamedTuple):
    '''
        Immutable waypoint entity representing target coordinates, tool orientation and speed.

        It defines:

            :attributes:
                | x - X Cartesian coordinate in mm.
                | y - Y Cartesian coordinate in mm.
                | z - Z height coordinate in mm.
                | phi - Tool orientation rotation angle in degrees.
                | speed - Motion feedrate speed in mm/s.
                | name - Optional waypoint identifier.
            :methods:
                | to_dto - Converts waypoint entity to lightweight PointDTO.
                | from_dto - Creates waypoint from PointDTO.
                | radial_distance - Calculates planar radial distance from base.
                | distance_to - Calculates 3D Euclidean distance to another waypoint.
                | to_ascii_packet - Formats point as standard firmware protocol packet string.
                | to_dict - Serializes point to dictionary for JSON persistence.
                | from_dict - Deserializes waypoint from dictionary.
    '''

    x: float
    y: float
    z: float = 20.0
    phi: float = 0.0
    speed: float = 40.0
    name: str = ''

    def to_dto(self) -> PointDTO:
        '''
            Converts waypoint entity to lightweight PointDTO.

            :return: PointDTO representation.
            :exceptions: None.
        '''
        return PointDTO(
            x=self.x,
            y=self.y,
            z=self.z,
            phi=self.phi,
            speed=self.speed,
            name=self.name
        )

    @classmethod
    def from_dto(cls, dto: PointDTO) -> Waypoint:
        '''
            Creates waypoint from PointDTO.

            :param dto: PointDTO data transfer object.
            :return: Waypoint instance.
            :exceptions: None.
        '''
        return cls(
            x=dto.x,
            y=dto.y,
            z=dto.z,
            phi=dto.phi,
            speed=dto.speed,
            name=dto.name
        )

    @property
    def radial_distance(self) -> float:
        '''
            Calculates planar radial distance from base r = sqrt(x^2 + y^2).

            :return: Radial distance in mm.
            :exceptions: None.
        '''
        return math.hypot(self.x, self.y)

    def distance_to(self, other: Waypoint) -> float:
        '''
            Calculates 3D Euclidean distance to another waypoint.

            :param other: Target waypoint.
            :return: 3D distance in mm.
            :exceptions: None.
        '''
        dx: float = other.x - self.x
        dy: float = other.y - self.y
        dz: float = other.z - self.z
        return math.sqrt(dx * dx + dy * dy + dz * dz)

    def to_ascii_packet(self) -> str:
        '''
            Formats point as standard firmware protocol packet string.

            :return: ASCII command string.
            :exceptions: None.
        '''
        if abs(self.phi) < 1e-4:
            return f'<pt#{self.x:.2f}#{self.y:.2f}#{self.z:.2f}#{self.speed:.1f}#end>'
        return f'<pt#{self.x:.2f}#{self.y:.2f}#{self.z:.2f}#{self.phi:.2f}#{self.speed:.1f}#end>'

    def to_dict(self) -> dict[str, float | str]:
        '''
            Serializes point to dictionary for JSON persistence.

            :return: Dictionary representation.
            :exceptions: None.
        '''
        return {
            'x': round(self.x, 3),
            'y': round(self.y, 3),
            'z': round(self.z, 3),
            'phi': round(self.phi, 3),
            'speed': round(self.speed, 2),
            'name': self.name
        }

    @classmethod
    def from_dict(cls, data: dict[str, float | str]) -> Waypoint:
        '''
            Deserializes waypoint from dictionary.

            :param data: Input dictionary.
            :return: Waypoint instance.
            :exceptions: None.
        '''
        return cls(
            x=float(data.get('x', 180.0)),
            y=float(data.get('y', 0.0)),
            z=float(data.get('z', 20.0)),
            phi=float(data.get('phi', 0.0)),
            speed=float(data.get('speed', 40.0)),
            name=str(data.get('name', ''))
        )
