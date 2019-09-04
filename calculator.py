#!/usr/bin/env python3

import sys
import csv
from collections import namedtuple

# 处理命令行程序
class Args(object):

    def __init__(self):
        self._args = sys.argv[1:]
        self.file_path_dict = {}

    def get_file_path(self):
        """从命令行获取文件路径"""

        try:
            for i in range(0, len(self._args), 2):
                self.file_path_dict[self._args[i]] = self._args[i + 1]
        except:
            print("ParameterError")
            sys.exit()
        return self.file_path_dict

# 配置文件类
class Config(object):

    def __init__(self, file_path):
        self._file_path = file_path
        self._config_dict = {}

    def get_config_file(self):
        """根据路径获取配置文件"""
        try:
            with open(self._file_path) as f:
                for data in f.readlines():
                    data_list = data.strip().split(" = ")
                    self._config_dict[data_list[0]] = float(data_list[1])
        except:
            print("ParameterError")
            sys.exit()
        return self._config_dict

# 用户文件类
class UserData(object):

    def __init__(self, file_path):
        self._file_path = file_path
        self._user_data = {}

    def get_userdata_file(self):
        """根据路径获取用户工资文件"""

        try:
            with open(self._file_path) as f:
                for data in list(csv.reader(f)):
                    self._user_data[data[0]] = int(data[1])
        except:
            print("ParameterError")
            sys.exit()
        return self._user_data

# 工资税务计算器
class IncomeTaxCalculator(object):

    def __init__(self, config_dict, user_data):
        self._config_dict = config_dict
        self._user_data = user_data
        self.social_insurance_charges_dict = {}
        self.taxable_income_dict = {}
        self.tax_dict = {}
        self.tax_ratio = namedtuple('tax_ratio', ['start', 'ratio', 'deduction'])
        self.tax_ratio_table = [
            self.tax_ratio(80000, 0.45, 15160),
            self.tax_ratio(55000, 0.35, 7160),
            self.tax_ratio(35000, 0.3, 4410),
            self.tax_ratio(25000, 0.25, 2660),
            self.tax_ratio(12000, 0.2, 1410),
            self.tax_ratio(3000, 0.1, 210),
            self.tax_ratio(0, 0.03, 0)
        ]
        self.after_tax_income_dict = {}
        self.export_income_list = []

    def get_social_insurance_charges(self):
        """计算用户社保金额"""

        social_insurance_charges_sum = sum([data for data in self._config_dict.values()])\
                                       - self._config_dict["JiShuL"] - self._config_dict["JiShuH"]
        for id, income in self._user_data.items():
            if income < self._config_dict["JiShuL"]:
                self.social_insurance_charges_dict[id] = self._config_dict["JiShuL"] * social_insurance_charges_sum
            elif income > self._config_dict["JiShuH"]:
                self.social_insurance_charges_dict[id] = self._config_dict["JiShuH"] * social_insurance_charges_sum
            else:
                self.social_insurance_charges_dict[id] = income * social_insurance_charges_sum

    def get_taxable_income(self):
        """计算用户应纳税所得额"""

        threshold = 5000
        special_deduction = 0
        for id, income in self._user_data.items():
            self.taxable_income_dict[id] = income - self.social_insurance_charges_dict.get(id)\
                                           - special_deduction - threshold

    def get_tax(self):
        """计算用户纳税金额"""

        for id, taxable_income in self.taxable_income_dict.items():
            for tax_ratio in self.tax_ratio_table:
                if taxable_income > tax_ratio.start:
                    self.tax_dict[id] = taxable_income * tax_ratio.ratio - tax_ratio.deduction
                    break
            else:
                self.tax_dict[id] = 0

    def get_after_tax_income(self):
        """计算税后工资表"""

        for id, income in self._user_data.items():
            self.after_tax_income_dict[id] = income - self.social_insurance_charges_dict.get(id)\
                                             - self.tax_dict.get(id)

    def export(self,file_path):
        """按照指定格式输出工资表文件"""

        for id, income, in self._user_data.items():
            row_list = [id, income, f'{self.social_insurance_charges_dict.get(id):.2f}',
                        f'{self.tax_dict.get(id):.2f}', f'{self.after_tax_income_dict.get(id):.2f}']
            self.export_income_list.append(row_list)

        with open(file_path, 'w') as f:
            csv.writer(f).writerows(self.export_income_list)


def main():
    # 获取文件路径
    args = Args()
    # 初始化配置文件类
    config = Config(args.get_file_path().get('-c'))
    # 初始化用户信息类
    userdata = UserData(args.get_file_path().get('-d'))
    # 初始化工资税务计算器类
    income_tax_calculator = IncomeTaxCalculator(config.get_config_file(), userdata.get_userdata_file())
    # 计算社保金额
    income_tax_calculator.get_social_insurance_charges()
    # 计算应纳税所得额
    income_tax_calculator.get_taxable_income()
    # 计算税额
    income_tax_calculator.get_tax()
    # 计算税后工资
    income_tax_calculator.get_after_tax_income()
    # 打印税后工资表
    income_tax_calculator.export(args.get_file_path().get('-o'))

if __name__ == "__main__":
    main()
