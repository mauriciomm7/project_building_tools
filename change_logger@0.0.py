import os
import pickle
import difflib

def log_changes(dir_path, log_path, snapshot):
    # Implement change logging
    new_snapshot = {f: os.path.join(dir_path, f) for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))}
    changes = {}

    for file, filepath in new_snapshot.items():
        if file not in snapshot:
            changes[file] = 'New file added'
        else:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    new_content = f.readlines()
            except UnicodeDecodeError:
                with open(filepath, 'r', encoding='latin-1') as f:
                    new_content = f.readlines()

            try:
                with open(snapshot[file], 'r', encoding='utf-8') as f:
                    old_content = f.readlines()
            except UnicodeDecodeError:
                with open(snapshot[file], 'r', encoding='latin-1') as f:
                    old_content = f.readlines()

            diffs = list(difflib.unified_diff(old_content, new_content, lineterm=''))
            if diffs:
                changes[file] = diffs

    with open(log_path, 'w', encoding='utf-8') as log_file:
        for file, changes in changes.items():
            log_file.write(f"Changes for {file}:\n")
            log_file.writelines(changes)
            log_file.write("\n")

    return new_snapshot

def initialize_snapshot(dir_path, snapshot_path):
    snapshot = {}
    for file in os.listdir(dir_path):
        filepath = os.path.join(dir_path, file)
        if os.path.isfile(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    snapshot[file] = f.read()
            except UnicodeDecodeError:
                with open(filepath, 'r', encoding='latin-1') as f:
                    snapshot[file] = f.read()

    with open(snapshot_path, 'wb') as f:
        pickle.dump(snapshot, f)

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Log changes to text files.")
    parser.add_argument('dir_path', type=str, help="Directory of text files")
    parser.add_argument('log_path', type=str, help="Path to log file")
    parser.add_argument('snapshot_path', type=str, help="Path to previous snapshot")

    args = parser.parse_args()

    if os.path.isfile(args.snapshot_path):
        with open(args.snapshot_path, 'rb') as f:
            prev_snapshot = pickle.load(f)
    else:
        initialize_snapshot(args.dir_path, args.snapshot_path)
        prev_snapshot = {}

    new_snapshot = log_changes(args.dir_path, args.log_path, prev_snapshot)

    with open(args.snapshot_path, 'wb') as f:
        pickle.dump(new_snapshot, f)

if __name__ == "__main__":
    main()
