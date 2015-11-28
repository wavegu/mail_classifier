import json
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from constants import AMINER_DATABASE_CONFIG

g_name_right_email_list_dict = {}


def get_top_citation():
    import urllib
    import requests
    import codecs
    import json
    from pymongo import MongoClient
    from bson import ObjectId
    username = AMINER_DATABASE_CONFIG['username']
    password = AMINER_DATABASE_CONFIG['password']
    client = MongoClient(AMINER_DATABASE_CONFIG['url'])
    db = client["bigsci"]
    db.authenticate(username, password)
    people_col = db["people"]

    resp = requests.get("https://api.aminer.org/api/rank/person/n_citation/0/1000")
    data = []
    cnt = 0
    for item in resp.json():
        result = people_col.find_one({"_id": ObjectId(item["id"])})
        if result:
            r = {
                "contact": result.get("contact", {}),
                "h_index": result["h_index"],
                "id": str(result["_id"]),
                "n_citation": result["n_citation"],
                "n_pubs": result["n_pubs"],
                "name": result["name"],
                "name_cn": result.get("name_zh", ""),
                "affiliation": result["org"],
                "affiliation_cn": result.get("org_zh", "")
            }
            data.append(r)
            cnt += 1
            print cnt
    with codecs.open("..resource/citation_top_1000.json", "w", encoding="utf-8") as f_out:
        json.dump(data, f_out, indent=4, ensure_ascii=False)


def get_known_top_1000():
    global g_name_right_email_list_dict
    with open('../resource/citation_top_1000.json') as json_file:
        json_content = json_file.read()
        person_list = sorted(json.loads(json_content), key=lambda person: person['name'])

    with open('../resource/known_Top_1000.txt', 'w') as known_file:
        for person in person_list:
            if 'email' not in person['contact']:
                person['contact']['email'] = ''
            person['contact']['email'] = person['contact']['email'].replace('\r\n', '').replace(' ', '')
            g_name_right_email_list_dict[person['name']] = person['contact']['email']
            known_file.write(('%s [%s]\n') % (person['name'], person['contact']['email']))


def get_top_person_names(top_num):
    with open('../resource/citation_top_1000.json') as json_file:
        json_content = json_file.read()
        person_list = sorted(json.loads(json_content), key=lambda person: person['name'])
    return person_list[:top_num]


# def handle_email_addr(addr):
#     if '\t' in addr:
#         addr = addr[:addr.find('\t')]
#     addr = addr.lower().replace('\n', '').replace(' ', '')
#     return addr


def create_dir_if_not_exist(dir_path):
    import os
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)


def del_a_from_b(a, b):
    if a not in b:
        return b
    part_pos = b.find(a)
    if part_pos + len(a) >= len(b):
        b = b[:part_pos]
    else:
        b = b[:part_pos] + b[(part_pos+len(a)):]
    return b


def is_a_in_b(a, b):
    a = str(a)
    b = str(b)
    if a not in b:
        return False
    start_pattern = a + ' '
    end_pattern = ' ' + a
    if (' ' + a + ' ') in b:
        return True
    if start_pattern in b and b.find(start_pattern) == 0:
        return True
    if end_pattern in b and b.find(end_pattern) == (len(b) - len(end_pattern)):
        return True
    return False


get_known_top_1000()

if __name__ == '__main__':
    get_top_citation()
    get_known_top_1000()