import os
import re
import json
import urllib.request
import urllib.error
from datetime import datetime

# --- CONFIGURATION ---
RB_LOG_PATH = os.path.expanduser("/tmp/RBValidation/RBDev.txt")
SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL", "")

def parse_stats_log(file_path):
    """
    Parses a log file containing Stats lines in the format:
    Stats [Uploaded]: Detected=967, Deduped=928, Ignored=7, Written=32, Uploaded=32 (Unaccounted: 0, Active: 5)
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
                # Format: Stats [Uploaded]: Detected=X, Deduped=X, Ignored=X, Written=X, Uploaded=X (Unaccounted: X, Active: X)
                match = re.search(r'Stats \[Uploaded\]:\s*Detected=(\d+),\s*Deduped=(\d+),\s*Ignored=(\d+),\s*Written=(\d+),\s*Uploaded=(\d+)\s*\(Unaccounted:\s*(-?\d+),\s*Active:\s*(-?\d+)\)', line)
                
                if match:
                    last_uploaded_stat = {
                        'detected': int(match.group(1)),
                        'deduped': int(match.group(2)),
                        'ignored': int(match.group(3)),
                        'written': int(match.group(4)),
                        'uploaded': int(match.group(5)),
                        'unaccounted': int(match.group(6)),
                        'active': int(match.group(7))
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
    print(f"  Detected:     {stat['detected']}")
    print(f"  Deduped:      {stat['deduped']}")
    print(f"  Ignored:      {stat['ignored']}")
    print(f"  Written:      {stat['written']}")
    print(f"  Uploaded:     {stat['uploaded']}")
    print(f"  Unaccounted:  {stat['unaccounted']}")
    print(f"  Active:       {stat['active']}")
    print("=" * 70)

def send_to_slack(stat, webhook_url):
    """
    Sends stats to Slack using a webhook with formatted message blocks.
    """
    if not webhook_url:
        print("⚠️  SLACK_WEBHOOK_URL not set. Skipping Slack notification.")
        return False
    
    if not stat:
        payload = {
            "text": "❌ RewardBox Validation Failed",
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "❌ RewardBox Validation Failed"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "No [Uploaded] stats data found in the log file."
                    }
                }
            ]
        }
    else:
        # Determine status emoji based on metrics
        status_emoji = "✅" if stat['unaccounted'] == 0 and stat['uploaded'] > 0 else "⚠️"
        
        payload = {
            "text": f"{status_emoji} RewardBox Validation Stats",
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"{status_emoji} RewardBox Validation Stats"
                    }
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f"*Detected:*\n{stat['detected']}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Deduped:*\n{stat['deduped']}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Ignored:*\n{stat['ignored']}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Written:*\n{stat['written']}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Uploaded:*\n{stat['uploaded']}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Unaccounted:*\n{stat['unaccounted']}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Active:*\n{stat['active']}"
                        }
                    ]
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "mrkdwn",
                            "text": f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                        }
                    ]
                }
            ]
        }
    
    try:
        request = urllib.request.Request(
            webhook_url,
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(request) as response:
            if response.status == 200:
                print("✅ Stats sent to Slack successfully!")
                return True
            else:
                print(f"⚠️  Slack webhook returned status {response.status}")
                return False
    except urllib.error.URLError as e:
        print(f"❌ Failed to send to Slack: {e}")
        return False
    except Exception as e:
        print(f"❌ Error sending to Slack: {e}")
        return False

def main():
    print(f"--- Parsing Stats Log from {RB_LOG_PATH} ---")
    last_uploaded = parse_stats_log(RB_LOG_PATH)
    print_stats(last_uploaded)
    
    # Send to Slack if webhook URL is configured
    if SLACK_WEBHOOK_URL:
        send_to_slack(last_uploaded, SLACK_WEBHOOK_URL)

if __name__ == "__main__":
    main()