import move
import delete
import rename
import copy_files


def main():
    print("Welcome to File Organizer.")

    while True:
        print("\n========== MAIN MENU ==========")
        print("1. Move files.")
        print("2. Rename files.")
        print("3. Delete files or folders.")
        print("4. Copy files.")
        print("5. Exit.")

        while True:
            try:
                choice = int(input("Enter your choice: "))

                if 1 <= choice <= 5:
                    break

                print("Select a number between 1 and 5.")

            except ValueError:
                print("Invalid input. Enter a number.")

        if choice == 1:
            move.move_batch()
        elif choice == 2:
            rename.rename_batch()
        elif choice == 3:
            delete.delete_batch()
        elif choice == 4:
            copy_files.copy_batch()
        elif choice == 5:
            print("Thank you for using File Organizer.")
            break

if __name__ == "__main__":
    main()