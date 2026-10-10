# Smart File Organizer v2

A Python-based command-line tool for managing files efficiently. Organize, move, copy, rename, and delete files through an interactive menu.

## Features

### 1. Move Files
- Move files in batches.
- Organize files into folders based on file types.
- Track moved, skipped, failed, and unknown files.

### 2. Copy Files
- Copy files in batches.
- Organize copied files by file type.
- Track copied, skipped, failed, and unknown files.

### 3. Rename Files
- Add prefixes and suffixes.
- Rename files using sequential numbering.
- Find and replace text in filenames.
- Remove specific words from filenames.

### 4. Delete Files
- Delete selected files.
- Delete files by extension.
- Delete files based on size.
- Delete files based on modification date.
- Remove empty folders.
- Detect duplicate files using MD5 hashes.

### 5. Input Validation
- Handle invalid menu input.
- Validate user choices to prevent common input errors.

## Technologies Used

- Python
- `os`
- `shutil`
- `hashlib`
- `datetime`

## Requirements

- Python 3.10 or newer recommended.
- No third-party Python packages required.

## Installation

Clone the repository:

```bash
git clone https://github.com/Najam547/Smart-File-Organizer-v2.git
```

Navigate to the project directory:

```bash
cd Smart-File-Organizer-v2
```

## Usage

Run the program:

```bash
python3 main.py
```

Follow the interactive menu to move, rename, delete, or copy files.

## Project Structure

```text
Smart-File-Organizer-v2/
├── main.py
├── move.py
├── copy_files.py
├── rename.py
├── delete.py
├── .gitignore
└── README.md
```

## Safety Notice

**Be careful when using deletion features.** Deleted files may not be recoverable from the program. Test the tool using sample folders and files before using it on important data.

## Author

GitHub: [Najam547](https://github.com/Najam547)