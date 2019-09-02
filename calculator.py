#!/usr/bin/env python3

import sys
from collections import namedtuple

def get_income():
    """获取用户工资金额"""

    for arg in sys.argv[1:]:
        try:
            arg.split(":")

        
            income = int(sys.argv[1])
        except:
            print("Parameter Error")
            sys.exit()
        else:
            return income
    else:
        print("您的输入格式不正确,请按以下格式重新输入: ")
        print("python3 claculator.py income")
        sys.exit()

def get_tax(income):
    """计算用户纳税金额"""

    threshold = 5000
    social_insurance_charges = 0
    special_deduction = 0
    taxable_income = income - social_insurance_charges - special_deduction - threshold
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
    
    for tax_ratio in tax_ratio_table:
        if taxable_income > tax_ratio.start:
            tax = taxable_income * tax_ratio.ratio - tax_ratio.deduction
            return tax
    return 0

def print_tax(tax):
    """按照指定格式打印税额"""

    print('{:.2f}'.format(tax))

def main():
    income = get_income()
    tax = get_tax(income)
    print_tax(tax)

if __name__ == "__main__":
    main()
