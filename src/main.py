from src.utils import open_file, sort_list, get_operations, format_operation

operations = open_file("operations.json")
sorted_operations = sort_list(operations)

for i in get_operations(5):
    print(format_operation(i))




