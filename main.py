import requests
import json
import base64
import csv
import config
from datetime import datetime
import math
import os
import time
from json.decoder import JSONDecodeError
from os import path

def banner():
    bname = [98, 121, 32, 65, 110, 117, 112, 32, 80, 117, 115, 104, 112, 97, 100]
    res = ''.join(map(chr, bname))
    gitul = [104, 116, 116, 112, 115, 58, 47, 47, 103, 105, 116, 104, 117, 98, 46, 99, 111, 109, 47, 97, 110, 117, 112, 112, 117, 115, 104, 112, 97, 100, 47, 71, 111, 77, 111, 122, 67, 104, 101, 99, 107, 101, 114]
    ngitul = ''.join(map(chr, gitul))

    RED = "\033[0;31m"
    BLUE = "\033[0;34m"
    CYAN = "\033[0;36m"
    WHITE = "\033[1;37m"
    YELLOW = "\033[1;33m"
    OFF = "\033[0;0m"

    intro = (BLUE + """
       _____       __  __           _____ _               _             
      / ____|     |  \/  |         / ____| |             | |            
     | |  __  ___ | \  / | ___ ___| |    | |__   ___  ___| | _____ _ __      
     | | |_ |/ _ \| |\/| |/ _ \_  / |    | '_ \ / _ \/ __| |/ / _ \ '__|    
     | |__| | (_) | |  | | (_) / /| |____| | | |  __/ (__|   <  __/ |   
      \_____|\___/|_|  |_|\___/___|\_____|_| |_|\___|\___|_|\_\___|_|   
                                                                        
                                                                        
    """ + CYAN + str(res) + "\n" + YELLOW + "\n" + "\n" + "✨ The  Github Repository" + "\n" + "\n" + WHITE + str(ngitul) + "\n" + "\n" + OFF)

    print(intro)
banner()

global m #url counter
m = 0
global starttime
starttime = 0
base_url = "https://lsapi.seomoz.com/v2/url_metrics"
global filename
filename = ""

axha = len(open('urls.txt', 'r').readlines())
##adding headers to csv
head = ['Domain Name', 'DA', 'PA', 'Spam Score']
filename = datetime.now().strftime("%d/%m/%Y %H:%M")
filename = filename.replace(" ", "_")
filename = filename.replace("/", "-")
with open(filename + ".csv", "a") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(head)
    csvfile.close()
##done adding headers

def clean_url():
    x = open("urls.txt")
    y = x.read()  ##regexto do this ^(https://)|(http://)|(www.)
    z = y.replace("https://", "")
    z = z.replace("http://", "")
    z = z.replace("www.", "")
    with open('urls.txt', 'w+') as f:
        z = z.replace("'", "\"")
        f.write(z)
        f.close()
    calculations()

    
def hash_auth_token(urlarray, urlbunch, count, leftover):
    creds = json.load(open('config.json', 'r'))
    for i in range(0, len(creds['id'])):
        access_id = creds['id'][i]
        sec_hash = creds['pass'][i]
        bauth = access_id + ":" + sec_hash
        bauth1 = bauth.encode("ascii")
        bauth2 = base64.b64encode(bauth1)
        finbauth = bauth2.decode("ascii")
        j = requests.post(base_url, headers={"Authorization": "Basic " + finbauth})
        if j.status_code == 400:
            print("Using the API : " + str(access_id))
            req_loop(finbauth, urlarray, urlbunch, count, leftover)
        if j.status_code == 401:
            print("API limit reached!")
            print("Change API. Run the addapi.py file.")
            break
        else:
            break




        
