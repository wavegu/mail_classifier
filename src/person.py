# encoding: utf-8

import json
from util import is_a_in_b
from util import get_top_person_names
from util import g_name_right_email_list_dict
from util import g_name_affiliation_word_list_dict
from email_model import EmailModel


class Person:

    def __init__(self, name):
        self.name = name
        self.affiliation_word_list = g_name_affiliation_word_list_dict[name]
        self.google_item_dict_list = []

        self.email_email_model_dict = {}
        self.personal_email_model_list = []
        self.get_google_item_dict_list()
        self.get_email_email_model_dict()

    def get_right_email_list(self):
        right_email_list = g_name_right_email_list_dict[self.name].split(',')
        if right_email_list == ['']:
            right_email_list = []
        return right_email_list

    def get_all_email_addr_list(self):
        all_email_addr_list = []
        for google_item_dict in self.google_item_dict_list:
            all_email_addr_list += google_item_dict['email_addr_list']
        return all_email_addr_list

    def get_google_item_dict_list(self):
        with open('../resource/Top1000_mail_list/' + self.name + '.txt') as google_item_file:
            self.google_item_dict_list = json.loads(google_item_file.read())
        return self.google_item_dict_list

    def get_email_email_model_dict(self):
        for google_item_dict in self.google_item_dict_list:
            title = google_item_dict['title'].lower()
            content = google_item_dict['content'].lower()
            cite_url = google_item_dict['cite_url'].lower()
            cite_name = google_item_dict['cite_name'].lower()
            email_addr_list = google_item_dict['email_addr_list']

            for email_addr in email_addr_list:
                # 若当前email地址没有对应的email_model，则创建一个新的
                if email_addr not in self.email_email_model_dict:
                    tag = -1
                    if email_addr in self.get_right_email_list():
                        tag = 1
                    self.email_email_model_dict[email_addr] = EmailModel(self.name, email_addr, self.get_all_email_addr_list(), tag)
                # 对当前model进行google_item相关的参数赋值
                person_last_name = self.name.lower().split(' ')[-1]
                tem_email_model = self.email_email_model_dict[email_addr]
                tem_email_model.is_last_name_in_google_title = tem_email_model.is_last_name_in_google_title or is_a_in_b(person_last_name, title)
                tem_email_model.is_last_name_in_google_content = tem_email_model.is_last_name_in_google_content or is_a_in_b(person_last_name, content)

                # TODO: is_affiliation_in_google_title
                aff_word_num_in_title = 0
                aff_word_num_in_content = 0
                for aff_word in self.affiliation_word_list:
                    if is_a_in_b(aff_word, title):
                        aff_word_num_in_title += 1
                    if is_a_in_b(aff_word, content):
                        aff_word_num_in_content += 1
                aff_word_proportion_in_title = float(aff_word_num_in_title) / float(len(self.affiliation_word_list)+1)
                aff_word_proportion_in_content = float(aff_word_num_in_content) / float(len(self.affiliation_word_list)+1)
                if tem_email_model.max_affiliation_proportion_in_title < aff_word_proportion_in_title:
                    tem_email_model.max_affiliation_proportion_in_title = aff_word_proportion_in_title
                if tem_email_model.max_affiliation_proportion_in_content < aff_word_proportion_in_content:
                    tem_email_model.max_affiliation_proportion_in_content = aff_word_proportion_in_content

                self.email_email_model_dict[email_addr] = tem_email_model



def write_feature_file(person_dict_list, filename):
    with open(filename, 'w') as feature_file:
        for person_dict in person_dict_list:
            person = Person(person_dict['name'])
            if not person.get_right_email_list() or not person.google_item_dict_list:
                continue
            for email_addr, email_model in person.email_email_model_dict.items():
                feature_file.write(email_model.get_feature_line() + '\n')


if __name__ == '__main__':
    train_person_num = 200
    top_person_list = get_top_person_names(250)
    write_feature_file(top_person_list[:train_person_num], '../svm_light/email/train.dat')
    write_feature_file(top_person_list[train_person_num:], '../svm_light/email/test.dat')


