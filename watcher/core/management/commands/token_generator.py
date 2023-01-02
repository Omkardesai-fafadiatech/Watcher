# 5. selenium method

# Install chrome driver
# wget https://chromedriver.storage.googleapis.com/2.41/chromedriver_linux64.zip
# unzip chromedriver_linux64.zip
# sudo mv chromedriver /usr/bin/chromedriver
# sudo chown root:root /usr/bin/chromedriver
# sudo chmod +x /usr/bin/chromedriver

# for venv:
# pip3 install selenium

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from django.core.management.base import BaseCommand
import time
import os
from django.conf import settings

"""
This token_generator.py will run and create new token at 12:00 p.m. of everyday if the computer system is switched on usinf crontab in settings.py.
"""

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # Github credentials.
        # Ask sir whether to place username and password in django settings.
        username = "Omkardesai-fafadiatech"
        password = "Omkar*123698741#"
        description = "github_selenium_key"

        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument("--test-type")
        options.add_argument("--headless")
        driver = webdriver.Chrome("chromedriver", options=options)

        driver.get("https://github.com/login")
        driver.find_element("id", "login_field").send_keys(username)
        driver.find_element("id", "password").send_keys(password)
        driver.find_element("name", "commit").click()
        driver.get("https://github.com/settings/tokens")
        token_name = driver.find_element(By.XPATH, '/html/body/div[1]/div[5]/main/div[2]/div/div[2]/div/div/div[1]/div[2]/div[1]/div/span/strong/a').text
        if token_name == "github_selenium_key":
            token_name = driver.find_element(By.XPATH, '/html/body/div[1]/div[5]/main/div[2]/div/div[2]/div/div/div[1]/div[2]/div[1]/div/span/strong/a').text
            print(token_name)
            if token_name == "github_selenium_key":
                driver.find_element(By.XPATH,"/html/body/div[1]/div[5]/main/div[2]/div/div[2]/div/div/div[1]/div[2]/div[1]/div/div[1]/details/summary").click()
            time.sleep(2)
            driver.find_element(By.XPATH,"/html/body/div[1]/div[5]/main/div[2]/div/div[2]/div/div/div[1]/div[2]/div[1]/div/div[1]/details/details-dialog/div[4]/form/button").click()
            time.sleep(3)

            driver.get("https://github.com/settings/tokens/new")
            driver.find_element("id", "oauth_access_description").send_keys(description)
            select = Select(driver.find_element("id", "oauth_access_default_expires_at"))
            select.select_by_value("none")
            driver.find_element(By.XPATH, ".//*[@value='repo']").click()
            driver.find_element(By.XPATH, ".//*[@value='workflow']").click()
            driver.find_element(By.XPATH, ".//*[@value='write:packages']").click()
            driver.find_element(By.XPATH, ".//*[@value='delete:packages']").click()
            driver.find_element(By.XPATH, ".//*[@value='admin:org']").click()
            driver.find_element(By.XPATH, ".//*[@value='admin:public_key']").click()
            driver.find_element(By.XPATH, ".//*[@value='admin:repo_hook']").click()
            driver.find_element(By.XPATH, ".//*[@value='admin:org_hook']").click()
            driver.find_element(By.XPATH, ".//*[@value='gist']").click()
            driver.find_element(By.XPATH, ".//*[@value='notifications']").click()
            driver.find_element(By.XPATH, ".//*[@value='user']").click()
            driver.find_element(By.XPATH, ".//*[@value='delete_repo']").click()
            driver.find_element(By.XPATH, ".//*[@value='write:discussion']").click()
            driver.find_element(By.XPATH, ".//*[@value='admin:enterprise']").click()
            driver.find_element(By.XPATH, ".//*[@value='audit_log']").click()
            driver.find_element(By.XPATH, ".//*[@value='codespace']").click()
            driver.find_element(By.XPATH, ".//*[@value='project']").click()
            driver.find_element(By.XPATH, ".//*[@value='admin:gpg_key']").click()
            driver.find_element(By.XPATH, ".//*[@value='admin:ssh_signing_key']").click()

            driver.find_element(By.XPATH,"//button[@class='btn-primary btn']").click()
            time.sleep(2)
            new_token = driver.find_element(By.XPATH, "//code[@class='token']").text
            path = os.path.join(settings.BASE_DIR,"new_token.txt")
            print(path)
            with open(path, "w") as feed:
                feed.write(new_token)
            print(new_token)
        else:
            driver.get("https://github.com/settings/tokens/new")
            driver.find_element("id", "oauth_access_description").send_keys(description)
            select = Select(driver.find_element("id", "oauth_access_default_expires_at"))
            select.select_by_value("none")
            driver.find_element(By.XPATH, ".//*[@value='repo']").click()
            driver.find_element(By.XPATH, ".//*[@value='workflow']").click()
            driver.find_element(By.XPATH, ".//*[@value='write:packages']").click()
            driver.find_element(By.XPATH, ".//*[@value='delete:packages']").click()
            driver.find_element(By.XPATH, ".//*[@value='admin:org']").click()
            driver.find_element(By.XPATH, ".//*[@value='admin:public_key']").click()
            driver.find_element(By.XPATH, ".//*[@value='admin:repo_hook']").click()
            driver.find_element(By.XPATH, ".//*[@value='admin:org_hook']").click()
            driver.find_element(By.XPATH, ".//*[@value='gist']").click()
            driver.find_element(By.XPATH, ".//*[@value='notifications']").click()
            driver.find_element(By.XPATH, ".//*[@value='user']").click()
            driver.find_element(By.XPATH, ".//*[@value='delete_repo']").click()
            driver.find_element(By.XPATH, ".//*[@value='write:discussion']").click()
            driver.find_element(By.XPATH, ".//*[@value='admin:enterprise']").click()
            driver.find_element(By.XPATH, ".//*[@value='audit_log']").click()
            driver.find_element(By.XPATH, ".//*[@value='codespace']").click()
            driver.find_element(By.XPATH, ".//*[@value='project']").click()
            driver.find_element(By.XPATH, ".//*[@value='admin:gpg_key']").click()
            driver.find_element(By.XPATH, ".//*[@value='admin:ssh_signing_key']").click()

            driver.find_element(By.XPATH,"//button[@class='btn-primary btn']").click()
            time.sleep(2)
            new_token = driver.find_element(By.XPATH, "//code[@class='token']").text
            path = os.path.join(settings.BASE_DIR,"new_token.txt")
            print(path)
            with open(path, "w") as feed:
                feed.write(new_token)
            print(new_token)