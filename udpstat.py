#!/usr/bin/python
# vim: sts=4 ts=8 et ai

''' UDP buffer size (RX, TX) and dropped packages statistics program, written by PZolee (pzoleex @ freemail.hu), 2012'''

import signal
import time
from re import search
from optparse import OptionParser
from datetime import datetime
from sys import exit


def signal_handler(signal, frame):
    print "Exiting"
    try:
        f.close()
        ofile.close()
    except:
        pass
    print "Maximum tx queue: " + q_res % ({'in_byte': max_tx, 'in_kbyte': max_tx / 1024, 'in_mbyte': max_tx / 1048576})
    print "Maximum rx queue: " + q_res % ({'in_byte': max_rx, 'in_kbyte': max_rx / 1024, 'in_mbyte': max_rx / 1048576})
    print "Dropped packages: %s " % drops

    exit(0)

signal.signal(signal.SIGINT, signal_handler)

udp_input = '/proc/net/udp'
'''  sl  local_address rem_address   st tx_queue rx_queue tr tm->when retrnsmt   uid  timeout inode ref pointer drops
   8: 00000000:02BA 00000000:0000 07 00000000:00000000 00:00000000 00000000     0        0 4515 2 ffff8802a94c0000 0
  59: 00000000:E16D 00000000:0000 07 00000000:00000000 00:00000000 00000000     0        0 4528 2 ffff8802a94b0000 0
  61: 00000000:006F 00000000:0000 07 00000000:00000000 00:00000000 00000000     0        0 4316 2 ffff8802a9498000 0
  73: 00000000:EC7B 00000000:0000 07 00000000:00000000 00:00000000 00000000     0        0 16701920 2 ffff8802a949cac0 0
'''

usage = "usage: %prog [options] port"
desc = "UDP buffer size (RX, TX) and dropped packages statistics program, written by PZolee (pzoleex @ freemail.hu), 2012"
parser = OptionParser(usage, description = desc, version = "%prog version: 1.0")
parser.add_option("-o", "--output", dest="filename", help="The name of the output file", metavar = "<filename>")
parser.add_option("-r", "--rx", help="Measure the size of RX(incoming) buffer", action="store_true", dest="rx", default=False)
parser.add_option("-t", "--tx", help="Measure the size of TX(outgoing) buffer", action="store_true", dest="tx", default=False)
parser.add_option("-d", "--drops", help="Measure the number of dropped packages for RX and TX buffers", action="store_true", dest="drops", default=False)
parser.add_option("-b", "--displayed-blocks", dest="block_size", help="The displayed block size for the TX, RX queues. Possible values: B, K, M, all; default: %default", default="all")
parser.add_option("-l", "--listened-port-type", help="The type of the listened port, default: %default",
                  action="store", dest="listened", default="local", metavar = "<local|remote>")
parser.add_option("-f", "--freq", help="The time between two polls in sec, default: %default", action="store", dest="freq", default=1, type="float")
parser.add_option("-u", "--run-time", help="The running time if given. Default: untill CTRL+C", action="store", dest="runtime", default=0, type="int")
parser.add_option("-c", "--csv", help="Generate CSV output format", action="store_true", dest="csv", default=False)

(opts, args) = parser.parse_args()

if opts.block_size.upper() == "B":
    q_res = "%(in_byte)s bytes; "
    q_header = "{0} in bytes"
    csv_res = "%(in_byte)s;"
elif opts.block_size.upper() == "K":
    q_res = "%(in_kbyte)s KB; "
    q_header = "{0} in kilobytes"
    csv_res = "%(in_kbyte)s;"
elif opts.block_size.upper() == "M":
    q_res = "%(in_mbyte)s MB; "
    q_header = "{0} in megabytes;"
    csv_res = "%(in_mbyte)s;"
else:
    q_res = "%(in_byte)s bytes, %(in_kbyte)s KB, %(in_mbyte)s MB; "
    q_header = "{0} in bytes;{0} in kilobytes;{0} in megabytes;"
    csv_res = "%(in_byte)s;%(in_kbyte)s;%(in_mbyte)s;"

