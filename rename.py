import os
import uuid


def get_batch_files(batch):
    try:
        files = []

        with os.scandir(batch) as entries:
            for entry in entries:
                try:
                    if entry.is_file(follow_symlinks=False):
                        files.append(entry.path)
                except OSError as e:
                    print("Cannot inspect file:", entry.path, e)

        return sorted(
            files,
            key=lambda file: os.path.basename(file).casefold()
        )

    except OSError as e:
        print("Cannot access folder:", e)
        return None


def valid_fragment(value, allow_empty=False):
    if not allow_empty and not value:
        print("Input cannot be empty.")
        return False

    separators = [os.sep, "\\", "\x00"]

    if os.altsep:
        separators.append(os.altsep)

    if any(separator in value for separator in separators):
        print("Filename input cannot contain path separators.")
        return False

    return True


def apply_rename_plan(plan):
    effective_plan = []

    for source, destination in plan:
        source = os.path.abspath(source)
        destination = os.path.abspath(destination)

        if source != destination:
            effective_plan.append((source, destination))

    if not effective_plan:
        print("No files need renaming.")
        return

    source_paths = {
        source for source, destination in effective_plan
    }

    target_paths = [
        destination for source, destination in effective_plan
    ]

    if len(set(target_paths)) != len(target_paths):
        print("Collision error: Multiple files have the same target name.")
        return

    for source, destination in effective_plan:
        if (
            os.path.lexists(destination)
            and destination not in source_paths
        ):
            print(
                "Collision error. Destination already exists:",
                os.path.basename(destination)
            )
            return

    staged = []

    for source, destination in effective_plan:
        directory = os.path.dirname(source)

        while True:
            temporary = os.path.join(
                directory,
                ".__rename_tmp_" + uuid.uuid4().hex
            )

            if (
                not os.path.lexists(temporary)
                and temporary not in target_paths
            ):
                break

        try:
            os.rename(source, temporary)
            staged.append((source, temporary, destination))

        except OSError as e:
            print(
                "Cannot prepare rename:",
                os.path.basename(source),
                "|",
                e
            )

            for original, temp, target in reversed(staged):
                try:
                    os.rename(temp, original)
                except OSError as rollback_error:
                    print(
                        "Could not restore:",
                        original,
                        "|",
                        rollback_error
                    )

            return

    completed = []

    for source, temporary, destination in staged:
        try:
            os.rename(temporary, destination)
            completed.append((source, temporary, destination))

        except OSError as e:
            print(
                "Cannot finish rename:",
                os.path.basename(source),
                "|",
                e
            )

            for original, temp, target in reversed(completed):
                try:
                    os.rename(target, temp)
                except OSError as rollback_error:
                    print(
                        "Could not roll back:",
                        target,
                        "|",
                        rollback_error
                    )

            for original, temp, target in reversed(staged):
                if os.path.lexists(temp):
                    try:
                        os.rename(temp, original)
                    except OSError as rollback_error:
                        print(
                            "Could not restore:",
                            original,
                            "|",
                            rollback_error
                        )

            return

    for source, temporary, destination in staged:
        print(
            "Renamed:",
            os.path.basename(source),
            "->",
            os.path.basename(destination)
        )

    print("\nFiles renamed successfully:", len(staged))


def rename_batch():
    batch_input = input(
        "Enter the folder containing files to rename: "
    ).strip()

    if not batch_input:
        print("Folder path cannot be empty.")
        return

    batch = os.path.realpath(
        os.path.abspath(os.path.expanduser(batch_input))
    )

    if not os.path.isdir(batch):
        print("Invalid folder path.")
        return

    files = get_batch_files(batch)

    if files is None:
        return

    if not files:
        print("No files available.")
        return

    print("\n========== RENAME MENU ==========")
    print("1. Prefix.")
    print("2. Suffix.")
    print("3. Sequential numbering.")
    print("4. Find and replace.")
    print("5. Back to main menu.")

    while True:
        try:
            choice = int(input("Enter your preference: "))

            if 1 <= choice <= 5:
                break

            print("Select a number between 1 and 5.")

        except ValueError:
            print("Enter a valid integer.")

    if choice == 5:
        return

    plan = []

    if choice == 1:
        prefix = input("Enter the prefix: ").strip()

        if not valid_fragment(prefix):
            return

        for file in files:
            file_name = os.path.basename(file)
            new_name = prefix + "_" + file_name
            plan.append((file, os.path.join(batch, new_name)))

    elif choice == 2:
        suffix = input("Enter the suffix: ").strip()

        if not valid_fragment(suffix):
            return

        for file in files:
            file_name = os.path.basename(file)
            base, extension = os.path.splitext(file_name)
            new_name = base + "_" + suffix + extension
            plan.append((file, os.path.join(batch, new_name)))

    elif choice == 3:
        print("\n1. Replace original names.")
        print("2. Add numbers to original names.")

        while True:
            try:
                numbering_choice = int(input("Enter your choice: "))

                if numbering_choice in (1, 2):
                    break

                print("Select 1 or 2.")

            except ValueError:
                print("Enter a valid integer.")

        if numbering_choice == 1:
            for counter, file in enumerate(files):
                file_name = os.path.basename(file)
                _, extension = os.path.splitext(file_name)
                new_name = f"{counter:03d}{extension}"
                plan.append((file, os.path.join(batch, new_name)))

        elif numbering_choice == 2:
            print("\n1. Number at the beginning.")
            print("2. Number at the end.")

            while True:
                try:
                    position_choice = int(input("Enter your choice: "))

                    if position_choice in (1, 2):
                        break

                    print("Select 1 or 2.")

                except ValueError:
                    print("Enter a valid integer.")

            for counter, file in enumerate(files, start=1):
                file_name = os.path.basename(file)
                base, extension = os.path.splitext(file_name)

                if position_choice == 1:
                    new_name = f"{counter:03d}_{file_name}"
                else:
                    new_name = f"{base}_{counter:03d}{extension}"

                plan.append((file, os.path.join(batch, new_name)))

    elif choice == 4:
        print("\n1. Replace word.")
        print("2. Remove word.")

        while True:
            try:
                replace_choice = int(input("Enter your choice: "))

                if replace_choice in (1, 2):
                    break

                print("Select 1 or 2.")

            except ValueError:
                print("Enter a valid integer.")

        search_text = input("Enter the text you want to find: ").strip()

        if not search_text:
            print("Find text cannot be empty.")
            return

        if not valid_fragment(search_text):
            return

        if replace_choice == 1:
            replacement = input("Enter the replacement text: ").strip()
        else:
            replacement = ""

        if not valid_fragment(replacement, allow_empty=True):
            return

        for file in files:
            file_name = os.path.basename(file)
            base, extension = os.path.splitext(file_name)

            if search_text not in base:
                continue

            new_base = base.replace(search_text, replacement)
            new_name = new_base + extension
            plan.append((file, os.path.join(batch, new_name)))

        if not plan:
            print("No matching filenames found.")
            return

    apply_rename_plan(plan)