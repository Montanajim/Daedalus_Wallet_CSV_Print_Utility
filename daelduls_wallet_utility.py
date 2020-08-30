# -*- coding: utf-8 -*-
"""
Created on Sat Aug 15 14:33:36 2020

@author: James Goudy

James Goudy
Kalispell, Montana

Wallet CSV Exporting Tool For Cardano Daedalus Wallet


Copyright 2020 James Goudy

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.




"""


import sqlite3
import datetime
import sys
import requests
import glob
import os
import ast



# Dictionary To Hold Wallet Names
walletDict={}

# List to hold wallet names
wnames = []

# Flow control flag 0 is go, 1 is stop
flowcontrol = 0

storedData = {"walletpath":"",
              "exportpath":""}

# Store wallet filepath 
fileStoredData ="storedData.txt"

# Script Path
scriptPath=""

# Wallet Directory
walletdir = ""

#stores the name of the ouptput csv dir
outputdir = ""

# get the wallet directory
# remembers previous wallet location
# stored file is in the same directory as the python script (scriptpath)

def getWalletPath():
    
    global scriptPath
    global fileStoredData
    global storedData
    global walletdir
    
    # retreive path of where the python script is running
    scriptPath = os.path.dirname(os.path.realpath(__file__))
    
    # add the filename
    fpath = scriptPath +"\\"+ fileStoredData
    
    # correct \\ due to escape character
    fpath = fpath.replace("\\", "\\\\")

    # check if stored data file exists
    if not(os.path.exists(fpath)):       
        return writeStoredData()             
    else:
        # file exists ask if user wants to use the stored file
        rfile=open(fpath,'r')
        fcontents =rfile.read()
        storedData = ast.literal_eval(fcontents)
        
        if storedData["walletpath"] != "":
            print("Use this wallet location:")
            print(storedData["walletpath"])
            choice = str(input("Enter y / n? ")).lower()

        
            if choice == "y":
                walletdir = storedData["walletpath"]
                return 
            else:
                return writeStoredData()
        else:
            return writeStoredData()
    
    return
    
         
# write the storeFile dictionary
# stores the wallet data file location so one only has to enter it once
def writeStoredData():
    
    global walletdir

    #scriptPath is the script file location- storage file will be written here
    scriptPath = os.path.dirname(os.path.realpath(__file__))
    fpath = scriptPath +"\\"+ fileStoredData
    fpath = fpath.replace("\\", "\\\\")
    wfile=open(fpath,"w")
   
    print("Locate the full path to the Daedalus wallet folder.")
    print("It is usually located at \nc\\Users\\username\\"\
          "AppData\\Roaming\\Daedula Wallets\\wallets")
    mydirinput = input("Enter the full path to the wallet directory.\n->")

    # replace the single \ with the \\ for correct file reading
    walletdir= mydirinput.replace("\\","\\\\")
    
    # store data in dictionary
    storedData["walletpath"]=walletdir
    
    # write file for stored data 
    wfile.write(str(storedData))
    wfile.flush()
    
    wfile.close()
    
    return    


# retreive wallet names / files
def dirInfo():
    
    global flowcontrol
    global scriptPath
    global walletdir
    
    scriptPath = os.path.dirname(os.path.realpath(__file__))
    
    ldir = []
    walletDict.clear()
    wnames.clear()
    
                          
    # walletdir = getWalletPath()
    # set the folder focus
    os.chdir(walletdir)
    
    # extract a list of Byran wallets
    ldirrnd = glob.glob("rnd*.sqlite")
    
    # extract a list of Shelley wallets
    ldirshe = glob.glob("she*.sqlite")
    
    

    try:   
        # menu system
        print("Wallets by era")
        print("Choose a wallets era\n1. Shelly\n2. Bryan\n3. All")
        whichWallets = int(input("Choose 1,2 or 3: "))
    
        if whichWallets == 1:
            ldir = ldirshe
        elif whichWallets == 2:
            ldir = ldirrnd
        elif whichWallets==3:
            ldir = ldirrnd + ldirshe
        else:
            print("That wasn't a choice")
            flowcontrol = 1
            return
        
    except:
        print("That wasn't a choice")
        flowcontrol = 1
        return
        
    # sort wallet names 
    ldir.sort()
    
    # reset wallet name variable
    wname = ""
    
    # iterate through selected list
    for item in ldir:
        temp = item
        lw = len(temp)


        #retreieve name of wallet named by user
        walletUserName = retreiveWalletName(item)
        
        #parse wallet name from file name
        for x in range(4,lw-7):
            wname = wname + temp[x]
        

        # list of fileame, user wallet name , walletname
        walletNameFileUserName=[item,walletUserName,wname]
        wnames.append(walletNameFileUserName)
        wname = ""

        
