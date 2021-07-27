#!/usr/bin/env python3
'''dS378 client'''
import sys

from ocs.matched_client import MatchedClient

def usage():
    print('usage: pcr_client.py', file=sys.stderr)

def main():
    '''PCR client'''
    pcr_client = MatchedClient('stm-heater-source', args=[])

    pcr_client.set_volt_ac(volt_set=0)
    pcr_client.set_output(output=False)


if __name__ == '__main__':
    main()