def calculations():
    global starttime
    starttime = time.perf_counter()
    global count
    count = len(open('urls.txt').readlines())
    
    
    if count>50:
        leftover = count % 50
        urlbunch = math.floor(count//50)
    else:
        leftover = 0 
        urlbunch = 1
    url_read(count, leftover, urlbunch)




def url_read(count, leftover, urlbunch):
    with open('urls.txt') as f:
        urlarray = f.read().split('\n')
    hash_auth_token(urlarray, urlbunch, count, leftover)


        
def req_loop(finbauth, urlarray, urlbunch, count, leftover):
    urllistlen = len(urlarray) - 1
    if urllistlen < 50:
            send_req(finbauth, urlarray, urllistlen)

    else:
        for i in range(0, urlbunch):
            modurlarray = urlarray[int(i*50):int(i*50+50)]

            
            #print("mod" +str(modurlarray))
            send_req(finbauth, modurlarray, urllistlen)

        ######request for leftover

        for i in range(0, 1):
            leftoverurlarray = urlarray[-int(leftover):]            
            tempvar = len(leftoverurlarray) - 1
            leftoverurlarray.pop(tempvar - 1) #remove last empty index
            #print("leftover "+str(leftoverurlarray))
            send_leftreq(finbauth, leftoverurlarray, tempvar)
            





def send_leftreq(finbauth, urlarray, urllistlen):
    
    headers = {"Authorization": "Basic " + finbauth}
    finurlarray = []
    for z in urlarray:
        if z != "":
            finurlarray.append(z)
        else:
            pass
    finurlarray = str(finurlarray)
    finurlarray = finurlarray.replace("'", "\"")
    data = "{\"targets\": " + finurlarray + "}"
    r = requests.post(base_url, headers=headers, data=data)
    try:
        x = json.loads(r.content)
    except JSONDecodeError:
        print("Error : " + str(x['name']))
    ###for le
    count = urllistlen
    leftparse(x, count)


    

def leftparse(x, count):
    global m
    for b in range(0, count):
        try:
            domain = x['results'][b]['root_domain']
        except(KeyError, IndexError):
            try:
                if x['message'] == (("Your monthly row limit reached. To increase your monthly request limit, see: http://moz.com/products/api/pricing") and ("This request exceeds the limit allowed by your current plan. To increase your request limit, see: http://moz.com/products/api/pricing")):
                    print("API limit reached")
                    #use next api
            except:
                break
        try:
            da = x['results'][b]['domain_authority'] #domain_authority
        except(IndexError, KeyError):
            break            
        try:
            pa = x['results'][b]['page_authority'] #page_authority
        except(IndexError, KeyError):
            break
        spamscore = x['results'][b]['spam_score'] #spam_score
        m += 1
        csv_input(domain, da, pa, spamscore)


    
def send_req(finbauth, urlarray, urllistlen):
    
    headers = {"Authorization": "Basic " + finbauth}
    finurlarray = []
    for z in urlarray:
        if z != "":
            finurlarray.append(z)
        else:
            pass
    finurlarray = str(finurlarray)
    finurlarray = finurlarray.replace("'", "\"")
    data = "{\"targets\": " + finurlarray + "}"
    r = requests.post(base_url, headers=headers, data=data)
    try:
        x = json.loads(r.content)
    except JSONDecodeError:
        print("Error : " + str(x['name']))
        print("Error!!!! Try adding new API or wait for some time.")
    ###for le
    count = urllistlen
    jsonparse(x, count)
    

    
def jsonparse(x, count):
    global m
    for b in range(0, 50):
        try:
            domain = x['results'][b]['root_domain']
        except(KeyError, IndexError):
            try:
                if x['message'] == (("Your monthly row limit reached. To increase your monthly request limit, see: http://moz.com/products/api/pricing") and ("This request exceeds the limit allowed by your current plan. To increase your request limit, see: http://moz.com/products/api/pricing")):
                    print("API limit reached")
                    #use next api
            except:
                pass                
        try:
            da = x['results'][b]['domain_authority'] #domain_authority
        except(IndexError, KeyError):
            break
        try:
            pa = x['results'][b]['page_authority'] #page_authority
        except(IndexError, KeyError):
            break
        spamscore = x['results'][b]['spam_score'] #spam_score
        m += 1
        csv_input(domain, da, pa, spamscore)


                
def csv_input(domain, da, pa, spamscore):
    rows = []
    rows.append(domain)
    rows.append(da)
    rows.append(pa)
    rows.append(spamscore)
    makecsv(rows)
    

def makecsv(rows):
    global filename
    global m
    global ci
    global axha
    with open(filename + ".csv", "a") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(rows)
        csvfile.close()

    totaltime = axha // 50 + 1
    timetaken = m // 50
    timerem = round(totaltime - timetaken, 2)
    if timerem < 0:
        timerem == 5
    else:
        timerem = timerem
    print("[+] Processed " + str(m) + " urls." + "  "  + "Time Remaining: " + str(timerem) + " seconds", end="\r")
    
            
                
clean_url()
stoptime = time.perf_counter()

if path.exists(filename+".csv") == True:
    print("Returned " + str(axha) +" rows in " + str(round(stoptime - starttime, 2)) + " seconds.")
else:
    print("Error Occured. Check API/url file.")


# Babye!