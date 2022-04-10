#!/bin/bash
# _DEBUG="on"
# PS4='LINENO:'

# function DEBUG()
# {
#    [ "$_DEBUG" == "on" ] && $@
# }
# DEBUG echo 'Testing Debudding'
# DEBUG set -x
# a=2
# b=3
# c=$(( $a + $b ))
# DEBUG set +x
# echo "$a + $b = $c"

# activate () {
#   . ./shra/bin/activate
# }

python3 -m venv shra
source ./shra/bin/activate
pip install -r requirements.txt
python bootstrap.py $1
deactivate
