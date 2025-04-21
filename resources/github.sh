# git guides: https://github.com/git-guides 

# add a repository to your working directory
# clone llama-on-uconn-hpc repository
git clone https://github.com/hernandezb3/llama-on-uconn-hpc.git
# create a branch to work off of
git branch branch-name

# upate your working branch with any changes made by others
# git pull is a combo of git fetch + git merge
git pull

# make changes and add to the branch:
# stage changes
git add
# stage all changes (not listed in .gitignore)
git add -A
# commit changes
git commit -m "descriptive commit message"
# sync changes with the remote repo
git push

# pull request: merge a set of changes from one branch to another
# https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests