from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException             
import time
import random

################################################### - Select Username or Hashtag - ####################################################

# inputVariable = input("Select your index (hashtag or username): ")

# while inputVariable != "username" and inputVariable != "hashtag":
#     inputVariable = input("Wrong command, try again\nSelect your index (hashtag or username): ")

# if inputVariable == "username":
#     user = input("Type the username: ")
#     hashtag = ""

# if inputVariable == "hashtag":
#     hashtag = input("Type the hashtag: ")
#     user = ""

inputVariable = "hashtag"
hashtag = "$BUBBLE"
user = ""

#####################################################################################################################################

class TwitterBot:
    def __init__(self, username, password, inputVariable, hashtag, user):
        '''
        This method asign the username and the password parameters inputs in the driver that will be used in the following methods
        '''
        self.username = username
        self.password = password
        self.bot = webdriver.Chrome(executable_path='chromedriver.exe') # Copy YOUR chromedriver path
        self.inputVariable = inputVariable
        self.hashtag = hashtag
        self.user = user

    def login(self):
        '''
        In this method firstly the driver searchs the login page of twitter, then detects the user and the password boxes and clean
        and fill them with the established parameters
        '''
        bot = self.bot
        bot.get('https://twitter.com/login')
        time.sleep(3)

        email = bot.find_element("xpath", '//input[@autocomplete="username"]')
        email.clear()
        email.send_keys(self.username)
        email.send_keys(Keys.RETURN)
        time.sleep(3)

        password = bot.find_element("xpath", '//input[@name="password"]')
        password.send_keys(self.password)
        time.sleep(3)
        password.send_keys(Keys.RETURN)
        time.sleep(3)

    def start_liking(self):
        '''
        This method works in the inputed page determined in the next method (where_to_like()) and in that page, after a quick 
        scroll, it detects all the like buttons and store's them in a list.
        
        Then it starts clicking each of them with the cooldown parameters established to control the number of likes and to make it
        in the most natural way posible in order to avoid possible bans. 
        
        This is fully explained in the README file.
        '''
        bot = self.bot

        ############################################# - Fit the parameters to your needs - ###############################################################

        num_likes = random.randint(30,40) # Max. number of likes of each serie (Recommended: 50)
        minutes = random.randint(15,25) # Cooldown between series of likes (Recommended: 5)
        interval_min, interval_max = (11,22) # Min. and Max. number of seconds of a random interval - Cooldown between each like (Recommended: (6,18))

        ##################################################################################################################################################
        
        count_likes = 0 # DO NOT CHANGE
        count_cooldown = 0 # DO NOT CHANGE
        count_scrolls = 0 # DO NOT CHANGE

        time.sleep(3)
        for i in range(1, 1000):
            if count_scrolls > 0:
                bot.execute_script('window.scrollTo(0,document.body.scrollHeight)')
            time.sleep(2)
            likeButton_list = bot.find_elements("xpath", '//div[@role="button" and @data-testid="like"]')             
            print("Tweets to Like: (", (len(likeButton_list)), ")")
            for likeButton in likeButton_list:
                try:
                    webdriver.ActionChains(bot).move_to_element(likeButton).click(likeButton).perform()
                    print("Tweet successfully liked.")
                    count_cooldown += 1
                    count_likes += 1
                    
                    if count_cooldown >= (num_likes):
                        print("You have " + str(num_likes) +" consecutive likes, its time to stop (" + str(minutes) + " min). " 
                        + str(count_likes) + " in total.\n\n")
                        time.sleep(minutes*60)
                        count_cooldown = 0

                    if count_cooldown < (num_likes):
                        print("You have " + str(count_cooldown) + " consecutive likes, " + str(num_likes - count_cooldown) + " left for the next break (" + str(minutes)
                              + " min). " + str(count_likes) + " in total.\n")
                        time.sleep(random.randint(interval_min,interval_max))

                except StaleElementReferenceException:
                    continue

            count_scrolls += 1

    def where_to_like(self):
        '''
        This method firstly reject the cookies pop-up to avoid future click problems, then there are two options:

        - If the command was "username", it goes to the user inputed profile page to start the liking process explained in
        the previous method (start_liking())

        - If the command was "hashtag", it goes to the inputed hashtag page to start the liking process explained in
        the previous method (start_liking())
        '''
        bot = self.bot

        try:
            RejectCookies = bot.find_element("xpath", '//*[@id="layers"]/div/div/div/div/div/div[2]/div[2]/div/span/span')        
            webdriver.ActionChains(bot).move_to_element(RejectCookies).click(RejectCookies).perform()

        except NoSuchElementException:
            pass

        if inputVariable == "username":
            bot.get("https://twitter.com/" + user)
            self.start_liking()

        if inputVariable == "hashtag":
            bot.get("https://twitter.com/search?q=" + hashtag + "&src=typed_query")
            time.sleep(2)
            self.start_liking()

UserParameters = TwitterBot('marioonrage', 'nike9999', inputVariable, hashtag, user) # Type your username and password
UserParameters.login()
UserParameters.where_to_like()
