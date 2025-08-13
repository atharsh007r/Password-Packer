import mysql.connector
import time as t
import pandas as pd
import os
from datetime import *
from datetime import date
import pwinput as pp
from colorama import Fore

u=[]
p=[]
s=[]
d=[]
ti=[]

passw=pp.pwinput(prompt='Enter Database Password :  ', mask="\N{skull}")
os.system('cls')
conn = mysql.connector.connect(host = "localhost",user = "root",password =passw,database="atharsh")
curr = conn.cursor()

def clear():
    global u,p,s,d,ti
    u=[]
    p=[]
    s=[]
    d=[]
    ti=[]
    
def show(x = None):
    clear()
    if x !=  None:
        curr.execute(f"select * from passwords where site = '{x}';")
    else:
        curr.execute("select * from passwords")
    for i in curr:
        s.append(i[0])
        u.append(i[1])
        p.append(i[2])
        d.append(i[3])
        ti.append(str(i[4]))
    df=pd.DataFrame({'      SITE      ':s,
                     '      USERNAME        ':u,
                     '      PASSWORD        ':p,
                     '      ENTRY_DATE      ':d,
                     '      ENTRY_TIME      ':ti})
    print(df)

def entry():
    print("Enter 'clg' for clg google account / 'per' for personal account\n")
    con="y"
    while con=="y":
        tt = t.strftime("%H:%M:%S", t.localtime())
        today = date.today()
        print("Enter values (site, un, pw) : ", end="")
        site, uname, pw = input().split()
        if uname=="clg":
            uname="22202001@rmd.ac.in"
        if uname=="per":
            uname="atharshatharsh007@gmail.com"
        curr.execute("INSERT INTO passwords VALUES (%s, %s, %s,%s,%s)", (site, uname, pw,str(today),str(tt)))
        conn.commit()
        print("ENTERED SUCCESFULLY ^_^\n")
        print("Wanna enter another one..? (y/n) : ",end="")
        con=input()
        print("\n")

def update():
    show()
    print("\nEnter the site name : ",end="")
    qr1=input().strip()
    os.system('cls')
    show(qr1)
    update2("ds")

def update2(x = None):
    if x == None:
        show()
    qr1 = int(input("Select the index: "))
    qr2 = input("Enter new password : ").strip()
    curr.execute(f"update passwords set password='{qr2}' where username='{u[qr1]}' and password='{p[qr1]}' and site='{s[qr1]}';")
    conn.commit()
    print("Updated Successfully \N{skull} ")
    
def dele():
    print("Enter the site : ",end="")
    qr=input().strip()

    try:
        curr.execute("delete from passwords where username=\""+qr+"\";")
        conn.commit()
    except:
        pass
    try:
        curr.execute("delete from passwords where password=\""+qr+"\";")
        conn.commit()
    except:
        pass

def search():
    print("Enter the site name : ",end="")
    sr=input()
    curr.execute(f"select * from passwords where site='{sr}';")
    for i in curr:
        s.append(i[0])
        u.append(i[1])
        p.append(i[2])
        d.append(i[3])
        ti.append(i[4])
    df=pd.DataFrame({'      SITE      ':s,'      USERNAME      ':u,'      PASSWORD      ':p,'      ENTRY_DATE      ':d,'      ENTRY_TIME      ':ti})
    print(df)

def getchoice():
    print("SELECT FROM THE BELOW \n1.Show all passwords\n2.Enter new Password\n3.Search passwords\n4.Delete a password\n5.Update a password")
    ch=int(input("Enter Your Choice : "))
    if(ch==1):
         os.system('cls')
         show()
         t.sleep(15)
    elif(ch==2):
        os.system('cls')
        entry()
        t.sleep(2)
    elif(ch==3):
        os.system('cls')
        search()
        t.sleep(5)
    elif(ch==4):
        os.system('cls')
        dele()
        t.sleep(5)
    elif(ch==5):
        os.system('cls')
        print("Update methods available :\n1.Search Update\n2.Index Update\nEnter the update type : ",end="")
        n = int(input())
        if(n==1):
            update()
        else:
            update2()
        t.sleep(5)
    else:
        os.system('cls')
        print(Fore.RED+"Please Enter a valid choice "+"\N{skull}"+Fore.WHITE)
        t.sleep(2)
        os.system('cls')
        getchoice()
    
getchoice()
conn.close()