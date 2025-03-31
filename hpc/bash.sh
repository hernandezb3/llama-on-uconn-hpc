# after job started, use the following to check
hostname # check node
date # gets date and timestamp
pwd # print working directory
ls # list contents of working directory
ls -a # list all contents of working directory (includes hidden files)
ls -lh # list files and their sizes
lsmod # view loaded modules

# ctrl + c to kill a running command

# misc code for navigating hpc
# start an interactive job (aka drop in)
srun --x11 -n 1 -t 0:30:00 --mem=64G --pty bash
srun -p general-gpu -t 0:30:00 --mem=64G --pty bash
srun --x11 -N 1 -n 126 -p general --pty bash
# type of job = srun
#
# node = 1
# time = 1:00:00 aka 1 hour, 0 min, 0 sec
# ram i.e., memory = 30g
# scripting language = bash

# by default files are stored in home/$USER
cd ../.. # go to parent of parent
cd "home/$USER" # go to node of user
cd "/scratch/"
cd ollama
df -k # check the storage of the partition
mv # move files e.g., scratch > shared
cat # print the contents of a file

#git clone https://github.com/hernandezb3/crisp_hpc