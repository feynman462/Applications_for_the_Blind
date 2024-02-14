import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
import pyperclip
import openpyxl

def is_valid_number(n):
    try:
        float(n)
        return True
    except ValueError:
        return False

def load_data():
    while True:
        method = input("Welcome to Stat Cruncher! Would you like to enter data manually or use an existing CSV file? Please type 'manual' or 'csv'.")
        if method.lower() == 'manual':
            column_names = input("Please enter column names, separated by commas: ").split(',')
            rows = []
            while True:
                row = input("Enter a row of data, separated by commas, or type 'done' when finished: ")
                if row.lower() == 'done':
                    break
                data = [float(x) if is_valid_number(x) else x for x in row.split(',')]
                if len(data) != len(column_names):
                    print("Error: Row length does not match the number of columns.")
                    continue
                rows.append(data)
            return pd.DataFrame(rows, columns=column_names)
        elif method.lower() == 'csv':
            file_name = input("Please enter the path to the CSV file: ")
            return pd.read_csv(file_name)
        else:
            print("Invalid input, please enter 'manual' or 'csv'.")

def ask_options():
    options = ["mean", "median", "mode", "range", "min", "max", "t-test", "ANOVA"]
    choices = {}
    print("Please type 'Y' or 'N' for the following options:")
    for option in options:
        while True:
            choice = input(f"Do you want to calculate {option}? ").lower()
            if choice in ['y', 'n']:
                choices[option] = choice == 'y'
                break
            else:
                print("Invalid choice. Please type 'Y' for Yes or 'N' for No.")
    return choices

def perform_statistical_tests(data, choices):
    results = {}
    for column in data.columns:
        if data[column].dtype in ['int64', 'float64']:
            if choices["mean"]:
                results[f"{column} mean"] = data[column].mean()
            if choices["median"]:
                results[f"{column} median"] = data[column].median()
            if choices["mode"]:
                mode_value = data[column].mode()
                if mode_value.empty:
                    results[f"{column} mode"] = "No mode"
                else:
                    results[f"{column} mode"] = mode_value.values[0]
            if choices["range"]:
                results[f"{column} range"] = data[column].max() - data[column].min()
            if choices["min"]:
                results[f"{column} min"] = data[column].min()
            if choices["max"]:
                results[f"{column} max"] = data[column].max()
            if choices["t-test"]:
                if len(data.columns) >= 2:
                    t_test_columns = input("Please enter the two column names, separated by comma, for the t-test: ").split(',')
                    t_stat, p_val = stats.ttest_rel(data[t_test_columns[0]], data[t_test_columns[1]])
                    results[f"t-test between {t_test_columns[0]} and {t_test_columns[1]}"] = f"t-statistic = {t_stat}, p-value = {p_val}"
            if choices["ANOVA"]:
                formula = input("Please enter the ANOVA formula (e.g., 'DependentVar ~ C(IndependentVar)'): ")
                model = ols(formula, data).fit()
                anova_table = anova_lm(model, typ=2)
                results["ANOVA"] = str(anova_table)
    return results

def main():
    while True:
        data = load_data()
        choices = ask_options()
        results = perform_statistical_tests(data, choices)
        for k, v in results.items():
            print(k, v)
        
        while True:
            next_step = input("What would you like to do next? (1: copy to clipboard, 2: export to Excel, 3: do another calculation, 4: quit) ")
            if next_step == '1':
                pyperclip.copy(str(results))
                print("Results copied to clipboard.")
            elif next_step == '2':
                df = pd.DataFrame(results, index=[0])
                df.to_excel('output.xlsx', index=False)
                print("Results exported to 'output.xlsx'.")
            elif next_step == '3':
                break
            elif next_step == '4':
                return
            else:
                print("Invalid choice. Please enter a number from 1 to 4.")

if __name__ == "__main__":
    main()
