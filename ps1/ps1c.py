# -*- coding: utf-8 -*-
"""
Created on Mon May 28 15:08:21 2018

Explore how both the percentage of your salary that you save each month and your 
annual raise affect how long it takes you to save for a down payment. 
Solve for portion of salary saved

@author: Alan Ly
"""

#user input
annual_salary = float(input("What is your annual salary: "))
base_annual_salary = annual_salary
monthly_salary = annual_salary/12
semi_annual_raise = 0.07

#margin of error
epsilon = 100

#number of months to make downpayment
months = 36

#return on investment per year
annual_return = 0.04

#initial balance
current_savings = 0.0

#down payment calculations
total_cost_home = 1000000
portion_down_payment = 0.25
down_payment = portion_down_payment*total_cost_home #250000

#initial bisection guess
initial_max = 10000
minrate = 0;
maxrate = initial_max;
portion_salary_saved = (maxrate + minrate)//2

#track number steps in bidirectional search
steps = 0

while(abs(current_savings - down_payment) > epsilon):
    
    steps += 1 #number of bisection cuts
    
#clear all initial values to recalculate a new savings rate
    current_savings = 0.0 
    annual_salary = base_annual_salary
    monthly_salary = annual_salary/12
    salary_saved = monthly_salary*(portion_salary_saved/10000)
#------------------------------------------------------------------------------
#Calculates the current_savings for 36 months with a "guess" savings rate 
    for month in range(1, months +1):
        
        current_savings *= 1 + annual_return/12
        current_savings += salary_saved

#a semi annual raise every 6*n months, takes into account the following month
        if month %6 == 0:
            annual_salary *= 1 + semi_annual_raise
            monthly_salary = annual_salary/12  
            salary_saved = monthly_salary*(portion_salary_saved/10000)
    
#stores previous savings rate to compare with future savings rate    
    prev_portion_saved = portion_salary_saved
#------------------------------------------------------------------------------
#Compares current_savings to down_payment, sets the limits of bisection cut

    if current_savings > down_payment:

        maxrate = portion_salary_saved
    
    else:
        minrate = portion_salary_saved
   
#Set new savings rate for the following iteration(next 36 month calculations)
    portion_salary_saved = int(round((maxrate + minrate)/2))
    
#if previous savings rate is equal to new savings rate, we have successfully
#found the best savings rate for 36 months
    if prev_portion_saved == portion_salary_saved:
        break
#------------------------------------------------------------------------------    
if portion_salary_saved == initial_max or prev_portion_saved == initial_max:
    print("Not possible to save for downpayment in 36 months, \n find a new job.")
else:   
    print("Best savings rate:", portion_salary_saved / 10000)
    print("Steps in bisection search", steps)




