sudo dpkg --add-architecture i386 && \
sudo apt-get -y update && \
sudo apt install -y \
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
    sudo rm -rf /var/lib/apt/list/*


sudo gem install one_gadget seccomp-tools && sudo rm -rf /var/lib/gems/2.*/cache/*

sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

python3 -m pip install -U pip && \
python3 -m pip install --no-cache-dir \
    pwntools

git clone --depth 1 https://github.com/pwndbg/pwndbg ~/pwndbg && \
cd ~/pwndbg && chmod +x setup.sh && ./setup.sh

# Install pwninit
curl https://sh.rustup.rs -sSf | sh -s -- -y && \
    . $HOME/.cargo/env && \
    cargo install pwninit

sudo chsh -s $(which zsh)
