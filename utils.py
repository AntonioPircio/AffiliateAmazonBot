import csv
from datetime import date, timedelta

import constant
from appearel import Appearel
from os.path import exists
from technlogy import Technology
import os
from cryptography.fernet import Fernet


def getScrapingType(type):
    if type == 'Elettronica/Informatica':
        tecnology = Technology()
        return tecnology.getTechnologyURLS()
    elif type == 'Abbigliamento':
        appearel = Appearel()
        return appearel.geAppearelURLS()
    else:
        tecnology = Technology()
        return tecnology.getTechnologyURLS()


def controlInputValue(value):
    if value.__str__().__len__() > 0:
        return True
    else:
        return False


def isValidTrialTime(file):
    with open(file, 'rb')as f:
         fernet = Fernet(constant.key)
         encryptedfile = f.read()
         decryptedfile = fernet.decrypt(encryptedfile)
         endDate = decryptedfile.__str__()[10:-5]
         if endDate.__str__() <= date.today().__str__():
                return False
         else:
                return True


def checkRequirments():
    if exists('data/tTime.csv'):
        if not isValidTrialTime('data/tTime.csv'):
            return False
        else:
            return True
    else:
        with open('data/trialTime.csv', 'w', encoding='UTF8', newline='') as f:
            header = ['Date']
            writer = csv.writer(f)
            writer.writerow(header)
            deltaDays = timedelta(days=2)
            currentDate = date.today() + deltaDays
            data = [currentDate.__str__()]
            writer.writerow(data)
        with open('data/trialTime.csv', 'rb') as f:
            fernet = Fernet(constant.key)
            originalfile = f.read()
        with open('data/tTime.csv', 'wb') as encryptedfile:
            encryptedfile.write(fernet.encrypt(originalfile))
            os.system("attrib +h data/tTime.csv")
            os.remove('data/trialTime.csv')
            return True
