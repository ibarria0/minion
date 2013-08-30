#!/usr/bin/python
import boto
import argparse

#boto.set_stream_logger('boto')
def parse_args():
  parser = argparse.ArgumentParser(description='AWS helper')
  parser.add_argument('--key', dest='key', type=str, default=False,required=True)
  parser.add_argument('--secret', dest='secret', type=str, default=False,required=True)
  parser.add_argument('--domain', dest='domain', type=str, default=False ,required=True)
  return parser.parse_args()

def connect_to_s3(aws_access_key_id,aws_secret_access_key):
  return boto.connect_s3(aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

def input_domain():
  domain_name = unicode(raw_input('enter domain name: '))
  return domain_name

def create_apex_bucket(s3,domain_name):
  if domain_name not in [b.name for b in s3.get_all_buckets()]:
    bucket = s3.create_bucket(domain_name)
    print 'bucket %s created' % domain_name
    return bucket
  else:
    print 'bucket %s already exists' % domain_name
    return s3.get_bucket(domain_name)

def create_www_bucket(s3,domain_name):
  domain_name = 'www.' + domain_name
  if domain_name not in [b.name for b in s3.get_all_buckets()]:
    bucket = s3.create_bucket(domain_name)
    print 'bucket %s created' % domain_name
    return bucket
  else:
    print 'bucket %s already exists' % domain_name
    return s3.get_bucket(domain_name)

def create_buckets(s3,domain_name):
  return {'apex': create_apex_bucket(s3,domain_name), 'www': create_www_bucket(s3,domain_name)}

def setup_site(buckets):
  buckets['apex'].configure_website(suffix='index.html')
  buckets['www'].configure_website(redirect_all_requests_to=boto.s3.website.RedirectLocation(hostname=buckets['apex'].get_website_endpoint()))
  return buckets

def upload_comming_soon(bucket):
  for html in ['index.html','404.html']:
    k = bucket.new_key(html)
    k.set_contents_from_filename(html)
    k.make_public()

if __name__=="__main__":
  args = parse_args()
  s3 = connect_to_s3(args.key,args.secret)
  domain_name = args.domain
  buckets = create_buckets(s3,domain_name)
  print dir(buckets['apex'])

