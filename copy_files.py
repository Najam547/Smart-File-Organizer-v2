import os 
import shutil
def copy_batch() :
    copy =0
    skip =0
    fail =0
    unknown =0

    source = input("Enter your source path : ")
    if not os.path.isdir(source) :
        print("Source folder does not exists.")
        return
    if os.listdir(source)==[] :
        print("Folder is empty.")
        return
    
    destination= input("Enter your destination path : ")
    source = os.path.realpath(os.path.abspath(source))
    destination = os.path.realpath(os.path.abspath(destination))

    if os.path.commonpath([source, destination]) == source:
        print("Destination cannot be inside source folder.")
        return

    try:
        os.makedirs(destination, exist_ok=True)
    except OSError as e:
        print("Cannot create destination folder:", e)
        return
    
    rules = {
                ".pdf"  : "PDF",
                ".txt"  : "Documents",
                ".doc"  : "Documents",
                ".docx" : "Documents",
                ".xls"  : "Excel",
                ".xlsx" : "Excel",
                ".jpeg" : "Images",
                ".png"  : "Images" ,
                ".jpg"  : "Images" ,
                ".mp4"  : "Videos" ,
                ".webm" : "Videos" ,
                ".py"   : "Python" ,
                ".pptx" : "Ppt",
                ".java" : "Java"
                    }
    for root,_,files in os.walk(source) :
        for file in files :
            file = os.path.join(root,file)
            file_size = os.path.getsize(file)
            file_name= os.path.basename(file)
            _,extension= os.path.splitext(file)
                 
            found=0
            for key,value in rules.items():           
                if extension == key:
                    copy,skip,fail=copy_file(file,os.path.join(destination,value),copy,skip,fail)
                    found+=1
                    print("File : ",file_name)
                    print("Size : ",file_size)
                    print("Type : ",key)
            if not found :
                unknown+=1
    print("File copied : ",copy)
    print("File skipped : ",skip)
    print("File failed : ",fail)
    print("Unknown files : ",unknown)
def copy_file(copying_file,Folder,c,s,f) :
    try:
        os.makedirs(Folder, exist_ok=True)
        if os.path.exists(os.path.join(Folder, os.path.basename(copying_file))):
            print("File already exists. Skipping...")
            s += 1
            return c, s, f
        shutil.copy2(copying_file,Folder)
        print("File Successfully copied.")
        c+=1
    except FileNotFoundError :
        f+=1
        print("File not found.")
    except PermissionError :
        f+=1
        print("We dont have permission to copy.")
    except OSError as e :
        f+=1
        print("System File failed because ",e)
    return c,s,f