def retreiveWalletName(walletfile):
    
    # create connection
    walletcon= sqlite3.connect(walletfile)
    
    # create cursor
    wcursor = walletcon.cursor()
    
    # select statment
    wsql_stmt = "SELECT wallet.name "\
                "FROM wallet"
    
    # execute select
    wcursor.execute(wsql_stmt)
    
    #fetch row
    row = wcursor.fetchone()
    
    # return wallet name
    rwalletname = row[0]

    walletcon.close()
    
    return rwalletname


def menu():
        

    global outputdir
    
    menuChoice =1
    userChoice = -1
    menuWalletList=[]
    userWalletFilename = ""
    
    
    # check if there was directory errors
    if flowcontrol == 1:
        return
    
    # Build menu
    for item in wnames:
        
        menuWalletList.append(item[1])
    
    # Sort by Wallet Names
    menuWalletList.sort()
    
    
    # print menu
    print("\nMenu")
      
    
    for item in menuWalletList:
        print(str(menuChoice)+ ".  "+ item)
        menuChoice +=1
        
    print(str(menuChoice) + ".  Print all wallets")
    
    try:    
        
        # user picks wallet
        userChoice = int(input("Please select a wallet 1,2,3... : ")) - 1

        if userChoice <= len(menuWalletList): 
            outputdir = input("Enter the file output folder path-> ")
            outputdir = outputdir.replace("\\", "\\\\")


        # print all wallet information
        if userChoice == len(menuWalletList):
            for item in wnames:
                                
                # print(item[0]) 
                  
                importData(item[0])        
            
        # print selected wallet   
        else:   
            
            userWalletChoice = menuWalletList[userChoice] 
            
            # retreive wallet filename to for connection string
            for item in wnames:
                if item[1] == userWalletChoice:
                    userWalletFilename = item[0]
        
        
            # print(userWalletFilename + " retreiving data") 
                
            importData(userWalletFilename)
    except Exception as e:
        print(e)
        print("\nThat was not a correct choice")
        return
    
    

# build the output string / file from sqllite file
def importData(dbwalletfilename):
    
    global outputdir
    rewardstring = ""
    
    # counter to keep track of number printed fields
    fieldcount = 1    

    # create connction
    con = sqlite3.connect(dbwalletfilename)
    
    # create cursor       
    xcursor = con.cursor()
    
 
    # sql statment    
    sql_stmt =  "SELECT   wallet.wallet_id, tx_meta.tx_id, wallet.name, "\
                "CASE "\
                    "WHEN tx_meta.direction == 1 "\
                        "THEN 'received' "\
                        "ELSE 'sent' "\
                "END AS xdirection, "\
                "CASE "\
                    "WHEN tx_meta.direction == 0 "\
                        "THEN (-1 * CAST(tx_meta.amount AS FLOAT) / 1000000) "\
                        "ELSE (CAST(tx_meta.amount AS FLOAT) / 1000000) "\
                "END AS Amount "\
                "FROM wallet "\
                "INNER JOIN tx_meta ON wallet.wallet_id = tx_meta.wallet_id "

    # execute statement - create datashet
    xcursor.execute(sql_stmt)
    
    # fetch data into an object
    rows= xcursor.fetchall()

    
    # setup output file
    
    # create timestamp for output file name yearmonthdayhourminutesec
    currentTime = datetime.datetime.now()
    timestamp= str(currentTime.year) + str(currentTime.month) +\
                str(currentTime.day) +\
                str(currentTime.hour) + str(currentTime.minute) +\
                str(currentTime.second)
    
    # retrieve first row so wallet name can be retreived
    frow = rows[0]
    
    # build the output file name string path
    outputfileName = outputdir + "\\\\" + str(frow[2])\
                        + "_"+ timestamp +".csv"
        
    
    print("\nRetreiving Wallet Data for " + str(frow[2]) + "- please wait\n")
    
    # create output file
    outputfile = open(outputfileName,"w+")



    # iterate through the transactions
    for row in rows:

        # retreive the transaction date and time 
        tDateTime= retreivetime2(str(row[1]))
        
        # write to screen and file
        sys.stdout.write(tDateTime + ",")
        outputfile.write(tDateTime + ",")
        
        for item in row:
            
            #prevent extra comma at end
            if fieldcount < 5:
                sys.stdout.write(str(item) + ",")
                outputfile.write(str(item) + "," )
            else:
                sys.stdout.write(str(item))
                outputfile.write(str(item))
            
            fieldcount += 1
        
        print()
        outputfile.write("\n")
        outputfile.flush()
        
        #reset fieldcount
        fieldcount = 1

    # retreive the reward amount with info as string
    try:
        rewardstring = retreieveRewardAmount(dbwalletfilename)
    except:
        # no rewards in Bryan
        pass
    
    
    # output to screen
    print(rewardstring)
    
    # output to file
    outputfile.write(str(rewardstring))
    outputfile.flush()
        
    print()
    
    # close the file and connections.
    outputfile.close()
    con.close()
    
    print("finished retreiving wallet data\n")


