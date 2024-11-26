alias csh="docker start $(docker ps -qaf ancestor='ubuntu-ctf') && docker exec -it -w /home/c0raline/ctf/work $(docker ps -qaf ancestor='ubuntu-ctf') zsh"
alias ctf-stop="docker stop $(docker ps -qaf ancestor='ubuntu-ctf')"
