# Network Simulations in Python on Rasperry Pi

An ongoing project for a networks class at Olin College of Engineering.

## Raspberry Pi Setup 

Install Arch on your Raspberry Pi SD card following this guide: [http://archlinuxarm.org/platforms/armv6/raspberry-pi](http://archlinuxarm.org/platforms/armv6/raspberry-pi).

If your SD card is larger than 2GB, you'll want to resize the root partition to take up all the space on your card. You can use gparted, or (risky) [resize it while mounted](http://jan.alphadev.net/post/53594241659/growing-the-rpi-root-partition).


Create a non-root user

```
useradd -m -g users -G wheel -s /bin/bash cypressf
passwd cypressf
```

Now install sudo, and edit the sudo config file to give the `wheel` group sudo privileges.

```
pacman -S sudo
pacman -S vim
VISUAL="/usr/bin/vim -p -X" visudo
```

Then uncomment the line that says

```
%wheel      ALL=(ALL) ALL
```

to give `wheel` sudo privileges.

```
exit
```

Now you can login as `cypressf`.

Install necessary packages

```
sudo pacman -S python git python-virtualenv base-devel python-virtualenvwrapper
```

Add the following lines to `~/.bashrc`:

```
export WORKON_HOME=~/.virtualenvs
source /usr/bin/virtualenvwrapper.sh
```

Create your virtualenv

```
mkvirtualenv networks
```

You need the [RPi.GPIO python package](https://pypi.python.org/pypi/RPi.GPIO) in order to control the GPIO pins on the Raspberry Pi. I had [an error](https://code.google.com/p/raspberry-gpio-python/issues/detail?id=48) when I tried installing it using `pip`. Now the error has a workaround, you can easily install using `pip`.

```
pip install RPi.GPIO --pre
```