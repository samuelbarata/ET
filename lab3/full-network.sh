#!/bin/bash
ip -all netns delete
# Hosts
ip netns add H1
ip netns add H2
ip netns add H3
ip netns add H4
ip netns add H5
ip netns add H6
ip netns add H7

# Switches
ip netns add SW1
ip netns add SW2
ip netns add SW3

# Routers
ip netns add R1
ip netns add R2

# H1-SW1
ip link add veth-H1 type veth peer name veth-SW1-H1
ip link set veth-H1 netns H1
ip link set veth-SW1-H1 netns SW1

# H2-SW1
ip link add veth-H2 type veth peer name veth-SW1-H2
ip link set veth-H2 netns H2
ip link set veth-SW1-H2 netns SW1

# SW1-R1
ip link add veth-SW1-R1 type veth peer name veth-R1-SW1
ip link set veth-SW1-R1 netns SW1
ip link set veth-R1-SW1 netns R1

# R1-SW3
ip link add veth-R1-SW3 type veth peer name veth-SW3-R1
ip link set veth-R1-SW3 netns R1
ip link set veth-SW3-R1 netns SW3

# SW3-H5
ip link add veth-H5 type veth peer name veth-SW3-H5
ip link set veth-H5 netns H5
ip link set veth-SW3-H5 netns SW3

# SW3-H6
ip link add veth-H6 type veth peer name veth-SW3-H6
ip link set veth-H6 netns H6
ip link set veth-SW3-H6 netns SW3

# SW3-H7
ip link add veth-H7 type veth peer name veth-SW3-H7
ip link set veth-H7 netns H7
ip link set veth-SW3-H7 netns SW3

# R1-R2
ip link add veth-R1-R2 type veth peer name veth-R2-R1
ip link set veth-R1-R2 netns R1
ip link set veth-R2-R1 netns R2

# R2-SW2
ip link add veth-R2-SW2 type veth peer name veth-SW2-R2
ip link set veth-R2-SW2 netns R2
ip link set veth-SW2-R2 netns SW2

# SW2-H3
ip link add veth-H3 type veth peer name veth-SW2-H3
ip link set veth-H3 netns H3
ip link set veth-SW2-H3 netns SW2

# SW2-H4
ip link add veth-H4 type veth peer name veth-SW2-H4
ip link set veth-H4 netns H4
ip link set veth-SW2-H4 netns SW2

#Network 1
ip netns exec H1 ip addr add 10.0.1.1/24 dev veth-H1
ip netns exec H1 ip link set veth-H1 up
ip netns exec H1 ip route add default via 10.0.1.254

ip netns exec H2 ip addr add 10.0.1.2/24 dev veth-H2
ip netns exec H2 ip link set veth-H2 up
ip netns exec H2 ip route add default via 10.0.1.254

ip netns exec SW1 ip link set veth-SW1-H1 up
ip netns exec SW1 ip link set veth-SW1-H2 up
ip netns exec SW1 ip link set veth-SW1-R1 up

ip netns exec R1 ip addr add 10.0.1.254/24 dev veth-R1-SW1
ip netns exec R1 ip link set veth-R1-SW1 up


#Network 2
ip netns exec R1 ip addr add 10.0.2.254/24 dev veth-R1-SW3
ip netns exec R1 ip link set veth-R1-SW3 up

ip netns exec H5 ip addr add 10.0.2.5/24 dev veth-H5
ip netns exec H5 ip link set veth-H5 up
ip netns exec H5 ip route add default via 10.0.2.254

ip netns exec H6 ip addr add 10.0.2.6/24 dev veth-H6
ip netns exec H6 ip link set veth-H6 up
ip netns exec H6 ip route add default via 10.0.2.254

ip netns exec H7 ip addr add 10.0.2.7/24 dev veth-H7
ip netns exec H7 ip link set veth-H7 up
ip netns exec H7 ip route add default via 10.0.2.254

ip netns exec SW3 ip link set veth-SW3-R1 up
ip netns exec SW3 ip link set veth-SW3-H5 up
ip netns exec SW3 ip link set veth-SW3-H6 up
ip netns exec SW3 ip link set veth-SW3-H7 up


#Network 3
ip netns exec R1 ip addr add 10.0.3.1/24 dev veth-R1-R2
ip netns exec R1 ip link set veth-R1-R2 up

ip netns exec R2 ip addr add 10.0.3.2/24 dev veth-R2-R1
ip netns exec R2 ip link set veth-R2-R1 up


#Network 4
ip netns exec R2 ip addr add 10.0.4.254/24 dev veth-R2-SW2
ip netns exec R2 ip link set veth-R2-SW2 up

ip netns exec H3 ip addr add 10.0.4.3/24 dev veth-H3
ip netns exec H3 ip link set veth-H3 up
ip netns exec H3 ip route add default via 10.0.4.254

ip netns exec H4 ip addr add 10.0.4.4/24 dev veth-H4
ip netns exec H4 ip link set veth-H4 up
ip netns exec H4 ip route add default via 10.0.4.254

ip netns exec SW2 ip link set veth-SW2-R2 up
ip netns exec SW2 ip link set veth-SW2-H3 up
ip netns exec SW2 ip link set veth-SW2-H4 up


#Enable IP Forwarding
ip netns exec R1 sysctl -w net.ipv4.ip_forward=1
ip netns exec R2 sysctl -w net.ipv4.ip_forward=1

# R1 routes
ip netns exec R1 ip route add 10.0.4.0/24 via 10.0.3.2

# R2 routes
ip netns exec R2 ip route add 10.0.1.0/24 via 10.0.3.1
ip netns exec R2 ip route add 10.0.2.0/24 via 10.0.3.1



# Configure SW1 (Network 1) as a Layer 2 bridge
ip netns exec SW1 ip link add name br0 type bridge
ip netns exec SW1 ip link set dev br0 up

# Attach interfaces to the bridge
ip netns exec SW1 ip link set veth-SW1-H1 master br0
ip netns exec SW1 ip link set veth-SW1-H2 master br0
ip netns exec SW1 ip link set veth-SW1-R1 master br0

# Configure SW2 (Network 4) as a Layer 2 bridge
ip netns exec SW2 ip link add name br0 type bridge
ip netns exec SW2 ip link set dev br0 up

# Attach interfaces to the bridge
ip netns exec SW2 ip link set veth-SW2-R2 master br0
ip netns exec SW2 ip link set veth-SW2-H3 master br0
ip netns exec SW2 ip link set veth-SW2-H4 master br0

# Configure SW3 (Network 2) as a Layer 2 bridge
ip netns exec SW3 ip link add name br0 type bridge
ip netns exec SW3 ip link set dev br0 up

# Attach interfaces to the bridge
ip netns exec SW3 ip link set veth-SW3-R1 master br0
ip netns exec SW3 ip link set veth-SW3-H5 master br0
ip netns exec SW3 ip link set veth-SW3-H6 master br0
ip netns exec SW3 ip link set veth-SW3-H7 master br0




# Ping from H1 in Network 1 to H3 in Network 4
ip netns exec H1 ping 10.0.4.3

# Ping from H5 in Network 2 to H2 in Network 1
ip netns exec H5 ping 10.0.1.2

# Ping from H3 in Network 4 to H6 in Network 2
ip netns exec H3 ping 10.0.2.6

# Ping from H7 in Network 2 to H4 in Network 4
ip netns exec H7 ping 10.0.4.4

# debug
# ip netns exec R1 tcpdump -i veth-SW1-H1
# ip netns exec R1 ip route
