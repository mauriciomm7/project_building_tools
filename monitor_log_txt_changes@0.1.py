import time
import os
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, log_file, monitored_folder):
        self.log_file = log_file
        self.monitored_folder = monitored_folder
        self.stop_file = os.path.join(monitored_folder, 'stop_file.txt')
        self.file_contents = {}  # Dictionary to keep track of file contents

    def on_modified(self, event):
        if event.is_directory:
            return

        # Check if the modified file is a .txt file
        if event.src_path.endswith('.txt'):
            # Check if the stop file exists
            if os.path.exists(self.stop_file):
                print(f"Stopping monitoring as {self.stop_file} was detected.")
                return

            # Read the current content of the file
            try:
                with open(event.src_path, 'r', encoding='utf-8') as f:
                    new_content = f.readlines()
            except UnicodeDecodeError as e:
                print(f"Error reading file {event.src_path}: {e}")
                return

            # Compare with previous content and log differences
            old_content = self.file_contents.get(event.src_path, [])
            changes = self.compare_lines(old_content, new_content)
            
            if changes:
                # Log changes to the log file
                with open(self.log_file, 'a', encoding='utf-8') as log:
                    log.write(f"\nModified file: {event.src_path} at {time.ctime()}\n")
                    
                    # Dictionary to track all replacements
                    replacement_code = {}
                    
                    for line_number, old_line, new_line in changes:
                        log.write(f"Line {line_number}: Old: {old_line.strip()} | New: {new_line.strip()}\n")
                        
                        # Track replacements
                        if old_line.strip() and new_line.strip() and old_line.strip() != new_line.strip():
                            old_text = old_line.strip()
                            new_text = new_line.strip()
                            if old_text not in replacement_code:
                                replacement_code[old_text] = new_text

                    # Log the replacement code
                    for old_text, new_text in replacement_code.items():
                        replace_code = f'str.replace("{old_text}", "{new_text}")'
                        log.write(f"Replacement code: {replace_code}\n")

            # Update the stored content
            self.file_contents[event.src_path] = new_content

    def compare_lines(self, old_lines, new_lines):
        changes = []
        max_len = max(len(old_lines), len(new_lines))
        
        for i in range(max_len):
            old_line = old_lines[i] if i < len(old_lines) else ''
            new_line = new_lines[i] if i < len(new_lines) else ''
            
            if old_line != new_line:
                # Record the change, including the code for replacement
                changes.append((i + 1, old_line, new_line))
        
        return changes

if __name__ == "__main__":
    # Check if the correct number of arguments are provided
    if len(sys.argv) != 3:
        print("Usage: python monitor_files.py <folder_to_watch> <log_file>")
        sys.exit(1)

    folder_to_watch = sys.argv[1]  # Folder path provided by the user
    log_file = sys.argv[2]         # Log file path provided by the user

    # Check if the folder exists
    if not os.path.isdir(folder_to_watch):
        print(f"The folder {folder_to_watch} does not exist.")
        sys.exit(1)

    event_handler = FileChangeHandler(log_file, folder_to_watch)
    observer = Observer()
    observer.schedule(event_handler, path=folder_to_watch, recursive=False)
    observer.start()

    print(f"Monitoring changes in {folder_to_watch}. Logging to {log_file}")
    print(f"To stop monitoring, create a file named 'stop_file.txt' in the monitored folder.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
