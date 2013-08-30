#!/usr/bin/python
import boto
import argparse
from modules import domain
from modules import bucket
from modules import gandi

#boto.set_stream_logger('boto') #debug
def parse_args():
  parser = argparse.ArgumentParser(description='AWS helper')
  parser.add_argument('--key', dest='key', type=str, default=False,required=True)
  parser.add_argument('--secret', dest='secret', type=str, default=False,required=True)
  parser.add_argument('--domain', dest='domain', type=str, default=False ,required=True)
  parser.add_argument('--gandi', dest='gandi', type=str, default=False ,required=True)
  return parser.parse_args()

args = parse_args()

#init connections
s3 = bucket.connect_to_s3(args.key,args.secret)
r53 = domain.connect_to_r53(args.key,args.secret)

#create buckets
buckets = bucket.create_buckets(s3,args.domain)
bucket.setup_site(buckets)
bucket.upload_comming_soon(buckets['apex'])

#setup zone
zone = domain.create_domain_zone(r53,args.domain)
domain.create_google_mx(r53,zone) 
domain.create_website_records(r53,zone,buckets)

#configure AWS nameservers
gandi_conn = gandi.connect_to_gandi()
aws_dns = domain.get_dns(r53,zone)
gandi.update_dns(gandi_conn,args.domain,aws_dns,args.gandi)
