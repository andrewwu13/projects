import pandas as pd
import numpy as np

# Load data with verification
try:
    data = pd.read_csv('/Users/andrewwu/Downloads/chem ia - Sheet1 (2).csv', skipinitialspace=True)
    assert 'change in height' in data.columns, "Missing 'change in height' column"
except Exception as e:
    print(f"Data loading error: {str(e)}")
    exit()

THEORETICAL_VOLUME = 620


def clean_compound_name(name):
    """Robust compound name standardization"""
    name = str(name).upper().strip().replace(" ", "")
    # Handle multiple ammonium carbonate representations
    if "NH2" in name:
        name = name.replace("NH2", "NH4")
    if ")3" in name and "CO3" in name:
        name = name.replace(")3", ")2")
    return name


results = []
for raw_name in data['compound'].dropna().unique():
    compound = clean_compound_name(raw_name)
    compound_data = data[data['compound'] == raw_name].copy()

    # Skip if no volume data
    if compound_data['change in height'].isna().all():
        continue

    # Theoretical yield adjustment
    theoretical_yield = THEORETICAL_VOLUME
    if compound == '(NH4)2CO3':
        theoretical_yield *= 0.5  # 50% NH₃ loss

    # Calculate percentage yields with proper uncertainty
    with np.errstate(divide='ignore', invalid='ignore'):
        percentage_yields = (compound_data['change in height'] / theoretical_yield) * 100
        yield_uncertainties = percentage_yields * (1.0 / compound_data['change in height'])

    # Calculate reaction rates with proper uncertainty
    rates = compound_data['temp change'] / compound_data['time taken']

    # Rate uncertainty using error propagation
    mean_rate = rates.mean()
    rate_uncertainty = mean_rate * np.sqrt(
        (compound_data['temp change'].std() / compound_data['temp change'].mean()) ** 2 +
        (compound_data['time taken'].std() / compound_data['time taken'].mean()) ** 2
    ) if len(compound_data) > 1 else 0

    # Data validation
    mean_experimental = compound_data['change in height'].mean()
    if mean_experimental > theoretical_yield * 1.05:  # Allow 5% margin
        print(f"Warning: {compound} experimental volume ({mean_experimental:.1f} cm³) "
              f"exceeds theoretical max ({theoretical_yield:.1f} cm³)")

    results.append({
        'Compound': raw_name,
        'Rate (K/s)': f"{mean_rate:.4f} ± {rate_uncertainty:.4f}",
        '% Yield': f"{percentage_yields.mean():.2f} ± {yield_uncertainties.mean():.2f}",
        'Trial Count': len(compound_data)
    })

# Generate results
results_df = pd.DataFrame(results)
print("\nFinal Results:")
print(results_df[['Compound', 'Rate (K/s)', '% Yield', 'Trial Count']])

# Save with timestamp
from datetime import datetime

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
results_df.to_csv(f'carbonate_results_{timestamp}.csv', index=False)