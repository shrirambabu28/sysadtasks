#! /usr/bin/python

import requests
from bs4 import BeautifulSoup
import os,shutil
import re
import threading
import time
import sys
from selenium import webdriver
import pynotify
from time import sleep
from pySmartDL import SmartDL
import wget

def mainMenu() :
    print("HELLO PEPS")
    print("1. GO FOR MANGA :D")
    print("2. SONGS 1_1")
    print("3. ANIMAE ;)")
    print("4.QUIT :)")
    while True:
        try:
            sel=int(input("ENTER THE CHOICE: "))
            if sel==1:
                manga()
                break
            elif sel==2:
                songs()
                break
            elif sel==3:
                anime()
                break
            elif sel==4:
                break
            else:
                print("INVALID CHOICE. ENTER AGAIN BETWEEN 1 AND 4")
                mainMenu()
        except ValueError:
            print("INVAILD CHOICE. ENTER AGAIN")
    exit


def manga():
    #Search for the desired manga
    search = input('Enter name of manga: ')
    print ()
    search = search.split()
    search = ('+').join(search)
    search_url = 'http://manga.animea.net/series_old.php?title_range=0&title='+search+'&author_range=0&author=&artist_range=0&artist=&completed=0&yor_range=0&yor=&type=3&genre%5BAction%5D=0&genre%5BAdventure%5D=0&genre%5BComedy%5D=0&genre%5BDoujinshi%5D=0&genre%5BDrama%5D=0&genre%5BEcchi%5D=0&genre%5BFantasy%5D=0&genre%5BGender_Bender%5D=0&genre%5BHarem%5D=0&genre%5BHistorical%5D=0&genre%5BHorror%5D=0&genre%5BJosei%5D=0&genre%5BMartial_Arts%5D=0&genre%5BMature%5D=0&genre%5BMecha%5D=0&genre%5BMystery%5D=0&genre%5BPsychological%5D=0&genre%5BRomance%5D=0&genre%5BSchool_Life%5D=0&genre%5BSci-fi%5D=0&genre%5BSeinen%5D=0&genre%5BShotacon%5D=0&genre%5BShoujo%5D=0&genre%5BShoujo_Ai%5D=0&genre%5BShounen%5D=0&genre%5BShounen_Ai%5D=0&genre%5BSlice_of_Life%5D=0&genre%5BSmut%5D=0&genre%5BSports%5D=0&genre%5BSupernatural%5D=0&genre%5BTragedy%5D=0&genre%5BYaoi%5D=0&genre%5BYuri%5D=0&input=Search'

    #Getting search results and links
    sc0 = requests.get(search_url)
    soup0 = BeautifulSoup(sc0.text,'lxml')
    search_li = []
    search_result = soup0.findAll('ul',{'class':'mangalisttext'})
    k = 1
    for i in range(len(search_result)):
        res = search_result[i].find_all('a')
        for j in range(len(res)):
            print (str(k)+'. '+res[j].text)
            search_li.append(res[j].get('href'))
            k += 1
    print ()

    #Select the desired search result
    user_input = int(input('Enter your choice number: '))
    url_sel = 'http://manga.animea.net'+search_li[user_input-1]
    x = len(res[user_input - 1].text)
    sc = requests.get(url_sel)
    soup = BeautifulSoup(sc.text,'lxml')
    chap_list = soup.select('.col2 a')
    chap_list.reverse()
    link_list = []

    #Creating directory and Getting chapters
    os.makedirs(search+'_Manga', exist_ok=True)
    os.chdir('./'+search+'_Manga')
    source = os.listdir(os.getcwd())
    print ('No. of chapters in your selected manga :',len(chap_list))
    for i in range(len(chap_list)):
        link_list.append(chap_list[i].get('href'))
    chap_no = []
    chap_name = re.compile(r'\d+(.)?\d*')
    for li in chap_list:
        mo = chap_name.search(li.text[x+1:])
        mo1 = mo.group()
        chap_no.append(mo1)

    sample = input('Enter 1 for full download & Enter 2 for sample: ')
    if sample == '1':
        star = 0
        end = len(chap_list)
    elif sample == '2':
        star = 0
        end = star + 2

    '''
    #Ending Chapter
    end = input('Enter ending chapter: ')
    for i in range(len(chap_no)):
        if chap_no[i] == end:
            end = i
            break
    '''

    def mangaDown(startchap, endchap):
    #Downloading Images
        for chap in range(startchap, endchap):
            url_sel = 'http://manga.animea.net'+link_list[chap]
            sc1 = requests.get(url_sel)
            soup1 = BeautifulSoup(sc1.text,'lxml')
            opt = soup1.findAll('option')
            chap_pages = int(opt[-1].text)
            print ('Pages in chapter '+chap_no[chap]+' '+str(chap_pages))
            page = 1
            while True:
                if page > chap_pages:
                    break
                try:
                    for fi in source:
                        if fi[:-4] == 'C'+chap_no[chap]+'P'+str(page) :
                            print ('Skipping...')
                            page += 1
                            break
                    else:
                        sc2 = requests.get(url_sel[:-5]+'-page-'+str(page)+'.html')
                        soup2 = BeautifulSoup(sc2.text,'lxml')
                        img = soup2.select('td img')
                        image_url = img[0].get('src')
                        sc3 = requests.get(image_url)
                        print ('Downloading page '+str(page))
                        with open('C'+chap_no[chap]+'P'+str(page)+image_url[-4:], 'wb') as file:
                            file.write(sc3.content)
                        page += 1
                except requests.exceptions.ConnectionError:
                    continue 
                     
    #Setting Threading strides                
    threadOb = end - star
    if threadOb <= 10:
        z = 1
    elif threadOb > 10 and threadOb <= 50:
        z = 5
    elif threadOb > 50:
        z = 10

    #Creating and starting threads
    startTime = time.time()
    downloadThreads = []  
    count = 0
    for i in range(star,end, z):
        downloadThread = threading.Thread(target=mangaDown, args=(i, min(i + z,end+1)))
        downloadThreads.append(downloadThread)
        downloadThread.start()
        count += 1

    #Ending the program
    for downloadThread in downloadThreads:
        downloadThread.join()
    endTime = time.time()
    print('Done in '+str(endTime - startTime))
    anykey=input("ENTER ANYTHING TO RETURN TO MAIN MENU")
    mainMenu


