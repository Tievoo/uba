#!/usr/bin/env python

"""
Nota: requiere instalar:
    - openvswitch-testcontroller
    - telnet
    - traceroute
    - iputils-tracepath
"""

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI


class LinuxRouter( Node ):
    "A Node with IP forwarding enabled."

    # pylint: disable=arguments-differ
    def config( self, **params ):
        super( LinuxRouter, self).config( **params )
        # Enable forwarding on the router
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )

    def terminate( self ):
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( LinuxRouter, self ).terminate()


class NetworkTopo( Topo ):
    "A LinuxRouter connecting three IP subnets"

    # pylint: disable=arguments-differ
    def build( self, **_opts ):

        s1, s2, s3, s4 = [ self.addSwitch(s) for s in ('s1', 's2', 's3', 's4') ]

        def router(name, defaultIP):
            return self.addNode(name, cls=LinuxRouter, ip=defaultIP)

        r1 = router('r1', '10.1.0.1/16')
        r2 = router('r2', '10.2.0.1/16')

        def link(s, r, iface, ip, **kwargs):
            self.addLink(s, r, intfName2=iface, params2={'ip': ip}, **kwargs)

        link(s1, r1, 'r1-eth0', '10.1.0.1/16')
        link(s4, r1, 'r1-eth1', '10.10.10.1/30')

        link(s2, r2, 'r2-eth0', '10.2.0.1/16')
        link(s4, r2, 'r2-eth1', '10.10.10.2/30')
        link(s3, r2, 'r2-eth2', '10.3.0.1/16')

        def host(s, name, ip, route):
            host = self.addHost(name, ip=ip, defaultRoute='via '+route)
            self.addLink(s, host)

        host(s1, 'pc1', '10.1.1.1/23', '10.1.0.1')
        host(s1, 'pc2', '10.1.2.2/16', '10.1.0.1')

        host(s2, 'pc3', '10.2.3.3/16', '10.2.0.1')
        host(s2, 'pc4', '10.2.4.4/16', '10.2.0.1')
        
        host(s3, 'pc5', '10.3.5.5/16', '10.3.0.1')
        host(s3, 'pc6', '10.3.6.6/16', '10.3.0.1')

def run():
    "Test linux router"
    topo = NetworkTopo()
    net = Mininet( topo=topo,
                   waitConnected=True )  # controller is used by s1-s3
    net.start()
    # info( '*** Routing Table on Router:\n' )
    # info( net[ 'r0' ].cmd( 'route' ) )

    # https://networkingtoolbox.net/reference/mtu-mss
    net['r1'].cmd('ifconfig r1-eth1 mtu 1436')
    net['r2'].cmd('ifconfig r2-eth1 mtu 1436')

    fullnet = '0.0.0.0/0'  # Equivalente a default route

    net['r1'].cmd('route add -net 10.0.0.0/8 gw 10.10.10.2')
    net['r2'].cmd('route add -net 10.0.0.0/8 gw 10.10.10.1')

    # Requerido para simular el escenario en que se recibe el Time Exceeded
    net['r1'].cmd('sysctl net.ipv4.conf.r1-eth1.rp_filter=2')
    net['r2'].cmd('sysctl net.ipv4.conf.r2-eth1.rp_filter=2')

    CLI( net )
    net.stop()


if __name__ == '__main__':
    setLogLevel( 'info' )
    run()
