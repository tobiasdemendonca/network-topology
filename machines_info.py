#!/usr/bin/env python3

import os
import sys
import uuid
from datetime import datetime

import requests
import yaml


def main():
    API_KEY = os.getenv("MAAS_APIKEY", None)
    if not API_KEY:
        print("No MAAS API key provided. Set it in the env variable 'MAAS_APIKEY'")
        print(
            "You can get it with the command `sudo maas apikey --username <username>`"
        )
        sys.exit(1)

    API_KEY = API_KEY.split(":")
    MAAS_IP = os.getenv("MAAS_IP", None)
    if not API_KEY:
        print("No MAAS IP provided. Set it in the env variable 'MAAS_IP'")
        sys.exit(1)

    headers = {
        "Authorization": f"OAuth oauth_version=1.0, oauth_signature_method=PLAINTEXT, oauth_consumer_key={API_KEY[0]}, oauth_token={API_KEY[1]}, oauth_signature=&{API_KEY[2]}, oauth_nonce={uuid.uuid4()}, oauth_timestamp={int(datetime.now().timestamp())}"
    }
    machines = requests.get(
        f"http://{MAAS_IP}:5240/MAAS/api/2.0/machines/", headers=headers
    )
    result = {}
    for machine in machines.json():
        ips = set()
        subnets = set()
        for interface in machine["interface_set"]:
            for link in interface["links"]:
                ips.add(link["ip_address"])
                subnets.add(link["subnet"]["cidr"])
        machine_dict = {
            "hostname": machine["hostname"],
            "ips": list(ips),
            "subnets": list(subnets),
        }
        result[machine["system_id"]] = machine_dict
    print(yaml.dump(result))


if __name__ == "__main__":
    main()
