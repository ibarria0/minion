#!/usr/bin/python
import xmlrpclib
from time import sleep

def connect_to_gandi():
  return xmlrpclib.ServerProxy('https://rpc.gandi.net/xmlrpc/')

def update_dns(gandi,domain_name,dns_servers,key):
  gandi.domain.nameservers.set(key,domain_name, dns_servers)
  ns = gandi.domain.info(key, domain_name)['nameservers']
  print 'Nameservers for %s: ' % domain_name
  for s in ns:
    print s

def check_domain_available(gandi,domain_name,key):
  result = gandi.domain.available(key, [domain_name])
  while result[domain_name] == 'pending':
    sleep(0.7)
    result = gandi.domain.available(key, [domain_name])
  return True if (result[domain_name] == 'available') else False
