import os

# Assurez vous d'utiliser la bonne version de pip: >> sudo apt-get install python3-pip

modules = ["beautifulsoup4==4.11.1", "bs4==0.0.1", "certifi==2021.10.8", "charset-normalizer==2.0.12", "idna==3.3", "requests==2.27.1", "soupsieve==2.3.2.post1", "urllib3==1.26.9"]

for mod in modules:
    try:
        commande = "pip install " + mod
        os.system(commande)
    except:
        print("")