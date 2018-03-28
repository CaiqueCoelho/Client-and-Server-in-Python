#!/usr/bin/python
# A simple http client that retrieves the first page of a web site
import socket, sys
import re
if len (sys.argv)!=3 and len (sys.argv)!=2:
	print "Usage : ",sys.argv[0]," hostname [port]"

hostname = sys.argv[1]

enderecoHost= []
hostlist = hostname.split("/")
caminho = []
caminho.append("/")

for host in hostlist:
	print host +'\n'

for host in hostlist:
	if ".br" in host:
		print 1
		enderecoHost.append(host)

	elif ".com" in host:
		print 2
		enderecoHost.append(host)

	elif "http" in host:
		print 3

	else:
		if re.search('[a-zA-Z]', host): 
			print 4
			caminho.append(host)
			caminho.append("/")

enderecoHost = ''.join(enderecoHost)
caminho = ''.join(caminho)

if not enderecoHost.isspace():
	enderecoHost = []
	for host in hostlist:
		enderecoHost.append(host)
	enderecoHost = ''.join(enderecoHost)
	caminho = []
	caminho = ''.join(caminho)


	#print host + '\n'

print "Endereco Host: " + enderecoHost + '\n'
if caminho.isspace():
	print "Endereco Caminho: " + caminho +'\n'

if len(sys.argv)==3 :
	port= int(sys.argv[2])
else:
	port = 80
READBUF=16384
s=None


# size of data read from web server
for res in socket.getaddrinfo(enderecoHost, port, socket.AF_UNSPEC, socket.SOCK_STREAM):
	af, socktype, proto, canonname, sa = res
	# create socket
	try:
		s = socket.socket(af, socktype, proto)
	except socket.error:
		s = None
		continue
	# connect to remote host
	try:
		print "Trying "+sa[0]
		s.connect(sa)
	except socket.error, msg:
		# socket failed
		s.close()
		s = None
		continue
	if s :
		print "Connected to "+sa[0]
		if re.search('[a-zA-Z]', caminho):
			print 'GET ' + caminho + ' HTTP/1.1\r\nHost:'+enderecoHost+'\r\n\r\n'
			s.send('GET ' + caminho + ' HTTP/1.1\r\nHost:'+enderecoHost+'\r\n\r\n')
		else:
			s.send('GET / HTTP/1.1\r\nHost:'+hostname+'\r\n\r\n')
		finished=False
		count=0
		while not finished:
			data=s.recv(READBUF)
			count=count+1
			if len (data)!=0:
				print repr (data)
			else:
				finished=True
		s.shutdown(socket.SHUT_WR)
		s.close()
		print "Data was received in ",count," recv calls"
		break