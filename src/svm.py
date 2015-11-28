# encoding: utf-8
import subprocess
from person import write_feature_file
from util import get_top_person_names
from util import create_dir_if_not_exist


class SVM:

    svm_name = 'SVM'

    def __init__(self, tot_data_num):
        self.tot_data_num = tot_data_num
        self.root_path = '../' + self.svm_name
        self.data_root_path = '../' + self.svm_name + '/email/'
        self.result_root_path = '../' + self.svm_name + '/result/'
        self.train_dir_path = self.data_root_path + 'train/'
        self.test_dir_path = self.data_root_path + 'test/'
        self.model_dir_path = self.data_root_path + 'model/'
        self.pred_dir_path = self.data_root_path + 'prediction/'
        self.result_test_dir_path = self.result_root_path + 'test/'
        self.result_compare_dir_path = self.result_root_path + 'compare/'
        create_dir_if_not_exist(self.root_path)
        create_dir_if_not_exist(self.data_root_path)
        create_dir_if_not_exist(self.result_root_path)
        create_dir_if_not_exist(self.test_dir_path)
        create_dir_if_not_exist(self.train_dir_path)
        create_dir_if_not_exist(self.model_dir_path)
        create_dir_if_not_exist(self.pred_dir_path)
        create_dir_if_not_exist(self.result_test_dir_path)
        create_dir_if_not_exist(self.result_compare_dir_path)

    def get_train_file_name(self, train_num):
        return self.train_dir_path + 'train' + str(train_num) + '.dat'

    def get_test_file_name(self, test_num):
        return self.test_dir_path + 'test' + str(test_num) + '.dat'

    def get_model_file_name(self, train_num):
        return self.model_dir_path + 'model' + str(train_num) + '.txt'

    def get_pred_file_name(self, test_num):
        return self.pred_dir_path + 'prediction' + str(test_num) + '.txt'

    def get_result_compare_file_name(self, test_num):
        return self.result_compare_dir_path + 'compare' + str(test_num) + '.txt'

    def get_result_test_file_name(self, test_num):
        return self.result_test_dir_path + 'test' + str(test_num) + '.txt'

    def get_train_test_file(self, test_start, test_end):
        print 'writing train and test file', test_start
        top_person_list = get_top_person_names(self.tot_data_num)
        write_feature_file(top_person_list[:test_start] + top_person_list[test_end:], self.get_train_file_name(test_start))
        write_feature_file(top_person_list[test_start: test_end], self.get_test_file_name(test_start))

    def compare_pred_and_test(self, test_num):
        compare_line_list = []
        with open(self.get_pred_file_name(test_num)) as pred_file:
            pred_lines = pred_file.readlines()
        with open(self.get_test_file_name(test_num)) as test_file:
            test_lines = test_file.readlines()
        if len(pred_lines) != len(test_lines):
            print 'error'
            return

        unmatch_num = 0
        miss_positive_num = 0
        mistake_judge_num = 0
        for looper in range(len(pred_lines)):
            pred_line = pred_lines[looper]
            test_line = test_lines[looper]
            if not pred_line:
                continue
            pred_tag = pred_line.split(' ')[0]
            test_tag = test_line.split(' ')[0]
            test_tag = int(test_tag)
            if float(pred_tag) < 0.0:
                pred_tag = -1
            else:
                pred_tag = 1
            if pred_tag == test_tag:
                continue
            else:
                unmatch_num += 1
                mistake_judge_num += int(pred_tag == 1)
                miss_positive_num += int(pred_tag == -1)
                compare_line = '[%d/%d] %s' % (pred_tag, test_tag, test_line[test_line.index('#'):])
                compare_line_list.append(compare_line)
                pass

        compare_line_list = sorted(compare_line_list)
        with open(self.get_result_compare_file_name(test_num), 'w') as compare_file:
            compare_file.write('Accuracy: %f [%d/%d]\n' % (float(len(pred_lines)-unmatch_num)/float(len(pred_lines)), unmatch_num, len(pred_lines)))
            compare_file.write('误判：%d\n' % mistake_judge_num)
            compare_file.write('漏判：%d\n' % miss_positive_num)
            for compare_line in compare_line_list:
                compare_file.write(compare_line)

    def svm_learn(self, test_start):
        pass

    def svm_test(self, test_start, model_filename):
        pass

    def get_accuracy_from_result(self, test_file_content):
        pass

    def get_precision_from_result(self, test_file_content):
        pass

    def get_recall_from_result(self, test_file_content):
        pass

    def calculate_average(self):
        test_len = self.tot_data_num / 5
        tot_accuracy = 0
        tot_precision = 0
        tot_recall = 0
        for looper in range(5):
            test_file_name = self.get_result_test_file_name(looper * test_len)
            test_file_content = open(test_file_name).read()
            tot_accuracy += self.get_accuracy_from_result(test_file_content)
            tot_precision += self.get_precision_from_result(test_file_content)
            tot_recall += self.get_recall_from_result(test_file_content)
        average_accuracy = tot_accuracy / float(5)
        average_precision = tot_precision / float(5)
        average_recall = tot_recall / float(5)
        with open(self.result_root_path + '5-fold_result.txt', 'w') as result_file:
            result_file.write('accuracy: %f\nprecision: %f\nrecall: %f' % (average_accuracy, average_precision, average_recall))

    def run_with_test_from_to(self, test_start, test_end):
        self.get_train_test_file(test_start, test_end)
        self.svm_learn(test_start)
        self.svm_test(test_start, self.get_model_file_name(test_start))
        self.compare_pred_and_test(test_start)

    def run_five_fold(self):
        test_len = self.tot_data_num / 5
        for looper in range(4):
            self.run_with_test_from_to(looper * test_len, (looper+1) * test_len)
        self.run_with_test_from_to(4 * test_len, self.tot_data_num)
        self.calculate_average()


