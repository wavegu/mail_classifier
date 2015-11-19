import json
from util import handle_email_addr
from util import get_top_person_names
from util import g_name_right_email_list_dict
from email_model import EmailModel
from email_model import g_email_model_list


class Person:

    def __init__(self, name):
        self.name = name
        self.email_addr_list = []
        self.personal_email_model_list = []
        self.get_email_list()

    def get_email_list(self):
        with open('../resource/Top1000_mail_list/' + self.name + '.txt') as email_file:
            self.email_addr_list = email_file.readlines()
        self.email_addr_list = [handle_email_addr(mail) for mail in self.email_addr_list]
        if self.email_addr_list == ['']:
            self.email_addr_list = []
        return self.email_addr_list

    def get_right_email_list(self):
        right_email_list = g_name_right_email_list_dict[self.name].split(',')
        if right_email_list == ['']:
            right_email_list = []
        return right_email_list

    def get_email_model_list(self):
        global g_email_model_list
        unique_email_addr_list = list(set(self.email_addr_list))
        for email_addr in unique_email_addr_list:
            tag = -1
            if email_addr in self.get_right_email_list():
                tag = 1
            email_model = EmailModel(self.name, email_addr, self.email_addr_list, tag)
            self.personal_email_model_list.append(email_model)
        return self.personal_email_model_list


def write_feature_file(person_dict_list, filename):
    with open(filename, 'w') as feature_file:
        for person_dict in person_dict_list:
            person = Person(person_dict['name'])
            if not person.get_right_email_list() or not person.email_addr_list:
                continue
            email_model_list = person.get_email_model_list()
            for email_model in email_model_list:
                feature_file.write(email_model.get_feature_line() + '\n')


if __name__ == '__main__':
    train_person_num = 200
    top_person_list = get_top_person_names(250)
    write_feature_file(top_person_list[:train_person_num], '../svm_light/email/train.dat')
    write_feature_file(top_person_list[train_person_num:], '../svm_light/email/test.dat')


