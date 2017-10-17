# Tailf Bot
This is simple telegram bot to send my logs from some servers. It's simple and configurable.

# Installation
Just clone this repo into some folder or:
  ```
  wget https://github.com/maxonrock/tailfbot/archive/master.zip
  unzip master.zip
 ``` 
Install **python3**, **pip** and **requests library**
#### Example for RHEL
```
  sudo yum install -y python34 python34-pip
  sudo pip3.4 install requests
```
#### Example for Ubuntu
```
  sudo apt install python3 pip
  sudo pip install requests
```

# Config
Edit send.cfg and paste your bot token in **token** section and cammands with paths in **paths** section
#### Example send.cfg
```
[token]
value=1234123:sdfgnlSDFgsDFgG_fSN

[paths]
info=/opt/some_path/logs/some.log
```

# Run

Just type following commands in terminal
```
cd tailfbot-master
./send.py
```
