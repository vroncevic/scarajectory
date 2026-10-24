#!/bin/bash
#
# @brief   scarajectory
# @version 1.0.3
# @date    Sun Aug 30 07:15:00 2026
# @company None, free software to use 2026
# @author  Vladimir Roncevic <elektron.ronca@gmail.com>
#

python3 coverage/ats_coverage.py scarajectory
pylint scarajectory > scarajectory.report
echo "Done"
