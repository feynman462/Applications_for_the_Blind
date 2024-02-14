import pandas as pd
from math import isnan

# Set up the dictionary of conversion factors
def setup_conversions():
    conversion_data = pd.read_excel('conversion_factors.xlsx')
    return conversion_data

# Perform conversion
def convert_units(conversion_data, from_unit, to_unit, value):
    # Find the conversion factor
    factor_df = conversion_data[(conversion_data['from_unit'] == from_unit) & 
                                (conversion_data['to_unit'] == to_unit)]
    if factor_df.empty:
        raise ValueError(f"No conversion factor found for {from_unit} to {to_unit}")

    factor = factor_df['factor'].values[0]
    if isnan(factor):
        raise ValueError(f"Conversion factor for {from_unit} to {to_unit} is not a real number")
    return value * factor

# Main function
def main():
    conversion_data = setup_conversions()

    from_unit = input("Enter the unit you want to convert from: ")
    to_unit = input("Enter the unit you want to convert to: ")
    value = float(input("Enter the value you want to convert: "))

    try:
        converted_value = convert_units(conversion_data, from_unit, to_unit, value)
        print(f"{value} {from_unit} is equivalent to {converted_value} {to_unit}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
