import csv

with open("../csv/employees.csv", mode="r", encoding="utf-8") as file:
    reader = csv.reader(file)
    employees_data = list(reader)

    header = employees_data[0]

    fn_idx = header.index("first_name")
    ln_idx = header.index("last_name")

    employee_names = [f"{row[fn_idx]} {row[ln_idx]}" for row in employees_data[1:] if len(row) > max(fn_idx, ln_idx)]
    print (employee_names)

    employees_with_e = [name for name in employee_names if 'e' in name or 'E' in name]
    print ("Employee names having e :")
    print(employees_with_e)