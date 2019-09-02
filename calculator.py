#!/usr/bin/env python3

import sys

def get_income():
    """获取用户工资金额"""

    if len(sys.argv[:]) == 2:
        try:
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
    if taxable_income <= 0:
        tax = 0
    elif 0 < taxable_income <= 3000:
        tax = taxable_income * 0.03
    elif 3000 < taxable_income <= 12000:
        tax = taxable_income * 0.1 - 210 
    elif 12000 < taxable_income <= 25000:
        tax = taxable_income * 0.2 - 1410
    elif 25000 < taxable_income <= 35000:
        tax = taxable_income * 0.25 - 2660
    elif 35000 < taxable_income <= 55000:
        tax = taxable_income * 0.3 - 4410
    elif 55000 < taxable_income <= 80000:
        tax = taxable_income * 0.35 - 7160
    elif taxable_income > 80000:
        tax = taxable_income * 0.45 - 15160
    return tax

def print_tax(tax):
    """按照指定格式打印税额"""

    print('{:.2f}'.format(tax))

def main():
    income = get_income()
    tax = get_tax(income)
    print_tax(tax)

if __name__ == "__main__":
    main()
