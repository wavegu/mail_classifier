# encoding: utf-8
from util import del_a_from_b

g_email_model_list = []


class EmailModel:

    def __init__(self, person_name, email_addr, brother_email_addr_list, tag):
        self.email_addr = email_addr
        self.brother_email_addr_list = brother_email_addr_list
        self.person_name = person_name.lower().replace('.', '').replace('-', '')
        self.tag = tag
        self.is_last_name_in_google_title = False
        self.is_last_name_in_google_content = False
        self.max_affiliation_proportion_in_title = 0.0
        self.max_affiliation_proportion_in_content = 0.0

    # 除last_name外，地址前缀包含名字的情况
    def get_f_contain_name_without_last(self):

        f_contain_name = 0
        last_name = self.person_name.split(' ')[-1]
        name_part_list = self.person_name.split(' ')[:-1]
        # 将名字部分列表按长度排序，长的部分先参与计算
        name_part_list = sorted(name_part_list, key=lambda name_part: len(name_part), reverse=True)

        temp_addr = self.email_addr[:self.email_addr.find('@')].replace('.', '').replace('_', '').replace('-', '')
        temp_addr = del_a_from_b(last_name, temp_addr)
        for name_part in name_part_list:
            # 如果名字的某部分在前缀中，f_contain_name加上该部分的长度，并从前缀和name_part_list中去掉该部分
            if name_part in temp_addr:
                temp_addr = del_a_from_b(name_part, temp_addr)
                f_contain_name += len(name_part)
                # 在for循环中使用remove是危险的，故标为空，相当于删除这个名字部分
                name_part_list[name_part_list.index(name_part)] = ''

        # 对于没有被全包含的名字部分，看其首字母是否在前缀中
        for name_part in name_part_list:
            if name_part and name_part[0] in temp_addr:
                f_contain_name += 1

        # 归一化
        f_contain_name = float(f_contain_name) / (float(len(del_a_from_b(last_name, self.email_addr[:self.email_addr.find('@')]))) + 1)
        return f_contain_name

    def get_f_contain_last_name(self):
        last_name = self.person_name.split(' ')[-1]
        addr_prefix = self.email_addr[:self.email_addr.find('@')]
        return float(last_name in self.email_addr) * float(len(last_name)) / (float(len(addr_prefix))+1)

    def get_f_addr_repeat_time(self):
        return float(self.brother_email_addr_list.count(self.email_addr)) / float(len(self.brother_email_addr_list))

    def get_f_domain_repeat_time(self):
        target_domain = self.email_addr[self.email_addr.find('@'):]
        domain_list = [mail[mail.find('@'):] for mail in self.brother_email_addr_list]
        return float(domain_list.count(target_domain)) / float(len(domain_list))

    def get_f_first_char_all_in_addr(self):
        name_part_list = self.person_name.split(' ')
        first_char_in_num = 0
        email_prefix = self.email_addr[:self.email_addr.find('@')]
        prefix_len = len(email_prefix)
        for name_part in name_part_list:
            if name_part[0] in email_prefix:
                first_char_in_num += 1
                del_a_from_b(name_part[0], email_prefix)
        return float(first_char_in_num) / float(prefix_len)

    def get_feature_line(self):
        feature_line = str(self.tag)
        # feature_line = ''
        feature_line += ' 1:' + str(self.get_f_contain_name_without_last())
        feature_line += ' 2:' + str(self.get_f_contain_last_name())
        feature_line += ' 3:' + str(self.get_f_addr_repeat_time())
        feature_line += ' 4:' + str(self.get_f_domain_repeat_time())
        feature_line += ' 5:' + str(self.get_f_first_char_all_in_addr())
        feature_line += ' 6:' + str(int(self.is_last_name_in_google_title))
        feature_line += ' 7:' + str(int(self.is_last_name_in_google_content))
        feature_line += ' 8:' + str(self.max_affiliation_proportion_in_title)
        feature_line += ' 9:' + str(self.max_affiliation_proportion_in_content)
        feature_line += ' 10:' + str(int(self.email_addr[:self.email_addr.find('@')] == 'email'))
        feature_line += ' 11:' + str(int(self.email_addr[:self.email_addr.find('@')] == 'info'))
        feature_line += '     # [%s] [%s] [%f, %f] [%d, %d] [%f, %f]' % (self.person_name, self.email_addr, self.get_f_addr_repeat_time(), self.get_f_domain_repeat_time(), int(self.is_last_name_in_google_title), int(self.is_last_name_in_google_content), self.max_affiliation_proportion_in_title, self.max_affiliation_proportion_in_content)
        return feature_line

    def display(self):
        print self.tag, self.email_addr, '[%s]' % self.person_name


if __name__ == '__main__':
    name = 'aart kraay'
    addr = 'akraay@worldbank.org'
    mail_model = EmailModel(name, addr, [], 1)
    # mail_list = ['fsa@126.com', 'lgwe@126.com', 'lala@432.com', 'wve@qq.com']
    # print mail_model.get_f_contain_name()