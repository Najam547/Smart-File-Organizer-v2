import os
import shutil


def move_batch():
    moved = 0
    skipped = 0
    failed = 0
    unknown = 0

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

    try:
        if not os.listdir(source):
            print("Folder is empty.")
            return
    except OSError as e:
        print("Cannot access source folder:", e)
        return

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
        print("Invalid source or destination path:", e)
        return

    if common_path == source:
        print("Destination cannot be the same as or inside source.")
        return

    try:
        os.makedirs(destination, exist_ok=True)
    except OSError as e:
        print("Cannot create destination folder:", e)
        return

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

    def handle_walk_error(error):
        nonlocal failed
        failed += 1
        print("Cannot access folder:", error.filename, "|", error)

    for root, _, files in os.walk(
        source,
        onerror=handle_walk_error,
        followlinks=False
    ):
        for file_name in files:
            file_path = os.path.join(root, file_name)

            if os.path.islink(file_path):
                skipped += 1
                print("Symbolic link skipped:", file_name)
                continue

            _, extension = os.path.splitext(file_name)
            extension = extension.lower()
            category = rules.get(extension)

            if category is None:
                unknown += 1
                continue

            if not os.path.isfile(file_path):
                skipped += 1
                print("Not a regular file. Skipping:", file_name)
                continue

            try:
                file_size = os.path.getsize(file_path)
            except OSError as e:
                failed += 1
                print("Cannot read file size:", file_path, "|", e)
                continue

            print("\nFile:", file_name)
            print("Size:", file_size, "bytes")
            print("Type:", extension)

            moved, skipped, failed = move_file(
                file_path,
                os.path.join(destination, category),
                moved,
                skipped,
                failed
            )

    print("\n========== MOVE REPORT ==========")
    print("Files moved:", moved)
    print("Files skipped:", skipped)
    print("Files failed:", failed)
    print("Unknown files:", unknown)
    print("=================================")


def move_file(source_file, destination_folder, moved, skipped, failed):
    file_name = os.path.basename(source_file)
    destination_file = os.path.join(destination_folder, file_name)

    try:
        os.makedirs(destination_folder, exist_ok=True)

        if os.path.lexists(destination_file):
            print("File already exists. Skipping:", file_name)
            skipped += 1
            return moved, skipped, failed

        shutil.move(source_file, destination_folder)
        print("File successfully moved:", file_name)
        moved += 1

    except FileNotFoundError as e:
        failed += 1
        print("File or folder not found:", e)

    except PermissionError as e:
        failed += 1
        print("Permission denied:", e)

    except OSError as e:
        failed += 1
        print("Move failed:", e)

    return moved, skipped, failed