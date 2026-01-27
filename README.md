# General

activate venv:
. .\.venv\Scripts\Activate.ps1

to start the server run:
py .\run.py
or: .\.venv\Scripts\python.exe run.py

to access the website open browser at:
http://localhost:5000



# for Docker

## build image (plain docker)
docker build -t penpaper:latest .

## run container (binds to host port 8000)
docker run --rm -p 8000:8000 -v ${PWD}\\/app\\/data:/app/app/data -e SECRET_KEY='replace-me' penpaper:latest

## or docker compose
docker-compose up --build -d


## Raspberry Pi / Docker quickstart

These instructions show a minimal workflow to build and run the app on a Raspberry Pi using Docker.

1. Build the image on the Pi (or pull a multi-arch image if you push one to a registry):

```powershell
docker build -t penpaper:latest .
```

2. Ensure the `./app/data` directory exists and is writable (this is where the SQLite DB will be stored):

```powershell
mkdir .\app\data
# adjust permissions if needed, e.g. chown for Linux hosts
```

3. Start the container (or use `docker-compose up --build -d`):

```powershell
docker run --rm -p 8000:8000 -v ${PWD}\\/app\\/data:/app/app/data -e SECRET_KEY='replace-me' penpaper:latest
```

4. The container will run a small `start.sh` script that initializes the DB and then starts gunicorn. The app will be reachable at `http://<pi-ip>:8000/`.

Notes:
- The Docker image installs system libraries required by Pillow (JPEG/WEBP). If you encounter build errors related to image formats, paste the build log and I'll add the needed packages for your Pi model.
- For production, set a non-default `SECRET_KEY` and consider using a reverse proxy (nginx) in front of the container.






# TODO

- improve flashed messages
    - more categories: success, error (for errors to the user), fatal (for internal errors)
- add more stats (See pictures)
    - Experience, with view and comments as a history
- move to a production database
- make it mobile compatible
- create Docker container
- host on Raspberry Pi 3 B
- add german as second language
- rename run.py to startup.py







# Update dependency notes

## max_hp
update if changes in:
- endurance_bonus
- profession
- level

## remaining attribute points
update if changes in:
- attributes

## attribute bonus
update if changes in:
- attributes
- tribe
- profession
- specialization
- weapons
- armour

## level
update if changes in:
- experience

## max ability points
update if changes in:
- intelligence_bonus
- level

## defense bonus
update if changes in:
- tribe
- profession
- specialization
- weapons
- armour





# Abilities
- class storing all abilities and their properties




# Raspi configs

## Wifi
sudo rfkill list
sudo rfkill unblock wifi
sudo rfkill list
sudo nmcli dev wifi connect "LAPTOP1366" password "78x3=14C"


## add python program to systemctl for autostart
sudo systemctl enable /home/jan/test/pennpaperless.service
sudo systemctl status pennpaperless.service
sudo systemctl start pennpaperless.service
sudo systemctl stop pennpaperless.service

