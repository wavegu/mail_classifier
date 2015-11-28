# encoding: utf-8
from svm import SVMLight
from svm import LibSVM


class ExpController:

    def __init__(self, svm):
        self.svm = svm

    def run_exp(self):
        self.svm.run_five_fold()


if __name__ == '__main__':
    # controller = ExpController(LibSVM(250))
    # controller.run_exp()
    controller = ExpController(SVMLight(250))
    controller.run_exp()