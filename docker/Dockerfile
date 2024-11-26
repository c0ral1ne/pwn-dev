# Use the official Ubuntu 22.04 base image
FROM ubuntu:22.04

LABEL maintainer="c0ralin3j0nesz@gmail.com"

ENV DEBIAN_FRONTEND=noninteractive

RUN dpkg --add-architecture i386 && \
    apt-get -y update && \
    apt install -y \
    sudo \
    libc6:i386 \
    libc6-dbg:i386 \
    libc6-dbg \
    libffi-dev \
    libssl-dev \
    liblzma-dev \
    ipython3 \
    vim \
    net-tools \
    python3-dev \
    python3-pip \
    build-essential \
    ruby \
    ruby-dev \
    tmux \
    strace \
    ltrace \
    nasm \
    wget \
    gdb \
    gdb-multiarch \
    netcat \
    git \
    patchelf \
    file \
    python3-distutils \
    zstd \
    zsh \
    ripgrep \
    python-is-python3 \
    tzdata --fix-missing && \
    rm -rf /var/lib/apt/list/*


RUN gem install one_gadget seccomp-tools && rm -rf /var/lib/gems/2.*/cache/*

RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" && \
    apt-get install zsh-syntax-highlighting -y

### Ordering is important so that directories have proper permissions
RUN useradd -m -s /bin/bash c0raline && echo 'c0raline:c0raline' | chpasswd && \
    usermod -aG sudo c0raline && \
    echo 'c0raline ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers
RUN chown -R c0raline:c0raline /home/c0raline
USER c0raline

RUN python3 -m pip install -U pip && \
    python3 -m pip install --no-cache-dir \
    pwntools \
    ropgadget \
    ropper

RUN git clone --depth 1 https://github.com/pwndbg/pwndbg ~/pwndbg && \
    cd ~/pwndbg && chmod +x setup.sh && ./setup.sh

RUN git clone --depth 1 https://github.com/scwuaptx/Pwngdb.git ~/Pwngdb && \
    cd ~/Pwngdb/pwndbg && \
    cp pwngdb.py ~/pwndbg/pwndbg/pwngdb.py && \
    cp angelheap.py ~/pwndbg/pwndbg/angelheap.py && \
    cp commands/pwngdb.py ~/pwndbg/pwndbg/commands/pwngdb.py && \
    cp commands/angelheap.py ~/pwndbg/pwndbg/commands/angelheap.py && \
    sed -i -e '/config_mod.init_params()/a import pwndbg.commands.pwngdb' ~/pwndbg/pwndbg/__init__.py && \
    sed -i -e '/config_mod.init_params()/a import pwndbg.commands.angelheap' ~/pwndbg/pwndbg/__init__.py

# Install pwninit
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y && \
    . $HOME/.cargo/env && \
    cargo install pwninit

RUN sudo chsh -s $(which zsh)

RUN cp /etc/zsh/newuser.zshrc.recommended ~/.zshrc
RUN echo "source /usr/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh" >> ~/.zshrc
RUN echo "source $(realpath ~/ctf/pwn-dev/scripts/pwnshell.sh)" >> ~/.zshrc

WORKDIR /home/c0raline/ctf
