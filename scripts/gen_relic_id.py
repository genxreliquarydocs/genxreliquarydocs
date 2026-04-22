import hashlib
import sys
import os

# Source of Truth path
RELICS_FILE = "data/relics.txt"

def get_relic_id(name):
    """Core SHA-1 logic for the ARD-7."""
    name_norm = name.lower().strip()
    sha1_hex = hashlib.sha1(name_norm.encode()).hexdigest()
    # Extract last 4 hex digits -> decimal
    decimal_id = int(sha1_hex[-4:], 16)
    return f"{decimal_id:05d}"

def analyze_registry(target_name, target_id):
    """
    Scans the existing source file for both exact name matches 
    and mathematical ID collisions.
    """
    if not os.path.exists(RELICS_FILE):
        return None, None

    with open(RELICS_FILE, "r") as f:
        for line in f:
            existing_name = line.strip().lower()
            if not existing_name:
                continue
            
            # Check 1: Exact Name Match
            if existing_name == target_name:
                return "NAME_EXISTS", existing_name
            
            # Check 2: Hash Collision (Different name, same ID)
            if get_relic_id(existing_name) == target_id:
                return "HASH_COLLISION", existing_name
                
    return None, None

def main():
    if len(sys.argv) < 2:
        print("Usage: python gen_relic_id.py [relic name]")
        return

    target_name = " ".join(sys.argv[1:]).lower().strip()
    target_id = get_relic_id(target_name)

    print(f"--- ARD-7 ID GENERATOR ---")
    print(f"Relic Name: {target_name}")
    print(f"Proposed ID: {target_id}")

    # Integrity Check
    issue_type, conflict_name = analyze_registry(target_name, target_id)
    
    if issue_type == "NAME_EXISTS":
        print(f"\n[!] DATA INTEGRITY ALERT: DUPLICATE ENTRY")
        print(f"The name '{conflict_name}' is already present in {RELICS_FILE}.")
        print(f"Status: No action taken. Use existing ID {target_id} for this relic.")

    elif issue_type == "HASH_COLLISION":
        print(f"\n[!] CRITICAL ALERT: ID COLLISION")
        print(f"Conflict: '{target_name}' and '{conflict_name}' both resolve to ID {target_id}.")
        print(f"Action: Modify the canonical name for '{target_name}' to resolve the hash conflict.")

    else:
        print(f"\nStatus: ID {target_id} is unique and valid.")
        print(f"Recommendation: Append '{target_name}' to {RELICS_FILE} and proceed.")

if __name__ == "__main__":
    main()
