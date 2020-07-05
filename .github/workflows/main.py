# -*- coding: utf-8 -*-

import glob
import json
import os
import sys, getopt #to get parameters
import twitter

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
        json_file.seek(0) #always go to beginning of file
        try:
            data = json.load(json_file)
        except Exception as e:
            json_file.seek(0) #always go to beginning of file
            json_file.read()
            if json_file.read() == '':
                return [] #empty file
            raise e

        return data['files']

# read post, create tweet, modify post
def createTweetAndModify(post_file_path):
    #read file
    reading_file = open(post_file_path, 'r')
    reading_file.seek(0) #go to beginning of file
    content = reading_file.read()
    reading_file.close()

    #identify metadata
    searchTerm1 =  'twitterContentBegin: '
    searchTerm2 = ':twitterContentEnd'
    startTwitter = content.find(searchTerm1)
    endTwitter = content.find(searchTerm2)
    if startTwitter == -1 or endTwitter == -1:
        print('Tweet Data not found: '+post_file_path)
        return 'Warning, tweet Data not found in post '+post_file_path
    ##get Content
    try:
        tweetContent = json.loads(content[startTwitter+len(searchTerm1):endTwitter])
    except Exception as e:
        print(str(e))
        print('String to json: '+content[startTwitter+len(searchTerm1):endTwitter])
        print('Error during processing of: '+post_file_path)
        return 'Error, tweet Data corrupt in post '+post_file_path
    ##remove :twitterContentEnd
    content = content.replace(':twitterContentEnd', '')

    #create tweet
    tweetId = ''
    try:
        api = twitter.Api(consumer_key=consumerKey,
                          consumer_secret=consumerSecret,
                          access_token_key=tokenKey,
                          access_token_secret=tokenSecret)

        #create a tweet / twitter status
        # PostUpdate(status, media=None, media_additional_owners=None, media_category=None, in_reply_to_status_id=None, auto_populate_reply_metadata=False, exclude_reply_user_ids=None, latitude=None, longitude=None, place_id=None, display_coordinates=False, trim_user=False, verify_status_length=True, attachment_url=None
        #https://python-twitter.readthedocs.io/en/latest/twitter.html#module-twitter.api
        tweetEssentials = tweetContent['url']
        hashtags = ''
        for entry in tweetContent['hashtags']:
            hashtags = hashtags + ' '+ entry
        tweetEssentials = tweetEssentials + ' ' + hashtags
        remainingLength = 280 - len(tweetEssentials)
        status = ''
        if remainingLength < 0:
            status = tweetEssentials[0:280]
        else:
            text = tweetContent['text'][0:remainingLength-4]
            text = text +'... '
            status = text + tweetEssentials

        twitterPost = api.PostUpdate(
            status = status,
        )
        print(twitterPost)
        tweetId = str(twitterPost.id)
        print('--------------------------')
        print('Tweet successfully created')
        print('--------------------------')
    except Exception as e:
        print('Error during processing of: '+post_file_path)
        print(str(e))
        return 'Error, issue with Twitter API for'+post_file_path

    #modify file content
    content = content.replace('tweet: XXXXXXXXXXXX|', 'tweet: '+tweetId)

    #write file and exit
    writing_file = open(post_file_path, 'w+')
    writing_file.write(content)
    writing_file.close()

if __name__ == '__main__':
    #because i am lazy... - global scope for keys
    consumerKey=''
    consumerSecret=''
    tokenKey=''
    tokenSecret=''    #get secrets for api

    paramMessage = 'main.py -c <consumerKey> -s <consumerSecret> -t <tokenKey> -o <tokenSecret>'
    try:
      opts, args = getopt.getopt(sys.argv[1:],"h:c:s:t:o:",["consumerKey=", "consumerSecret=", "tokenKey=", "tokenSecret=" ])
    except getopt.GetoptError as e:
      print(str(e))
      sys.exit(2)

    if not opts:
        print(paramMessage)
        sys.exit(2)
    for opt, arg in opts:
        import pdb
        if opt == '-h':
            print(paramMessage)
            sys.exit()
        elif opt in ("-c", "--consumerKey"):
            #TODO
            if arg and not arg == '':
                consumerKey = arg
            else:
                print('Missing parameter. Pass '+paramMessage)
                sys.exit(2)
        elif opt in ("-s", "--consumerSecret"):
            #TODO
            if arg and not arg == '':
                consumerSecret = arg
            else:
                print('Missing parameter. Pass '+paramMessage)
                sys.exit(2)
        elif opt in ("-t", "--tokenKey"):
            #TODO
            if arg and not arg == '':
                tokenKey = arg
            else:
                print('Missing parameter. Pass '+paramMessage)
                sys.exit(2)
        elif opt in ("-o", "--tokenSecret"):
            #TODO
            if arg and not arg == '':
                tokenSecret = arg
            else:
                print('Missing parameter. Pass '+paramMessage)
                sys.exit(2)

    ## Algorithm
    # 1. Read existing metadata file and get the list of files
    # 2. Read all files from the `/data` folder
    # 3. Figure out the list of new files
    # 4. Update metadata file if required
    # 5. loop over new posts and read content line by line into lists
    # 5.1 call twitter api and create tweet
    # 5.2 replace line string with tweet id and write / update post file

    # Constants
    #### replace DATA_FOLDER_PATH with env
    DATA_FOLDER_PATH = './content/posts'
    METADATA_FILE_PATH = os.path.join(DATA_FOLDER_PATH, '0_metadata.json') # file required to identify delta between commits

    # 1. Read existing metadata file and get the list of files
    list_current_files = get_current_files(
        metadata_file_path=METADATA_FILE_PATH)
    print("Current files:" + str(list_current_files))

    # 2. Read all files from the `/data` folder
    list_updated_files = get_data_files(data_folder_path=DATA_FOLDER_PATH)
    print("Files in folder: " + str(list_updated_files))


    # 3. Figure out the list of new files
    list_new_files = (list(set(list_updated_files) - set(list_current_files)))
    print("New files: " + str(list_new_files))

    # 4. Update metadata file if required
    if list_new_files:
        status = update_metadata_file(file_list=list_updated_files,
                             metadata_file_path=METADATA_FILE_PATH)
        print("Updated metadata file: " + str(status))

    if list_new_files:
        print(list_new_files)
        for entry in list_new_files:
            file_path = os.path.join(DATA_FOLDER_PATH, entry)
            # call function to create tweets
            createTweetAndModify(file_path)
    print('End of tweet generation')
