#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A parser to load an OFX file into a sequence of QifItem.
"""

import sys
from ofxparse import OfxParser
from qif import QifItem
from datetime import timedelta
import time

def parse_ofx(infile):
    """
    Parse an ofx file and return a list of entries.
    infile should be open file-like object (supporting readline() ).
    """

    items = []
    ofx = OfxParser.parse(infile)
    for trn in ofx.account.statement.transactions:
        curItem = QifItem()
        # trn.date is in UTC, it should be converted to local time before importing to Gnucash
        curItem.date = trn.date - timedelta(seconds=time.timezone)
        # trn.payee represents <NAME> element of OFX transaction, which should be the description of Gnucash transaction.
        # OFX has also <MEMO> element, but this is optional and sometimes empty.
        curItem.memo = trn.payee.encode('utf-8')
        curItem.split_amount = str(trn.amount)
        curItem.num = trn.id
        items.append(curItem)

    return items


if __name__ == '__main__':
    # read from stdin and write CSV to stdout
    items = parse_ofx(sys.stdin)
    for item in items:
        print item
