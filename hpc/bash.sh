# misc bash commands for navigating UConn Storrs HPC
date # gets date and timestamp

hostname # show the system's host name i.e., check the node

pwd # pwd = print working directory
# cd = change directory
cd .. # change to parent
cd ../.. # change to parent of parent
cd ollama # change to ollama folder
cd "home/$USER" # change to node of user
cd "/scratch/" # change to scratch folder (where files are saved in UConn Storrs HPC)
# by default files are stored in home/$

# ls = list
ls # list files in the working directory
ls -a # list all files, including hidden ones
ls -lh # list files and their sizes
lsmod # view loaded modules
# mkdir = make directory
mkdir test # create a new folder called test
# rmdir = remove directory
rmdir test # remove the folder called test
# rm = remove file
rm goodreads_20.csv # remove the file called goodreads_20.csv
# mv = move: move files and directories from one directory to another
mv output shared # move output.csv from scratch to shared
cat # print the contents of a file

# df = disk space usage
df -k # check the storage of the partition

# modules
module avail
module avail apptainer # check which versions of apptainer are available
module avail python # check which versions of python are available

# github
git clone https://github.com/hernandezb3/llama-on-uconn-hpc.git # clone this repo
git fetch # retrieve changes without affecting the local repository
git pull # retrieve changes and synchronize local repository

# ctrl + c to kill a running command