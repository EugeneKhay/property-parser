# pip3 install jproperties

# Script should be triggered with at least 3 parameters:
# script name, source directory, target directory, i.e:
# python3 parser.py ./source_dir ./target_dir

import os
import json
import argparse
from os.path import exists
from jproperties import Properties

PROPERTIES_EXTENSION = '.properties'
JSON_EXTENSION = '.json'

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--source", help="Source path")
parser.add_argument("-t", "--target", help="Target path")
parser.add_argument("-ct", "--createtarget", 
                    help="Should target be created if not exists: 0 - false, 1 - true", 
                    type=int)
args = parser.parse_args()

target_dir = args.target

def is_creating_files_mode():
    if args.createtarget != None:
        value = args.createtarget
        if (value != 0 and value != 1):
            print('Wrong parameter -cp provided. Only 0 as false and 1 as true are allowed')
            exit()
        return bool(args.createtarget)
    return True
    
    
def parse():          
    if not args.source:
        print('No source provided')
        exit()
    if not args.target:
        print('No target provided')
        exit()    
        
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
        
            
def create_json_file_name(properties_file):
    return target_dir + '/' + properties_file.rsplit('.', 1)[0] + JSON_EXTENSION        
            
            
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