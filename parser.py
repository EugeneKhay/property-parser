# pip3 install jproperties

# Script should be triggered with at least 3 parameters:
# script name, source directory, target directory, i.e:
# python3 parser.py ./source_dir ./target_dir

import os
import sys
import json
from os.path import exists
from jproperties import Properties

ARGS_MINIMAL_NUMBER = 3
PROPERTIES_EXTENSION = '.properties'
JSON_EXTENSION = '.json'
TARGET_DIR = sys.argv[2] 
    
def parse():          
    if len(sys.argv) < ARGS_MINIMAL_NUMBER:
        print(f'Wrong parameters number: {len(sys.argv) - 1} is provided, 2 is needed')
        print('Parameters are: 1 - source dir, 2 - target dir')
        exit()
        
    try:
        global TARGET_DIR
        if (not exists(TARGET_DIR)):
                print(f'Target directory parameter {TARGET_DIR} does not exist, creating it ...')
                os.makedirs(TARGET_DIR) 
        source = sys.argv[1]
        
        if os.path.isfile(source) and source.endswith(PROPERTIES_EXTENSION):
            filename = source.rsplit(os.sep, 1)[1]
            write_props_to_json(filename, source)
        else:    
            files_list = os.listdir(source)
            for file in files_list:
                if (file.endswith(PROPERTIES_EXTENSION)):
                    path = f'{source}/{file}'
                    print(f'Processing file: {path} ...')
                    write_props_to_json(file, path)  
                          
    except FileNotFoundError:
        print(f'Source directory parameter {source} is incorrect')
        exit()
        
            
def create_json_file_name(properties_file):
    return TARGET_DIR + '/' + properties_file.rsplit('.', 1)[0] + JSON_EXTENSION        
            
            
def write_props_to_json(properties_file, full_path):
    configs = Properties()

    with open(full_path, 'rb') as config_file:
        configs.load(config_file)
        
    items = configs.items()
    dict = {}

    for item in items:
        dict[item[0]] = item[1].data
            
    json_file = create_json_file_name(properties_file)  
        
    with open(json_file, "w") as outfile:
        json.dump(dict, outfile, indent=2)
        print(f'File {json_file} created')            
            
            
if __name__ == '__main__':
    parse()            