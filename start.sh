SCRIPTPATH=$0
TESTSTR=${SCRIPTPATH:0:2}
if [ $TESTSTR = "./" ]; then
        SCRIPTPATH=`pwd`${SCRIPTPATH:1}
fi
DIRPATH=$(dirname "$SCRIPTPATH")
cd $DIRPATH
echo $DIRPATH/.venv/bin/activate
source $DIRPATH/.venv/bin/activate && $DIRPATH/.venv/bin/python $DIRPATH/main.py