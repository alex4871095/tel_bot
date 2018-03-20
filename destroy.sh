#!/bin/bash -x
sudo service docker restart 
for i in {406..425}; do
	sudo docker stop doc$i
	sudo docker rm doc$i
	sudo ip link delete A$i
	sudo ip link delete br$i
	sudo ip link delete eth3.$i
done
sudo service docker restart
