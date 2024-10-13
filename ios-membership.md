# Step 1: Create a base DataFrame for EU membership
# This will hold the countries and their accession years to the EU.
import pandas as pd

# Example data structure:
data = {
    'Country': ['Country1', 'Country2'],
    'EU_Membership': [(2004, 2020)],  # Year of accession and exit if applicable
}

eu_membership_df = pd.DataFrame(data)

# Step 2: Expand the DataFrame for other international organizations
# Add columns for each organization you want to track, with their respective membership periods.
# Example: Adding NATO and OECD membership with periods
eu_membership_df['NATO_Membership'] = [((NATO_start_year1, NATO_end_year1), (NATO_start_year2, NATO_end_year2))]
eu_membership_df['OECD_Membership'] = [((OECD_start_year1, OECD_end_year1), (OECD_start_year2, OECD_end_year2))]

# Step 3: Include functions to update the DataFrame
# Define functions to add or update membership information as needed.
def add_membership(df, country, org, start_year, end_year=None):
    # Check if country exists, if not, create a new entry
    if country not in df['Country'].values:
        new_row = {'Country': country}
        df = df.append(new_row, ignore_index=True)
    
    # Update the respective organization's membership periods
    current_membership = df.loc[df['Country'] == country, f'{org}_Membership'].values[0]
    if pd.isna(current_membership[0]):
        df.loc[df['Country'] == country, f'{org}_Membership'] = [(start_year, end_year)]
    else:
        # Append a new membership period
        df.loc[df['Country'] == country, f'{org}_Membership'].append((start_year, end_year))

# Step 4: Keep your dataset flexible
# You can easily expand this structure by adding more organizations and their respective membership periods.
# Ensure to document each organization you are tracking.

# Example usage of the function:
add_membership(eu_membership_df, 'Country1', 'NATO', 2004, 2010)  # Example with end year
add_membership(eu_membership_df, 'Country1', 'NATO', 2015)         # Example without end year

# Step 5: Save the DataFrame for future use
# Use pandas to save the DataFrame to a CSV or Excel file for persistence.
eu_membership_df.to_csv('membership_data.csv', index=False)
