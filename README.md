# snips-custom-hotword
Using Snowboy to customize the snips hotword


# Install

I'm using raspbian stretch light

We need a few dependencies first:

```sudo apt-get install python-pip python-pyaudio python3-pyaudio sox libatlas-base-dev```

```pip install pyaudio```
```pip install pytoml```
```pip install pahoo_mqtt```

Now, I perfectly know that *libatlas-base-dev* might be in conflict with Snips. That is why I do install it **before** Snips!

Once you sorted that out, you can download this project

```git https://github.com/Psychokiller1888/snips-custom-hotword.git```


# Creating a custom hotword

* Head to [Snowboy](https://snowboy.kitt.ai/dashboard), create an account if you don't yet own one and login.
* Create or download a hotword of your choice
* Place the downloaded **.pmdl** file into *snips-custom-hotword*

You're good to go!

```sudo python customHotword.py YOUR MODEL NAME SENSITIVITY```

Whaaat? Ok, calm down, here's an exemple:

```sudo python customHotword.py Alice 0.45```

Given that you downloaded the model Alice.pmdl and you want a sensitivity of 0.45 for it. (Sensitivity from 0 - not hearing you and 1 - full blast)

# Disabling Snips hotword

By this line of this little guide, your Snips instance still listens to both your custom hotword and your Snips hotword. Wanna disable the Snips hotword?

```sudo systemctl stop snips-hotword```

```sudo systemctl disable snips-hotword```


# But but but.... Nothing happens!

Ok, the aim of this is to change your hotword by a custom one, I didn't include any script... What you could do is start "customHotword" via ssh, and also start "snips-watch -v" and talk to your raspberry. When the custom hotword is heard, I simply publish on the mqtt server and Snips catches it!


# Special thanks
* Snips: https://snips.ai
* The base: https://github.com/oziee/hotword
* Snowboy: http://docs.kitt.ai/snowboy/


# Todo

I'm open to any suggestions. Here a little TODO list for this simple project:
* Hook Piwho, but not force it, passed as an argument