def songs():

    print ('Enter 1 if you want to search for your desired song')
    print ('Enter 2 if you want to download songs from your list')
    print ('Enter 3 if you want to download billboard top 100 songs')

    while True:
        try:
            user_input = int(input('Enter your response: '))
            if user_input < 1 or user_input > 3:
                print ('Enter correct input')
                continue
            break
        except ValueError:
            print ('Enter correct input')
            continue

    #Download top 100 Songs from billboard
    if user_input == 3 :
        fw = open('.songs.txt','w')
        try:
            fr = open('.downloaded.txt','r')
            downloaded = fr.read()
            downloaded = downloaded.split('\n')
            fr.close()
        except FileNotFoundError:
            downloaded = []
        url1 = 'http://www.billboard.com/charts/hot-100'
        sc = requests.get(url1)
        soup1 = BeautifulSoup(sc.text,'lxml')
        li = soup1.findAll('h2',{'class':'chart-row__song'})
        art = soup1.findAll('h3',{'class':'chart-row__artist'})
        for i in range(len(li)):
            fw.write(li[i].text+' '+art[i].find('a').text.strip()+'\n')
        fw.close()

        fr = open('.songs.txt','r')
        songs = fr.read()
        songs = songs.split('\n')
        fa = open('.downloaded.txt','a')

        for x in songs:
            for y in downloaded:
                if x == y:
                    break
            else:
                url2 = 'https://www.youtube.com/results?search_query='+x
                sc =requests.get(url2)
                soup2 = BeautifulSoup(sc.text,'lxml')
                title = soup2.findAll('h3',{'class':'yt-lockup-title '})
                print ('Downloading...')
                os.system("youtube-dl --extract-audio --audio-format mp3 " + 'https://www.youtube.com'+title[0].find('a')['href'])
                print ('Downloaded.')
                fa.write(x+'\n')
        print ('Download Complete')   
        fr.close()
        fa.close()


    #Download songs from the file song.txt
    elif user_input == 2:
        #fr = open('.downloaded.txt','r')
        #downloaded = fr.read()
        #downloaded = downloaded.split('\n')
        #fr.close()
        songs = []
        print ('Enter song names to download and Enter nothing to exit')
        while True:
            song_name = input('Enter song name: ')
            if song_name != '':
                songs.append(song_name)
            else:
                if len(songs) == 0:
                    print ('Enter atleast one song')
                    continue
                else:
                    break
        #fa = open('.downloaded.txt','a')

        for x in songs:
          for y in downloaded:
            if x == y:
                break
            else:
                url2 = 'https://www.youtube.com/results?search_query='+x
                sc =requests.get(url2)
                soup2 = BeautifulSoup(sc.text,'lxml')
                title = soup2.findAll('h3',{'class':'yt-lockup-title '})
                print ('Downloading...')
                os.system("youtube-dl --extract-audio --audio-format mp3 " + 'https://www.youtube.com'+title[0].find('a')['href'])
                print ('Downloaded.')
                fa.write(x+'\n')
        print ('Download Complete')   
        #fa.close()

    #Search and download songs
    elif user_input == 1:
        #fa = open('.downloaded.txt','a')
        search = input('Enter the name of the song: ')
        url = 'https://www.youtube.com/results?search_query='+search
        sc =requests.get(url)
        soup = BeautifulSoup(sc.text,'lxml')
        title = soup.findAll('h3',{'class':'yt-lockup-title '})
        link = []
        for i in range(min(10,len(title))):
            link.append(title[i].find('a')['href'])
        for i in range(min(10,len(title))):
            print (str(i+1)+'. '+title[i].find('a').text)
        
        while True:
            try:
                user_input = int(input('Enter the song no. to download: '))
                if user_input not in range(1,11):
                    print ('Enter correct input')
                    continue
                break
            except NameError:
                print ('Enter correct input')
                continue

        print ('Downloading...')
        os.system("youtube-dl --extract-audio --audio-format mp3 " + 'https://www.youtube.com'+link[user_input-1])
        #fa.write(search+'\n')
        #fa.close()
    anykey=input("ENTER ANYTHING TO RETURN TO MAIN MENU")
    mainMenu()


