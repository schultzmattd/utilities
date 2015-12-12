FROM ubuntu:15.10
RUN useradd -m mschultz
RUN  apt-get update
RUN  apt-get install -y git \
curl \
zsh
RUN chsh -s $(which zsh)
USER mschultz
RUN cd $HOME
CMD ["zsh"]
