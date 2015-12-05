"""
Problem description:
input: person_dict_list: [{'name', 'aff_words', 'email_list'}], we want to know whether these emails are right
output: feature_file
"""
import json
from person import Person


class FeatureGenerator:

    def __init__(self, person_dict_json_filename, google_item_file_path, output_feature_filename):
        self.name_person_dict = {}
        self.google_item_file_path = google_item_file_path
        self.output_feature_filename = output_feature_filename
        self.person_dict_list = json.loads(open(person_dict_json_filename).read())
        self.get_name_person_dict()

    def get_name_person_dict(self):
        for person_dict in self.person_dict_list:
            self.name_person_dict[person_dict['name']] = Person(person_dict, google_item_file_path)
        return self.name_person_dict

    def get_feature_line_list(self):
        feature_line_list = []
        for person_dict in self.person_dict_list:
            name = person_dict['name']
            person = self.name_person_dict[name]
            test_email_list = person_dict['contact']['email'].split(',')
            for test_email in test_email_list:
                if not test_email or test_email not in person.email_email_model_dict:
                    continue
                email_model = person.email_email_model_dict[test_email]
                email_model.tag = 1
                feature_line_list.append(email_model.get_feature_line())
        return feature_line_list

    def write_feature_file(self):
        feature_line_list = self.get_feature_line_list()
        with open(self.output_feature_filename, 'w') as feature_file:
            for feature_line in feature_line_list:
                feature_file.write(feature_line + '\n')


if __name__ == '__main__':
    resource_path = '../resource/liu_email_list/'
    foreign_person_dict_list_path = resource_path + 'data_parser/chinese_person_list_with_affwords.json'
    google_item_file_path = resource_path + 'google_item_list/chinese_google_item_list/'
    feature_file_path = resource_path + 'svm/test_feature_file.txt'
    generator = FeatureGenerator(foreign_person_dict_list_path, google_item_file_path, feature_file_path)
    generator.write_feature_file()

