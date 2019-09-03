#!/usr/bin/env python3

import sys
from collections import namedtuple

def get_income():
    """获取用户工资金额"""
    
    income_dict = {}
    for arg in sys.argv[1:]:
        try:
            income_list = arg.split(":")
            income_dict[income_list[0]] = int(income_list[1])
        except:
            print("Parameter Error")
            sys.exit()
    return income_dict

def get_social_insurance_charges(income_dict):
    """计算用户社保金额"""
    
    social_insurance_charges_dict = {}
    social_insurance_charges_table = {'YangLao': 0.08, 'YiLiao': 0.02, 'ShiYe': 0.005, 'GongShang': 0, 'ShengYu':0, 'GongJinJin': 0.06}
    special_deduction = 0
    social_insurance_charges_sum = sum([charges for charges in social_insurance_charges_table.values()])
    for id, income in income_dict.items():
        social_insurance_charges_dict[id] = income * social_insurance_charges_sum
    return social_insurance_charges_dict

def get_taxable_income(income_dict, social_insurance_charges_dict):
    """计算用户应纳税所得额"""
    
    taxable_income_dict = {}
    threshold = 5000
    special_deduction = 0
    for id, income in income_dict.items():    
        taxable_income_dict[id] = income - social_insurance_charges_dict.get(id) - special_deduction - threshold
    return taxable_income_dict

def get_tax(taxable_income_dict):
    """计算用户纳税金额"""
    
    tax_dict = {}
    tax_ratio = namedtuple('tax_ratio', ['start', 'ratio', 'deduction'])
    tax_ratio_table = [
                        tax_ratio(80000, 0.45, 15160),
                        tax_ratio(55000, 0.35, 7160),
                        tax_ratio(35000, 0.3, 4410), 
                        tax_ratio(25000, 0.25, 2660),
                        tax_ratio(12000, 0.2, 1410),
                        tax_ratio(3000, 0.1, 210),
                        tax_ratio(0, 0.03, 0)
                        ]
    for id, taxable_income in taxable_income_dict.items():
        for tax_ratio in tax_ratio_table:
            if taxable_income > tax_ratio.start:
                tax_dict[id] = taxable_income * tax_ratio.ratio - tax_ratio.deduction
                break
        else:
            tax_dict[id] = 0
    return tax_dict

def get_after_tax_income(income_dict, social_insurance_charges_dict, tax_dict):
    """计算税后工资表"""

    after_tax_income_dict = {}
    for id, income in income_dict.items():
        after_tax_income_dict[id] = income - social_insurance_charges_dict.get(id) - tax_dict.get(id)
    return after_tax_income_dict

def print_tax(after_tax_income_dict):
    """按照指定格式打印税后工资表"""

    for id, after_tax_income in after_tax_income_dict.items():
        print('{}:{:.2f}'.format(id, after_tax_income))

def main():
    # 获取工资单
    income_dict = get_income()
    # 计算社保金额
    social_insurance_charges_dict = get_social_insurance_charges(income_dict)
    # 计算应纳税所得额
    taxable_income_dict = get_taxable_income(income_dict, social_insurance_charges_dict)
    # 计算税额
    tax_dict = get_tax(taxable_income_dict)
    # 计算税后工资
    after_tax_income_dict = get_after_tax_income(income_dict, social_insurance_charges_dict, tax_dict)
    # 打印税后工资表
    print_tax(after_tax_income_dict)

if __name__ == "__main__":
    main()
