# TUTORIAL
Click on the video to see the tutorial:

[![How to use BruteFlash ](https://user-images.githubusercontent.com/47490330/164007194-8bf783b8-9b6a-466d-b580-512732e84295.png)](https://youtu.be/SpmlBQNpE5c?t=1s "How to use BruteFlash ")

# DESCRIPTION

BruteFlash is a BruteForce login page tool.
It is similar to hydra with the advantage that it can bypass the protections with the csrf token.
Indeed the tool was conceived especially in solving this problem which slowed down a lot the missions of pentest or the CTF. 

# Advantage

**Easy to use:**
It uses explicit flags allowing easy understanding.

**Speed:** 
It uses the Threading module of python to allow multi-thread requests and increase its execution speed.

**Adaptability:** 
Coded in python, it can be modified to fit your needs, as far as complex sites are concerned.

**Portability:**
It is independent of the operating system and can therefore run on Windows, Linux, Mac OS... .

# Installation 

```
$ git clone https://github.com/alexispondo/BruteFlash.git
```

```
$ cd BruteFlash 
```

```
$ python3 installer.py 
```

# Usage

To make it easy to use, the tool takes as parameters simple flags that allow us to launch the attack in a single line.
```
$ python3 BruteFlash.py -h

optional arguments:
  -h, --help       show this help message and exit
  -u U             Login URL
  -m M             Methode Used GET/POST (Default POST)
  -l L             username/email value
  -L L             Wordlist path of username/email values
  -p P             password value
  -P P             Wordlist path of password values
  --user USER      Name parameter of username/email input
  --passw PASSW    Name parameter of password input
  --submit SUBMIT  Name parameter of submit input
  --csrf CSRF      Name parameter of csrf_token input
  -e E             Error return for bad credential
  -C C             Cookies ex: "param1:value1, param2:value2"
  -v               Allow to display attempt in terminal output

```
**Simple login page**

This is a simple login page: not use csrf token
```
$ python3 BruteFlash.py -u http://127.0.0.1/Web/con.php -l user -P passwords.txt --user username --passw passw --submit submit -e "Désolé" -v
```
**Secure login page**

This is secure login page: is use csrf token
```
$ python3 BruteFlash.py -u http://127.0.0.1:8000/admin/ -l admin -P passwords.txt --user username --passw passw --submit Login --csrf csrfmiddlewaretoken -e "Username and/or password incorrect." -v
```
**Login page which needed cookies before bruteforcing**

This usually happens when the form you want to brute force is on a page that requires authentication. So all you have to do is copy the cookies that prove you have already authenticated from your browser to the command BruteFlash.py.
```
$ python3 BruteFlash.py -u  http://127.0.0.1:8000/admin2/ -l admin2 -P passwords.txt --user username --passw passw --submit Login --csrf csrfmiddlewaretoken -e "Username and/or password incorrect." -C "security: high, PHPSESSID: nbkttnti5kikvru5a4etei6oq8" -v
```


# Additional

All information about this code can be found in the comments of the code.
Please contact me for any bug or anomaly detected in connection with this tool:

Linkedin: https://www.linkedin.com/in/alexis-pondo/

GitHub: https://github.com/alexispondo/

BruteFlash: https://github.com/alexispondo/BruteFlash