def anime():

    #Getting search results
    anime_list = 'http://animeshow.tv/anime-list.html'
    sc = requests.get(anime_list)
    soup = BeautifulSoup(sc.text,'lxml')
    anime = soup.select('li a')
    search = raw_input('Enter anime name: ')
    j = 0
    animes = []
    for i in range(len(anime)):
        if search in anime[i].text.lower():
            animes.append(anime[i].get('href'))
            print str(j+1)+'. '+anime[i].text
            j += 1
            
    #Selecting the anime to download
    user_input = int(raw_input('Enter the anime no. to download: '))
    anime_url = animes[user_input-1]

    sc = requests.get(anime_url)
    soup = BeautifulSoup(sc.text,'lxml')
    li = soup.select('#episode-list-entry-tbl a')
    li.reverse()
    epi = re.compile(r'\d+')
    mo = epi.search(li[-1].text)
    episodes = int(mo.group())
    print 'No. of Episodes:',episodes
    select = int(raw_input('Enter episode to start: '))
    k =0

    #Downloading episodes
    for ep_no in range(select,episodes+1):
        print 'Downloading Episode',ep_no
        pynotify.init('test')
        n = pynotify.Notification('Episode '+str(ep_no)+' released','Firefox Will open Automatically and download will begin shortly')
        n.show()          
        url = 'http://9xbuddy.com/download?url='+li[k+2].get('href')
        driver = webdriver.Firefox()
        driver.get(url)
        sleep (15)
        down = driver.find_element_by_link_text('Download Now')
        href = down.get_attribute('href')
        wget.download(href)
        print '\nDownloaded Episode '+str(ep_no)
        k += 2
        driver.quit()

    print 'All Episodes Downloaded'
    anykey=input("ENTER ANYTHING TO RETURN TO MAIN MENU")
    mainMenu()

#main routine
mainMenu()
