# This is a comment
FROM ubuntu:14.04
RUN apt-get update && apt-get install -y iproute2 openssh-server dhcpcd5 net-tools iputils-arping iputils-ping tcpdump isc-dhcp-client python-pip dnsutils inetutils-traceroute vim wget coreutils fping python-software-properties software-properties-common transmission-cli pppoe pppoeconf
RUN add-apt-repository ppa:mc3man/trusty-media
RUN apt-get update -y
RUN apt-get dist-upgrade -y
RUN apt-get install ffmpeg -y
RUN apt-get install mplayer -y
RUN service ssh restart
RUN echo nameserver 8.8.8.8 > /etc/resolv.conf
RUN mkdir ~/.ssh
RUN touch ~/.ssh/authorized_keys
RUN echo "ssh-rsa AAAAB3NzaC1yc2EAAAABJQAAAQEAqPk7ERCf7pY+YcEKP3fTTxLPiFLn42yTDoGGAgo4xrlq00nAximscadwyIzuv7nQ0um6Gw5vxjH8OwJQBCW58aDtco5LWflpFLVWXEUBgg8icNmhgn2dUtErTLePrL44kDKReGdW4SREnGTkYpynbZGCaJDWUEtJLcNtVGrH1tcfQOvoqyflHrUxoz3d3NOLjSBXRzTNBc+b6bheQ7RBiZp16yv+nZTdHcYixY8HejWpXfdN6o6xm3F8d9JpYC/bzHw8t5yEGVgt1CIKn2kHMzJmJTaM/z6sce20qBx7/Bm+lEzSIWD7mIFMtmVpdfvFSty/vf+gablamSc0UeXOKw== rsa-key-20160426" >> ~/.ssh/authorized_keys
RUN pip install speedtest-cli
COPY bot.py /root/
RUN chmod +x ~/bot.py
RUN echo "export TERM=xterm" >> /root/.profile
RUN echo "export TERM=xterm" >> /root/.bashrc
CMD ["/usr/bin/python","/root/bot.py"]
