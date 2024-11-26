docker build --platform linux/amd64 -t ubuntu-ctf .
docker run -it --cap-add=SYS_PTRACE --security-opt seccomp=unconfined -v ~/ctf:/home/c0raline/ctf --hostname jones ubuntu-ctf zsh