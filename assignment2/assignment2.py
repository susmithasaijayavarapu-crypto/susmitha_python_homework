import csv
import sys
import traceback

def read_employees():
    data ={}
    rows=[]
    try :
        with open("../csv/employees.csv", mode ='r') as csvfile:
            reader = csv.reader(csvfile)
            is_first_row = True
            for row in reader:
                if is_first_row:
                    data["fields"]= row
                    is_first_row = False
                else :
                    rows.append(row)
            data["rows"]= rows
            return data

    except Exception as e:
        # Handle exceptions using the traceback module
        trace_back = traceback.extract_tb(e.__traceback__)
        stack_trace = list()
        for trace in trace_back:
            stack_trace.append(f'File : {trace[0]} , Line : {trace[1]}, Func.Name : {trace[2]}, Message : {trace[3]}')
        
        print("An exception occurred.")
        print(f"Exception type: {type(e).__name__}")
        message = str(e)
        if message:
            print(f"Exception message: {message}")
        print(f"Stack trace: {stack_trace}")
        
        # Exit the program upon exception
        sys.exit()
employees = read_employees()
print(employees)


#task 3 column index

def column_index(column_name):
    return employees["fields"].index(column_name)

employee_id_column = column_index("employee_id")


#task 4 
def first_name(row_number):
    index = column_index("first_name")
    return employees["rows"][row_number][index]
   

#task 5 
def employee_find(employee_id):
    def employee_match(row):
        
        return int(row[employee_id_column]) == employee_id
    matches=list(filter(employee_match, employees["rows"]))
    return matches
    

#task 6
def employee_find_2(employee_id):
    matches = list(filter(lambda row : int(row[employee_id_column]) == employee_id,employees["rows"] ))
    return matches


#task 7
def sort_by_last_name():
    last_name_idx = column_index("last_name")
    employees["rows"].sort(key=lambda row: row[last_name_idx])
    return employees["rows"]
sort_by_last_name()
print(employees)

#task 8
def employee_dict(row):
    emp_data = {}
    id_index = column_index("employee_id")
    for i, header in enumerate(employees["fields"]):
        if i == id_index:
            continue
        emp_data[header] = row[i]
    return emp_data

#task 9
def all_employees_dict():
    combined_dict = {}
    id_index = column_index("employee_id")
    for row in employees["rows"]:
        emp_id = row[id_index]
        
        combined_dict[emp_id] = employee_dict(row)
    return combined_dict  
all_emp=all_employees_dict()
print(all_emp)

#task 10
import os

def get_this_value():

    return os.environ.get("THISVALUE")
this_value = get_this_value()
print(f"The value of THISVALUE is: {this_value}")

#task 11
import custom_module
def set_that_secret(new_secret):
    custom_module.set_secret(new_secret)
set_that_secret("Abracadabra!")
print(f"The new secret is: {custom_module.secret}")

#task12
def _read_csv_to_dict(file_path):
    
    data = {"fields": [], "rows": []}
    with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        data["fields"] = next(reader)
        # Convert each row to a tuple as requested
        for row in reader:
            data["rows"].append(tuple(row))
    return data
def read_minutes():
    
    minutes1 = _read_csv_to_dict("../csv/minutes1.csv")
    minutes2 = _read_csv_to_dict("../csv/minutes2.csv")
    return minutes1, minutes2


minutes1, minutes2 = read_minutes()
print("Minutes 1 Data:", minutes1)
print("Minutes 2 Data:", minutes2)


#task13

def create_minutes_set():
    
    set1 = set(minutes1["rows"])
    set2 = set(minutes2["rows"])
    
    minutes_set = set1 | set2
    
    return minutes_set


minutes_set = create_minutes_set()

print("Combined unique minutes set:", minutes_set)

#task 14

from datetime import datetime

def create_minutes_list():
   
    temp_list = list(minutes_set)
  
    minutes_mapped = map(lambda x: (x[0], datetime.strptime(x[1], "%B %d, %Y")), temp_list)
    return list(minutes_mapped)


minutes_list = create_minutes_list()

print("Minutes list with datetime objects:")
for item in minutes_list:
    print(item)
        
#task15
def write_sorted_list():
  
    minutes_list.sort(key=lambda x: x[1])
    converted_list = list(map(lambda x: (x[0], x[1].strftime("%B %d, %Y")), minutes_list))
    
   
    with open('./minutes.csv', mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        writer.writerow(minutes1["fields"])
       
        writer.writerows(converted_list)
        
    return converted_list


sorted_data = write_sorted_list()


print("Sorted and saved minutes:")
for row in sorted_data:
    print(row)
