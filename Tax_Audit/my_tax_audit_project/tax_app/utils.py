def calculate_tax(income, expenses, deductions):
    taxable_income = income - expenses - deductions
    tax_rate = 0.2  # Example flat tax rate
    tax_due = taxable_income * tax_rate
    return max(tax_due, 0)