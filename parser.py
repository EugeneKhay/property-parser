# pip3 install jproperties
# pip3 install dictdiffer
# Description: python3 parser.py -h

import os
import json
import argparse
from os.path import exists
from jproperties import Properties
from dictdiffer import diff

PROPERTIES_EXTENSION = '.properties'
JSON_EXTENSION = '.json'

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--source", help="Source path")
parser.add_argument("-t", "--target", help="Target path")
parser.add_argument("-ct", "--createtarget", 
                    help="Should target be created if not exists: 0 - false, 1 - true", 
                    type=int)
parser.add_argument("-i", "--info", 
                    help="Shows info about changed values", 
                    type=int)
args = parser.parse_args()

target_dir = args.target
show_info = False


def read_bool_cli_flag(arg, name_for_error, default_value):
    if arg != None:
        if (arg != 0 and arg != 1):
            print(f'Wrong parameter for {name_for_error} provided. Only 0 as false and 1 as true are allowed')
            exit()
        return bool(arg)
    return default_value 


def is_creating_files_mode():
    return read_bool_cli_flag(args.createtarget, "-ct", True)


def is_info_mode():
    return read_bool_cli_flag(args.info, "-i", True)

          
# todo implement full naming            
def create_json_file_name(properties_file):
    return target_dir + '/' + properties_file.rsplit('.', 1)[0] + JSON_EXTENSION


def print_changes_info(old_json, new_json):        
        print()
        change_counter = 0 
        add_counter = 0 
        remove_counter = 0
        
        for t, key, value in list(diff(old_json, new_json)):
            if t == 'change':
                print(f'Changed: {key}, {value[0]} -> {value[1]}')
                change_counter += 1
            if t == 'add':
                for key, value in value:
                    print(f'Added: {key} = {value}')
                    add_counter += 1
            if t == 'remove':
                for key, value in value:
                    print(f'Removed: {key} = {value}')
                    remove_counter += 1
        print('\n' + f'Total: changed - {change_counter}, added - {add_counter}, removed - {remove_counter}')            
            
            
def write_props_to_json(properties_file, full_path):
    configs = Properties()
    old_json = {}

    with open(full_path, 'rb') as config_file:
        configs.load(config_file)
        
    items = configs.items()
    new_json = {}

    for item in items:
        new_json[item[0]] = item[1].data
            
    json_file = create_json_file_name(properties_file)
    
    try:
        with open(json_file) as f_in:
            old_json = json.load(f_in)
    except Exception:
        pass  # empty target file         
        
    with open(json_file, "w") as outfile:
        json.dump(new_json, outfile, indent=2)
        c = 'created' if len(old_json) == 0 else 'updated'
        print(f'File {json_file} {c}')
    
    if show_info:
        print_changes_info(old_json, new_json)        
          
        
def main():          
    if not args.source:
        print('No source provided')
        exit()
    if not args.target:
        print('No target provided')
        exit()
        
    global show_info
    show_info = is_info_mode()    
    
    try:
        global target_dir
        if (not exists(target_dir)):
            if is_creating_files_mode():
                print(f'Target directory parameter {target_dir} does not exist, creating it ...')
                os.makedirs(target_dir)
            else:
                print(f'Target directory parameter {target_dir} does not exist, exiting ...')
                exit()
                  
        source = args.source
        
        if os.path.isfile(source) and source.endswith(PROPERTIES_EXTENSION):
            filename = source.rsplit(os.sep, 1)[1]
            write_props_to_json(filename, source)
        else:    
            files_list = os.listdir(source)
            if len(files_list) == 0:
                print(f'Source dir {source} is empty')
            for file in files_list:
                if (file.endswith(PROPERTIES_EXTENSION)):
                    path = f'{source}/{file}'
                    print(f'Processing file: {path} ...')
                    write_props_to_json(file, path)  
                          
    except FileNotFoundError:
        print(f'Source parameter {source} is incorrect')
        exit()
                    
if __name__ == '__main__':
    main()            