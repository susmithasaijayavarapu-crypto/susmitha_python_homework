import pandas as pd

data = {
        "Name": ['Alice', 'Bob', 'Charlie'],
        "Age": [25, 30, 35],
        "City": ['New York', 'Los Angeles', 'Chicago']
}

task1_data_frame = pd.DataFrame(data)
print(task1_data_frame)

task1_with_salary = task1_data_frame.copy()
task1_with_salary["Salary"] = [70000, 80000, 90000]
print(task1_with_salary)

task1_older= task1_with_salary.copy()
task1_older['Age'] = task1_older['Age'] +1
print(task1_older)

task1_older.to_csv('employees.csv', index=False)

task2_employees = pd.read_csv('employees.csv')
print (task2_employees)

additional_employees = [
    {"Name": "Eve", "Age": 28, "City": "Miami", "Salary": 60000},
    {"Name": "Frank", "Age": 40, "City": "Seattle", "Salary": 95000}
]
json_employees = pd.DataFrame(additional_employees)
json_employees.to_json('additional_employees.json', orient='records', indent=4)
print(json_employees)

more_employees = pd.concat([task2_employees,json_employees],ignore_index=True )
print(more_employees)
    
first_three = more_employees.head(3)
print(first_three)

last_two= more_employees.tail(2)
print(last_two)

employee_shape= more_employees.shape
print(employee_shape)

employee_info= more_employees.info()
print(employee_info)

dirty_data = pd.read_csv('dirty_data.csv')
print(dirty_data)
clean_data  = dirty_data.copy()
print(clean_data)
clean_data.drop_duplicates(inplace=True)

clean_data['Age']= pd.to_numeric(clean_data['Age'], errors= "coerce")
mean_age = clean_data['Age'].mean()
clean_data['Age'] = clean_data['Age'].fillna(mean_age)
print(clean_data)

import numpy as np


clean_data['Salary'] = clean_data['Salary'].replace(['unknown', 'n/a', 'N/A', 'Unknown'], np.nan)
clean_data['Salary']= pd.to_numeric(clean_data['Salary'], errors= "coerce")
print(clean_data)

median_salary = clean_data['Salary'].median()
clean_data['Salary'] = clean_data['Salary'].fillna(median_salary)
print(clean_data)

clean_data['Hire Date'] = pd.to_datetime(clean_data['Hire Date'], format='mixed',errors='coerce')
clean_data['Hire Date'] = clean_data['Hire Date'].fillna(pd.to_datetime('2021-01-01'))
print(clean_data)

clean_data['Name'] = clean_data['Name'].str.strip()
clean_data['Department'] = clean_data['Department'].str.upper()
print(clean_data)