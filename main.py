import json
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.headless = True
options.add_argument("start-maximized")
driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))


def searchReddit(username):
    url = "https://www.reddit.com/search/?q=" + username + "&type=user&include_over_18=1"

    driver.get(url)
    # wait = WebDriverWait(driver, 10)
    # wait.until(EC.presence_of_element_located((By.CLASS_NAME, "_2torGbn_fNOMbGw3UAasPl")))
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    returnlist = []
    h6 = driver.find_elements(By.CLASS_NAME, "_2torGbn_fNOMbGw3UAasPl")

    for element in h6:
        returnlist.append(element.text)

    return returnlist


def searchGitHub(username):
    url = "https://www.github.com/search/?q=" + username + "&type=users"

    driver.get(url)
    # time.sleep(5)
    content = driver.page_source
    soup = BeautifulSoup(content, "html.parser")
    returnlist = []
    A = soup.find_all("a", {"class": "color-fg-muted"})

    for a in A:
        returnlist.append(a.get('href'))

    # totalP = soup.find_all("em"})[-1].get('data-total-pages')
    # print(totalP)
    # i=2
    # while i <= totalP:
    #     time.sleep(3)
    #     driver.get(url + "&p=" + str(i))
    #     content = driver.page_source
    #     soup = BeautifulSoup(content, "html.parser")
    #     ems = soup.find_all("em")
    #     if not ems:
    #         time.sleep(10)
    #         continue;
    #
    #     for em in ems:
    #         if em.parent.name == 'a':
    #             returnlist.append(em.string)
    #     i+=1;
    return returnlist


def searchHabr(username):
    url = "https://career.habr.com/resumes?q=" + username
    print(url)
    driver.get(url)

    content = driver.page_source
    soup = BeautifulSoup(content, "html.parser")
    returnlist = []
    A = soup.find_all("a", {"class": "resume-card__title-link"})

    for a in A:
        returnlist.append(a.get('href'))

    return returnlist


def searchTiktok(username):
    url = 'https://www.tiktok.com/@'+username
    returnList = []
    driver.get(url)
    err = driver.find_elements(By.CLASS_NAME, "tiktok-1osbocj-DivErrorContainer")
    if not err:
        returnList.append("@"+username)
    return returnList

def searchInstagram(username):
    url = 'https://www.instagram.com/'+username
    returnList = []
    driver.get(url)
    err = driver.find_elements(By.CLASS_NAME, "_aadb")
    if not err:
        returnList.append(username)
    print(returnList)
    return returnList



def searchPikabu(username):
    url  = 'https://pikabu.ru/@'+ username
    response = requests.get(url)
    returnList=[]
    if response.status_code==404:
        print(response.status_code)
        return returnList
    returnList.append("@"+username)
    return returnList


def searchByUsername(username):
    redditList = searchReddit(username)
    githubList = searchGitHub(username)
    habrList = searchHabr(username)
    tiktokList = searchTiktok(username)
    pikabuList = searchPikabu(username)
    instagramList = searchInstagram(username)
    linksList = []
    if redditList:
        linksList.append("https://www.reddit.com/user" + redditList[0][1:])
    if githubList:
        linksList.append("https://github.com"+githubList[0])
    if habrList:
        linksList.append("https://career.habr.com"+habrList[0])
    if tiktokList:
        linksList.append("https://www.tiktok.com/" + tiktokList[0])
    if pikabuList:
        linksList.append("https://pikabu.ru/" + pikabuList[0])
    if instagramList:
        linksList.append("https://www.instagram.com/"+instagramList[0])

    dictionary = {
        username: linksList
    }
    json_object = json.dumps(dictionary, indent=4)
    with open(username+".json", "w") as outfile:
        outfile.write(json_object)


username = "alex"

searchByUsername(username)