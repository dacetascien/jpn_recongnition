SCRIPTPATH=$0
TESTSTR=${SCRIPTPATH:0:2}
if [ $TESTSTR = "./" ]; then
        SCRIPTPATH=`pwd`${SCRIPTPATH:1}
fi
DIRPATH=$(dirname "$SCRIPTPATH")
cd $DIRPATH

python3 -m venv .venv
source .venv/bin/activate
pip install -Ur requirements.txt
cp jpn_recognition.desktop /usr/share/applications
cp -r $DIRPATH /usr/bin/jpn_recognition