# encoding: utf-8
from svm import SVMLight
from svm import LibSVM


class ExpController:

    def __init__(self, svm):
        self.svm = svm

    def run_exp(self, min_train_num, max_train_num, delta_train_num):
        for train_num in range(min_train_num, max_train_num, delta_train_num):
            self.svm.run(train_num)


if __name__ == '__main__':
    controller = ExpController(LibSVM(250))
    controller.run_exp(150, 240, 10)
    # controller = ExpController(SVMLight(250))
    # controller.run_exp(150, 240, 10)