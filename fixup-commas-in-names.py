import sys
lines = open(sys.argv[1]).readlines()
k = set()
for l in lines:
    ls = l.split(',')
    count = ls[0]
    rest = ls[1:]
    n = len(rest)
    assert n % 2 == 0
    # we have the same name repeated twice so we need to find out how many extra commas are in it
    cms = (n - 4) / 2
    #print ','.join(rest[:cms])
    sys.stdout.write('\t'.join([count] + [','.join(rest[:cms])] + rest[cms:-cms] + [','.join(rest[-cms:])]))
    #k.add(len(ls))
    #ls = [",".join(ls[:-7])] + ls[-7:]
    #print ls
#print k
