#Python script which identifies new posts
1.  Posts folder required metadata file:
  0_metadata.json
  {
   "files": [
    "0_metadata.json",
    ]
  }

  This file is used to track delta between posts.

2. Secondly the script reads the frontmatter for twitter and creates a new tweet

3. New tweet id is stored and updated in post

4. iterate over list and repeat till done

5. push to master

#### TODO
- TODO replace DATA_FOLDER_PATH with env
- Getting list of new files works
- Env replacement string and twitter comment
- next read content of new files into string
- identify twitter sections
- create new tweet
- update files