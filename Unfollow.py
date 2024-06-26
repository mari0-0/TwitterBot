from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException             
import time
import random

class TwitterBot:
    def __init__(self, username, password):
        '''
        This method asign the username and the password parameters inputs in the driver that will be used in the following methods
        '''
        self.username = username
        self.password = password
        self.bot = webdriver.Chrome(executable_path='HERE') # Copy YOUR chromedriver path

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

    def unfollow(self):
        '''
        This method firstly reject the cookies pop-up to avoid future click problems, then search your profile page and your 
        "following page". After a quick scroll in that page detects all the usernames and store them in a list that will
        later be the index from wich unfollow each of them.

        Then it starts unfollowing each of them with the cooldown parameters established to control the number of follows and to make
        it in the most natural way posible in order to avoid possible bans. This is fully explained in the README file.
        '''
        bot = self.bot

        ############################################# - Fit the parameters to your needs - ###############################################################

        num_unfollows = 20 # Max. number of unfollows of each serie (Recommended: 20)
        minutes = 10 # Cooldown between series of unfollows (Recommended: 10)
        interval_min, interval_max = (6,18) # Min. and Max. number of seconds of a random interval - Cooldown between each unfollow (Recommended: (6,18))

        ##################################################################################################################################################
        
        count_unfollows = 0 # DO NOT CHANGE
        count_cooldown = 0 # DO NOT CHANGE
        count_scrolls = 0 # DO NOT CHANGE 

        try:
            RejectCookies = bot.find_element("xpath", '//*[@id="layers"]/div/div/div/div/div/div[2]/div[2]/div/span/span')        
            webdriver.ActionChains(bot).move_to_element(RejectCookies).click(RejectCookies).perform()

        except NoSuchElementException:
            pass
        
        bot.get("https://twitter.com/"+ self.username)
        time.sleep(3)
        bot.get("https://twitter.com/"+ self.username + "/following")
        time.sleep(3)

        for k in range(1, 1000):
            if count_scrolls > 0:
                    bot.execute_script('window.scrollTo(0,document.body.scrollHeight)')

            time.sleep(3)
            usernames_detected = bot.find_elements("xpath", '//a[@role="link" and @aria-hidden="true"]')
            usernames_list = [arroba.get_attribute('href') for arroba in usernames_detected]

            cleaned_usernames_list = []
            for arroba in usernames_list[0:15]:
                arroba = "@" + arroba.split("/")[3]
                cleaned_usernames_list.append(arroba)

            print("List of '@' detected (", len(cleaned_usernames_list), "): ", cleaned_usernames_list)

            for n in cleaned_usernames_list:
                   
                time.sleep(2)
                try:
                    unfollows_b = bot.find_element(By.XPATH, "//div[@aria-label='Following " + n + "']")
                    webdriver.ActionChains(bot).move_to_element(unfollows_b).click(unfollows_b).perform()
                    time.sleep(1)
                    unfollows_b_confirm = bot.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div[2]/div[1]/div')
                    unfollows_b_confirm.click()
                    print("You have unfollowed ", n)
                    count_unfollows += 1
                    count_cooldown += 1
                    time.sleep(2)

                    if count_cooldown >= (num_unfollows):
                        print("\n-------------------------------------------------------")
                        print("You have " + str(num_unfollows) + " consecutive unfollows, its time to stop (" + str(minutes) 
                                + " min). " + str(count_unfollows) + " in total.\n")
                        print("-------------------------------------------------------\n")
                        time.sleep(minutes*60)
                        count_cooldown = 0

                    if count_cooldown < (num_unfollows):
                        print("You have " + str(count_cooldown) + " consecutive unfollows, " + str(num_unfollows - count_cooldown)
                            + " left for the next break (" + str(minutes) + " min). " + str(count_unfollows) + " in total.\n")
                        time.sleep(random.randint(interval_min, interval_max))

                except NoSuchElementException:
                    continue

            count_scrolls += 1
                
UserParameters = TwitterBot('YourUsername', 'YourPassword') # Type your username and password
UserParameters.login()
UserParameters.unfollow()
