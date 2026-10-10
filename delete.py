import os 
import hashlib 
from datetime import datetime
def delete_batch():
    ori_path = os.getcwd()
    path = input("Enter the folder you wanna delete: ")
    delete = 0
    path = os.path.abspath(path)

    if not os.path.isdir(path):
        print("Folder does not exist.")
        return

    os.chdir(path)

    print("1. Delete selected files.")
    print("2. Delete by file type.")
    print("3. Delete by file size.")
    print("4. Delete by age.")
    print("5. Delete empty folders.")
    print("6. Delete duplicate files.")
    print("7. Back to main menu.")

    choice = -1

    while choice < 1 or choice > 7:
        try:
            choice = int(input("What you wanna do: "))
        except ValueError:
            print("Enter a valid integer input.")

    if choice == 1:
        counter = 1
        re_files = []

        print("Available Files:")

        for files in os.listdir(path):
            if os.path.isfile(files):
                file_name = str(counter) + "." + files
                print(file_name)
                re_files.append(files)
                counter += 1

        if not re_files:
            print("No files available.")
            os.chdir(ori_path)
            return

        while True:
            try:
                selected_files = list(
                    map(int, input("Enter the numbers: ").split(","))
                )

                if any(file < 1 or file >= counter for file in selected_files):
                    print("Select numbers from the available files.")
                    continue

                if len(set(selected_files)) != len(selected_files):
                    print("You selected a file number more than once.")
                    continue

                break

            except ValueError:
                print("Enter valid numbers separated by commas.")

        for file in selected_files:
            os.remove(re_files[file - 1])
            delete += 1
            print("File deleted successfully:", re_files[file - 1])

        print("Files deleted:", delete)
        os.chdir(ori_path)

    elif choice == 2:
        extension = input("Enter the extension you wanna delete: ")
        print("Searching for matching files...")

        for files in os.listdir(path):
            if os.path.isfile(files):
                _, ext = os.path.splitext(files)

                if extension == ext:
                    os.remove(files)
                    delete += 1
                    print("File deleted successfully:", files)

        print("Files deleted:", delete)
        os.chdir(ori_path)

    elif choice == 3:
        while True:
            try:
                f_size = int(input("Enter the size in Bytes: "))

                if f_size < 0:
                    print("Size cannot be negative.")
                    continue

                break

            except ValueError:
                print("Enter a valid integer.")

        print("1. Minimum.")
        print("2. Maximum.")

        while True:
            try:
                choic = int(input("Enter your choice: "))

                if choic in (1, 2):
                    break

                print("Select 1 or 2.")

            except ValueError:
                print("Enter a valid integer.")

        for file in os.listdir(path):
            if os.path.isfile(file):
                file_size = os.path.getsize(file)

                if choic == 1 and file_size < f_size:
                    os.remove(file)
                    delete += 1
                    print("File deleted successfully:", file)

                elif choic == 2 and file_size > f_size:
                    os.remove(file)
                    delete += 1
                    print("File deleted successfully:", file)

        print("Files deleted:", delete)
        os.chdir(ori_path)

    elif choice == 4:
        while True:
            date_text = input("Enter date (YYYY-MM-DD): ").strip()

            try:
                date = datetime.strptime(
                    date_text, "%Y-%m-%d"
                ).timestamp()
                break

            except ValueError:
                print("Invalid date. Use YYYY-MM-DD.")

        print("1. Modified before given date.")
        print("2. Modified after given date.")

        while True:
            try:
                choic = int(input("Enter your choice: "))

                if choic in (1, 2):
                    break

                print("Select 1 or 2.")

            except ValueError:
                print("Enter a valid integer.")

        for file in os.listdir(path):
            if os.path.isfile(file):
                modified_time = os.path.getmtime(file)

                if choic == 1 and modified_time < date:
                    os.remove(file)
                    delete += 1
                    print("File deleted successfully:", file)

                elif choic == 2 and modified_time > date:
                    os.remove(file)
                    delete += 1
                    print("File deleted successfully:", file)

        print("Files deleted:", delete)
        os.chdir(ori_path)

    elif choice == 5:
        folders_deleted = 0

        for root, dirs, files in os.walk(path, topdown=False):
            if root == path:
                continue

            try:
                if not os.listdir(root):
                    os.rmdir(root)
                    folders_deleted += 1
                    print("Empty folder deleted:", root)

            except OSError as e:
                print("Cannot remove folder:", e)

        print("Empty folders deleted:", folders_deleted)
        os.chdir(ori_path)

    elif choice == 6:
        hashes = {}

        for files in os.listdir(path):
            if os.path.isfile(files):
                try:
                    with open(files, "rb") as file:
                        data = file.read()

                    hash_value = hashlib.md5(data).hexdigest()

                    if hash_value in hashes:
                        print("Duplicate file found:", files)
                        os.remove(files)
                        delete += 1
                        print("Duplicate file deleted successfully:", files)

                    else:
                        hashes[hash_value] = files

                except OSError as e:
                    print("Cannot process file:", files, e)

        print("Duplicate files deleted:", delete)
        os.chdir(ori_path)

    elif choice == 7:
        os.chdir(ori_path)
        return