python3 -m venv shra
source ./shra/bin/activate
pip install -r requirements.txt
python child_node_bootstrap.py $1 $2
# python bootstrap.py
deactivate