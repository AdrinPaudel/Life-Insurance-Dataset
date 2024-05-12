import random
import csv

# Function to calculate regular expenses
def calculate_expenses(income):
    h = 50000
    b = 200000
    a = 2500000
    m = 10000000
    n = 300000
    x = income
    y = -(h * (((a - b) / h) ** (((m - (x / 1.2)) / (m - n))))) + a
    return y

# Function to generate unexpected expenditure
def generate_unexpected_expense():
    return int(random.triangular(0, 3000, 100000))  # Triangular distribution around 3000

# Function to load tab rates from CSV
def load_tab_rates():
    tab_rates = []
    with open('X:\\Ai 1\\premium_calc_datasheet.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header row
        for row in reader:
            tab_rates.append(row[1:])  # Exclude the first column (age)
    return tab_rates

# Function to calculate insurance premium
def calculate_premium(age, insured_years, income, insured_amount, tab_rates, rebate, loading_charge):
    tab_rate = float(tab_rates[age - 18][insured_years - 5])
    premium = (tab_rate * loading_charge - rebate) * insured_amount / 1000
    return premium

# Open CSV file for writing
with open('insurance_data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Age', 'Income', 'Insurance Type', 'Premium Amount', 'Insured Years', 'Payment Type', 'Insured Amount', 'Percentage of Payment'])

    # Generate 10 instances
    for _ in range(100000):
        age = random.randint(18, 60)
        income_factor = random.randint(30, 1000)
        income = income_factor * 10000
        initial_income = income 
        max_for_individual = min(50000000, income * 8)
        insured_amount = random.randint(5, max_for_individual // 1000) * 1000
        insured_years = random.randint(5, 70 - age)
        rebate = 0
        if 25000 <= insured_amount < 50000:
            rebate = 0.5
        elif 50000 <= insured_amount < 100000:
            rebate = 1
        elif 100000 <= insured_amount < 200000:
            rebate = 1.5
        elif insured_amount >= 200000:
            rebate = 0.5
        
        loading_choice = random.choice(["yearly", "half_yearly", "quarterly", "monthly"])
        if loading_choice == "yearly":
            loading_charge = 1  # Yearly loading charge
        elif loading_choice == "half_yearly":
            loading_charge = 1.02 # Half-yearly loading charge
        elif loading_choice == "quarterly":
            loading_charge = 1.028 # Quarterly loading charge
        elif loading_choice == "monthly":
            loading_charge = 1.044 # Monthly loading charge
            
        expenses = calculate_expenses(income)
        tab_rates = load_tab_rates()
        
        savings = 0.1 * income  # Initial savings 10% of yearly income
        paid_term = 0
        for year in range(1, insured_years + 1):
            unexpected_expense = generate_unexpected_expense()
            unexpected_expense = (income/3000000) * unexpected_expense
            total_expenses = expenses + unexpected_expense 
            premium = calculate_premium(age, year, income, insured_amount, tab_rates, rebate, loading_charge)
            remaining_money = income - total_expenses
            
            if remaining_money >= premium:
                paid_term += 1
                savings += remaining_money - premium
            elif (remaining_money < premium) and (savings >= premium - remaining_money):
                paid_term += 1
                savings -= (premium - remaining_money)
            else:
                break

            # Apply inflation to total expenses
            expenses *= 1.05
        
            # Apply income growth
            income *= 1.07
        
        percent_completed = (paid_term / insured_years) * 100 if insured_years > 0 else 0
        
        yearly_premium = premium * (1 if insured_years == 0 else insured_years)

        writer.writerow([age, initial_income, 'Endowment', yearly_premium, insured_years, loading_choice, insured_amount, percent_completed])

print("CSV file generated successfully.")
