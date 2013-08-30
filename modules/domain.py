#!/usr/bin/python
import boto

#boto.set_stream_logger('boto')

def get_dns(r53,zone):
  return [b for b in r53.get_hosted_zone(zone.id)['GetHostedZoneResponse']['DelegationSet']['NameServers']]

def connect_to_r53(aws_access_key_id,aws_secret_access_key):
  return boto.connect_route53(aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

def input_domain():
  domain_name = unicode(raw_input('enter domain name: '))
  if domain_name[-1] != unicode('.'): domain_name += unicode('.') 
  return domain_name

def create_domain_zone(r53,name):
  zones = r53.get_zones()
  if name not in [z.name[:-1] for z in zones]:
    zone = r53.create_zone(name)
    print 'domain %s created' % name
    return zone
  else:
    print 'domain %s already exists' % name
    return r53.get_zone(name)

def create_google_mx(r53,zone):
  try:
    records = r53.get_all_rrsets(zone.id)
    mx_records = ['1 ASPMX.L.GOOGLE.COM','5 ALT1.ASPMX.L.GOOGLE.COM','5 ALT2.ASPMX.L.GOOGLE.COM','10 ASPMX2.GOOGLEMAIL.COM','10 ASPMX3.GOOGLEMAIL.COM']
    change = records.add_change('CREATE', zone.name, 'MX')
    [change.add_value(mx) for mx in mx_records]
    records.commit()
  except boto.route53.exception.DNSServerError:
    print 'MX records already exists'
  return records

def create_website_records(r53,zone,buckets):
  try:
    records = r53.get_all_rrsets(zone.id)
    change = records.add_change('CREATE', zone.name, 'A',alias_hosted_zone_id='Z3AQBSTGFYJSTF',alias_dns_name='s3-website-us-east-1.amazonaws.com')
    change.add_value('ALIAS s3-website-us-east-1.amazonaws.com (Z3AQBSTGFYJSTF)')
    change = records.add_change('CREATE', 'www.' + zone.name, 'CNAME')
    change.add_value('%s' % buckets['www'].get_website_endpoint())
    records.commit()
  except boto.route53.exception.DNSServerError:
    print 'webiste records already exists'
  return records
