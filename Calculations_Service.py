"""
Admin.py

Helper module for calculating hours for each student and outputting as
either a simple list or spreadsheet.
"""


import imp
import os
import settingsFile
from myFunctions import myInput
from myFunctions import myRound
Settings=settingsFile.Settings

# CHANGELOG - PATH TO FOLDER:
    ##functions.py##
def checkName(firstLastName):
    error=False
    L=firstLastName.split()
    if len(L)!=2: error=True
    else:
        for item in L:
            if item[0].islower(): error=True
    return error

def myInput(message,errorMessage=None,strs=[],ints=[]):
    while True:
        I=input(message)
        if strs!=[] and I in strs: return I
        elif len(ints)==2 and I.isnumeric() and int(I)>=ints[0] and int(I)<=ints[1]: return int(I)
        elif strs==[] and ints==[]: return I
        if errorMessage!=None: print(errorMessage)
    ####


months=["January","February","March","April","May","June","July","August","September","October","November","December"] # To use later for converting a month to a number

rankDict={} # Dictionary of the 'rank' of each person (student or mentor)   {name:rank}
nameList=[] # List of all names                                             [name]
dateList=[] # List of all dates                                             [date]
dateDict={} # Dictionary for names, dates, and hours/minutes                {name:{date:time}}
timeDict={} # Dictionary for total hours/minutes for each person            {name:time}
missDict={} # Dictionary for number of times each person forgot to sign out {name:forgot}
numDict={"Student":0,"Mentor":0}

def calcNumDict():
    for name in rankDict:
        if timeDict[name]!=0:
            numDict[rankDict[name]]+=1

def getTimeFormat():
    if Settings['hours']==True: return "hours"
    else: return "minutes"

def findMaxLength(alist):
    maxLength=0
    for item in alist:
        if len(item)>maxLength: maxLength=len(item)
    return maxLength

##############################################################

def calculateSingle(name):
    totalTime=0
    
    try:
# CHANGELOG - PATH TO FOLDER:
        with open(Settings['path']+name+'.txt','r') as dataFile:
            datalist=dataFile.readlines() # Open their old records file, and create datalist
        for linenum in range(len(datalist)): # Iterate through each line in this student's file, by index
            if linenum+1<len(datalist): # If this is not the last line in the file:
                signIn=datalist[linenum].split() # Create signIn, the information from the "in" line
                signOut=datalist[linenum+1].split() # Create signOut, the information from the "out" line

                if datalist[linenum].split()[1]=="in" and datalist[linenum+1].split()[1]=="out": # If this line and the next are a valid in-out sequence
                    #Calculate time:
                    if signIn[7]==signOut[7]: # If same day, subtract the in time from the out time to get the minutes in between
                        time=int(signOut[3])-int(signIn[3])
                    else: #Different Day (past midnight)
                        time=1440-int(signIn[3])+int(signOut[3]) # (1440 minutes = 24 hours) (1440-in time)=minutes from first day + out time = minutes from both days
                        for i in range(int(signOut[7])-int(signIn[7])-1):
                            time+=1440 # For each extra day (double all-nighter), add 1440 minutes
                    time=myRound(time/60,2) # convert minutes to hours and round to 2 decimal places
##                    i=str(time).index(".")
##                    time=int(str(time)[:i+2])
                    totalTime+=time # add the time to the total for this student
    except:
        pass
    return totalTime

##########################################################################

def calculate(pt=False):
    rankDict.clear()
    nameList.clear()
    dateList.clear()
    dateDict.clear()
    timeDict.clear()
    missDict.clear()
    
    with open("usernameFile.py",'r') as nameFile: # Open the file that contains all student names (file name specified in Settings)
        tempList=nameFile.readlines() # Make a list of all the names
        for i in range(len(tempList)):
            if tempList[i][0]!="#":
                lineList=tempList[i].strip("\n").split("|")
                rankDict[lineList[0]]=lineList[2]
                tempList[i]=lineList[0]
        for i in range(tempList.count("")): tempList.remove("") # Remove the extra space(s) from the end
    tempList.sort() # Sort
    for name in tempList:
        if name[0]!="#":
            nameList.append(name)
    
    for name in nameList: # Iterate through each student name
        try:
            dateDict[name]={} # In dateDict, set their name as a key to a new dictionary, which will contain their individual dates and hours/minutes
            timeDict[name]=0 # Set total hours for this student to 0
            missDict[name]=0 # Set forget times for this student to 0
