#!/bin/bash
ip netns add examplens
ip link add external0 type veth peer name internal0
ip link set internal0 netns examplens
ip netns exec examplens ip addr add 10.0.0.2/24 dev internal0
ip addr add 10.0.0.1/24 dev external0
ip netns exec examplens ip link set internal0 up
ip link set dev external0 up

# DELETE
# ip netns del examplens
