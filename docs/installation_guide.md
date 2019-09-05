## Asennusohje

Sovelluksen lokaali asennus vaatii
* Python (min) 3.5
* pip
* git
* venv

1. Lataa sovellus githubista ja mene kansioon
```
> git clone git@github.com:TetsuHari/MinimalForum.git
> cd MinimalForum
```
2. Luo virtuaaliympäristö ja aktivoi se
```
> python -m venv venv
> source venv/bin/activate
```
3. Asenna dependenssit
```
(venv)
> pip install -r requirements.txt
```
4. Käynnistä sovellus
```
(venv)
> python3 run.py
```
