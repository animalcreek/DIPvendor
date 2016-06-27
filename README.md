# DIPvendor
A simple database and python script to register vendor IDs.

## A Minimally Viable Vendor Registration System

The JSON file is the master file that keeps track of DIP maker vendor IDs. Please only register what you need.

In brief:
 - Clone this repository to your computer
 - run the `genID.py` script
 - create a pull request to update

The simple python 2.7 script can be called from the terminal.
Call script with three arguments: contact email address, name of company, and, optionally, a preferred 32-bit vendor ID number in hex format. For example:
```
$ python genID.py person@dipmaker.com "DIP Makers Inc." 0x00000001'
```
The script will check if the email is a valid format, but will not attempt any further validation.
If you provide a vendor ID, the script will make sure it is not already taken. If it is, it will offer to randomly generate one for you. 

An example session:
```
$ python genID.py person@dipmaker.com "DIP Makers Inc." 0x009d011a
 :( Your chosen Vendor ID 0x009d011a is already taken.
 > Type "e" to exit or "g" to generate a new ID: g
 + Your new vendor ID is: 0x20bc2e55
 :) vendorDB updated
```

Once the script is updated, create a pull request on this repo so we can officially add the Vendor ID.
