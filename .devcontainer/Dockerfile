FROM archlinux:latest

RUN pacman --noconfirm -Syu base-devel sudo

RUN pacman --noconfirm -S git
RUN pacman --noconfirm -S python

RUN sed -E 's/^#\s*(%wheel\s*ALL=\(ALL\)\s*ALL)/\1/' /etc/sudoers | EDITOR='tee' visudo
RUN useradd -Um -G wheel vscode &&\
    echo "vscode:vscode" | chpasswd

USER vscode
