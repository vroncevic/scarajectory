# -*- coding: UTF-8 -*-

'''
Module
    dsl_pipeline_builder.py
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
    Builder assembling binary frame codecs and constructing IScaraDslService pipeline.
'''

from __future__ import annotations

from scaralang.core.model.kinematics.transmission_parameters import TransmissionParameters
from scaralang.core.service.dsl.iscara_dsl_service import IScaraDslService
from scaralang.core.service.dsl.scara_dsl_pipeline_bundle import ScaraDslPipelineBundle
from scaralang.core.service.dsl.scara_dsl_service_factory import ScaraDslServiceFactory
from scaralang.core.service.kinematics.ikinematics_service import IKinematicsService
from scaralang.core.service.protocol.ibinary_frame_builder import IBinaryFrameBuilder
from scaralang.core.service.protocol.ibinary_frame_parser import IBinaryFrameParser
from scaralang.core.service.protocol.ibinary_payload_unpacker import IBinaryPayloadUnpacker
from scaralang.core.service.trajectory.validation.itrajectory_validator import ITrajectoryValidator
from scaralang.infrastructure.communication.protocol.binary.builder.binary_frame_builder_factory import BinaryFrameBuilderFactory
from scaralang.infrastructure.communication.protocol.binary.parser.binary_frame_parser_factory import BinaryFrameParserFactory
from scaralang.infrastructure.communication.protocol.binary.parser.binary_payload_unpacker_factory import BinaryPayloadUnpackerFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DslPipelineBuilder:
    '''
        Builder assembling binary frame codecs and constructing IScaraDslService pipeline.

        It defines:

            :methods:
                | build - Assembles DSL pipeline bundle and instantiates ScaraDslService.
    '''

    @classmethod
    def build(
        cls,
        *,
        validator: ITrajectoryValidator,
        kinematics: IKinematicsService,
        transmission: TransmissionParameters,
    ) -> IScaraDslService:
        '''
            Assembles binary codecs, creates pipeline bundle, and returns IScaraDslService.

            :param validator: Injected ITrajectoryValidator instance.
            :param kinematics: Injected IKinematicsService instance.
            :param transmission: Injected TransmissionParameters domain model.
            :return: Fully assembled IScaraDslService instance.
            :exceptions: None.
        '''
        frame_builder: IBinaryFrameBuilder = BinaryFrameBuilderFactory.create()
        frame_parser: IBinaryFrameParser = BinaryFrameParserFactory.create()
        payload_unpacker: IBinaryPayloadUnpacker = (
            BinaryPayloadUnpackerFactory.create()
        )
        dsl_bundle = ScaraDslPipelineBundle(
            validator=validator,
            kinematics=kinematics,
            transmission=transmission,
            frame_builder=frame_builder,
            frame_parser=frame_parser,
            payload_unpacker=payload_unpacker,
        )

        return ScaraDslServiceFactory.create(bundle=dsl_bundle)
