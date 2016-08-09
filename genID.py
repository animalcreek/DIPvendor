# A script to log and generate Vendor IDs for C.H.I.P. DIP add-on boards
# Script by Peter Nyboer peter@nextthing.co

# TO DO:
# Add a 'delete' or 'delete last' ID function

import sys
import random
import json
import re

def makeid(email,vendorname,preferredID=None):
    prefID = ''

    if preferredID:
        prefID = preferredID.lower()
    else:
        prefID = hex(random.randrange(0,2147483647))

    # read json of existing IDs
    jsonfile = open('DIP_vendors.json')
    vendorDB = json.load(jsonfile)

    errors = list()     # keep track of things that go wrong
    currentIDs = dict() # dictionary form of vendor list, for ease of later checks
    prototypeIDs = 0    # keep track of which prototype IDs are present

    if "vendorIDs" not in vendorDB:
        errors.append("No vendorIDs at toplevel of DIP_vendors.json")
    else:
        vendorIDs = vendorDB["vendorIDs"]

        # parse existing IDs into list to use to check uniqueness:
        for vid, vinfo in vendorIDs.iteritems():
            # Is this a prototype ID?
            intID = int(vid, 0)

            if intID < 16:
                # Yup.
                prototypeIDs |= (1 << intID)
            else:
                print("Vendor %s is %s" % (vid, vinfo['vendor']))

                if vid in currentIDs:
                    errors.append("Vendor ID %s is duplicated" % vid)
                else:
                    currentIDs[vid] = vinfo

        print("Loaded %d vendor ID%s" % (len(currentIDs), "" if (len(currentIDs) == 1) else "s"))

        # We know all the IDs are unique. Do we have all the prototype IDs?
        if prototypeIDs != 0xFFFF:
            errors.append("Prototype IDs 0 - F must be present; some are missing")

        # Do we have Next Thing's ID?
        if "0x009d011a" not in currentIDs:
            errors.append("Next Thing isn't in the vendors list!")

    if errors:
        sys.stderr.write("\n".join(errors))
        sys.stderr.write("\n")
        sys.stderr.write("Please fix DIP_vendors.json and try again.\n")
        quit()
    else:
        # if the desired ID matches an existing ID, generate a new one
        if prefID in currentIDs:
            print(" :( Your chosen Vendor ID %s is already taken" % prefID)
            choice = raw_input(' > Type "e" to exit or "g" to generate a new ID: ')
            if choice == 'g':
                while prefID in currentIDs:
                    prefID = hex(random.randrange(0,2147483647))
            else:
                print("quit")
                quit()

        print(" + Your new vendor ID is: %s" % prefID)

        # add info to JSON file
        vendorDB["vendorIDs"][prefID] = {
            "vendor": vendorname,
            "contact": email
        }

        # save it!
        with open('DIP_vendors.json','w') as writejson:
            json.dump(vendorDB, writejson, indent=4, separators=(',',':'), sort_keys=True)

        print(" :) vendorDB updated")

# simple regex check of email format.
def valid_email(email):
    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)
    if match:
        return match
    else:
        print(' ! email not valid format. Call script with 3 arguments (last is optional):\n  $ python genID.py person@dipmaker.com "DIP Makers Inc." 0x00000001')
        quit()

# TO DO - insert preflight on JSON to make sure it is OK
# test arguments sys.argv to make sure all is good, then call makeid.
if len(sys.argv) < 3:
    print(' ! Call genID.py with at least email and vendorname arguments.\n  Optional 3rd argument is desired ID, e.g.:\n     $ python genID.py person@dipmaker.com "DIP Makers Inc." 0x00000001')
elif len(sys.argv) == 3:
    if valid_email(sys.argv[1]):
        makeid(sys.argv[1],sys.argv[2])
elif len(sys.argv) == 4:
    if valid_email(sys.argv[1]):
        makeid(sys.argv[1],sys.argv[2],sys.argv[3])
