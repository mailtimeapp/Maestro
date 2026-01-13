RUN_COUNT=0

while true; do
  RUN_COUNT=$((RUN_COUNT + 1))
  echo "========================================="
  echo "Starting run #${RUN_COUNT} at $(date)"
  echo "========================================="
  
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
  
  kill $PID_RB 2>/dev/null || true
  
  echo "Run #${RUN_COUNT} completed. Waiting 5 seconds before next run..."
  sleep 5
done