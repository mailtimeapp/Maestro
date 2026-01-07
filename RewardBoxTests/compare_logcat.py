import os
import re

# --- CONFIGURATION ---
# Update these paths if your files are located elsewhere
RB_LOG_PATH = os.path.expanduser("/tmp/RBValidation/RBDev.txt")
RC_LOG_PATH = os.path.expanduser("/tmp/RBValidation/RCDev.txt")

def parse_fingerprints(file_path):
    """
    Parses a log file and returns a set of unique fingerprints found.
    Assumes the fingerprint is the last word on the line.
    """
    fingerprints = set()
    
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return fingerprints

    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                # Split the line by whitespace
                parts = line.split()
                
                # The fingerprint is the last element in the line
                if len(parts) > 0:
                    fingerprint = parts[-1]
                    # Basic validation to ensure it looks like a hex string (optional)
                    if len(fingerprint) > 10: 
                        fingerprints.add(fingerprint)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

    return fingerprints

def main():
    print("--- Parsing Logs ---")
    rb_hashes = parse_fingerprints(RB_LOG_PATH)
    rc_hashes = parse_fingerprints(RC_LOG_PATH)

    print(f"Unique fingerprints in RewardBox (RB): {len(rb_hashes)}")
    print(f"Unique fingerprints in ResearcherConnect (RC): {len(rc_hashes)}")

    # Calculate Matches
    # Intersection: Hashes present in BOTH files
    matches = rb_hashes.intersection(rc_hashes)
    num_matches = len(matches)

    # Calculate Missing
    # In RB but NOT in RC
    missing_in_rc = rb_hashes - rc_hashes
    # In RC but NOT in RB
    missing_in_rb = rc_hashes - rb_hashes

    print("\n--- Comparison Results ---")
    print(f"Total Matches: {num_matches}")
    
    # Calculate Match Rate based on RB as the source of truth (usually the standard)
    if len(rb_hashes) > 0:
        match_rate = (num_matches / len(rb_hashes)) * 100
        print(f"Match Rate (RB coverage): {match_rate:.2f}%")
    else:
        print("Match Rate: N/A (No RB logs found)")

    print("-" * 30)
    
    if missing_in_rc:
        print(f"\n[!] {len(missing_in_rc)} fingerprints found in RB but MISSING in RC:")
        for h in list(missing_in_rc)[:5]: # Print first 5 only to avoid spam
            print(f" - {h}")
        if len(missing_in_rc) > 5: print(" ... (and others)")

    if missing_in_rb:
        print(f"\n[!] {len(missing_in_rb)} fingerprints found in RC but MISSING in RB (Unexpected):")
        for h in list(missing_in_rb)[:5]:
            print(f" - {h}")
        if len(missing_in_rb) > 5: print(" ... (and others)")

if __name__ == "__main__":
    main()