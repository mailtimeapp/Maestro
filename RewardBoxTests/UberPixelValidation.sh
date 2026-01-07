mkdir -p /tmp/RBValidation

adb logcat -c

adb logcat | grep --line-buffered -E "REWARDBOX_VALIDATION" > /tmp/RBValidation/RBDev.txt &
PID_RB=$!

adb logcat | grep --line-buffered -E "RESEARCHERCONNECT_VALIDATION" > /tmp/RBValidation/RCDev.txt &
PID_RC=$!

sleep 2

echo "--- Starting Maestro Test ---"
~/.maestro/bin/maestro test Pixel/UberCallCarComplete.yaml

sleep 2

echo "--- Running Comparison ---"
python3 compare_logcat.py

kill $PID_RB $PID_RC