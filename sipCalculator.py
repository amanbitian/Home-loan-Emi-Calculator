def calculate_sip_details(sip_amount, annual_increment, tenure, rate_of_return):
    total_investment = 0
    total_interest = 0
    total_return = 0
    total_tax_deducted = 0

    for month in range(1, tenure * 12 + 1):
        monthly_increment = (sip_amount * annual_increment / 100) / 12
        sip_amount += monthly_increment

        monthly_investment = sip_amount
        total_investment += monthly_investment

        monthly_interest = (total_investment - monthly_investment) * (rate_of_return / 100) / 12
        total_interest += monthly_interest

        monthly_return = monthly_investment + monthly_interest
        total_return += monthly_return

        # Assuming 10% tax on the gains for SIP in India
        tax_rate = 0.10
        monthly_tax_deducted = monthly_interest * tax_rate
        total_tax_deducted += monthly_tax_deducted

    final_return_post_tax = total_return - total_tax_deducted

    return {
        "Total Investment": total_investment,
        "Total Interest Gained": total_interest,
        "Total Return": total_return,
        "Total Tax Deducted (10% on gains)": total_tax_deducted,
        "Final Return Post Tax Deduction": final_return_post_tax
    }


# Get user inputs
sip_amount = float(input("Enter SIP amount per month: "))
annual_increment = float(input("Enter annual increment in percentage: "))
tenure = int(input("Enter tenure in years: "))
rate_of_return = float(input("Enter expected rate of return in percentage: "))

# Calculate SIP details
sip_details = calculate_sip_details(sip_amount, annual_increment, tenure, rate_of_return)

# Display the results
print("\nSIP Details:")
for key, value in sip_details.items():
    print(f"{key}: {value:.2f}")
