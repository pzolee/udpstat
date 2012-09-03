udpstat
======

UDP buffer size (RX, TX) and dropped packages statistics program, written by PZolee (pzoleex @ freemail.hu), 2012
https://github.com/pzolee/udpstat

This little tool lists the usage of the incoming and outgoing buffers of the UDP socket belongs to the specified port, and the number of dropped packages.
Example:
:~# ./udpstat.py 5001 -u 10
Start collecting RX and TX queue statistics information and dropped packages result for port (5001)
2012-09-03T14:28:38.550504;tx queue: 0 bytes, 0 KB, 0 MB; rx queue: 0 bytes, 0 KB, 0 MB; dropped packages: 0;
2012-09-03T14:28:39.551747;tx queue: 0 bytes, 0 KB, 0 MB; rx queue: 0 bytes, 0 KB, 0 MB; dropped packages: 0;
2012-09-03T14:28:40.552996;tx queue: 0 bytes, 0 KB, 0 MB; rx queue: 0 bytes, 0 KB, 0 MB; dropped packages: 0;
2012-09-03T14:28:41.554350;tx queue: 0 bytes, 0 KB, 0 MB; rx queue: 332055496 bytes, 324272 KB, 316 MB; dropped packages: 0;
2012-09-03T14:28:42.555650;tx queue: 0 bytes, 0 KB, 0 MB; rx queue: 536869432 bytes, 524286 KB, 511 MB; dropped packages: 118733;
2012-09-03T14:28:43.556819;tx queue: 0 bytes, 0 KB, 0 MB; rx queue: 536869432 bytes, 524286 KB, 511 MB; dropped packages: 374088;
2012-09-03T14:28:44.558018;tx queue: 0 bytes, 0 KB, 0 MB; rx queue: 509777816 bytes, 497829 KB, 486 MB; dropped packages: 493162;
2012-09-03T14:28:45.559211;tx queue: 0 bytes, 0 KB, 0 MB; rx queue: 481418456 bytes, 470135 KB, 459 MB; dropped packages: 493162;
2012-09-03T14:28:46.560400;tx queue: 0 bytes, 0 KB, 0 MB; rx queue: 481418456 bytes, 470135 KB, 459 MB; dropped packages: 493162;
2012-09-03T14:28:47.561667;tx queue: 0 bytes, 0 KB, 0 MB; rx queue: 443327512 bytes, 432937 KB, 422 MB; dropped packages: 493162;
Maximum tx queue: 0 bytes, 0 KB, 0 MB; 
Maximum rx queue: 536869432 bytes, 524286 KB, 511 MB; 
Dropped packages: 493162 

Help:
:~# ./udpstat.py -h
Usage: udpstat.py [options] port

UDP buffer size (RX, TX) and dropped packages statistics program, written by
PZolee (pzoleex @ freemail.hu), 2012

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -o <filename>, --output=<filename>
                        The name of the output file
  -r, --rx              Measure the size of RX(incoming) buffer
  -t, --tx              Measure the size of TX(outgoing) buffer
  -d, --drops           Measure the number of dropped packages for RX and TX
                        buffers
  -b BLOCK_SIZE, --displayed-blocks=BLOCK_SIZE
                        The displayed block size for the TX, RX queues.
                        Possible values: B, K, M, all; default: all
  -l <local|remote>, --listened-port-type=<local|remote>
                        The type of the listened port, default: local
  -f FREQ, --freq=FREQ  The time between two polls in sec, default: 1
  -u RUNTIME, --run-time=RUNTIME
                        The running time if given. Default: untill CTRL+C
  -c, --csv             Generate CSV output format
