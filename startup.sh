
BASEDIR=$(dirname "$0")
DIR="$BASEDIR/venv"

if [ -d "$DIR" ]; then
    echo "Environment found"
else
    echo "Creating virtualenvit=ronment ..."
    CURDIR=$PWD
    cd $BASEDIR
    python3 -m venv venv
    cd $CURDIR
fi

echo "Activate venv"
source "$BASEDIR/venv/bin/activate"

echo "Installing reqirements..."
pip install -r "$BASEDIR/requirements.txt"

echo "Running bot..."
python "$BASEDIR/src/main.py"
