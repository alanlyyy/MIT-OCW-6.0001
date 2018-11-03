# -*- coding: utf-8 -*-
"""
Created on Mon May 28 12:55:22 2018

The goal of this program is to to determine how 
long it will take you to save enough money to 
make the down payment given the following 
assumptions:

@author: Alan Ly
"""
#user input
total_cost_home = float(input("What is the cost of your dream home: "))
annual_salary = float(input("What is your annual salary: "))
portion_salary_saved = float(input("What portion of salary do you want to save: "))

#down payment calculations
portion_down_payment = 0.25
down_payment = portion_down_payment*total_cost_home

#initial balance
current_savings = 0

#return on investment per year
annual_return = 0.04

monthly_salary = annual_salary/12

#counter variable for the number of months
months = 0

while current_savings <= down_payment:
    salary_saved = monthly_salary*portion_salary_saved
    monthly_return = current_savings*annual_return/12
    #print(monthly_return)
    current_savings = current_savings + salary_saved + monthly_return
    months += 1

print("Number of months: ", months)
