from src.utils import open_file, sort_list, get_operations, format_operation, clean_data

operations = open_file("../operations.json")
cleaned_data = clean_data(operations)
sorted_operations = sort_list(cleaned_data)

for i in get_operations(5):
    print(format_operation(i))
