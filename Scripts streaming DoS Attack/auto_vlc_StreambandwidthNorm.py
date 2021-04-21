#!/usr/bin/python
"""Custom topology example

Sin Ataque DoS streaming vlc 
"""
import inspect
import re
import csv
import time
from time import sleep
from cmd import Cmd
from glob import glob
from os import system, path
from functools import partial
from mininet.cli import CLI
from mininet.log import info, output, error, setLogLevel
from mininet.net import Mininet
from mininet.util import quietRun, dumpNodeConnections
from mininet.topo import Topo
from mininet.node import NOX, UserSwitch, RemoteController
from mininet.link import TCLink


####################

###################



class tree_Topo(Topo):
	"Single switch connected to n hosts."
	def __init__(self, **opts):
	        # Initialize topology and default options
	        Topo.__init__(self, **opts)
	        info ('*** Add Access Point\n')
	    	s1 = self.addSwitch('s1')  
	    	s2 = self.addSwitch('s2') 
	    	s3 = self.addSwitch('s3') 
	    	s4 = self.addSwitch('s4')  
	    	s5 = self.addSwitch('s5') 
	    	s6 = self.addSwitch('s6')
	    	s7 = self.addSwitch('s7')
	  	#Add Host
	    	info ("*** Add Host\n ")
	    	h1 = self.addHost('h1', ip = '10.0.0.1')
	    	h2 = self.addHost('h2', ip = '10.0.0.2')
	    	h3 = self.addHost('h3', ip = '10.0.0.3')
	    	h4 = self.addHost('h4', ip = '10.0.0.4')
	    	h5 = self.addHost('h5', ip = '10.0.0.5')
	    	h6 = self.addHost('h6', ip = '10.0.0.6')
	    	h7 = self.addHost('h7', ip = '10.0.0.7')
	    	h8 = self.addHost('h8', ip = '10.0.0.8')
	    	info ('**** Add Links\n')
	    	#self.addLink (c0, s2)
	    	self.addLink (h1, s3, cls=TCLink,bw=1 )
	    	self.addLink (h2, s3, cls=TCLink,bw=1 )
	    	self.addLink (h3, s4, cls=TCLink,bw=1 )
	    	self.addLink (h4, s4, cls=TCLink,bw=1 )
	    	self.addLink (h5, s6, cls=TCLink,bw=1 )
	    	self.addLink (h6, s6, cls=TCLink,bw=1 )
	    	self.addLink (h7, s7, cls=TCLink,bw=1 )
	    	self.addLink (h8, s7, cls=TCLink,bw=1 )
	    	#Switch link
	    	self.addLink (s1, s2, cls=TCLink,bw=1)
	    	self.addLink (s1, s5, cls=TCLink,bw=1)
	    	self.addLink (s2, s4, cls=TCLink,bw=1)
	    	self.addLink (s2, s3, cls=TCLink,bw=1)
	    	self.addLink (s5, s6, cls=TCLink,bw=1)
	    	self.addLink (s5, s7, cls=TCLink,bw=1)
	    	
################################


"""
def get_file_path():
    "Return the path of the this file."
    #return path.dirname(inspect.getfile(inspect.currentframe()))
    return path.dirname(path.abspath(__file__))
    """

def vlc_start_stream( self, host, filename, target, port ):
    "Start a VLC server at 'host' streaming 'filename' to 'port' of 'target'."
    try:
        ip = target.IP()
    except AttributeError:
        ip = target
    title = '%s:%s' % (host.name, port)
    pidfile = '/data/Descargas/tmp/mininet_vlc_%s_%s.pid' % (host.name, port)
    cmd = ' vlc -vvv %s'%filename
    cmd += ' --daemon --pidfile %s '%pidfile
    cmd += ' --video-title server_%s'% title
    cmd += " --sout '#duplicate{dst=display,dst=rtp{access=udp,mux=ts,dst=%s,port=%s}}'" % ( ip, port ) 
    host.cmd(cmd + ' &') 
    info( 'server_stream: %s\n'%cmd)
    

