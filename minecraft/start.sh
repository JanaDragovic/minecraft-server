#!/bin/sh

echo "eula=true" > eula.txt

JAVA_OPTS="-Xms256M -Xmx256M"

exec java -server $JAVA_OPTS -jar paper-1.20.4-496.jar nogui
