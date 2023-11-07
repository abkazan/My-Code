import pstats
from pstats import SortKey
p = pstats.Stats('results.txt')
p.strip_dirs().sort_stats(SortKey.TIME).print_stats(10)