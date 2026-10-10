import os 

def presuff_rename(replace,new,rename) :
    try :
        os.rename(replace,new)
        rename+=1
    except FileNotFoundError:
        print("File not found.")
    except PermissionError :
        print("You are not allowed to do it.")
    except OSError :
        print("Os is not allowing this specific operation.")
    return rename

def sequential_rename(replace,new,rename,counter) :
    try :
        os.rename(replace,new)
        rename+=1
        counter+=1
    except FileNotFoundError:
        print("File not found.")
    except PermissionError :
        print("You are not allowed to do it.")
    except OSError :
        print("Os is not allowing this specific operation.")
    return rename,counter

def rename_batch() :

    rename =0
    ori_directory=os.getcwd()
    batch= input("Enter your file batch you wanna  rename : ")
    batch=os.path.abspath(batch)
    if not os.path.isdir(batch) :
        print("Invalid path.")
        return
    if os.listdir(batch)== [] :
        print("Folder is empty.")
        return
    os.chdir(batch)

    print("How you wanna rename your batch : ")
    print("1.Prefix.")
    print("2.Suffix")
    print("3.Sequential numbering.")
    print("4.Find and replace.")
    print("5.Back to main menu.")
    dec =-1
    while dec < 1 or dec>5 :
        try :
            dec = int(input("Enter your preference : "))
        except ValueError: 
            print("Select a valid integer.")
    if dec == 1 :
        prefix = input("Enter the new name you want : ")
        for file in os.listdir(batch) :
            if os.path.isfile(file) :
                new_name = prefix+"_"+file
                if os.path.exists(new_name) :
                    print("Collision error.")
                else :
                    rename=presuff_rename(file,new_name,rename)

    elif dec == 2 :
        suffix = input("Enter the new name you want : ")
        for selected_file in os.listdir(batch) :
            if os.path.isfile(selected_file) :
                base1,extension1=os.path.splitext(os.path.basename(selected_file))
                suff_name=base1+"_"+suffix+extension1
                if os.path.exists(suff_name) :
                    print("Collosion error.")
                else :
                    rename=presuff_rename(selected_file,suff_name,rename)

    elif dec ==3 :
        print("1.Replace original name.")
        print("2.Add number to original name.")
        a=-1
        while a < 1 or a > 2 :
            try :
                a=int(input("Enter your choice : "))
            except ValueError :
                print("Select a valid integer.")
        if a==1 :
            counter=0
            for all_files in os.listdir(batch) :
                if os.path.isfile(all_files):
                    _,extension2 = os.path.splitext(os.path.basename(all_files))
                    new_name = str(0)+str(counter) + extension2 
                    if os.path.exists(new_name) :
                        print("Collision error.")
                        counter+=1
                    else :
                        rename,counter=sequential_rename(all_files,new_name,rename,counter)
        
        elif a==2:
            print("1.Number at begginning.")
            print("2.Number at end.")
            b=-1
            while b<1 or b>2 : 
                try :
                    b=int(input("Enter your choice : "))
                except ValueError :
                    print("Select a valid integer.")
            if b ==1 :
                cou=0
                for every in os.listdir(batch) :
                    if os.path.isfile(every) :
                        a_name = str(0)+str(cou) + os.path.basename(every)
                        if os.path.exists(a_name) :
                            print("Collosion error.")
                            cou+=1
                        else : 
                            rename,cou=sequential_rename(every,a_name,rename,cou)

            elif b ==2 :
                coun=0
                for ever in os.listdir(batch) :
                    if os.path.isfile(ever) :
                        base3,extension3=os.path.splitext(os.path.basename(ever))
                        an_name = base3+str(0)+str(coun)+extension3
                        if os.path.exists(an_name) :
                            print("Collosion error.")
                            coun+=1
                        else :
                            rename,coun=sequential_rename(ever,an_name,rename,coun)
                            
    elif dec == 4 :
        print("1.Replace word.")
        print("2.Remove word.")
        choi =-1
        while choi < 1 or choi > 2 :
            try :
                choi = int(input("Enter your choice : "))
            except ValueError :
                print("Select a valid integer.")
        if(choi==1) :
            rep_name = input("Enter the name you wanna replace : ")
            if rep_name=="":
                print("Find cant be empty.")
                os.chdir(ori_directory)
                return
            newrep_name = input("Enter the new name : ")
            for rep in os.listdir(batch) :
                if os.path.isfile(rep) :
                    if rep_name in rep :
                        new_name2 = rep.replace(rep_name,newrep_name)
                        if os.path.exists(new_name2) :
                            print("Collosion error.")
                        else :
                            rename = presuff_rename(rep,new_name2,rename)        
                    
        elif(choi==2) :
            rep_name2 = input("Enter the name you wanna remove : ")
            if rep_name2=="":
                print("Find cant be empty.")
                os.chdir(ori_directory)
                return
            for rep2 in os.listdir(batch) :
                if os.path.isfile(rep2) :
                    if rep_name2 in rep2 :
                        new_name3 = rep2.replace(rep_name2,"")
                        if os.path.exists(new_name3):
                            print("Collosion error.")
                        else :
                            rename =presuff_rename(rep2,new_name3,rename)
                        
    elif dec == 5 :
        os.chdir(ori_directory)
        return
    else :
        print("You entered an invalid value.")
    if rename==0:
        print("No files renamed.")
    else :
        print(f"{rename} Files renamed successfully. ") 
    os.chdir(ori_directory)