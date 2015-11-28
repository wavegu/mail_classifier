file_content = open('test100.txt').read()


def get_accuracy_from_result(test_file_content):
	end_pos = test_file_content.find('%')
	start_pos = test_file_content.find('Accuracy') + 22
	return test_file_content[start_pos: end_pos]

def get_precision_from_result(test_file_content):
	start_pos = test_file_content.find('Precision') + 30
	end_pos = test_file_content.find('%', start_pos)
	return test_file_content[start_pos: end_pos]

def get_recall_from_result(test_file_content):
	start_pos = test_file_content.find('Precision') + 37
	end_pos = test_file_content.find('%', start_pos)
	return test_file_content[start_pos: end_pos]
	pass


print get_accuracy_from_result(file_content)
print get_precision_from_result(file_content)
print get_recall_from_result(file_content)