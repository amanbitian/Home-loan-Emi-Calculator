import streamlit as st
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Set seaborn color palette similar to McKinsey
sns.set_palette("Set2")
mckinsey_colors = sns.color_palette("Set2").as_hex()

def calculate_sip_details(sip_amount, annual_increment, tenure, rate_of_return):
    total_investment = 0
    total_interest = 0
    total_return = 0
    total_tax_deducted = 0

    sip_data = []

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

        sip_data.append({
            'Month': month,
            'Investment': total_investment,
            'Interest': total_interest,
            'TotalReturn': total_return,
            'TaxDeducted': total_tax_deducted
        })

    final_return_post_tax = total_return - total_tax_deducted

    return {
        "Total Investment": total_investment,
        "Total Interest Gained": total_interest,
        "Total Return": total_return,
        "Total Tax Deducted (10% on gains)": total_tax_deducted,
        "Final Return Post Tax Deduction": final_return_post_tax,
        'SIP Data': pd.DataFrame(sip_data)
    }

# Streamlit UI
st.set_page_config(page_title="SIP Calculator", page_icon="💹")

# Header
st.title("SIP Calculator")
st.subheader("Calculate and visualize the details of your Systematic Investment Plan")

# Get user inputs
sip_amount = st.number_input("Enter SIP amount per month:", value=1000.0)
annual_increment = st.number_input("Enter annual increment in percentage:", value=0.0)
tenure = st.number_input("Enter tenure in years:", value=10)
rate_of_return = st.number_input("Enter expected rate of return in percentage:", value=12.0)

# Calculate SIP details
sip_details = calculate_sip_details(sip_amount, annual_increment, tenure, rate_of_return)

# Display the results
st.header("SIP Details:")
st.write(f"Total Investment: {sip_details['Total Investment']:.2f}")
st.write(f"Total Interest Gained: {sip_details['Total Interest Gained']:.2f}")
st.write(f"Total Return: {sip_details['Total Return']:.2f}")
st.write(f"Total Tax Deducted (10% on gains): {sip_details['Total Tax Deducted (10% on gains)']:.2f}")
st.write(f"Final Return Post Tax Deduction: {sip_details['Final Return Post Tax Deduction']:.2f}")

# Plotting SIP data
st.header("SIP Data Over Time:")
fig, ax1 = plt.subplots(figsize=(10, 6))
ax2 = ax1.twinx()

sip_data = sip_details['SIP Data']
ax1.plot(sip_data['Month'], sip_data['Investment'], 'g-', label='Investment')
ax2.plot(sip_data['Month'], sip_data['Interest'], 'b-', label='Interest', linestyle='dashed')

ax1.set_xlabel('Month')
ax1.set_ylabel('Investment', color='g')
ax2.set_ylabel('Interest', color='b')

st.pyplot(fig)

# Pie chart for Total Return Composition
st.header("Total Return Composition:")
composition_data = pd.DataFrame({
    'Category': ['Total Investment', 'Total Interest Gained'],
    'Amount': [sip_details['Total Investment'], sip_details['Total Interest Gained']]
})
fig_pie = px.pie(composition_data, values='Amount', names='Category',
                 title="Composition of Total Return",
                 hole=0.3, color_discrete_sequence=mckinsey_colors)
st.plotly_chart(fig_pie)
