import csv
from datetime import date, timedelta

import constant
from appearel import Appearel
from os.path import exists
from technlogy import Technology
import os
import platform
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


def isValidTrialTime(file, systemName):
    with open(file, 'rb')as f:
         getKey(systemName)
         fernet = Fernet(constant.key)
         encryptedfile = f.read()
         decryptedfile = fernet.decrypt(encryptedfile)
         endDate = decryptedfile.__str__()[10:-5]
         if endDate.__str__() <= date.today().__str__():
                return False
         else:
                return True

def createDeltafile(systemName):
    if systemName == constant.systemOne:
        with open('.data/delta.txt', 'w', encoding='UTF8', newline='') as f:
            header = ['Delta']
            writer = csv.writer(f)
            writer.writerow(header)
            days = [constant.days.__str__()]
            writer.writerow(days)
        with open('.data/delta.txt', 'rb') as f:
            fernet = Fernet(constant.key)
            originalfile = f.read()
        with open('.data/cDelta.txt', 'wb') as encryptedfile:
            encryptedfile.write(fernet.encrypt(originalfile))
            os.remove('.data/delta.txt')
    else:
        with open('data/delta.txt', 'w', encoding='UTF8', newline='') as f:
            header = ['Delta']
            writer = csv.writer(f)
            writer.writerow(header)
            data = [constant.days.__str__()]
            writer.writerow(data)
        with open('data/delta.txt', 'rb') as f:
            fernet = Fernet(constant.key)
            originalfile = f.read()
        with open('data/cDelta.txt', 'wb') as encryptedfile:
            encryptedfile.write(fernet.encrypt(originalfile))
            os.remove('data/delta.txt')


def getDeltaFile(systemName):
    if systemName == constant.systemOne:
        with open('.data/cDelta.txt', 'rb') as f:
            getKey(systemName)
            fernet = Fernet(constant.key)
            encryptedfile = f.read()
            decryptedfile = fernet.decrypt(encryptedfile)
            return decryptedfile.__str__()[11:-5]
    else:
        with open('data/cDelta.txt', 'rb') as f:
            getKey(systemName)
            fernet = Fernet(constant.key)
            encryptedfile = f.read()
            decryptedfile = fernet.decrypt(encryptedfile)
            return decryptedfile.__str__()[11:-5]


def createKeyFile(systemName):
    if systemName == constant.systemOne:
        with open('.data/key.txt', 'wb') as key_file:
            key_file.write(Fernet.generate_key())
    else:
        with open('data/key.txt', 'wb') as key_file:
            key_file.write(Fernet.generate_key())


def getKey(systemName):
    if systemName == constant.systemOne:
        with open('.data/key.txt', 'rb') as key_file:
            constant.key = key_file.read()

    else:
        with open('data/key.txt', 'rb') as key_file:
            constant.key = key_file.read()



def checkRequirments():
    systemName = platform.system()
    if systemName == constant.systemOne:
        return checkLinuxRequirments(systemName)
    else:
        return checkWindowsRequirements(systemName)


def checkLinuxRequirments(systemName):
    if exists('.data/tTime.csv'):
        if not isValidTrialTime('.data/tTime.csv', systemName):
            return False
        else:
            return True
    else:
        os.mkdir('.data')
        createKeyFile(systemName)
        getKey(systemName)
        createDeltafile(systemName)
        with open('.data/trialTime.csv', 'w', encoding='UTF8', newline='') as f:
            header = ['Date']
            writer = csv.writer(f)
            writer.writerow(header)
            deltaDays = timedelta(float(getDeltaFile(systemName)))
            currentDate = date.today() + deltaDays
            data = [currentDate.__str__()]
            writer.writerow(data)
        with open('.data/trialTime.csv', 'rb') as f:
            fernet = Fernet(constant.key)
            originalfile = f.read()
        with open('.data/tTime.csv', 'wb') as encryptedfile:
            encryptedfile.write(fernet.encrypt(originalfile))
            os.remove('.data/trialTime.csv')
            return True

def checkWindowsRequirements(systemName):
    if exists('data/tTime.csv'):
        if not isValidTrialTime('data/tTime.csv',systemName):
            return False
        else:
            return True
    else:
        os.mkdir('data')
        os.system("attrib +h data")
        createKeyFile(systemName)
        getKey(systemName)
        createDeltafile(systemName)
        with open('data/trialTime.csv', 'w', encoding='UTF8', newline='') as f:
            header = ['Date']
            writer = csv.writer(f)
            writer.writerow(header)
            deltaDays = timedelta(float(getDeltaFile(systemName)))
            currentDate = date.today() + deltaDays
            data = [currentDate.__str__()]
            writer.writerow(data)
        with open('data/trialTime.csv', 'rb') as f:
            fernet = Fernet(constant.key)
            originalfile = f.read()
        with open('data/tTime.csv', 'wb') as encryptedfile:
            encryptedfile.write(fernet.encrypt(originalfile))
            os.remove('data/trialTime.csv')
            return True



