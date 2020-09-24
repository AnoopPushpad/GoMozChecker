import json
uid = input("Enter your Access ID : ")
passwd = input("Enter your Secret Key : ")
try:
    x = open("config.json").read()
    x = json.loads(x)
    x['id'].append(uid)
    x['pass'].append(passwd)
    x['creditsused'].append('0')
    with open("config.json", "w+") as f:
            x = str(x)
            x = x.replace("'", "\"")
            f.write(x)
            f.close()
    print("Successfully added the following API keys to the list." + "\n" + "\n" + uid + "\n" + "\n"+ passwd + "\n")
except FileNotFoundError:
    print("Error encountered! Please check if config.json file exists.")


