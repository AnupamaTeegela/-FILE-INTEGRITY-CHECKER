import hashlib
import os
import json

# Constants
HASH_ALGO = 'sha256'  # You can change to 'md5', 'sha1', etc.
HASHES_FILE = 'file_hashes.json'


def compute_hash(filepath, algorithm='sha256'):
    """Compute hash of a file using the given hashing algorithm."""
    hash_func = hashlib.new(algorithm)
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(8192):
                hash_func.update(chunk)
        return hash_func.hexdigest()
    except FileNotFoundError:
        return None


def save_hashes(directory, hash_file=HASHES_FILE):
    """Generate and save hashes of all files in the directory."""
    file_hashes = {}
    for root, _, files in os.walk(directory):
        for name in files:
            path = os.path.join(root, name)
            rel_path = os.path.relpath(path, directory)
            file_hashes[rel_path] = compute_hash(path, HASH_ALGO)
    
    with open(hash_file, 'w') as f:
        json.dump(file_hashes, f, indent=4)
    print(f"[INFO] Hashes saved to {hash_file}")


def verify_integrity(directory, hash_file=HASHES_FILE):
    """Check if any file has been changed, added, or removed."""
    with open(hash_file, 'r') as f:
        saved_hashes = json.load(f)

    current_hashes = {}
    for root, _, files in os.walk(directory):
        for name in files:
            path = os.path.join(root, name)
            rel_path = os.path.relpath(path, directory)
            current_hashes[rel_path] = compute_hash(path, HASH_ALGO)

    print("\n--- Integrity Check Results ---")
    for path in saved_hashes:
        if path not in current_hashes:
            print(f"[MISSING] {path} has been deleted.")
        elif saved_hashes[path] != current_hashes[path]:
            print(f"[MODIFIED] {path} has been changed.")
    
    for path in current_hashes:
        if path not in saved_hashes:
            print(f"[NEW] {path} is a new file.")


# -------- Main Menu --------
if __name__ == "__main__":
    print("File Integrity Checker - CODTECH Internship Task-01")
    print("1. Save file hashes")
    print("2. Verify file integrity")
    choice = input("Choose an option (1/2): ").strip()

    path = input("Enter file or directory to monitor: ").strip()

    if os.path.isfile(path):
     # For single file
         if choice == '1':
             file_hash = compute_hash(path, HASH_ALGO)
             with open(HASHES_FILE, 'w') as f:
                 json.dump({os.path.basename(path): file_hash}, f, indent=4)
                 print(f"[INFO] Hash saved for file: {path}")
         elif choice == '2':
             with open(HASHES_FILE, 'r') as f:
                 saved = json.load(f)
                 current = compute_hash(path, HASH_ALGO)
                 filename = os.path.basename(path)
                 print("\n--- Integrity Check Results ---")
                 if filename not in saved:
                    print(f"[NEW] {filename} is a new file.")
                 elif saved[filename] != current:
                    print(f"[MODIFIED] {filename} has been changed.")
                 else:
                    print(f"[OK] {filename} is unchanged.")
         else:
            print("Invalid choice.")
    elif os.path.isdir(path):
        if choice == '1':
            save_hashes(path)
        elif choice == '2':
             verify_integrity(path)
        else:
             print("Invalid choice.")
    else:
         print("The path entered does not exist.")
