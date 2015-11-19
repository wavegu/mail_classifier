# encoding=utf8 
import json
import sys 
reload(sys) 
sys.setdefaultencoding('utf8')


person_list = []
with open('resource/citation_top_1000.json') as json_file:
	json_content = json_file.read()
	person_list = json.loads(json_content)

not_match_num = 0
unknown_name_list = []
with open('compare.txt', 'w') as compare_file:
	for person_dict in person_list:
		if 'email' not in person_dict['contact']:
			person_dict['contact']['email'] = ''
		if not person_dict['contact']['email']:
			unknown_name_list.append(person_dict['name'])
			continue
		name = person_dict['name']
		expected_email = person_dict['contact']['email'].lower().replace('\n', '').replace(' dot ', '.').replace(' at ', '@').replace(' ', '').replace('[at]', '@').replace('[dot]', '.').replace('\r\n', '')

		try:
			with open('resource/Top1000_mail_list/' + name + '.txt') as person_file:
				flag = False
				google_mail_list = person_file.readlines()
				if not google_mail_list:
					continue
				candidate_list = []
				for mail_candidate in google_mail_list:
					mail_candidate = mail_candidate.lower().replace('\n', '').replace(' dot ', '.').replace(' at ', '@').replace(' ', '').replace('\t', '')
					mail_candidate = mail_candidate[:mail_candidate.find('[')]
					if mail_candidate == expected_email:
						flag = True
						# print name, 'match...'
						break
					candidate_list.append(mail_candidate)
				if not flag:
					not_match_num += 1
					compare_file.write(('%s [%s]\n') % (name, expected_email))
					for candidate in candidate_list:
						compare_file.write(candidate + '\n')
					compare_file.write('\n\n')
		except Exception as e:
			print name, e

	for name in unknown_name_list:
		candidate_list = open('resource/Top1000_mail_list/' + name + '.txt').readlines()
		if not candidate_list:
			continue
		compare_file.write('%25s {%s}\n' % (name, candidate_list[0].lower().replace('\n', '').replace(' dot ', '.').replace(' at ', '@').replace(' ', '').replace('\t', '')))
	compare_file.write('not match num ' + str(not_match_num) + '\n')
	compare_file.write('new email num ' + str(len(unknown_name_list)))