# CHANGELOG - PATH TO FOLDER:
            with open(Settings['path']+name+'.txt','r') as dataFile: datalist=dataFile.readlines() # Open their old records file, and create datalist
            for linenum in range(len(datalist)): # Iterate through each line in this student's file, by index
                if linenum+1<len(datalist): # If this is not the last line in the file:
                    signIn=datalist[linenum].split() # Create signIn, the information from the "in" line
                    signOut=datalist[linenum+1].split() # Create signOut, the information from the "out" line

                    #Calculate date:
                    if Settings['short']:
                        date=str(signIn[7]) # Get the date in ddd form
                        for i in range(3-len(date)): date="0"+date # Add leading zeros
                    else: # Get the date in mm/dd form
                        month=str(months.index(signIn[12])+1)
                        for i in range(2-len(month)): month="0"+month # Add leading zeros
                        day=str(signIn[13])
                        for i in range(2-len(day)): day="0"+day # Add leading zeros
                        date=month+"/"+day
                    if Settings['year']: date+="/"+str(signIn[14][1:-1]) # Add the year
                    if date not in dateList: dateList.append(date) # Add the date to dateList. After this has been done for all students, we will have a complete list of all dates

                    if datalist[linenum].split()[1]=="in" and datalist[linenum+1].split()[1]=="out": # If this line and the next are a valid in-out sequence
                        #Calculate time:
                        if signIn[7]==signOut[7]: time=int(signOut[3])-int(signIn[3]) # If same day, subtract the in time from the out time to get the minutes in between
                        else: #Different Day (past midnight)
                            time=1440-int(signIn[3])+int(signOut[3]) # (1440 minutes = 24 hours) (1440-in time)=minutes from first day + out time = minutes from both days
                            for i in range(int(signOut[7])-int(signIn[7])-1): time+=1440 # For each extra day (double all-nighter), add 1440 minutes
                        if Settings['hours']: time=myRound(time/60,2) # convert minutes to hours and round to 2 decimal places
                        if date not in dateDict[name]: dateDict[name][date]=time # In dateDict, under this student, create a date and the minutes/hours
                        else: # if this date already exists
                            if dateDict[name][date]=='Forgot': dateDict[name][date]=time # If forgot there, replace that with time
                            else: dateDict[name][date]+=time # Else, add the time to the time already there.
                        timeDict[name]+=time # add the time to the total for this student
                    elif datalist[linenum].split()[1]=="in" and datalist[linenum+1].split()[1]=="in": #Forgot to sign out
                        missDict[name]+=1 # Add one to miss count
                        if date not in dateDict[name]: dateDict[name][date]="Forgot" # Set time for that date to 'forgot'
        except:
            if(pt):
                print(name,"does not have an old records file in the correct folder. There is no data available for them")
    dateList.sort()
    calcNumDict()

def changeSettings():
    while True:
        if Settings['short']==False and Settings['year']==True: dateFormat="mm/dd/yyyy"
        elif Settings['short']==False and Settings['year']==False: dateFormat="mm/dd"
        elif Settings['short']==True and Settings['year']==True: dateFormat="ddd/yyyy"
        elif Settings['short']==True and Settings['year']==False: dateFormat="ddd"
        if Settings['hours']: timeFormat="hours"
        else: timeFormat="minutes"
        keyboardStatus=Settings['onScreenKeyBoard']
        print()
        print("0) Exit settings")
        print("1) Change date format. Current:",dateFormat)
        print("2) Change between hours/minutes. Current:",timeFormat)
        print("3) Turn on-screen keyboard on or off. Current:",keyboardStatus)
        answer=myInput("Please enter a value in the range 0-3: ","Invalid menu choice.",ints=[0,3])
        print()
        if answer==1:
            print("Date formats:\n     1) mm/dd/yyyy\n     2) mm/dd\n     3) ddd/yyyy\n     4) ddd")
            choice=myInput("Please enter a value in the range 1-4: ","Invalid menu choice.",ints=[1,4])
            if choice==1:
                Settings['short']=False
                Settings['year']=True
            elif choice==2:
                Settings['short']=False
                Settings['year']=False
            elif choice==3:
                Settings['short']=True
                Settings['year']=True
            else:
                Settings['short']=True
                Settings['year']=False
        elif answer==2:
            print("Time formats:\n     1) hours\n     2) minutes")
            choice=myInput("Please enter a value in the range 1-2: ","Invalid option.",ints=[1,2])
            Settings['hours']=choice==1
        elif answer==3:
            print("Keyboard Status:\n     1) On\n     2) Off")
            choice=myInput("Please enter a value in the range 1-2: ","Invalid option.",ints=[1,2])
            Settings['onScreenKeyBoard']=choice==1
        else: break
        for i in range(50): print()
    with open("settingsFile.py","w") as file:
        file.write("Settings="+str(Settings))
    calculate()

