import os
import time

import requests
import CloudFlare

# Set environment variables
TOKEN = os.environ.get('CLOUDFLARE_API_TOKEN')
ZONE = os.environ.get('CLOUDFLARE_ZONE_NAME')
DNS_NAME = os.environ.get('CLOUDFLARE_DNS_NAME')
DNS_TYPE = os.environ.get('CLOUDFLARE_DNS_TYPE', 'A')
IP_SOURCE_URL = os.environ.get('IP_SOURCE_URL', 'https://api.ipify.org')
POLL_INTERVAL = int(os.environ.get('POLL_INTERVAL', 60 * 30))

def main():
    while True:
        # Create a connection to the CloudFlare API
        cf = CloudFlare.CloudFlare(token=TOKEN)

        # Get the zone ID for the requested zone
        zone = cf.zones.get(params={'name': ZONE})
        zone_id = zone[0]['id']

        # Get current IP address
        ip = requests.get(IP_SOURCE_URL).text
        assert ip != ''

        current_dns_records = cf.zones.dns_records.get(zone_id, params={'name': DNS_NAME + '.' + ZONE})
        assert current_dns_records != []
        assert len(current_dns_records) == 1

        current_dns_record = current_dns_records[0]

        if current_dns_record['content'] == ip:
            print('DNS record for ' + DNS_NAME + '.' + ZONE + ' is already up to date, sleeping for ' + str(POLL_INTERVAL) + ' seconds')
            time.sleep(POLL_INTERVAL)
            continue

        assert current_dns_record['zone_id'] == zone_id
        assert current_dns_record['zone_name'] == ZONE
        assert current_dns_record['type'] == DNS_TYPE
        current_dns_record_id = current_dns_record['id']

        # Delete the current DNS record
        cf.zones.dns_records.delete(zone_id, current_dns_record_id)

        # Create a new DNS record
        dns_record = {
            'name': DNS_NAME,
            'type': DNS_TYPE,
            'content': ip,
            'proxied': True
        }
        cf.zones.dns_records.post(zone_id, data=dns_record)

        print('Successfully updated DNS record for ' + DNS_NAME + '.' + ZONE + ' to ' + ip)

if __name__ == '__main__':
    main()