# WhatBreach

WhatBreach is a tool to search for breached emails and their corresponding database. It takes either a single email or a list of emails and searches them leveraging [haveibeenpwned.com](https://haveibeenpwned.com)'s API, from there (if there are any breaches) it will search for the query link on Dehashed pertaining to the database, and output all breaches along with all pastes that this email is included in (if any). If you are trying to find the database, passing a certain flag will also attempt to download available freely public databases from [databases.today](https://databases.today). If the query is found within the publicly listed it will download the database for you and save it into the projects home folder which will be located under `~/.whatbreach_home/downloads`.

# Examples

As an example we will use `user@gmail.com` as the example search:

```
(venv) admin@Hades:~/whatbreach$ python whatbreach.py -e "user@gmail.com"
[ i ] starting search on single email address: user@gmail.com
[ i ] searching breached accounts on HIBP related to: user@gmail.com
[ i ] searching for paste dumps on HIBP related to: user@gmail.com
[ i ] found a total of 67 database breach(es) and a total of 59 paste(s) pertaining to: user@gmail.com
------------------------------------------------------------------------------------
Breached Site:	     | Database Link:
Paste#26             | https://pastebin.com/b0zdYUzc 
Paste#27             | https://pastebin.com/C6YUMUxk 
Paste#24             | https://pastebin.com/JFvBG4HW 
Paste#25             | https://pastebin.com/hi5yXRCn 
Paste#22             | https://pastebin.com/mVrrDb9d 
Paste#23             | https://pastebin.com/jBCPwT1e 
Paste#20             | https://pastebin.com/uyG5ggf8 
Paste#21             | https://pastebin.com/QrudBvXf 
Paste#28             | https://pastebin.com/6fZtANAb 
Paste#29             | https://pastebin.com/gffDmJ5X 
...                  | ...  # truncated to save space
Paste#13             | https://pastebin.com/RLVk8j3E 
Paste#12             | https://pastebin.com/zaN47ZZJ 
Paste#11             | https://pastebin.com/k193QzRG 
Paste#10             | https://pastebin.com/Qhaf51b6 
Paste#17             | http://siph0n.in/exploits.php?id=4440
Paste#16             | https://pastebin.com/j7YX2sJm 
Paste#15             | https://pastebin.com/Sin9fR7f 
Paste#14             | https://pastebin.com/jvSgnZkK 
Paste#19             | https://pastebin.com/2rVemphh 
VK                   | https://www.dehashed.com/search?query=VK
ArmyForceOnline      | https://www.dehashed.com/search?query=ArmyForceOnline
Gawker               | https://www.dehashed.com/search?query=Gawker
Paste#9              | http://www.pemiblanc.com/test.txt
Paste#8              | https://pastebin.com/EGS77pC4 
Paste#7              | https://pastebin.com/pQdmx6mc 
Paste#6              | https://pastebin.com/ZwUh4tcG 
Paste#5              | https://pastebin.com/RkdC5arB 
MySpace              | https://www.dehashed.com/search?query=MySpace
Paste#3              | https://pastebin.com/GUV70Jqa 
Paste#2              | https://pastebin.com/2eENex9n 
Paste#1              | https://pastebin.com/rSd85uLK 
Onverse              | https://www.dehashed.com/search?query=Onverse
------------------------------------------------------------------------------------
```

You also have the option to suppress the discovered pastes:

```
(venv) admin@Hades:~/whatbreach$ python whatbreach.py -e "user@gmail.com" -nP
[ i ] starting search on single email address: user@gmail.com
[ i ] searching breached accounts on HIBP related to: user@gmail.com
[ i ] searching for paste dumps on HIBP related to: user@gmail.com
[ w ] suppressing discovered pastes
[ i ] found a total of 67 database breach(es) and a total of 0 paste(s) pertaining to: user@gmail.com
------------------------------------------------------------------------------------
Breached Site:	     | Database Link:
Dropbox              | https://www.dehashed.com/search?query=Dropbox
Leet                 | https://www.dehashed.com/search?query=Leet
MySpace              | https://www.dehashed.com/search?query=MySpace
MyHeritage           | https://www.dehashed.com/search?query=MyHeritage
ArmyForceOnline      | https://www.dehashed.com/search?query=ArmyForceOnline
17Media              | https://www.dehashed.com/search?query=17Media
Xbox360ISO           | https://www.dehashed.com/search?query=Xbox360ISO
LinkedIn             | https://www.dehashed.com/search?query=LinkedIn
QuinStreet           | https://www.dehashed.com/search?query=QuinStreet
Bookmate             | https://www.dehashed.com/search?query=Bookmate
...                  | ... # truncated to save space
Dubsmash             | https://www.dehashed.com/search?query=Dubsmash
MangaFox             | https://www.dehashed.com/search?query=MangaFox
FashionFantasyGame   | https://www.dehashed.com/search?query=FashionFantasyGame
Trillian             | https://www.dehashed.com/search?query=Trillian
Disqus               | https://www.dehashed.com/search?query=Disqus
NemoWeb              | https://www.dehashed.com/search?query=NemoWeb
Gawker               | https://www.dehashed.com/search?query=Gawker
CashCrate            | https://www.dehashed.com/search?query=CashCrate
Tumblr               | https://www.dehashed.com/search?query=Tumblr
PoliceOne            | https://www.dehashed.com/search?query=PoliceOne
Onverse              | https://www.dehashed.com/search?query=Onverse
Interpals            | https://www.dehashed.com/search?query=Interpals
Seedpeer             | https://www.dehashed.com/search?query=Seedpeer
HeroesOfNewerth      | https://www.dehashed.com/search?query=HeroesOfNewerth
Bell2017             | https://www.dehashed.com/search?query=Bell2017
------------------------------------------------------------------------------------
```

As well as the discovered databases:

```
(venv) admin@Hades:~/whatbreach$ python whatbreach.py -e "user@gmail.com" -nD
[ i ] starting search on single email address: user@gmail.com
[ i ] searching breached accounts on HIBP related to: user@gmail.com
[ i ] searching for paste dumps on HIBP related to: user@gmail.com
[ i ] found a total of 67 database breach(es) and a total of 59 paste(s) pertaining to: user@gmail.com
[ w ] suppressing discovered databases
-----------------------------------------------------------------------
Breached Site:	     | Database Link:
Paste#26             | https://pastebin.com/b0zdYUzc 
Paste#27             | https://pastebin.com/C6YUMUxk 
Paste#24             | https://pastebin.com/JFvBG4HW 
Paste#25             | https://pastebin.com/hi5yXRCn 
Paste#22             | https://pastebin.com/mVrrDb9d 
Paste#23             | https://pastebin.com/jBCPwT1e 
...                  | ... # truncated to save space
Paste#9              | http://www.pemiblanc.com/test.txt
Paste#8              | https://pastebin.com/EGS77pC4 
Paste#7              | https://pastebin.com/pQdmx6mc 
Paste#6              | https://pastebin.com/ZwUh4tcG 
Paste#5              | https://pastebin.com/RkdC5arB 
Paste#4              | https://pastebin.com/4qH2fRMc 
Paste#3              | https://pastebin.com/GUV70Jqa 
Paste#2              | https://pastebin.com/2eENex9n 
Paste#1              | https://pastebin.com/rSd85uLK 
Paste#52             | https://pastebin.com/ffkjfRrY 
Paste#48             | http://balockae.online/files/Lizard Stresser.txt
Paste#49             | https://pastebin.com/bUq60ZKA 
Paste#44             | http://siph0n.in/exploits.php?id=3667
Paste#45             | https://pastebin.com/MAFfXwGA 
Paste#46             | http://pxahb.xyz/emailpass/www.chocolate.at.txt
Paste#47             | https://pastebin.com/zchq7iQS 
Paste#40             | https://pastebin.com/sj9eyM5w 
Paste#41             | https://pastebin.com/wY9ghBM9 
Paste#42             | https://pred.me/gmail.html    
Paste#43             | https://pastebin.com/AnTUDMtj 
-----------------------------------------------------------------------
```

I have also implemented the ability to search through a list of email addresses and check for the possibility of the email being a "Ten minute email", it will prompt you to continue if the email is found, since the possibility of using this email is next to none:

```
(venv) admin@Hades:~/whatbreach$ python whatbreach.py -l test.txt -cT
[ i ] parsing email file: test.txt
[ i ] starting search on a total of 3 email(s)
[ i ] searching breached accounts on HIBP related to: user@gmail.com
[ i ] searching for paste dumps on HIBP related to: user@gmail.com
[ i ] found a total of 67 database breach(es) and a total of 59 paste(s) pertaining to: user@gmail.com
------------------------------------------------------------------------------------
Breached Site:	     | Database Link:
Paste#26             | https://pastebin.com/b0zdYUzc 
Paste#27             | https://pastebin.com/C6YUMUxk 
Paste#24             | https://pastebin.com/JFvBG4HW 
Paste#25             | https://pastebin.com/hi5yXRCn 
Paste#22             | https://pastebin.com/mVrrDb9d 
Paste#23             | https://pastebin.com/jBCPwT1e 
Paste#20             | https://pastebin.com/uyG5ggf8 
Paste#21             | https://pastebin.com/QrudBvXf 
R2Games              | https://www.dehashed.com/search?query=R2Games
NemoWeb              | https://www.dehashed.com/search?query=NemoWeb
Disqus               | https://www.dehashed.com/search?query=Disqus
Adobe                | https://www.dehashed.com/search?query=Adobe
...                  | ... # truncated to save space
Paste#15             | https://pastebin.com/Sin9fR7f 
Paste#14             | https://pastebin.com/jvSgnZkK 
Paste#19             | https://pastebin.com/2rVemphh 
VK                   | https://www.dehashed.com/search?query=VK
ArmyForceOnline      | https://www.dehashed.com/search?query=ArmyForceOnline
Gawker               | https://www.dehashed.com/search?query=Gawker
Paste#9              | http://www.pemiblanc.com/test.txt
Paste#8              | https://pastebin.com/EGS77pC4 
Paste#7              | https://pastebin.com/pQdmx6mc 
Paste#6              | https://pastebin.com/ZwUh4tcG 
Paste#5              | https://pastebin.com/RkdC5arB 
MySpace              | https://www.dehashed.com/search?query=MySpace
Paste#3              | https://pastebin.com/GUV70Jqa 
Paste#2              | https://pastebin.com/2eENex9n 
Paste#1              | https://pastebin.com/rSd85uLK 
Onverse              | https://www.dehashed.com/search?query=Onverse
------------------------------------------------------------------------------------
[ w ] email: user@0815.ru0clickemail.com appears to be a ten minute email
[ ? ] would you like to process the email[y/N]: n
[ i ] searching breached accounts on HIBP related to: someuser@gmail.com
[ i ] searching for paste dumps on HIBP related to: someuser@gmail.com
[ i ] found a total of 6 database breach(es) and a total of 4 paste(s) pertaining to: someuser@gmail.com
----------------------------------------------------------------------------
Breached Site:	     | Database Link:
Adobe                | https://www.dehashed.com/search?query=Adobe
Paste#4              | http://xn--e1alhsoq4c.xn--p1ai/base/Gmail.txt
Paste#3              | https://pastebin.com/GUV70Jqa 
Paste#2              | https://pred.me/gmail.html    
Paste#1              | https://pastebin.com/VVgL8Fzp 
NemoWeb              | https://www.dehashed.com/search?query=NemoWeb
----------------------------------------------------------------------------
```

The program is pretty straight forward but for simplicity I have provided the acceptable arguments below:

```
(venv) admin@Hades:~/whatbreach$ python whatbreach.py --help
usage: whatbreach.py [-h] [-e EMAIL] [-l PATH] [-nD] [-nP] [-cT] [-d]

optional arguments:
  -h, --help            show this help message and exit

mandatory opts:
  -e EMAIL, --email EMAIL
                        Pass a single email to scan for
  -l PATH, -f PATH, --list PATH, --file PATH
                        Pass a file containing emails one per line to scan

search opts:
  -nD, --no-dehashed    Suppres dehashed output
  -nP, --no-pastebin    Suppress Pastebin output

misc opts:
  -cT, --check-ten-minute
                        Check if the provided email address is a ten minute
                        email or not
  -d, --download        Attempt to download the database if there is one
                        available
```

# Installation

Installing is extremely easy, just run `pip install -r requirements.txt`

# Why?

During my time in information technology, during researching and doing OSINT, I have noticed a need to find email addresses as well as their password. I have found reliable tools that do this successfully and make the process quick and easy, however I have not found a tool that meets my exact requirements. This tool is basically my own personal take on how I think email searching should work and ties in the database searching and database downloading as well. What better way to break into an email then to have the possible password as well as all _known_ breaches it's been seen in?

# TODO:/

 - Add [domain searching](https://twitter.com/CryptoCypher/status/1119344370036113409) while using dehashed so that we can search for everything related to the domain instead of the specific breach
 - Add the ability to use cookies so we can download out of dehashed
 - Add a pretty banner, who doesn't like a pretty banner?
 - Add more database searches
 - Check the databases for hashes and verify the hash type, maybe store the hashes into a file for cracking?

# Shoutouts

 - [NullArray](https://github.com/NullArray) for providing me with the idea for the hash checking and the idea for the databases.today downloads, as well as being an awesome and supportive person at all times.