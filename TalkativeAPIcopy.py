from curses import window
from datetime import datetime
from bs4 import BeautifulSoup as bs
import requests
import argparse
from random import randint 
import time
from tkinter import *
import wikipedia as wiki
import time 
from os import system

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
# US english
LANGUAGE = "en-US,en;q=0.5"

class Weather:   
    def get_weather_data(url):
        session = requests.Session()
        session.headers['User-Agent'] = USER_AGENT
        session.headers['Accept-Language'] = LANGUAGE
        session.headers['Content-Language'] = LANGUAGE
        html = session.get(url)
        # create a new soup
        soup = bs(html.text, "html.parser")
        # store all results on this dictionary
        result = {}
        # extract region
        result['region'] = soup.find("div", attrs={"id": "wob_loc"}).text
        # extract temperature now
        result['temp_now'] = soup.find("span", attrs={"id": "wob_tm"}).text
        # get the day and hour now
        result['dayhour'] = soup.find("div", attrs={"id": "wob_dts"}).text
        # get the actual weather
        result['weather_now'] = soup.find("span", attrs={"id": "wob_dc"}).text
        # get the precipitation
        result['precipitation'] = soup.find("span", attrs={"id": "wob_pp"}).text
        # get the % of humidity
        result['humidity'] = soup.find("span", attrs={"id": "wob_hm"}).text
        # extract the wind
        result['wind'] = soup.find("span", attrs={"id": "wob_ws"}).text
        # get next few days' weather
        next_days = []
        days = soup.find("div", attrs={"id": "wob_dp"})
        for day in days.findAll("div", attrs={"class": "wob_df"}):
            # extract the name of the day
            day_name = day.findAll("div")[0].attrs['aria-label']
            # get weather status for that day
            weather = day.find("img").attrs["alt"]
            temp = day.findAll("span", {"class": "wob_t"})
            # maximum temparature in Celsius, use temp[1].text if you want fahrenheit
            max_temp = temp[0].text
            # minimum temparature in Celsius, use temp[3].text if you want fahrenheit
            min_temp = temp[2].text
            next_days.append({"name": day_name, "weather": weather, "max_temp": max_temp, "min_temp": min_temp})
        # append to result
        result['next_days'] = next_days
        return result
    # print data
    def DataPrint(data):
        strorage=""
        strorage+="Weather for: {}".format(data["region"])
        #print("Now:", data["dayhour"])
        strorage+="\nNow: {}".format(data["dayhour"])
        #print(f"Temperature now: {data['temp_now']}°C")
        strorage+="\nTemperature now: {}°C".format(data["temp_now"])
        #print("Description:", data['weather_now'])
        strorage+="\nDescription: {}".format(data["weather_now"])
        #print("Precipitation:", data["precipitation"])
        strorage+="\nPrecipitation: {}".format(data["precipitation"])
        #print("Humidity:", data["humidity"])
        strorage+="\nHumidity: {}".format(data["humidity"])
        #print("Wind:", data["wind"])
        strorage+="\nWind: {}".format(data["wind"])
        #print("Next days:")
        strorage+="\nNext days: "
        for dayweather in data["next_days"]:
            #print("="*40, dayweather["name"], "="*40)
            strorage+="\n {} {} {}".format(("="*40),dayweather["name"],("="*40))
            #print("Description:", dayweather["weather"])
            strorage+="\n Description: {}".format(dayweather["weather"])
            #print(f"Max temperature: {dayweather['max_temp']}°C")
            strorage+="\n Max temperature: {}°C".format(dayweather["max_temp"])
            #print(f"Min temperature: {dayweather['min_temp']}°C")
            strorage+="\n Min temperature: {}°C".format(dayweather['min_temp'])
        return strorage
