# encoding=utf8 
import sys 
reload(sys) 
sys.setdefaultencoding('utf8')

import json
import codecs
from openpyxl import load_workbook


def get_person_dict_list_from(filename):
	print '-'*10 + filename + '-'*10
	person_dict_list = []

	wb = load_workbook(filename)
	sheet_name = wb.get_sheet_names()[0]
	sheet = wb['reviewer']

	name_col = 'B'
	affi_col = 'C'
	mail_col = 'G'

	name = 'name'
	line_num = 2
	while name:
		line_num += 1
		name = sheet[name_col + str(line_num)].value
		affi = sheet[affi_col + str(line_num)].value
		mail = sheet[mail_col + str(line_num)].value
		if not mail:
			continue
		mail = mail.lower().replace('、', ',').replace(' or ', ',').replace('/', ',')
		mail = mail.replace('(at)', '@').replace('{at}', '@').replace('[at]', '@').replace(' at ', '@')
		mail = mail.replace('(dot)', '@').replace('{dot}', '@').replace('[dot]', '@').replace(' at ', '@')
		mail = mail.replace(' ', '')
		print mail
		person_dict = {
			'name': name,
			'affiliation': affi,
			'contact': {
				'email': mail
			}
		}
		person_dict_list.append(person_dict)
	return person_dict_list


def get_all_person_dict_list(isChina):
	import os
	error_file = open('error_log.txt', 'w')
	all_person_dict_list = []
	for looper in range(12):
		dirpath = str(looper) + '/'
		for filename in os.listdir(dirpath):
			if isChina and '.china.' not in filename:
				continue
			if not isChina and '.foreign.' not in filename:
				continue
			filename = dirpath + filename
			try:
				all_person_dict_list += get_person_dict_list_from(filename)
			except Exception as e:
				error_file.write('[ERROR] %s\n' % filename)
				error_file.write(str(e)+'\n')
	error_file.close()
	return all_person_dict_list


def get_merged_name_person_dict_from_list(person_dict_list):
	name_person_dict = {}
	for person_dict in person_dict_list:
		name = person_dict['name']
		affi = person_dict['affiliation']
		mail = person_dict['contact']['email']
		if name not in name_person_dict:
			name_person_dict[name] = person_dict
			continue
		if mail not in name_person_dict[name]['contact']['email']:
			name_person_dict[name]['contact']['email'] += ',' + mail	
	return name_person_dict


def get_name_person_dict():
	chinese_person_dict_list = get_all_person_dict_list(True)
	foreign_person_dict_list = get_all_person_dict_list(False)
	print len(chinese_person_dict_list)
	print len(foreign_person_dict_list)

	chinese_name_person_dict = get_merged_name_person_dict_from_list(chinese_person_dict_list)
	foreign_name_person_dict = get_merged_name_person_dict_from_list(foreign_person_dict_list)

	with codecs.open("chinese_name_list.json", "w", encoding="utf-8") as f_out:
	    json.dump(sorted(chinese_name_person_dict), f_out, indent=4, ensure_ascii=False)

	with codecs.open("foreign_name_list.json", "w", encoding="utf-8") as f_out:
	    json.dump(sorted(foreign_name_person_dict), f_out, indent=4, ensure_ascii=False)

	chinese_person_dict_list = []
	foreign_person_dict_list = []
	for name, person in chinese_name_person_dict.items():
		chinese_person_dict_list.append(person)
	for name, person in foreign_name_person_dict.items():
		foreign_person_dict_list.append(person)


	with codecs.open("chinese_person_list.json", "w", encoding="utf-8") as f_out:
	    json.dump(chinese_person_dict_list, f_out, indent=4, ensure_ascii=False)

	with codecs.open("foreign_person_list.json", "w", encoding="utf-8") as f_out:
	    json.dump(foreign_person_dict_list, f_out, indent=4, ensure_ascii=False)


if __name__ == '__main__':
	# get_person_dict_list_from('9/Vibration-Driven Microrobot Positioning Methodologies for Nonholonomic Constraint Compensation.foreign.xlsx')
	get_name_person_dict()