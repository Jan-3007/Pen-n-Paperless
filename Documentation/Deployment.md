

# Deployment on a Raspberry Pi 3B

## OS installation

1. Download Raspberry Pi Imager from: https://www.raspberrypi.com/software/
2. Install the software
3. Start Raspberry Pi Imager
	1. Select Raspberry Pi Model (Raspberry Pi 3)
	2. Select OS (other -> Lite 64 bit)
	3. Select Storage
	4. Hostname: idefix
	5. Localisation
		1. Location: Berlin
		2. Timezone: Berlin
		3. keyboard: ge
	6. User
		1. username: jan
		2. pasword: same as all other PCs
	7. WiFi
		1. not configured
	8. Remote Access
		1. SSH enabled with password login
	9. Raspberry Pi Connect
		1. not configured
4. Run the Writing process



## OS configuration
1. create Alias
	1. alias ll='ls -l'
2. install all packages
	1. python3-pip
	2. python3-flask
	3. python3-sqlalchemy
	4. python3-flask-sqlalchemy
	5. python3-pil


## Upload project
1. open Bitvise
2. select SFTP Server
3. upload the project files using the opened window



## connect to a wifi
![[Pasted image 20251205191607.png]]
