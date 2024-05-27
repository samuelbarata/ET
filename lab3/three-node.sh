#!/bin/bash
ip -all netns delete
ip netns add near
ip netns add far
ip link add one type veth peer name two
ip link add three type veth peer name four
ip link set two netns near
ip link set three netns near
ip link set four netns far
ip addr add 10.0.11.1/24 dev one
ip netns exec near ip addr add 10.0.11.2/24 dev two
ip netns exec near ip addr add 10.0.12.1/24 dev three
ip netns exec far ip addr add 10.0.12.2/24 dev four
ip link set dev one up
ip netns exec near ip link set two up
ip netns exec near ip link set three up
ip netns exec far ip link set four up

ip netns exec far ip addr add 10.0.13.1/24 dev lo
ip netns exec far ip link set dev lo up

# enable ip routing
ip netns exec near sysctl -w net.ipv4.ip_forward=1

# Add routes
ip route add 10.0.12.0/24 via 10.0.11.2
ip route add 10.0.13.0/24 via 10.0.11.2
ip netns exec near ip route add 10.0.13.0/24 via 10.0.12.1
ip netns exec far ip route add 10.0.11.0/24 via 10.0.12.1

# DELETE
# ip netns del near
# ip netns del far
