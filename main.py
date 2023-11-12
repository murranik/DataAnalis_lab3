import os
import json
import csv

def find_files_with_extension(directory, target_extension, results=None):
    if results is None:
        results = []

    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith(target_extension):
                results.append(os.path.join(root, filename))

    return results

def modify_json_with_array_indexes(data):
    def modify_object(obj):
        if isinstance(obj, dict):
            new_obj = {}
            for key, value in obj.items():
                if isinstance(value, list):
                    for i, item in enumerate(value):
                        new_key = f"{key}_{i}"
                        new_obj[new_key] = item
                else:
                    new_obj[key] = modify_object(value)
            return new_obj
        elif isinstance(obj, list):
            return [modify_object(item) for item in obj]
        else:
            return obj

    return modify_object(data)

def convert_and_save_to_csv(json_file, result_directory):
    with open(json_file, 'r') as json_file:
        json_data = json.load(json_file)
        
    modified_json = modify_json_with_array_indexes(json_data)
    
    base_filename = os.path.splitext(os.path.basename(json_file.name))[0]
    csv_filename = os.path.join(result_directory, f"{base_filename}.csv")

    counter = 1
    while os.path.exists(csv_filename):
        csv_filename = os.path.join(result_directory, f"{base_filename}({counter}).csv")
        counter += 1

    with open(csv_filename, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(modified_json.items())

def main():
    directory_to_search = "data"
    target_extension = ".json"
    result_directory = "result"
    
    if not os.path.exists(result_directory):
        os.makedirs(result_directory)
    
    found_files = find_files_with_extension(directory_to_search, target_extension)

    for file in found_files:
        convert_and_save_to_csv(file, result_directory)

if __name__ == "__main__":
    main()