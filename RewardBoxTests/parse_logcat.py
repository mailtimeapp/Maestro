import os
import re

# --- CONFIGURATION ---
RB_LOG_PATH = os.path.expanduser("/tmp/RBValidation/RBDev.txt")

def parse_stats_log(file_path):
    """
    Parses a log file containing Stats lines in the format:
    Stats [Uploaded]: Detected=967, Deduped=928, Ignored=7, Written=32, Uploaded=32 (Diff: 0)
    Returns the LAST entry with [Uploaded] tag.
    """
    last_uploaded_stat = None
    
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return last_uploaded_stat

    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or 'Stats [Uploaded]' not in line:
                    continue
                
                # Parse Stats line using regex
                # Format: Stats [Uploaded]: Detected=X, Deduped=X, Ignored=X, Written=X, Uploaded=X (Diff: X)
                match = re.search(r'Stats \[Uploaded\]:\s*Detected=(\d+),\s*Deduped=(\d+),\s*Ignored=(\d+),\s*Written=(\d+),\s*Uploaded=(\d+)\s*\(Diff:\s*(-?\d+)\)', line)
                
                if match:
                    last_uploaded_stat = {
                        'detected': int(match.group(1)),
                        'deduped': int(match.group(2)),
                        'ignored': int(match.group(3)),
                        'written': int(match.group(4)),
                        'uploaded': int(match.group(5)),
                        'diff': int(match.group(6))
                    }
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

    return last_uploaded_stat

def print_stats(stat):
    """
    Prints the last uploaded stats in a formatted display.
    """
    if not stat:
        print("No [Uploaded] stats data found")
        return
    
    print("\n" + "=" * 70)
    print("LAST UPLOADED STATS")
    print("=" * 70)
    print(f"  Detected:  {stat['detected']}")
    print(f"  Deduped:   {stat['deduped']}")
    print(f"  Ignored:   {stat['ignored']}")
    print(f"  Written:   {stat['written']}")
    print(f"  Uploaded:  {stat['uploaded']}")
    print(f"  Diff:      {stat['diff']}")
    print("=" * 70)

def main():
    print(f"--- Parsing Stats Log from {RB_LOG_PATH} ---")
    last_uploaded = parse_stats_log(RB_LOG_PATH)
    print_stats(last_uploaded)

if __name__ == "__main__":
    main()