import os 
import shutil
import move
import delete
import rename
import copy_files

print("Welcome to file organizer.")
while True :
    print("1.Move your file.")
    print("2.Rename your whole directory batch.")
    print("3.Delete batch or files.")
    print("4.Copy batch or file")
    print("5.Exit.")
    while True:
        try:
            choice = int(input("Enter your choice: "))

            if 1 <= choice <= 5:
                break

            print("Select a number between 1 and 5.")

        except ValueError:
            print("Invalid input. Enter a number.")

    if choice == 1 :
        move.move_batch()

    elif choice == 2 :
        rename.rename_batch()

    elif choice == 3 :
        delete.delete_batch()

    elif choice == 4 :
        copy_files.copy_batch()
    elif choice == 5 :
        break
    else :
        print("You entered an invalid choice.")