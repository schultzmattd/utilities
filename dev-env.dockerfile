FROM ubuntu:15.10
RUN apt-get update
RUN apt-get install -y git \
curl \
tmux \
sudo \
wget \
vim \
bzip2 \
zsh 

RUN wget https://3230d63b5fc54e62148e-c95ac804525aac4b6dba79b00b39d1d3.ssl.cf1.rackcdn.com/Anaconda2-2.4.1-Linux-x86_64.sh && \
 bash Anaconda2-2.4.1-Linux-x86_64.sh -b -p /opt/anaconda2/ && \
 chmod -R a+rx /opt/anaconda2/

RUN useradd -m mschultz -p "" && \
sudo adduser mschultz sudo

USER mschultz
WORKDIR /home/mschultz

RUN sudo sh -c "$(wget https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh -O -)"
RUN git clone git://github.com/andsens/homeshick.git $HOME/.homesick/repos/homeshick && \
  printf '\nsource $HOME/.homesick/repos/homeshick/homeshick.sh\n' >> $HOME/.bashrc
RUN $HOME/.homesick/repos/homeshick/bin/homeshick clone -qqq https://github.com/schultzmattd/dotfiles.git && \
  $HOME/.homesick/repos/homeshick/bin/homeshick link -f dotfiles

RUN sudo chsh -s $(which zsh)

CMD ["zsh"]
