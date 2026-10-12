import os
import hashlib
from datetime import datetime

def confirm_delete():
    answer = input("Type DELETE to confirm deletion: ").strip()
    return answer.upper() == "DELETE"

def get_files(path):
    try:
        files = []

        with os.scandir(path) as entries:
            for entry in entries:
                try:
                    if entry.is_file(follow_symlinks=False):
                        files.append(entry.path)

                except OSError as e:
                    print("Cannot inspect entry:", entry.path, e)

        return sorted(
            files,
            key=lambda file: os.path.basename(file).casefold()
        )

    except OSError as e:
        print("Cannot access folder:", e)
      
def remove_files(files):
    deleted = 0
    failed = 0

    for file in files:
        try:
            os.remove(file)
            deleted += 1
            print("File deleted successfully:", file)

        except FileNotFoundError:
            failed += 1
            print("File no longer exists:", file)

        except PermissionError:
            failed += 1
            print("Permission denied:", file)

        except OSError as e:
            failed += 1
            print("Could not delete:", file, "|", e)

    print("\nFiles deleted:", deleted)
    print("Files failed:", failed)

def delete_selected_files(files):

    if not files:
        print("No matching files found.")
        return

    print("\nFiles selected for deletion:")

    for number, file in enumerate(files, start=1):
        print(f"{number}. {file}")

    print("\nTotal files to delete:", len(files))

    if not confirm_delete():
        print("Deletion cancelled.")
        return

    remove_files(files)

