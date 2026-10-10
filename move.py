import os 
import shutil
def move_batch() :
    move =0
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
    for root,dirs,files in os.walk(source) :
        for file in files :
            file = os.path.join(root,file)
            file_size = os.path.getsize(file)
            file_name= os.path.basename(file)
            _,extension= os.path.splitext(file)
            os.makedirs(destination, exist_ok=True)
            source = os.path.abspath(source)
            destination = os.path.abspath(destination)
            if os.path.commonpath([source, destination]) == source:
                print("Destination cannot be inside source folder.")
                return
            
            found=0
            for key,value in rules.items():           
                if extension == key:
                    move,skip,fail=move_file(file,os.path.join(destination,value),move,skip,fail)
                    found+=1
                    print("File : ",file_name)
                    print("Size : ",file_size)
                    print("Type : ",key)
            if not found :
                unknown+=1
    print("File moved : ",move)
    print("File skipped : ",skip)
    print("File failed : ",fail)
    print("Unknown files : ",unknown)
def move_file(moving_file,Folder,m,s,f) :
    
    try:
        os.makedirs(Folder, exist_ok=True)
        if os.path.exists(os.path.join(Folder, os.path.basename(moving_file))):
            print("File already exists. Skipping...")
            s += 1
            return m, s, f
        shutil.move(moving_file,Folder)
        print("File Successfully moved.")
        m+=1
    except FileExistsError :
        s+=1
        print("File already exists. Skipping.....")
    except FileNotFoundError :
        f+=1
        print("File not found.")
    except PermissionError :
        f+=1
        print("We dont have permission to move.")
    except OSError as e :
        f+=1
        print("System File failed because ",e)
    return m,s,f