def vlc_start_client( self, host, port ):	
    "Start a VLC client at 'host' listening at 'port' and move it to 'x','y'."
    title = '%s:%s' % (host.name, port)
    pidfile = '/data/Descargas/tmp/mininet_vlc_%s_%s.pid' % (host.name, port)
    vidfile = '/data/Descargas/media_org/temp/mininet_video_%s_%s.mp4' % (host.name, port)
    cmd = ' vlc '
    cmd += " --sout '#duplicate{dst=display,dst=std{access=file,mux=ts,dst=%s}}'" % ( vidfile )
    cmd += ' --daemon --pidfile %s ' % pidfile
    cmd += 'rtp://@:%s' % port   
    host.cmd(cmd + ' &') 
    info( 'client_stream: %s\n'%cmd)
    
def vlc_start_vlc( self ):
    "Start VLC programs."
    port_1 = 1234
    port_2 = 1111
    path_video = "/data/Descargas/media_org/media/bunny.mp4"
    
    for f in [path_video]:
        if not path.exists(f):
            info( 'File does not exists: %s\n' % f )
            return
    h1 = self.mn.hosts[ 0 ]
    h2 = self.mn.hosts[ 1 ]
    h3 = self.mn.hosts[ 2 ]
    h4 = self.mn.hosts[ 3 ]
    h5 = self.mn.hosts[ 4 ]
    h7 = self.mn.hosts[ 6 ]
    
    self.vlc_start_client( h7, port_1 )
    sleep(2)
    self.vlc_start_stream( h1, path_video, h7 , port_1 )

def do_vlc( self, line ):
    """Start VLC video streams at h1 and h3, and VLC receivers at h3, h4.
    Usage: vlc [start|stop|restart]"""

    args = line.split()
    if len(args) == 0:
        self.vlc_start_vlc()
        return
    elif len(args) > 1:
        error( 'invalid number of args: see help vlc\n' )
        return
    elif args[0] == 'start':
        self.vlc_start_vlc()
        return 
    elif args[0] == 'stop':
        self.vlc_stop_vlc()
        return 
    elif args[0] == 'restart':
        self.vlc_stop_vlc()
        self.vlc_start_vlc()
        return
    else:
        error( 'unknown command: see help vlc\n' )

def complete_vlc(self, text, line, begidx, endidx):
    a = [ 'start', 'stop', 'restart' ]
    return [i for i in a if i.startswith(text)]

	
def vlc_stop_vlc( self ):
    "Stop vlc programs."
    for filename in glob( '/tmp/mininet_vlc_*' ):
        self.kill_from_pid_file( filename )

def kill_from_pid_file( self, filename ):
    "Kill the program whose pid is stored in `filename'."
    from os import kill, unlink
    from glob import glob
    from signal import SIGKILL

    try:
        file = open( filename, 'r' )
    except IOError:
        return
    pid = file.read(100)
    kill( int(pid), SIGKILL )
    unlink( filename )

def my_stop_all( self ):
    "Stop the traffic monitor, vlc programs and then stop the nodes."
    self.kill_from_pid_file( '/tmp/traffic_monitor.pid' )
    self.vlc_stop_vlc()
    self.my_stop_orig()

CLI.vlc_start_stream = vlc_start_stream
CLI.vlc_start_client = vlc_start_client
CLI.vlc_start_vlc = vlc_start_vlc
CLI.vlc_stop_vlc = vlc_stop_vlc
CLI.kill_from_pid_file = kill_from_pid_file
CLI.do_vlc = do_vlc
CLI.complete_vlc = complete_vlc

################################
def myNetwork ():
	topo = tree_Topo()
	#net = Mininet (topo) 
	info ('**** Adding controller \n ')
	net = Mininet ( topo = topo , controller = partial(RemoteController, ip = '192.168.0.37', port = 6633)) 
	info ('**** Starting network')
	net.start()
	#h1.cmdPrint('dhclient '+ h1.defaultIntf().name)
	#h2.cmdPrint('dhclient '+ h2.defaultIntf().name)
	net.pingAll()
	net.pingAll()
	linet = '/data/Descargas/media_org/scripts/commands.txt'
    	CLI(net, script = linet)
	sleep(30)
	#CLI(net)
	net.stop()
	
if __name__ == '__main__':
    setLogLevel('info')
    myNetwork()