def delete_batch():

    path_input = input(
        "Enter the folder you want to delete files from: "
    ).strip()

    if not path_input:
        print("Folder path cannot be empty.")
        return

    path = os.path.realpath(
        os.path.abspath(os.path.expanduser(path_input))
    )

    if not os.path.isdir(path):
        print("Folder does not exist.")
        return

    # Prevent accidental operations on filesystem root
    # or the user's home directory itself.

    home_path = os.path.realpath(os.path.expanduser("~"))

    if os.path.dirname(path) == path or path == home_path:
        print("Operation refused for this protected folder.")
        return

    print("\n========== DELETE MENU ==========")
    print("1. Delete selected files.")
    print("2. Delete by file type.")
    print("3. Delete by file size.")
    print("4. Delete by modification date.")
    print("5. Delete empty folders.")
    print("6. Delete duplicate files.")
    print("7. Back to main menu.")

    while True:
        try:
            choice = int(input("Enter your choice: "))

            if 1 <= choice <= 7:
                break

            print("Select a number between 1 and 7.")

        except ValueError:
            print("Enter a valid integer.")

    if choice == 7:
        return

    if choice == 1:

        files = get_files(path)

        if files is None:
            return

        if not files:
            print("No files available.")
            return

        print("\nAvailable files:")

        for number, file in enumerate(files, start=1):
            print(f"{number}. {os.path.basename(file)}")

        # FIX 8: Validate selected file numbers

        while True:
            try:
                entered = input(
                    "Enter file numbers separated by commas: "
                ).strip()

                if not entered:
                    print("Select at least one file.")
                    continue

                selected_numbers = [
                    int(number.strip())
                    for number in entered.split(",")
                ]

                if any(
                    number < 1 or number > len(files)
                    for number in selected_numbers
                ):
                    print("Select numbers from the available files.")
                    continue

                if len(set(selected_numbers)) != len(selected_numbers):
                    print("Duplicate file numbers are not allowed.")
                    continue

                break

            except ValueError:
                print("Enter valid numbers separated by commas.")

        selected_files = [
            files[number - 1]
            for number in selected_numbers
        ]

        delete_selected_files(selected_files)

    elif choice == 2:

        extension = input(
            "Enter the extension you want to delete (e.g. .pdf): "
        ).strip().lower()

        if not extension or extension == ".":
            print("Extension cannot be empty.")
            return

        if "/" in extension or "\\" in extension:
            print("Enter a file extension, not a path.")
            return

        if not extension.startswith("."):
            extension = "." + extension

        files = get_files(path)

        if files is None:
            return

        matching_files = []

        for file in files:
            _, file_extension = os.path.splitext(file)

            if file_extension.lower() == extension:
                matching_files.append(file)

        delete_selected_files(matching_files)

    elif choice == 3:

        while True:
            try:
                file_size_limit = int(
                    input("Enter the size limit in bytes: ")
                )

                if file_size_limit < 0:
                    print("Size cannot be negative.")
                    continue

                break

            except ValueError:
                print("Enter a valid integer.")

        print("\n1. Files smaller than the given size.")
        print("2. Files larger than the given size.")

        while True:
            try:
                size_choice = int(input("Enter your choice: "))

                if size_choice in (1, 2):
                    break

                print("Select 1 or 2.")

            except ValueError:
                print("Enter a valid integer.")

        files = get_files(path)

        if files is None:
            return

        matching_files = []

        for file in files:

            try:
                current_size = os.path.getsize(file)

            except OSError as e:
                print("Cannot read file size:", file, "|", e)
                continue

            if (
                size_choice == 1
                and current_size < file_size_limit
            ):
                matching_files.append(file)

            elif (
                size_choice == 2
                and current_size > file_size_limit
            ):
                matching_files.append(file)

        delete_selected_files(matching_files)

    elif choice == 4:

        while True:
            date_text = input(
                "Enter date (YYYY-MM-DD): "
            ).strip()

            try:
                target_date = datetime.strptime(
                    date_text, "%Y-%m-%d"
                ).date()

                break

            except ValueError:
                print("Invalid date. Use YYYY-MM-DD.")

        print("\n1. Files modified before the given date.")
        print("2. Files modified after the given date.")

        while True:
            try:
                date_choice = int(input("Enter your choice: "))

                if date_choice in (1, 2):
                    break

                print("Select 1 or 2.")

            except ValueError:
                print("Enter a valid integer.")

        files = get_files(path)

        if files is None:
            return

        matching_files = []

        for file in files:

            try:
                modified_date = datetime.fromtimestamp(
                    os.path.getmtime(file)
                ).date()

            except (OSError, OverflowError, ValueError) as e:
                print(
                    "Cannot read modification date:",
                    file,
                    "|",
                    e
                )
                continue

            if (
                date_choice == 1
                and modified_date < target_date
            ):
                matching_files.append(file)

            elif (
                date_choice == 2
                and modified_date > target_date
            ):
                matching_files.append(file)

        delete_selected_files(matching_files)

    elif choice == 5:

        empty_folders = []
        empty_folder_set = set()

        def handle_walk_error(error):
            print("Cannot access folder:", error)

        try:
            for root, dirs, files in os.walk(
                path,
                topdown=False,
                onerror=handle_walk_error,
                followlinks=False
            ):

                # Never delete the selected root folder itself.
                if root == path:
                    continue

                child_paths = [
                    os.path.join(root, directory)
                    for directory in dirs
                ]

                if (
                    not files
                    and all(
                        child in empty_folder_set
                        for child in child_paths
                    )
                ):
                    empty_folders.append(root)
                    empty_folder_set.add(root)

        except OSError as e:
            print("Folder traversal failed:", e)
            return

        if not empty_folders:
            print("No empty folders found.")
            return

        print("\nEmpty folders selected for deletion:")

        for number, folder in enumerate(
            empty_folders, start=1
        ):
            print(f"{number}. {folder}")

        print("\nTotal empty folders:", len(empty_folders))

        if not confirm_delete():
            print("Deletion cancelled.")
            return

        folders_deleted = 0
        folders_failed = 0

        for folder in empty_folders:
            try:
                os.rmdir(folder)
                folders_deleted += 1
                print("Empty folder deleted:", folder)

            except FileNotFoundError:
                folders_failed += 1
                print("Folder no longer exists:", folder)

            except PermissionError:
                folders_failed += 1
                print("Permission denied:", folder)

            except OSError as e:
                folders_failed += 1
                print("Cannot remove folder:", folder, "|", e)

        print("\nEmpty folders deleted:", folders_deleted)
        print("Empty folders failed:", folders_failed)

    elif choice == 6:

        files = get_files(path)

        if files is None:
            return

        hashes = {}
        duplicate_pairs = []

        for file in files:

            try:
                hasher = hashlib.sha256()

                with open(file, "rb") as current_file:

                    for chunk in iter(
                        lambda: current_file.read(1024 * 1024),
                        b""
                    ):
                        hasher.update(chunk)

                hash_value = hasher.hexdigest()

            except OSError as e:
                print("Cannot process file:", file, "|", e)
                continue

            if hash_value in hashes:

                original_file = hashes[hash_value]

                duplicate_pairs.append(
                    (file, original_file)
                )

            else:
                hashes[hash_value] = file

        if not duplicate_pairs:
            print("No duplicate files found.")
            return

        duplicate_files = [
            duplicate
            for duplicate, original in duplicate_pairs
        ]



        print("\nDuplicate files selected for deletion:")

        for number, (duplicate, original) in enumerate(
            duplicate_pairs, start=1
        ):
            print(f"\n{number}. Delete: {duplicate}")
            print(f"   Keep:   {original}")

        print(
            "\nTotal duplicate files to delete:",
            len(duplicate_files)
        )

        if not confirm_delete():
            print("Deletion cancelled.")
            return

        remove_files(duplicate_files)