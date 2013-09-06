# Network Simulations in Python on Rasperry Pi

An ongoing project for a networks class at Olin College of Engineering.

## Raspberry Pi Setup 

Install Arch on your Raspberry Pi SD card following this guide: [http://archlinuxarm.org/platforms/armv6/raspberry-pi](http://archlinuxarm.org/platforms/armv6/raspberry-pi).


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

You need the [RPi.GPIO python package](https://pypi.python.org/pypi/RPi.GPIO) in order to control the GPIO pins on the Raspberry Pi. I had an error when I tried installing it using `pip`, so I had to download and build from the [AUR RPi.GPIO package](https://aur.archlinux.org/packages.php?ID=59458).

Install the AUR package by following the [instructions for AUR packages](https://wiki.archlinux.org/index.php/Arch_User_Repository#Installing_packages) in the Arch wiki.

```
wget https://aur.archlinux.org/packages/ra/raspberry-gpio-python/raspberry-gpio-python.tar.gz
tar -xzf raspberry-gpio-python.tar.gz
cd raspberry-gpio-python
makepkg -a
packman -S raspberry-gpio-python-0.5.3a-1-any.pkg.tar.xz
```

Now navigate to the src directory, and run the python distribute `setup.py` file to install the python package in your virtualenv.

```
sudo python setup.py install
```