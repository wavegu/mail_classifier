# encoding: utf-8
import subprocess
from person import write_feature_file
from util import get_top_person_names
from util import create_dir_if_not_exist


class ExpController:

    def __init__(self, tot_data_num):
        self.tot_data_num = tot_data_num
        self.data_root_path = '../svm_light/email/'
        self.result_root_path = '../result/'
        self.train_dir_path = self.data_root_path + 'train/'
        self.test_dir_path = self.data_root_path + 'test/'
        self.model_dir_path = self.data_root_path + 'model/'
        self.pred_dir_path = self.data_root_path + 'prediction/'
        self.result_test_dir_path = self.result_root_path + 'test/'
        self.result_compare_dir_path = self.result_root_path + 'compare/'
        create_dir_if_not_exist(self.data_root_path)
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

    def get_train_test_file(self, train_num):
        print 'writing train and test file', train_num
        top_person_list = get_top_person_names(self.tot_data_num)
        write_feature_file(top_person_list[:train_num], self.get_train_file_name(train_num))
        write_feature_file(top_person_list[train_num:], self.get_test_file_name(self.tot_data_num - train_num))

    def svm_learn(self, train_num):
        print 'svm learning', train_num
        cmd = '../svm_light/svm_learn ' + self.get_train_file_name(train_num) + ' ' + self.get_model_file_name(train_num)
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.wait()

    def svm_test(self, test_num, model_filename):
        print 'svm classifying', test_num
        cmd = '../svm_light/svm_classify ' + self.get_test_file_name(test_num) + ' ' + model_filename + ' ' + self.get_pred_file_name(test_num) + ' > ' + self.get_result_test_file_name(test_num)
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.wait()

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

    def run_exp_with_train_num(self, train_num):
        self.get_train_test_file(train_num)
        self.svm_learn(train_num)
        self.svm_test(self.tot_data_num-train_num, self.get_model_file_name(train_num))
        self.compare_pred_and_test(self.tot_data_num - train_num)

    def run_exp(self, min_train_num, max_train_num, delta_train_num):
        for train_num in range(min_train_num, max_train_num, delta_train_num):
            self.run_exp_with_train_num(train_num)


if __name__ == '__main__':
    controller = ExpController(250)
    controller.run_exp(150, 241, 10)