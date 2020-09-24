answer = input("Do you want reset API keys data ? Enter yes or no: ") 
if answer == "yes": 
    file1 = open("config.json","w") 
    L = ["{\"id\": [""], \"pass\": [""], \"creditsused\": [""]}"]
    file1.writelines(L) 
    file1.close()
    print("API Keys Resetted to Default")
    watxt = input("Do you also wants to clean URLs txt file ? Enter yes or no: ")
    if watxt == "yes":
        file2 = open("urls.txt","w")
        btxt = []
        file2.writelines(btxt) 
        file2.close()
        print("URLs txt have ben cleaned")
elif answer == "no": 
    print("Not Reseted!")
else: 
    print("Please enter yes or no.")