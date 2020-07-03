# -*- coding: utf-8 -*-

import glob
import json
import os
import sys, getopt #to get parameters


def update_metadata_file(file_list, metadata_file_path):
    file_list.sort()

    metadata = {}
    metadata.setdefault("files", file_list)
    # add to the file
    with open(metadata_file_path, 'w+') as f:
        f.write(json.dumps(metadata, indent=1))

    return True

def get_data_files(data_folder_path):
    extension = '.md'

    # if given empty path, it starts from the current directory
    files = [f for f in
             glob.glob(data_folder_path + "**/*" + extension, recursive=True)]
    file_list = []

    for file in files:
        # Construct the metadata json
        print(file)
        filename = os.path.basename(file)
        print(filename)
        file_list.append(filename)

    file_list.sort()
    return file_list


#works as expected
def get_current_files(metadata_file_path):
    with open(metadata_file_path) as json_file:
        data = json.load(json_file)
        return data['files']


if __name__ == '__main__':
    twitterSecret = ''
    #get secrets for api
    paramMessage = 'main.py -ck <consumerKey> -cs <consumerSecret> -tk <tokenKey> -ts <tokenSecret>'
    try:
      opts, args = getopt.getopt(sys.argv[1:],"hck:cs:tk:ts",["consumerKey=", "consumerSecret=", "tokenKey=", "tokenSecret=" ])
    except getopt.GetoptError as e:
      print(e.toString())
      sys.exit(2)

    if not opts:
        print(paramMessage)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(paramMessage)
            sys.exit()
        elif opt in ("-ck", "--consumerKey"):
            #TODO
            if not arg and not arg == '':
                twitterSecret = arg
            else:
                print('Missing parameter. Pass '+paramMessage)
                sys.exit(2)
        elif opt in ("-cs", "--consumerSecret"):
            #TODO
            if not arg and not arg == '':
                twitterSecret = arg
            else:
                print('Missing parameter. Pass '+paramMessage)
                sys.exit(2)
        elif opt in ("-tk", "--tokenKey"):
            #TODO
            if not arg and not arg == '':
                twitterSecret = arg
            else:
                print('Missing parameter. Pass '+paramMessage)
                sys.exit(2)
        elif opt in ("-ts", "--tokenSecret"):
            #TODO
            if not arg and not arg == '':
                twitterSecret = arg
            else:
                print('Missing parameter. Pass '+paramMessage)
                sys.exit(2)


    ## Algorithm
    # 1. Read existing metadata file and get the list of files
    # 2. Read all files from the `/data` folder
    # 3. Figure out the list of new files
    # 4. Update metadata file if required
    # 5. loop over new posts

    # Constants
    #### replace DATA_FOLDER_PATH with env
    DATA_FOLDER_PATH = './content/posts'
    README_FILE_PATH = 'README.md'
    METADATA_FILE_PATH = os.path.join(DATA_FOLDER_PATH, '0_metadata.json') # file required to identify delta between commits

    # 1. Read existing metadata file and get the list of files
    list_current_files = get_current_files(
        metadata_file_path=METADATA_FILE_PATH)
    print("Current files:" + str(list_current_files))

    # 2. Read all files from the `/data` folder
    list_updated_files = get_data_files(data_folder_path=DATA_FOLDER_PATH)
    print("Updated files: " + str(list_updated_files))

    # 3. Figure out the list of new files
    list_new_files = (list(set(list_updated_files) - set(list_current_files)))
    print("New files: " + str(list_new_files))

    # 4. Update metadata file if required
    if list_new_files:
        status = update_metadata_file(file_list=list_updated_files,
                             metadata_file_path=METADATA_FILE_PATH)
        print("Updated metadata file: " + str(status))

    if list_new_files:
        print('Todo')
