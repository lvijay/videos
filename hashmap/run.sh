#!/bin/bash

FILENAME=$1

echo 'keyNewline=η
keyMeta=±
----
«±%«⑤η' > record.robo
java -cp ~/other-code/robotonous/bin com.lvijay.robotonous.Main -audio mock record.robo
osascript activate.scpt &
time -p java -cp ~/other-code/robotonous/bin com.lvijay.robotonous.Main -audio festival $FILENAME
osascript deactivate.scpt

## run.sh ends here
