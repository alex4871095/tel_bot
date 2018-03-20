#!/bin/bash -x
for i in {406..425}; do 
	echo "Spinning docker $i"
#	docker run -d --name=doc$i --hostname=doc$i --net=none chatbot /usr/sbin/sshd -D 
	docker run -d --name=doc$i --hostname=doc$i --net=none chatbot 
	sudo vconfig add eth3 $i;
	sudo brctl addbr br$i;
	sudo brctl addif br$i eth3.$i;
	sudo ifconfig br$i up;
	sudo ifconfig eth3.$i up;
	a=$(docker inspect -f '{{.State.Pid}}' doc$i);
	sudo mkdir -p /var/run/netns;
	sudo ln -s /proc/$a/ns/net /var/run/netns/$a;
	echo "Making networking to $i"
	sudo ip link add A$i type veth peer name B$i;
	sudo brctl addif br$i A$i;
	sudo ip link set A$i up;
	sudo ip link set B$i netns $a;
	sudo ip netns exec $a ip link set dev B$i name eth1;
	sudo ip netns exec $a ip link set eth1 up;
	sudo ip netns exec $a pon dsl-provider;
#	sudo ip netns exec $a dhclient eth1;
	sudo ip netns exec $a ifconfig eth1 10.9.8.7/24;
	sudo ip netns exec $a route add -net 224.0.0.0/4 dev eth1;
	sudo ip netns exec $a route add -net 10.224.3.0/24 dev eth1;
#	sudo ip netns exec $a route add -net 233.3.2.0/24 dev eth1;
	sudo ip netns exec $a sysctl net.ipv4.conf.eth1.mc_forwarding=1;
	sudo ip netns exec $a sysctl net.ipv4.conf.eth1.force_igmp_version=2;
	sudo ip netns exec $a sysctl net.ipv4.conf.eth1.rp_filter=0;
	echo "done"

	
done