class SVMLight(SVM):

    svm_name = 'SVMlight'

    def __init__(self, tot_data_num):
        SVM.__init__(self, tot_data_num)

    def get_accuracy_from_result(self, test_file_content):
        end_pos = test_file_content.find('%')
        start_pos = test_file_content.find('Accuracy') + 22
        return float(test_file_content[start_pos: end_pos])

    def get_precision_from_result(self, test_file_content):
        start_pos = test_file_content.find('Precision') + 30
        end_pos = test_file_content.find('%', start_pos)
        return float(test_file_content[start_pos: end_pos])

    def get_recall_from_result(self, test_file_content):
        start_pos = test_file_content.find('Precision') + 37
        end_pos = test_file_content.find('%', start_pos)
        return float(test_file_content[start_pos: end_pos])

    def svm_learn(self, test_start):
        print 'svm learning', test_start
        cmd = '../svm_light/svm_learn ' + self.get_train_file_name(test_start) + ' ' + self.get_model_file_name(test_start)
        print cmd
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.wait()

    def svm_test(self, test_start, model_filename):
        print 'svm classifying', test_start
        cmd = '../svm_light/svm_classify ' + self.get_test_file_name(test_start) + ' ' + model_filename + ' ' + self.get_pred_file_name(test_start) + ' > ' + self.get_result_test_file_name(test_start)
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.wait()


class LibSVM(SVM):

    svm_name = 'LibSVM'

    def __init__(self, tot_data_num):
        SVM.__init__(self, tot_data_num)

    def svm_learn(self, test_start):
        print 'svm lib learning ', test_start
        cmd = '../libsvm-3/svm-train -t 0 ' + self.get_train_file_name(test_start) + ' ' + self.get_model_file_name(test_start)
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.wait()

    def svm_test(self, test_start, model_filename):
        print 'svm lib classifying', test_start
        cmd = '../libsvm-3/svm-predict ' + self.get_test_file_name(test_start) + ' ' + model_filename + ' ' + self.get_pred_file_name(test_start) + ' > ' + self.get_result_test_file_name(test_start)
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.wait()