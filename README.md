# Description of workflow
Workflow is triggered on push to branch *update*.
1. A job is run which checks out the repo and executes a python script that iterates over new files in *content/posts/*. The script then generates twitter tweets according to the metadata and adapts the files.
2. Then an action to build Hugo files is executed
3. The changes are then committed to the branch *update*
4. A new job is executed to merge the update changes to master and commit

5. On commit/push to master a new workflow is triggered which deploys the Hugo page to firebase

## How to use automation workflow
- add .github/ folder to your repo
- create file 0_metadata.json in folder where you want to track and adapt the files. Content of the file:
  ```
  {
   "files": [
    "0_metadata.json",
    ]
  }
  ```
- go to github and define action and workflow
- create branch update as well as remote branch
  - the update branch is the entry point for the workflow
  - create local branch `git checkout -b feature_branch_name` or via git `git branch <name>`
  - create/update remote repo `git push -u origin feature_branch_name`

- since the action is going to change the update branch remotely you need to perform `git pull` to get the latest changes before adding local changes and pushing again.

To cleanup:
- to delete branch local run `git branch -d <name of branch>`
- to delete branch remote run `git push origin --delete <branch>`

## Configuration & Pre-requisites
1. copy .github/workflows to your repo, create a local and remote update branch
2. create a the 0_metadata.json file in the *content/posts/* folder. This is required to track new files
3. make sure to remove the mergeTest.yml from the .github/workflows/ folder => This is not needed and can have a negative impact on the workflow
4. Create the Github secret FIREBASE_TOKEN
  - To get the token execute `firebase login:ci` in your local env. Copy the key in the Github secret
    - [Firebase CLI wrapper](https://github.com/w9jds/firebase-action)
    - [Hugo execution](https://github.com/srt32/hugo-action)

## Important note if you want to generate Twitter tweets and use the script
1. To use the twitter script you need to add the following github secrets
2. Every post for which you want to create a tweet needs to have the following strings somewhere in the file:
```
tweet: XXXXXXXXXXXX|
twitterContentBegin: {"text": "This is the text", "hashtags": ["#theprogress", "#number2"], "url": "https://theprogress.site/{{ .Name }}" }:twitterContentEnd
```
  This code was written for hugo. Hugo removes the Metadata or so called frontmatter from the displayed content. If you use something different then you might need to adapt the script and also your metadata in the posts.
