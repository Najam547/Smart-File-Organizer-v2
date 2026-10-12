import os
import shutil


def copy_batch():
    copied = 0
    skipped = 0
    failed = 0
    unknown = 0

    # FIX 1: Source path validation
    source_input = input("Enter your source path: ").strip()

    if not source_input:
        print("Source path cannot be empty.")
        return

    source = os.path.realpath(
        os.path.abspath(os.path.expanduser(source_input))
    )

    if not os.path.isdir(source):
        print("Source folder does not exist.")
        return

    # FIX 2: Handle source folder access errors
    try:
        if not os.listdir(source):
            print("Folder is empty.")
            return
    except OSError as e:
        print("Cannot access source folder:", e)
        return

    # FIX 3: Destination path validation
    destination_input = input("Enter your destination path: ").strip()

    if not destination_input:
        print("Destination path cannot be empty.")
        return

    destination = os.path.realpath(
        os.path.abspath(os.path.expanduser(destination_input))
    )

    try:
        common_path = os.path.commonpath([source, destination])
    except ValueError as e:
        print("Invalid source/destination paths:", e)
        return

    if common_path == source:
        print("Destination cannot be the same as or inside source.")
        return

    # FIX 4: Destination creation error handling
    try:
        os.makedirs(destination, exist_ok=True)
    except OSError as e:
        print("Cannot create destination folder:", e)
        return

    # File classification rules
    rules = {
        ".pdf": "PDF",
        ".txt": "Documents",
        ".doc": "Documents",
        ".docx": "Documents",
        ".xls": "Excel",
        ".xlsx": "Excel",
        ".jpeg": "Images",
        ".png": "Images",
        ".jpg": "Images",
        ".mp4": "Videos",
        ".webm": "Videos",
        ".py": "Python",
        ".pptx": "Ppt",
        ".java": "Java"
    }

    # FIX 5: Handle errors while traversing source folders
    def handle_walk_error(error):
        nonlocal failed

        failed += 1
        print(
            "Cannot access folder:",
            error.filename,
            "| Error:",
            error
        )

    for root, _, files in os.walk(
        source,
        onerror=handle_walk_error,
        followlinks=False
    ):
        for file_name in files:

            file_path = os.path.join(root, file_name)

            # FIX 6: Skip symbolic links
            if os.path.islink(file_path):
                skipped += 1
                print("Symbolic link skipped:", file_name)
                continue

            # FIX 7: Check file extension
            _, extension = os.path.splitext(file_name)
            extension = extension.lower()

            category = rules.get(extension)

            if category is None:
                unknown += 1
                continue

            # FIX 8: Skip non-regular files
            if not os.path.isfile(file_path):
                skipped += 1
                print("Not a regular file. Skipping:", file_name)
                continue

            # FIX 9: Handle file size errors
            try:
                file_size = os.path.getsize(file_path)
            except OSError as e:
                failed += 1
                print("Cannot read file size:", file_path, "|", e)
                continue

            print("\nFile:", file_name)
            print("Size:", file_size, "bytes")
            print("Type:", extension)

            # FIX 10: Copy file and update counters
            copied, skipped, failed = copy_file(
                file_path,
                os.path.join(destination, category),
                copied,
                skipped,
                failed
            )

    # Final report
    print("\n========== COPY REPORT ==========")
    print("Files copied:", copied)
    print("Files skipped:", skipped)
    print("Files failed:", failed)
    print("Unknown files:", unknown)
    print("=================================")


def remove_partial_file(file_path):
    """
    Remove an incomplete destination file after a failed copy.
    """
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.remove(file_path)

    except OSError as e:
        print("Could not remove incomplete file:", e)


def copy_file(source_file, destination_folder, copied, skipped, failed):

    file_name = os.path.basename(source_file)
    destination_file = os.path.join(destination_folder, file_name)

    copy_started = False

    try:
        os.makedirs(destination_folder, exist_ok=True)

        # FIX 11: Detect existing destination entries
        if os.path.lexists(destination_file):
            print("File already exists. Skipping:", file_name)
            skipped += 1
            return copied, skipped, failed

        # FIX 12: Copy file and handle partial failures
        copy_started = True

        shutil.copy2(source_file, destination_file)

        print("File successfully copied:", file_name)
        copied += 1

    except FileNotFoundError as e:
        if copy_started:
            remove_partial_file(destination_file)

        failed += 1
        print("File or folder not found:", e)

    except PermissionError as e:
        if copy_started:
            remove_partial_file(destination_file)

        failed += 1
        print("Permission denied:", e)

    except OSError as e:
        if copy_started:
            remove_partial_file(destination_file)

        failed += 1
        print("Copy failed:", e)

    return copied, skipped, failed