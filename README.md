# Smart Time Clock Machine
Tired of the current time clock system used at the place where I work, I decided to create my own system. It 
includes both hardware and software, a easy and practical way to keep track of employees hours and respective 
paychecks.<br>

## Hardware:
The hardware is pretty simple, it is composed by a 4x4 keyboard, a 16x2 LCD display, a fingerprint scanner, 
and a couple of buttons to confirm commands. All inputs go to a raspbarry pi that is connected to the WiFi and can be
accessed by any computer in the Library.

## Software:
The software is written all in Python3, it is a very simple and objective software connecting the inputs given
by the machine and a database locatate in one of the machines in the Library. Credentials are a combination of 
fingerprint and IDs, only the managers have total access on the system.

