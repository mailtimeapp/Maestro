mkdir -p /tmp/RBValidation

adb logcat -c

adb logcat | grep --line-buffered -E "ValidationTracker" > /tmp/RBValidation/RBDev.txt &
PID_RB=$!

sleep 2

echo "--- Starting Maestro Test ---"
~/.maestro/bin/maestro test Pixel/UberCallCarComplete.yaml

sleep 10

echo "--- Running Comparison ---"
python3 parse_logcat.py

kill $PID_RB