if not opts.rx and not opts.tx and not opts.drops:
    #If no limits, display all counters
    use_all_counter = True
else:
    use_all_counter = False

if len(args) < 1:
    print "Port is required!"
    parser.print_help()
    exit(1)

hexport = "%x" % int(args[0])
print "Start collecting RX and TX queue statistics information and dropped packages result for port (%s)" % args[0]

if opts.filename:
    ofile = open(opts.filename, 'wb')

is_header = False
header = ""
max_rx = 0
max_tx = 0

stime = atime = time.time()
while stime >= atime - opts.runtime:
    f = open(udp_input, 'rb')
    lines = f.readlines()
    f.close()
    for item in lines:
        if search(hexport, item) != None:
            buffers = item.strip().split() # 0:sl, 1:local_address, 2:rem_address, 3:st, 4:tx_queue rx_queue, 5:tr tm->when retrnsmt
                                           # 6:retrnsmt, 7:uid, 8:timeout, 9:inode, 10:ref, 11:pointer, 12:drops
            sl, la, ra, st, tx_rx, tr, retrnsmt, uid, timeout, inode, ref, pointer, drops = buffers
            if opts.listened == 'local' and search(la.split(':')[1], hexport) == None:
                # The local port does not match to the given local port
                print "There is no matching port yet"
                time.sleep(opts.freq)
                continue
            if opts.listened == 'remote' and search(ra.split(':')[1], hexport) == None:
                # The remote port does not match to the given remote port
                print "There is no matching port yet"
                time.sleep(opts.freq)
                continue

            tx_queue, rx_queue = tx_rx.split(':')
            rx_queue = int(rx_queue, 16) # convert to dec
            tx_queue = int(tx_queue, 16) # convert to dec

            if rx_queue > max_rx:
                max_rx = rx_queue
            if tx_queue > max_tx:
                max_tx = tx_queue

            header = "time;"
            res = datetime.now().isoformat() + ";"
            if opts.tx or use_all_counter:
                if opts.csv:
                    res = res + csv_res % ({'in_byte': tx_queue, 'in_kbyte': tx_queue / 1024, 'in_mbyte': tx_queue / 1048576})
                    if not is_header:
                        header = header + q_header.format("tx")
                else:
                    res = res + "tx queue: " + q_res % ({'in_byte': tx_queue, 'in_kbyte': tx_queue / 1024, 'in_mbyte': tx_queue / 1048576})

            if opts.rx or use_all_counter:
                if opts.csv:
                    res = res + csv_res % ({'in_byte': rx_queue, 'in_kbyte': rx_queue / 1024, 'in_mbyte': rx_queue / 1048576})
                    if not is_header:
                        header = header + q_header.format("rx")
                else:
                    res = res + "rx queue: " + q_res % ({'in_byte': rx_queue, 'in_kbyte': rx_queue / 1024, 'in_mbyte': rx_queue / 1048576})

            if opts.drops or use_all_counter:
                if opts.csv:
                    res = res + "%s;" % drops
                    if not is_header:
                        header = header + "dropped packages;"
                else:
                    res = res + "dropped packages: %s;" % drops

            if opts.csv and not is_header:
                print header
                if opts.filename:
                    ofile.write(header + '\n')
                    ofile.flush()
                is_header = True

            print res
            if opts.filename:
                ofile.write(res + '\n')
                ofile.flush()

    time.sleep(opts.freq)
    if opts.runtime > 0:
        atime = time.time()

print "Maximum tx queue: " + q_res % ({'in_byte': max_tx, 'in_kbyte': max_tx / 1024, 'in_mbyte': max_tx / 1048576})
print "Maximum rx queue: " + q_res % ({'in_byte': max_rx, 'in_kbyte': max_rx / 1024, 'in_mbyte': max_rx / 1048576})
print "Dropped packages: %s " % drops

if opts.filename:
    ofile.close()
