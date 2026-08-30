#!/bin/bash
#
# @brief   scarajectory
# @version 1.0.0
# @date    Sun Aug 30 07:15:00 2026
# @company None, free software to use 2026
# @author  Vladimir Roncevic <elektron.ronca@gmail.com>
#

python3 gates/gates/interfaces_checker.py scarajectory
python3 gates/gates/isp_checker.py scarajectory
python3 gates/gates/limits_checker.py scarajectory
python3 gates/gates/srp_checker.py scarajectory

echo "Done"
