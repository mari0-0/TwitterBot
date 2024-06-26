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
        time.sleep(5)

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

    def start_RT(self):
        '''
        This method works in the inputed page determined in the next method (where_to_RT()) and in that page, after a quick 
        scroll, it detects all the RT buttons and store's them in a list.

        Then it starts clicking each of them and his "confirmRetweet" button with the cooldown parameters established to control the
        number of retweets and to make it in the most natural way posible in order to avoid possible bans.
        
        This is fully explained in the README file.
        '''
        bot = self.bot

        ############################################# - Fit the parameters to your needs - ###############################################################
        num_likes = random.randint(30,40) # Max. number of likes of each serie (Recommended: 50)
        num_RTs = random.randint(20,30) # Max. number of retweets of each serie (Recommended: 30)
        minutes = random.randint(15,25) # Cooldown between series of retweets (Recommended: 5)
        interval_min1, interval_max1 = (2,4) # Min. and Max. number of seconds of a random interval - Cooldown between each RT (Recommended: (6,18))
        interval_min2, interval_max2 = (12,25) # Min. and Max. number of seconds of a random interval - Cooldown between each RT (Recommended: (6,18))
        ##################################################################################################################################################
        count_likes = 0 # DO NOT CHANGE
        count_retweets = 0 # DO NOT CHANGE0
        count_cooldown_rt = 0 # DO NOT CHANGE
        count_cooldown_like = 0
        count_scrolls = 0 # DO NOT CHANGE

        time.sleep(3)
        for _ in range(1, 1000):
            if count_scrolls > 0:
                bot.execute_script('window.scrollTo(0,document.body.scrollHeight)')

            time.sleep(2)
            rtButton_list = bot.find_elements("xpath", '//div[@role="button" and @data-testid="retweet"]')     
            likeButton_list = bot.find_elements("xpath", '//div[@role="button" and @data-testid="like"]')           
            print("Tweets to Retweet: (", (len(rtButton_list)), ")")
            print("Tweets to Like: (", (len(likeButton_list)), ")")

            for i in range(len(rtButton_list)):
                try:
                    webdriver.ActionChains(bot).move_to_element(likeButton_list[i]).click(likeButton_list[i]).perform()
                    print("Tweet successfully liked.")
                    count_cooldown_like += 1
                    count_likes += 1
                    
                    if count_cooldown_like >= (num_likes):
                        print("You have " + str(num_likes) +" consecutive likes, its time to stop (" + str(minutes) + " min). " 
                        + str(count_likes) + " in total.\n\n")
                        # time.sleep(minutes*60)
                        count_cooldown_like = 0

                    if count_cooldown_like < (num_likes):
                        print("You have " + str(count_cooldown_like) + " consecutive likes, " + str(num_likes - count_cooldown_like) + " left for the next break (" + str(minutes)
                              + " min). " + str(count_likes) + " in total.\n")
                        time.sleep(random.randint(interval_min1,interval_max1))

                except StaleElementReferenceException:
                    continue
                
                try:
                    webdriver.ActionChains(bot).move_to_element(rtButton_list[i]).click(rtButton_list[i]).perform()
                    time.sleep(2)
                    rtButtonConfirm = bot.find_element("xpath", '//div[@data-testid="retweetConfirm"]')   
                    webdriver.ActionChains(bot).move_to_element(rtButtonConfirm).click(rtButtonConfirm).perform()
                    print("Tweet succesfully retweeted.")
                    count_cooldown_rt += 1
                    count_retweets += 1

                    if count_cooldown_rt >= (num_RTs):
                        print("You have " + str(num_RTs) +" consecutive retweets, its time to stop (" + str(minutes) + " min). " 
                              + str(count_retweets) + " in total.\n\n")
                        time.sleep(minutes*60)
                        count_cooldown_rt = 0

                    if count_cooldown_rt < (num_RTs):
                        print("You have " + str(count_cooldown_rt) + " consecutive retweets, " + str(num_RTs - count_cooldown_rt) + " left for the next break (" 
                              + str(minutes) + " min). " + str(count_retweets) + " in total.\n")
                        time.sleep(random.randint(interval_min2,interval_max2))

                except StaleElementReferenceException:
                    continue
           

            count_scrolls += 1


UserParameters = TwitterBot('marioonrage', 'nike9999', inputVariable, hashtag, user) # Type your username and password
UserParameters.login()
UserParameters.start_RT()
