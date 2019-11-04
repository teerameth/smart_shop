from datetime import datetime
from passlib.hash import pbkdf2_sha256
def find_lastest(datetimes):
    date = []
    for i in range(len(datetimes)):
        string = datetimes[i] # stored in format dd:mm:yy-hh:mm:ss
        buff = ""
        buff += string[6:8]+string[3:5]+string[:2]+string[9:11]+string[12:14]+string[15:]
        date.append(buff)
    maximum = max(date)
    return date.index(maximum)
def new_date_time():
    buff = str(datetime.datetime.now())
    return buff[2:4] + ":" + buff[5:7] + ":" + buff[8:10] + "-" + buff[11:13] + ":" + buff[14:16] + ":" + buff[17:19]
###### HASH Password with PBKDF2-SHA256 algorithm ######https://passlib.readthedocs.io/en/stable/
def password_encode(password): #encode password to store
    return pbkdf2_sha256.hash(password)
def password_verify(password, stored_hash): #return True if password match with stored hash
    return pbkdf2_sha256.verify(password, stored_hash)