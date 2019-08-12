# WhatBreach

WhatBreach is an OSINT tool that simplifies the task of discovering what breaches an email address has been discovered in. WhatBreach provides a simple and effective way to search either multiple, or a single email address and discover all known breaches that this email has been seen in. From there WhatBreach is capable of downloading the database if it is publicly available, downloading the pastes the email was seen in, or searching the domain of the email for further investigation. To perform this task successfully WhatBreach takes advantage of the following websites and/or API's:

 - WhatBreach takes advantage of [haveibeenpwned.com](https://haveibeenpwned.com/)'s API. HIBP's API is no longer free and costs 3.50 USD per month. To get an API key please see [here](https://haveibeenpwned.com/API/Key)
 - WhatBreach takes advantage of [dehashed.com](https://dehashed.com/) in order to discover if the database has been seen in a breach before. WhatBreach provides a link to a dehashed search for effective downloading
 - WhatBreach takes advantage of [hunter.io](https://hunter.io/)'s API (requires free API token) this allows simple and effective domain searching and will provide further information on the domain being searched along with store the discovered results in a file for later processing
 - WhatBreach takes advantage of pastes from [pastebin.com](https://pastebin.com/) that have been found from HIBP. It will also provide a link to the paste that the breach was seen in and is capable of downloading the raw paste if requested
 - WhatBreach takes advantage of [databases.today](https://databases.today/) to download the databases off the website. This allows a simple and effective way of downloading databases without having to search manually
 - WhatBreach takes advantage of [weleakinfo.com](https://weleakinfo.com/)'s API (requires free API token) this provides an extra search for the email in order to discover even more public breaches
 - WhatBreach takes advantage of [emailrep.io/](https://emailrep.io/)'s simple open API to search for possible profiles associated with an email, it also dumps all information discovered into a file for further processing

Some interesting features of WhatBreach include the following:
 
 - Ability to detect if the email is a ten minute email or not and prompt to process it or not
 - Check the email for deliverable status using hunter.io
 - Ability to throttle the requests in order to help prevent HIBP from blocking you
 - Download the databases (since they are large) into a directory of your choice
 - Search either a single email or a text file containing one email per line

# Examples

Help page:
```
usage: whatbreach.py [-h] [-e EMAIL] [-l PATH] [-nD] [-nP] [-sH] [-wL] [-dP]
                     [-vH] [-cT] [-d] [-s DIRECTORY-PATH] [--throttle TIME]

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
  -sH, --search-hunter  Search hunter.io with a provided email address and
                        query for all information, this will process all
                        emails found as normal
  -wL, --search-weleakinfo
                        Search weleakinfo.com as well as HIBP for results

misc opts:
  -dP, --download-pastes
                        Download pastes associated with the email address
                        found (if any)
  -vH, --verify-hunter  Verify the emails found on hunter.io for deliverable
                        status
  -cT, --check-ten-minute
                        Check if the provided email address is a ten minute
                        email or not
  -d, --download        Attempt to download the database if there is one
                        available
  -s DIRECTORY-PATH, --save-dir DIRECTORY-PATH
                        Pass a directory to save the downloaded databases into
                        instead of the `HOME` path
  --throttle TIME       Throttle the HIBP requests to help prevent yourself
                        from being blocked

```

Simple email search:
```
python whatbreach.py -e user1337@gmail.com

	                                                    _____ 
	   _ _ _ _       _   _____                 _       |___  |
	  | | | | |_ ___| |_| __  |___ ___ ___ ___| |_       |  _|
	  | | | |   | .'|  _| __ -|  _| -_| .'|  _|   |      |_|  
	  |_____|_|_|__,|_| |_____|_| |___|__,|___|_|_|[][][]|_|
	Find emails and their associated leaked databases.. v0.1.5


[ i ] starting search on single email address: user1337@gmail.com
[ i ] searching breached accounts on HIBP related to: user1337@gmail.com
[ i ] searching for paste dumps on HIBP related to: user1337@gmail.com
[ i ] found a total of 9 database breach(es) pertaining to: user1337@gmail.com
---------------------------------------------------------------------------
Breach/Paste:	     | Database/Paste Link:
Dailymotion          | https://www.dehashed.com/search?query=Dailymotion
500px                | https://www.dehashed.com/search?query=500px
LinkedIn             | https://www.dehashed.com/search?query=LinkedIn
MyFitnessPal         | https://www.dehashed.com/search?query=MyFitnessPal
Bolt                 | https://www.dehashed.com/search?query=Bolt
Dropbox              | https://www.dehashed.com/search?query=Dropbox
Lastfm               | https://www.dehashed.com/search?query=Lastfm
Apollo               | https://www.dehashed.com/search?query=Apollo
OnlinerSpambot       | N/A                           
---------------------------------------------------------------------------
```

Searching with weleakinfo and haveibeenpwned:
```
python whatbreach.py -e user1337@gmail.com -wL

	                                                    _____ 
	   _ _ _ _       _   _____                 _       |___  |
	  | | | | |_ ___| |_| __  |___ ___ ___ ___| |_       |  _|
	  | | | |   | .'|  _| __ -|  _| -_| .'|  _|   |      |_|  
	  |_____|_|_|__,|_| |_____|_| |___|__,|___|_|_|[][][]|_|
	Find emails and their associated leaked databases.. v0.1.5


[ i ] starting search on single email address: user1337@gmail.com
[ i ] searching breached accounts on HIBP related to: user1337@gmail.com
[ i ] searching for paste dumps on HIBP related to: user1337@gmail.com
[ i ] searching weleakinfo.com for breaches related to: user1337@gmail.com
[ i ] discovered a total of 12 more breaches from weleakinfo.com
[ i ] found a total of 21 database breach(es) pertaining to: user1337@gmail.com
[ w ] large amount of database breaches, obtaining links from dehashed (this may take a minute)
-------------------------------------------------------------------------------
Breach/Paste:	     | Database/Paste Link:
Pesfan.com           | https://www.dehashed.com/search?query=Pesfan.com
Dailymotion          | https://www.dehashed.com/search?query=Dailymotion
Apollo               | https://www.dehashed.com/search?query=Apollo
MyFitnessPal         | https://www.dehashed.com/search?query=MyFitnessPal
500px                | https://www.dehashed.com/search?query=500px
Collection 4         | https://www.dehashed.com/search?query=Collection 4
OnlinerSpambot       | N/A                           
LinkedIn             | https://www.dehashed.com/search?query=LinkedIn
Dropbox.com          | https://www.dehashed.com/search?query=Dropbox.com
500px.com            | https://www.dehashed.com/search?query=500px.com
Dailymotion.com      | https://www.dehashed.com/search?query=Dailymotion.com
Last.fm March 2012   | https://www.dehashed.com/search?query=Last.fm March 2012
Dropbox              | https://www.dehashed.com/search?query=Dropbox
Myfitnesspal.com     | https://www.dehashed.com/search?query=Myfitnesspal.com
Collection 1         | https://www.dehashed.com/search?query=Collection 1
Collection 2         | https://www.dehashed.com/search?query=Collection 2
Bolt.cd              | https://www.dehashed.com/search?query=Bolt.cd
Lastfm               | https://www.dehashed.com/search?query=Lastfm
Bolt                 | https://www.dehashed.com/search?query=Bolt
Collection 3         | https://www.dehashed.com/search?query=Collection 3
LinkedIn.com         | https://www.dehashed.com/search?query=LinkedIn.com
-------------------------------------------------------------------------------
```

Downloading public databases:
```
python whatbreach.py -e user1337@gmail.com -d

	                                                    _____ 
	   _ _ _ _       _   _____                 _       |___  |
	  | | | | |_ ___| |_| __  |___ ___ ___ ___| |_       |  _|
	  | | | |   | .'|  _| __ -|  _| -_| .'|  _|   |      |_|  
	  |_____|_|_|__,|_| |_____|_| |___|__,|___|_|_|[][][]|_|
	Find emails and their associated leaked databases.. v0.1.5


[ i ] starting search on single email address: user1337@gmail.com
[ i ] searching breached accounts on HIBP related to: user1337@gmail.com
[ i ] searching for paste dumps on HIBP related to: user1337@gmail.com
[ i ] found a total of 9 database breach(es) pertaining to: user1337@gmail.com
---------------------------------------------------------------------------
Breach/Paste:	     | Database/Paste Link:
Dailymotion          | https://www.dehashed.com/search?query=Dailymotion
500px                | https://www.dehashed.com/search?query=500px
LinkedIn             | https://www.dehashed.com/search?query=LinkedIn
MyFitnessPal         | https://www.dehashed.com/search?query=MyFitnessPal
Bolt                 | https://www.dehashed.com/search?query=Bolt
Dropbox              | https://www.dehashed.com/search?query=Dropbox
Lastfm               | https://www.dehashed.com/search?query=Lastfm
Apollo               | https://www.dehashed.com/search?query=Apollo
OnlinerSpambot       | N/A                           
---------------------------------------------------------------------------
[ i ] searching for downloadable databases using query: dailymotion
[ w ] no databases appeared to be present and downloadable related to query: Dailymotion
[ i ] searching for downloadable databases using query: 500px
[ w ] no databases appeared to be present and downloadable related to query: 500px
[ i ] searching for downloadable databases using query: linkedin
[ ? ] discovered publicly available database for query LinkedIn, do you want to download [y/N]: n
[ i ] skipping download as requested
[ w ] no databases appeared to be present and downloadable related to query: LinkedIn
[ i ] searching for downloadable databases using query: myfitnesspal
[ w ] no databases appeared to be present and downloadable related to query: MyFitnessPal
[ i ] searching for downloadable databases using query: bolt
[ w ] no databases appeared to be present and downloadable related to query: Bolt
[ i ] searching for downloadable databases using query: dropbox
[ ? ] discovered publicly available database for query Dropbox, do you want to download [y/N]: n
[ i ] skipping download as requested
[ w ] no databases appeared to be present and downloadable related to query: Dropbox
[ i ] searching for downloadable databases using query: lastfm
[ ? ] discovered publicly available database for query Lastfm, do you want to download [y/N]: n
[ i ] skipping download as requested
[ w ] no databases appeared to be present and downloadable related to query: Lastfm
[ i ] searching for downloadable databases using query: apollo
[ w ] no databases appeared to be present and downloadable related to query: Apollo
[ i ] searching for downloadable databases using query: onlinerspambot
[ w ] no databases appeared to be present and downloadable related to query: OnlinerSpambot
```

Using hunter.io for domain hunting and throttling the requests to attempt prevention of HIBP from blocking you:
```
python whatbreach.py -e user1337@fbi.com -sH --throttle 35

	                                                    _____ 
	   _ _ _ _       _   _____                 _       |___  |
	  | | | | |_ ___| |_| __  |___ ___ ___ ___| |_       |  _|
	  | | | |   | .'|  _| __ -|  _| -_| .'|  _|   |      |_|  
	  |_____|_|_|__,|_| |_____|_| |___|__,|___|_|_|[][][]|_|
	Find emails and their associated leaked databases.. v0.1.5


[ i ] starting search on hunter.io using user1337@fbi.com
[ i ] discovered a total of 11 email(s)
[ i ] information discovered associated with fbi.com
[ i ] discovered possible pattern to emails: {first}.{last}@fbi.com
[ w ] did not discover any associated phone number(s)
[ i ] discovered associated email address(es):
	-> user1337@fbi.com
	-> blackeagle@fbi.com
	-> jillian.cartwright@fbi.com
	-> management@fbi.com
	-> info@fbi.com
	-> fmulder@fbi.com
	-> markamorgan@fbi.com
	-> james.bond@fbi.com
	-> robert.mueller@fbi.com
[ w ] hit maximum length, total of 1 not displayed
[ i ] discovered associated external URL(s):
	-> http://jobsnotification.blogspot.com/2011/03/ifbi-pgdbo-admission-2011-pg-diploma-in.html
	-> http://complaintsboard.com/complaints/fbi-robert-s-muelleriii-huber-heights-ohio-c121118.html
	-> http://user.xmission.com/~daina/known_scammers.html
	-> http://anonymousxwrites.blogspot.com/2012/02
	-> http://boingboing.net/2012/02/14
	-> http://joewein.net/dbl-update/2014-06/2014-06-22.htm
	-> http://anonymousxwrites.blogspot.fr/2012/02/federal-bureau-of-investigation-fbi-yet.html
	-> http://anonymousxwrites.blogspot.sg/2012/02
	-> http://meg-golpistasvirtuais.blogspot.fr/2013/04/update-emails-addresses-scammers-dia.html
[ w ] hit maximum length, total of 35 not displayed
[ i ] dumping all information into json file for further processing
[ i ] information written to: /Users/admin/.whatbreach_home/downloads/json_dumps/cbNcFiXZsU_fbi.com.json
[ i ] searching breached accounts on HIBP related to: user1337@fbi.com
[ i ] searching for paste dumps on HIBP related to: user1337@fbi.com
[ ! ] email user1337@fbi.com was not found in any breach
[ i ] searching breached accounts on HIBP related to: blackeagle@fbi.com
[ i ] searching for paste dumps on HIBP related to: blackeagle@fbi.com
[ ! ] email blackeagle@fbi.com was not found in any breach
[ i ] searching breached accounts on HIBP related to: jillian.cartwright@fbi.com
[ i ] searching for paste dumps on HIBP related to: jillian.cartwright@fbi.com
...
```

Checking for ten minute emails:
```
python whatbreach.py -l test.txt -cT 

	                                                    _____ 
	   _ _ _ _       _   _____                 _       |___  |
	  | | | | |_ ___| |_| __  |___ ___ ___ ___| |_       |  _|
	  | | | |   | .'|  _| __ -|  _| -_| .'|  _|   |      |_|  
	  |_____|_|_|__,|_| |_____|_| |___|__,|___|_|_|[][][]|_|
	Find emails and their associated leaked databases.. v0.1.5


[ i ] parsing email file: test.txt
[ i ] starting search on a total of 2 email(s)
[ i ] searching breached accounts on HIBP related to: user1337@gmail.com
[ i ] searching for paste dumps on HIBP related to: user1337@gmail.com
[ i ] found a total of 9 database breach(es) pertaining to: user1337@gmail.com
---------------------------------------------------------------------------
Breach/Paste:	     | Database/Paste Link:
Dailymotion          | https://www.dehashed.com/search?query=Dailymotion
500px                | https://www.dehashed.com/search?query=500px
LinkedIn             | https://www.dehashed.com/search?query=LinkedIn
MyFitnessPal         | https://www.dehashed.com/search?query=MyFitnessPal
Bolt                 | https://www.dehashed.com/search?query=Bolt
Dropbox              | https://www.dehashed.com/search?query=Dropbox
Lastfm               | https://www.dehashed.com/search?query=Lastfm
Apollo               | https://www.dehashed.com/search?query=Apollo
OnlinerSpambot       | N/A                           
---------------------------------------------------------------------------
[ w ] email: userl337@uhren.com appears to be a ten minute email
[ ? ] would you like to process the email[y/N]: n
```

Searching for profiles associated with the email:
```
python whatbreach.py -e user@gmail.com -cA

                                                            _____ 
           _ _ _ _       _   _____                 _       |___  |
          | | | | |_ ___| |_| __  |___ ___ ___ ___| |_       |  _|
          | | | |   | .'|  _| __ -|  _| -_| .'|  _|   |      |_|  
          |_____|_|_|__,|_| |_____|_| |___|__,|___|_|_|[][][]|_|
        Find emails and their associated leaked databases.. v0.1.8


[ i ] starting search on single email address: user@gmail.com
[ i ] searching for possible profiles related to user@gmail.com
[ i ] all data dumped to file for future processing: /Users/admin/.whatbreach_home/downloads/json_dumps/user_emailrep.json
[ i ] found a total of 5 possible profiles associated with user@gmail.com on the following domains:
        -> Twitter
        -> Instagram
        -> Pastebin
        -> Pinterest
        -> Spotify
...
```

# Installation

Installing is extremely easy, just run `pip install -r requirements.txt`

# Why?

During my time in information technology, during researching and doing OSINT, I have noticed a need to find email addresses as well as their password. I have found reliable tools that do this successfully and make the process quick and easy, however I have not found a tool that meets my exact requirements. This tool is basically my own personal take on how I think email searching should work and ties in the database searching and database downloading as well. What better way to break into an email then to have the possible password as well as all _known_ breaches it's been seen in?

# Shoutouts

 - [NullArray](https://github.com/NullArray) for providing me with the idea for the hash checking and the idea for the databases.today downloads, as well as being an awesome and supportive person at all times.