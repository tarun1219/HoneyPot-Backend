import os
import uuid
from datetime import datetime

import OrgSQLRepository as r
import itertools


def process_honey_tokens(mailfrom, rcpttos, data, honeytoken_tuple=r.get_honey_tokens()):
    honey_token_list = list(itertools.chain(*honeytoken_tuple))
    for rcpto in rcpttos:
        if rcpto in honey_token_list:
            print("Email Recieved to honey token email")
            subject = str(data).lower().split("subject")[1].split("\\n")[0].replace("\'","")
            body = str(data).lower().split("subject")[1].split("\\n")[1].replace("\'","")
            r.insert_blocked_email_contents(mailfrom, subject, body, rcpto)
            meta_data_reciever(data)
            r.insert_banned_email(mailfrom)
            print("Captured email contents and blocked sender")
        else:
            pass

def process_email(mailfrom, rcpttos, data, honeytoken_tuple=r.get_honey_tokens()):
    honey_token_list = list(itertools.chain(*honeytoken_tuple))
    for rcpto in rcpttos:
        if rcpto in honey_token_list:
            subject = str(data).lower().split("subject")[1].split("\\n")[0].replace("\'","")
            body = str(data).lower().split("subject")[1].split("\\n")[1].replace("\'","")
            r.insert_blocked_email_contents(mailfrom, subject, body, rcpto)
            meta_data_reciever(data)
            print("Captured email contents from blocked sender")
        else:
            pass


def meta_data_reciever(data):
    emailuuid = uuid.uuid4()
    metadata = f'Blocked'
    if not os.path.exists(metadata):
        os.makedirs(metadata)
    filename = '%s-%s.eml' % (datetime.now().strftime('%Y%m%d%H%M%S'),emailuuid)
    f = open(f"{metadata}/{filename}", 'wb')
    f.write(data)
    f.close
    print('%s captured for analysis.' % filename)