class Weathercall:
    def inputString(bemenet):   
        st="This city does not exist or you miswrote it!"
        bemenettömb=bemenet.split()
        def Ugyanaz(be, masikbe):
            for i in range(0,len(be)):
                if (be[i]==masikbe[i]):
                    return True
        Nagybetus=[]
        MegynitandoVaros=[]
        for i in range(0,len(bemenettömb)):
            if(bemenettömb[i][0].isupper()):
                Nagybetus.append(bemenettömb[i])
                MegynitandoVaros.append(f"City{bemenettömb[i][0]}.txt")
        #print(Nagybetus)
        #print(MegynitandoVaros)
        for k in range(0,len(bemenettömb)): 
            #print(f"Én vagyok a k:{k}")       
            for j in range(0,len(bemenettömb)):
                #print(f"Én vagyok a j:{j}") 
                if (Ugyanaz(bemenettömb[k],"weather")):
                    #print("Én vagyok az ellenőr") 
                    z=0;
                    if len(MegynitandoVaros)!=0 & z<=len(MegynitandoVaros):#Sajnos a subproces nem müködött
                        with open(MegynitandoVaros[z], "r+",encoding="utf-8")as f:
                            help=f.read()
                            lista=help.split("\n")
                        if (lista.__contains__(bemenettömb[j])):
                            URL = "https://www.google.com/search?lr=lang_en&ie=UTF-8&q=weather"
                            parser = argparse.ArgumentParser(description="Quick Script for Extracting Weather data using Google Weather")
                            parser.add_argument("region", nargs="?", help="""Region to get weather for, must be available region.
                                                                Default is your current location determined by your IP Address""", default="")
                            # parse arguments
                            args = parser.parse_args()    
                            region=bemenettömb[j]     
                            URL += region
                            # get data
                            data = Weather.get_weather_data(URL)
                            #Weather.DataPrint(data)
                            st=Weather.DataPrint(data)
                            z+=1
                            return st
                    elif len(MegynitandoVaros)==0:
                        URL = "https://www.google.com/search?lr=lang_en&ie=UTF-8&q=weather"
                        parser = argparse.ArgumentParser(description="Quick Script for Extracting Weather data using Google Weather")
                        parser.add_argument("region", nargs="?", help="""Region to get weather for, must be available region.
                                                            Default is your current location determined by your IP Address""", default="")
                        # parse arguments
                        args = parser.parse_args()    
                        region=args.region    
                        URL += region
                        # get data
                        data = Weather.get_weather_data(URL)
                        #Weather.DataPrint(data)
                        st=Weather.DataPrint(data)
                        z+=1
                        return st
        return st
class Joke:
    def Joke():   
        jokes=["Whoever said that the definition of insanity is doing the same thing over and over again and expecting different results has obviously never had to reboot a computer.", "Did you hear about the monkeys who shared an Amazon account? They were Prime mates.", "Why are iPhone chargers not called Apple Juice?!", "PATIENT: Doctor, I need your help. I'm addicted to checking my Twitter! DOCTOR: I'm so sorry, I don't follow.", "He: You are \';\' to me. She: I code in Python"]
        st=jokes[randint(0,len(jokes)-1)]
        return st
class Time:
    def current_time():
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        st=f"Actual time: {current_time}"
        return st
class WhoAmI:
    def Who():
        st1="I am just a program"#Én csak egy program vagyok
        return st1
    def Old():
        t = datetime.today()
        old="04-15-2022"
        oldtime=datetime.strptime(old,"%m-%d-%Y")
        deltatime=t-oldtime
        if(deltatime.days>365):
            st2=f"I born {round((deltatime.days)/365,2)} years ago."
        else:
            st2=f"I born {deltatime.days} days ago."
        return st2
    def Name():
        st3="My name is LAIS"
        return st3
