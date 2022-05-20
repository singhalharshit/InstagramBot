from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import time
import random
import numpy


class InstagramBot():
    
    # -------- Constructer Created -----------#

    #---|| Login Credentials ||---#
    def __init__(self, username, password):
        self.loggedin = False
        self.username = username
        self.password = password
        self.base_url = "https://www.instagram.com/"
        self.follwersCount = 0
        self.followingCount = 0
        self.followedList = []
        self.doNotFollowList = []
        self.whiteList = []
        self.Login()
        self.CreateFiles()
        self.GetInfo()
        self.FollowFollowers()

    #---------------------------------------------#
        
#|_________________________________________________________|# 
    #---|| Chooser ||---#
    
    def Choose(self):
       #The UI
       return
#|_________________________________________________________|#     
    
                #Function Created#
#|_________________________________________________________|#     
   
             #---|| Helper Methods ||---#

    def ConvertToNumber(self,text):
        #converts insta K,M etc into number
        if "k" in text:
            return int((float(text.replace("k","")))*1000)
        elif "m" in text:
            return int((float(text.replace("m","")))*1000000)
        else:
            return int(text)
    
#|_________________________________________________________|# 
    
                #Function Created#
    
#|_________________________________________________________|#   
    
             #---|| Timeout Logic ||---#

    def Wait(self,min,max):
        # Pause for random time
        time.sleep(random.choice(numpy.arange(min,max,0.1)))

#|_________________________________________________________|# 
    
                #Function Created#
    
#|_________________________________________________________|# 

             #---|| Go to User Page ||---#

    def GotoUser(self,user):
        # Go To Particular User
        self.driver.get("{}{}/".format(self.base_url,user))
        self.Wait(1,2)

#|_________________________________________________________|# 
    
                #Function Created#
    
#|_________________________________________________________|# 

    def CreateFiles(self):
        #Create Files if they dont exist
        temp=open("[Followed][{}]".format(self.username), "a+")
        temp.close
        temp=open("[DoNotFollow][{}]".format(self.username), "a+")
        temp.close

#|_________________________________________________________|# 
    
                #Function Created#
    
#|_________________________________________________________|# 

    def ReadFiles(self):
        # Obtains previously followed usernames from file
        with open("[Followed][{}]".format(self.username), "r+") as flist:
            lines = flist.readlines()
            for line in lines:
                self.followedList.append(line.strip())
        
        with open("[DoNotFollow][{}]".format(self.username), "r+") as flist:
            lines = flist.readlines()
            for line in lines:
                self.doNotFollowList.append(line.strip())
    

#|_________________________________________________________|# 
    
                #Function Created#
    
#|_________________________________________________________|# 

    def AddFollowList(self, name):
        with open("[Followed][{}]".format(self.username), "a+") as flist:
            temp = name.strip() +"\n"
            flist.write(temp)
        
        with open("[DoNotFollow][{}]".format(self.username), "a+") as flist:
            temp = name.strip() +"\n"
            flist.write(temp)   

#|_________________________________________________________|# 
    
                #Function Created#
    
#|_________________________________________________________|# 

    def RemFollowedList(self, name):
        #Removed followed username from the List
        with open("[Followed][{}]".format(self.username), "r") as flist:
            lines = flist.readlines()
        with open("[Followed][{}]".format(self.username), "w") as flist:
            for line in lines:
                if line.strip() != name:
                    flist.write(line)

#
#_______________________________________________________________________________________________________________________________________________________#
    # ||||||||-- Login --||||||||#

    def Login(self):
    
        self.driver=webdriver.Chrome("C:/Users/hasinghal/Downloads/chromedriver_win32 (1)/chromedriver.exe")
        print("Logging In: {}".format(self.username))
        self.driver.get("{}accounts/login/?next=%2Faccount%2Flogin&source=desktop_nav".format(self.base_url))
        self.Wait(2,3)
        self.driver.find_element_by_name("username").send_keys(self.username)
        self.Wait(1,2)
        self.driver.find_element_by_name("password").send_keys(self.password)
        self.Wait(1,2)
        self.driver.find_elements_by_xpath("//div[contains(text(), 'Log In')]")[0].click()
        print("Logged In: {}".format(self.username))
        self.loggedin = True
        self.Wait(4,5)


    #---|| Get Info ||---#

    def GetInfo(self):
        # Get Followers and Following Info
        self.GotoUser(self.username)
        # Time for Number of followers
        temp = self.driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[2]/a/div/span").text
        self.follwersCount = self.ConvertToNumber(temp)
        #Time for numner of Following
        temp = self.driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[3]/a/div/span").text
        self.followingCount = self.ConvertToNumber(temp)
        print(self.follwersCount , self.followingCount)
        self.ReadFiles()


#_______________________________________________________________________________________________________________________________________________#

    def FollowFollowers(self):
        #Follow the Followers
        #Get username and number of followers to follow
        user=input("Account Name:\t")
        self.GotoUser(user)                 # The user's account you want to follow
        temp = self.driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[2]/a/div/span").text # Number of Followers the User has
        numoffollowers = self.ConvertToNumber(temp) #Conversion of the number of followers to the text to number 
        amount = int(input("How many to follow? (Less than {})\t".format(temp))) # Number of followers you want to follow
        while amount > numoffollowers: #To verify the number that the required number of followers dont exceed
            amount = int(input("How many to follow? (Less than {})\t".format(temp)))

        #Clicks on the followers tab and goes through the list one by one
        self.driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[2]/a/div").click()
        i, k = 1, 1
        while (k <= amount):
            self.Wait(2,3.5)
            currentUser = self.driver.find_element_by_xpath("/html/body/div[6]/div/div/div/div[2]/ul/div/li[{}]".format(i))
            button = currentUser.find_elements_by_xpath(".//button")
            name = currentUser.find_element_by_css_selector(".notranslate").text
            # If a strictly follow button exists, it clicks it
            if (button) and (button[0].text == "Follow"):
                self.Wait(30,45)
                button[0].click()
                self.AddFollowList(name) #Writes username to file
                k +=1
            self.Wait(7,10)
            #Scrolls Down for the user to be  at the top of the tab
            self.driver.execute_script("arguments[0].scrollIntoView()",currentUser)
            i+=1    





TestRun=InstagramBot("sampl.etestuser","harshit2000")