#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A parser to load a json file into a sequence of QifItem.
"""

import sys
import json
from qif import QifItem
from datetime import timedelta
import time

def parse_json(infile):
    """
    Parse a json file and return a list of entries.
    infile should be open file-like object (supporting readline() ).
    """

    items = []
    trans = json.load(infile)
    for tran in trans:
        curItem = QifItem()
        curItem.memo = tran['place'].encode('utf-8')
        curItem.split_amount = tran['amount']
        curItem.split_category = tran['genre_gnucash'].encode('utf-8')
        curItem.account = tran['from_account_gnucash'].encode('utf-8')
        curItem.date = datetime.datetime.strptime(tran['date'], '%Y-%m-%d')
        items.append(curItem)
    return items

if __name__ == '__main__':
    # read from stdin and write CSV to stdout
    items = parse_json(sys.stdin)
    for item in items:
        print item