def printTime(p=True):
    print("How do you want it displayed?")
    print("     1) Sort by name, students and mentors together\n     2) Sort by name, students and mentors seperate\n     3) Sort by time, students and mentors together\n     4) Sort by time, students and mentors seperate")
    choice=myInput("Please enter a value in the range 1-4: ","Invalid menu choice.",ints=[1,4])
    for i in range(50): print()
    timeFormat=getTimeFormat()
    nameMax=findMaxLength(nameList)+1
    toPrint=""
    if choice==1:
        for name in nameList:
            if timeDict[name]!=0:
                toPrint+=name.rjust(nameMax)+str(myRound(timeDict[name],2)).rjust(7)+" "+timeFormat+" | Forgot "+str(missDict[name]).rjust(2)+" times\n"
    elif choice==2:
        for rank in ["Student","Mentor"]:
            toPrint+="\n"+rank+"s:\n"
            for name in nameList:
                if rankDict[name]==rank:
                    if timeDict[name]!=0:
                        toPrint+=name.rjust(nameMax)+str(myRound(timeDict[name],2)).rjust(7)+" "+timeFormat+" | Forgot "+str(missDict[name]).rjust(2)+" times\n"
    else:
        result=[]
        for item in list(timeDict.items()):
            result.append([item[1],item[0]])
        result.sort()
        result.reverse()
        if choice==3:
            for item in result:
                if timeDict[item[1]]!=0:
                    toPrint+=item[1].rjust(nameMax)+str(myRound(item[0],2)).rjust(7)+" "+timeFormat+" | Forgot "+str(missDict[item[1]]).rjust(2)+" times\n"
        elif choice==4:
            for rank in ["Student","Mentor"]:
                toPrint+="\n"+rank+"s:\n"
                for item in result:
                    if rankDict[item[1]]==rank:
                        if timeDict[item[1]]!=0:
                            toPrint+=item[1].rjust(nameMax)+str(myRound(item[0],2)).rjust(7)+" "+timeFormat+" | Forgot "+str(missDict[item[1]]).rjust(2)+" times\n"
    if p: print(toPrint)
    else: return toPrint

def writeCSV():
    # Prompt for name of file:
    while True:
        print("Sample format: '2016 Build Season; Jan 9 - Feb 23'")
        fileName=input("What do you want to name this file? => ")
        try:
            dataFile=open(fileName+".csv",'w')
            break
        except FileNotFoundError: print("Invalid file name!")
        except PermissionError: print("Close the file before overwriting it.")

    

    # Create lines:
    lineNum="1"
    for rank in ["Student","Mentor"]:
        
        # Create the dates line:
        dateLine=rank+"s,"+getTimeFormat().capitalize()+",Forgot"
        for date in dateList:
            dateLine+=","+date
        dataFile.write(dateLine+"\nTotal:,=SUM(B5:B"+str(numDict[rank]+4)+")\nAverage:,=ROUND(AVERAGE(B5:B"+str(numDict[rank]+4)+"))\n\n")
        lineNum=str(int(lineNum)+4) # Three new lines
                                          
        for name in nameList: # Iterate through all names
            if timeDict[name]!=0 and rankDict[name]==rank:
                timeLine = name # Create the first 3 cells (name and two equations)
                timeLine+= ",=SUM(D"+lineNum+":ZZ"+lineNum+")"
                timeLine+= ",=COUNTA(D"+lineNum+":ZZ"+lineNum+")-COUNT(D"+lineNum+":ZZ"+lineNum+")"
                for date in dateList: # Iterate through the list of all dates
                    timeLine+="," # New cell
                    if date in dateDict[name]:
                        timeLine+=str(dateDict[name][date]) # If they have time for that date, write it
                dataFile.write(timeLine+"\n") # Write that line to the file
                lineNum=str(int(lineNum)+1) # Next line
        dataFile.write("\n")
        lineNum=str(int(lineNum)+1) # Next line
    dataFile.close() # Close the file

def printRaw():
    print("Times in "+getTimeFormat()+":")
    print()
    print("nameList:",nameList)
    print()
    print("rankDict:",rankDict)
    print()
    print("numDict:",numDict)
    print()
    print("dateList:",dateList)
    print()
    print("dateDict:",dateDict)
    print()
    print("timeDict:",timeDict)
    print()
    print("missDict:",missDict)

def checkNameFile():
    for i in range(len(nameList)):
        oldName=nameList[i]
        if checkName(oldName):
            print("Error with",oldName)
            newName=input("Enter the fixed name: ")
            while checkName(newName):
                newName=input("Error! Enter a different fixed name: ")
            print("Converting",oldName,"to",newName)
            nameList[i]=newName
            try: os.rename(Settings['path']+oldName+".txt",Settings['path']+newName+".txt")
            except: pass
            with open('usernameFile.py','r') as nameFile:
                fileList=nameFile.readlines()
            with open('usernameFile.py','w') as nameFile:
                for line in fileList:
                    lineList=line.strip("\n").split("|")
                    if lineList[0]==oldName:
                        nameFile.write(newName+"|"+lineList[1]+"|"+lineList[2]+"\n")
                    else:
                        nameFile.write(line.strip("\n")+"\n")
            print()
                
    print("Done checking names.")

def main():
    calculate()
    optionList=[['Exit Admin'],
                ['Change settings', changeSettings],
                ['Print all the students and mentors with their times', printTime],
                ['Write times to a spreadsheet', writeCSV],
                ['Print raw data', printRaw],
                ['Recalculate times', calculate],
                ['Check nameFile for errors', checkNameFile]]
    while True:
        for i in range(50): print()
        for i in range(len(optionList)): print(str(i)+": "+optionList[i][0])
        print()
        choice=myInput("Enter your menu choice: ","Invalid menu choice.",ints=[0,len(optionList)-1])
        for i in range(50): print()
        if choice==0: return
        optionList[choice][1]()
        if optionList[choice][1] in [printTime,printRaw,checkNameFile]:
            input("\nHit enter to continue...")

if __name__=="__main__":
    main()