def retreieveRewardAmount(dbwalletfilename):
    

    # create connction
    rwcon = sqlite3.connect(dbwalletfilename)
    
    # create cursor       
    rwcursor = rwcon.cursor()
    
 
    # sql statment    
    rwsql_stmt = "SELECT wallet.wallet_id, wallet.name, "\
                "CAST(delegation_reward.account_balance "\
                "AS FLOAT)/1000000 AS reward "\
                "FROM wallet "\
                "INNER JOIN delegation_reward "\
                "ON delegation_reward.wallet_id = wallet.wallet_id"                

    # execute statement - create datashet
    rwcursor.execute(rwsql_stmt)
    
    # fetch data into an object
    rows= rwcursor.fetchall()
    rewardString =  ","+ str(rows[0][0])+",rewards,"+ str(rows[0][1]) + \
                    ",received," + str(rows[0][2])
    
    return rewardString
    

# retreive transaction date and time
def retreivetime2(tx_id):
    
    # while condition flag
    check = True
    
    ec=1


    # NOTE IF ctsTxTimeIssued WAS RECORDED IN CLIENT DAEDALUS DATABASE
    # THERE WOULD BE NO NEED TO MAKE A URL CALL 
    # TO RETREIVE TRANACTION DATE AND TIME
    
    # Cardano Explorer API
    mybaseURL = "https://explorer.cardano.org/api/txs/summary/"

    # complete the API get url for speciic transaction
    fullURL = mybaseURL + tx_id
    

    # --- Retreiving json file from webserver
    # It should be noted that the webserver will periodically return 
    # an 502 error.  The while statement will continue to  check until
    # a good response is achieved
    
    while check:
     
        try:
            # requested data returns jason file
            # note dictionary within dictionary
            rr = requests.get(fullURL).json()
        except:
            ec+=1
            
            # prevent a run on condition
            if(ec == 2000):
                print("Web Server Busy Please Try Again Later")
                check = False
        else:
            check = False
        
    
    # note - Dictionary within dictionary 
    # separating out the inner dictionary
    newDict =rr.get("Right")
    

    # retreive the issue time from json file
    # note it is in the epoch time format
    yy = str(datetime.datetime.fromtimestamp(newDict.get("ctsTxTimeIssued")))

    return yy
        

def main():
    
    global flowcontrol

    
    run = "n"
    
    intro = "The purpose of the program is to "\
            "export a csv file \nof the wallet information "\
            "in the following order:\n\n"\
            "tranaction time-date in utc, wallet name, transaction id, "\
            "user wallet name, direction, amount\n\n"\
            "The program writes a copy to the screen \nas well as "\
            "to the actual file. An individual \ncsv is created for each "\
            "wallet file. The file is \nnamed "\
            "the userwalletname_timestamp.csv\n\n"\
            "\nNOTE: The wallet storage location \nfile(storedData.txt) "\
            "may be deleted anytime. \nYou can exit "\
            "any menu by picking an nonchoice\n "\
            "\n\nALWAYS DOUBLE CHECK WITH YOUR ORIGINAL WALLET"\
            
            
    
    print("Start\n")
    print(intro)
    
    while run != "y":
        
        try:
            
            getWalletPath()
            
            dirInfo()
        
            menu()
            
            run = input("Would you like to quit y/n: ").lower()
        

        except:
            print("\n***\nThere was an error - try again\n***\n")
            run = input("Would you like to quit y/n: ").lower()
        
        # reset flow control 
        flowcontrol = 0     
  

    print("\nbye")
    
    

main()