class Info:
    def Info(bemenet):
        st=""
        #wiki first few row implementation
        bemenettömb=bemenet.split()
        #print(bemenettömb)
        Nagybetus=[]
        MegynitandoVaros=[]
        for i in range(0,len(bemenettömb)):
            if(bemenettömb[i][0].isupper()):
                Nagybetus.append(bemenettömb[i])
                MegynitandoVaros.append(f"City{bemenettömb[i][0]}.txt")
        for k in range(0,len(bemenettömb)): 
            #print(f"Én vagyok a k:{k}")       
            for j in range(0,len(bemenettömb)):
                #print(f"Én vagyok a j:{j}") 
                if (bemenettömb[k]=="info"):
                    #print("Én vagyok az ellenőr") 
                    z=0;
                    if len(MegynitandoVaros)!=0 & z<=len(MegynitandoVaros):
                        with open(MegynitandoVaros[z], "r+",encoding="utf-8")as f:
                            help=f.read()
                            lista=help.split("\n")
                        if (lista.__contains__(bemenettömb[j])):
                            #st+="{}\n".format(("="*60))
                            st+=wiki.summary(bemenettömb[j])
                            #st+="{}\n".format(("="*60))   
                            z+=1
                    elif len(MegynitandoVaros)==0:
                        def IP(): 
                            response = requests.get('https://api64.ipify.org?format=json').json()
                            ip_address =response["ip"]
                            #print(ip_address)
                            #print(f"1: {ip_address}")
                            response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
                            location_data = response.get("city")
                            return location_data
                        tester=IP()
                        #print(tester)
                        if((tester=="Debrecen")|(tester=="debrecen")):
                            checker=IP()
                            #print(checker)
                            #st+="{}\n".format(("="*60))
                            st+=wiki.summary(checker)
                            #st+="{}\n".format(("="*60))   
                        else:
                            #print(tester)
                            #st="{}\n".format(("="*60))
                            st+=f"{wiki.summary(tester)}\n"
                            #st+="{}".format(("="*60))
                            z+=1
                    else:
                        st+="Something went wrong"
        return st        
class Main:
    def WhatIsIt(bemenet):
        bemenetcopy=bemenet.lower()
        bemenettömb=bemenetcopy.split()
        if(bemenettömb.__contains__("weather")):
            st=Weathercall.inputString(bemenet)
            return st
        elif(bemenettömb.__contains__("joke")):
            st=Joke.Joke()
            system("say "+st)
            return st
        elif(bemenettömb.__contains__("time") & (bemenettömb.__contains__("weather")==True)):
            st=Weathercall.inputString(bemenet)
            return st
        elif(bemenettömb.__contains__("info")):
            st=Info.Info(bemenet)
            return st     
        elif(bemenettömb.__contains__("time")):
            st=Time.current_time()
            system("say "+st)
            return st  
        elif(bemenettömb.__contains__("old")|bemenettömb.__contains__("who")):
            if(bemenettömb.__contains__("old")):
                st=WhoAmI.Old()
                system("say "+st)
                return st  
            else:
                st=WhoAmI.Who()
                system("say "+st)
                return st  
        elif(bemenettömb.__contains__("name")):
            st=WhoAmI.Name()
            system("say "+st)
            return st  
        else:
            st="Sorry, I am not capable answearing that question! :("
            system("say "+st)
            return st
    
window=Tk()
window.geometry("822x722")
window.title("Creativ machine")
window.configure(bg="Green")
label=Label(window,text="Ask something:", font=("Times New Roman", 30,"bold"),fg="Black")
label.configure(bg="Green")
ent=Entry(window)
out=Text(window, fg = "black",bg="White", cursor="hand", font=("Times New Roman", 16,"bold") ,width=500,height=500, yscrollcommand=True,spacing1=2)
out.insert(INSERT,"Hello...")
bemenet=""
def bekero():
    bemenet=ent.get()
    #print(bemenet)
    #bemenet[0].lower()
    help=Main.WhatIsIt(bemenet)
    #print(help)
    Settext(help)
def Settext(text):
    out.delete('1.0',END)
    out.insert(INSERT,text)
def Clear():
    ent.delete(0,END)
    out.delete('1.0',END)
label.pack()
btns_frame = Frame(window, bg="Green",border=0)
ent.pack(expand=True,ipadx=100,ipady=0)
btns_frame.pack(expand=True,ipadx=0,ipady=0)
out.pack(expand=True)#, width = 9, height = 3
aff=Button(btns_frame, text = "Talk",font=("Times New Roman", 16,"bold"),border=0,fg = "Black", width = 10,height=1,bd = 0, bg = "Green", cursor = "hand2", command =lambda:bekero()).grid(row = 0, column = 0, columnspan = 1, padx = 1, pady = 1) 
clear=Button(btns_frame,text="Clear",font=("Times New Roman", 16,"bold"), border=0,fg = "Black", width = 10,height=1,bd = 0, bg = "Green", cursor = "hand2", command=lambda:Clear()).grid(row = 0, column = 5, columnspan = 1, padx = 1, pady = 1)
window.mainloop()

    