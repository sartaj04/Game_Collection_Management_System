## MSc Software Development CourseWork 

**Smith__Hale_and_Wagner Project:**

This file consists of methods to access our prototype. 

# Method 1

The prototype is currently hosted on Google Cloud Platform as a website naed 'Game Shack'. Click on the below link to access our web-based solution for the coursework:

Link: http://34.83.111.87:8001/

*Only if the above link doesn't work or it says that the server is down, follow the steps mentioned in method 2 below*

# Method 2

In case the first method is unavailable then please follow the below steps. 

## Requisites 

1. Ensure Python3 is installed on the server using below command: 

```
s2424386sdoc@eidf018-sdoc6:~$ python3 --version
Python 3.8.10
```


2. Ensure that pip3 is working and up to date: 

```
s2424386sdoc@eidf018-sdoc6:~$ python3 -m pip install --upgrade pip
Defaulting to user installation because normal site-packages is not writeable
Requirement already satisfied: pip in /home/eidf018/eidf018/s2424386sdoc/.local/lib/python3.8/site-packages (23.1)
```


3. Once pip3 and Python3 are both available, install Django package as shown below: 

```
s2424386sdoc@eidf018-sdoc6:~$ python3 -m pip install Django
Defaulting to user installation because normal site-packages is not writeable
Collecting Django
  Downloading Django-4.2-py3-none-any.whl (8.0 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 8.0/8.0 MB 36.7 MB/s eta 0:00:00
Collecting asgiref<4,>=3.6.0 (from Django)
  Downloading asgiref-3.6.0-py3-none-any.whl (23 kB)
Collecting sqlparse>=0.3.1 (from Django)
  Downloading sqlparse-0.4.4-py3-none-any.whl (41 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 41.2/41.2 kB 2.2 MB/s eta 0:00:00
Collecting backports.zoneinfo (from Django)
  Downloading backports.zoneinfo-0.2.1-cp38-cp38-manylinux1_x86_64.whl (74 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 74.0/74.0 kB 4.6 MB/s eta 0:00:00
Installing collected packages: sqlparse, backports.zoneinfo, asgiref, Django
```



## Clone the repository

1. Using below ssh command, clone the Smith__Hale_and_Wagnar repository: 

```
s2424386sdoc@eidf018-sdoc6:~/Desktop$ git clone https://git.ecdf.ed.ac.uk/sdoc2223/Smith__Hale_and_Wagner.git
Cloning into 'Smith__Hale_and_Wagner'...
Username for 'https://git.ecdf.ed.ac.uk': s2424386
Password for 'https://s2424386@git.ecdf.ed.ac.uk': 
remote: Enumerating objects: 853, done.
remote: Counting objects: 100% (254/254), done.
remote: Compressing objects: 100% (162/162), done.
remote: Total 853 (delta 129), reused 200 (delta 92), pack-reused 599
Receiving objects: 100% (853/853), 21.93 MiB | 23.39 MiB/s, done.
Resolving deltas: 100% (473/473), done.
```


NOTE: You may have to give your credentials while cloning the repository

2. After cloning it, navigate to below path to be in the myproject/ directory:

```
s2424386sdoc@eidf018-sdoc6:~/Desktop$ cd Smith__Hale_and_Wagner/myproject/
s2424386sdoc@eidf018-sdoc6:~/Desktop/Smith__Hale_and_Wagner/myproject$ ls
Clubs.xlsx  __init__.py  boardgames  db.sqlite3  game_details.csv  import_club.py  import_csv.py  manage.py  myproject  static
```


3. Next, execute the commands as shown below: 

Command 1 : python3 manage.py makemigrations

```
s2424386sdoc@eidf018-sdoc6:~/SWD/Smith__Hale_and_Wagner/myproject$ python3 manage.py makemigrations
No changes detected
```


Command 2: python3 manage.py migrate

```
s2424386sdoc@eidf018-sdoc6:~/SWD/Smith__Hale_and_Wagner/myproject$ python3 manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, boardgames, contenttypes, sessions
Running migrations:
  No migrations to apply.
```


Command 3: python3 manage.py runserver

```
s2424386sdoc@eidf018-sdoc6:~/SWD/Smith__Hale_and_Wagner/myproject$ python3 manage.py runserver
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
April 18, 2023 - 19:22:10
Django version 4.2, using settings 'myproject.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```


You need to copy the link generated in the console above and paste it in the web browser to access the prototype successfully: 

http://127.0.0.1:8000/

NOTE: Sometimes, if the code is not up to date, the above commands will create models and apply relevant migrations. Nevertheless, they should be successfully executed and run server command will generate a link as shown above. This link must be used for accessing the prototype. 



The Smith__Hale_and_Wagnar repository is cloned in below path in s2424386sdoc’s VM 

```
s2424386sdoc@eidf018-sdoc6:~/Desktop/Smith__Hale_and_Wagner$ pwd
/home/eidf018/eidf018/s2424386sdoc/Desktop/Smith__Hale_and_Wagner
```


You can connect to this server and go to the path and execute the makemigrations, migrations and runserver commands as shown above in step 3. 

## Things to know

1. The code of the prototype is present in the below path: 
https://git.ecdf.ed.ac.uk/sdoc2223/Smith__Hale_and_Wagner/-/tree/main/myproject
2. The images and screenshots of the prototype are present in below directory: 
https://git.ecdf.ed.ac.uk/sdoc2223/Smith__Hale_and_Wagner/-/tree/main/Prototype_Images
3. All the data monitoring and documentations from Requirement Gathering to prototype evaluation are present in below path:
https://git.ecdf.ed.ac.uk/sdoc2223/Smith__Hale_and_Wagner/-/tree/main/Project_Documentation



## Troubleshooting

1. In case you face issues while executing the runserver command, execute below commands as part of pre-requisites.

```
 python3 -m pip install Django
 python3 -m pip install Pandas
 python3 -m pip install Numpy
 python3 -m pip install openpyxl
```



2. After installing the dependencies please navigate to Smith__Hale_and_Wagnar/myproject then run the following commands in sequence

```
 python3 manage.py makemigrations
 python3 manage.py migrate
 python3 import_csv.py
 python3 import_club.py
 python3 manage.py runserver 
```

After which the server should be turned up with relevant data inserted into the database.

NOTE: In case any issues are observed and you need to contact us, please send a mail to N.Vupparapalli@sms.ed.ac.uk

