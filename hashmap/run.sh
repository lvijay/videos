#!/bin/bash

FILENAME=$1

echo 'keyNewline=η
keyMeta=±
----
«±%«⑤η' > record.robo
java -cp ~/other-code/robotonous/bin com.lvijay.robotonous.Main record.robo
osascript activate.scpt &
time -p java -cp ~/other-code/robotonous/bin com.lvijay.robotonous.Main $FILENAME
osascript deactivate.scpt

## run.sh ends here
