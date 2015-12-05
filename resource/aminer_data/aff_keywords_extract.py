import json
import re

__author__ = 'hong'


STOP_WORDS = []


def get_stop_words():
    content_ori = open('stopwords.txt')
    lines = content_ori.readlines()
    for line in lines:
        STOP_WORDS.append(line.replace('\n', ''))


if __name__ == '__main__':
    get_stop_words()
    # lines = get_file_lines('citation_top_1000.json')
    # person_info = ''
    # for line in lines:
    #     person_info += line
    with open('citation_top_1000.json', 'r') as f:
        persons = json.load(f)
    # persons = json.loads(content_ori)
    for person in persons:
        print person.get('id')
        aff = person.get('affiliation')
        if person.get('contact').get('affiliation') is not None:
            aff = aff + ' ' + person.get('contact').get('affiliation')

        aff = aff.replace('\n', ' ')
        aff = aff.replace('.', ' ').replace(',', ' ').replace('|', ' ')
        aff = aff.replace('(', ' ').replace(')', ' ')
        aff = re.sub('\s+', ' ', aff).strip(' ')

        aff_words = aff.lower().split(' ', -1)
        aff_word_list = set()
        for word in aff_words:
            if word in STOP_WORDS:
                continue
            if word in aff_word_list:
                continue
            # if word in dictionary.keys():
            #     dictionary[word] += 1
            #     continue
            # dictionary.setdefault(word, 1)
            aff_word_list.add(word)
        person['affiliation_words'] = list(aff_word_list)
    with open('citation_top_1000_with_affwords.json', 'w') as f:
        f.write(json.dumps(persons, indent=4))
    # dictionary = sorted(dictionary.iteritems(), key=lambda d: d[1], reverse=True)



