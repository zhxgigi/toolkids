#!/usr/bin/python

def read_to_dict(fpath):
    data = {}
    with open(fpath) as f:
        for rank, line in enumerate(f):
            if not line.strip():
                continue
            data[rank] = line.strip()
    return data


def statistics(fpath1, fpath2):
    rank_entry_data1 = read_to_dict(fpath1)
    rank_entry_data2 = read_to_dict(fpath2)
    assert len(rank_entry_data1) == len(rank_entry_data2), "file len not equal."

    entry_rank_data1 = {v: k for k, v in rank_entry_data1.items()}
    entry_rank_data2 = {v: k for k, v in rank_entry_data2.items()}

    add_entry_count = 0
    miss_entry_count = 0
    
    max_rank_diff = 0
    standard_deviation_rank_diff = 0.0

    new_add_entry = set(rank_entry_data2.values()) - set(rank_entry_data1.values())
    miss_entry = set(rank_entry_data1.values()) - set(rank_entry_data2.values())
    shared_entry = set(rank_entry_data1.values()) & set(rank_entry_data2.values())

    add_entry_count = len(new_add_entry)
    miss_entry_count = len(miss_entry)

    rankdiff_list = []
    for entry in shared_entry:
        rank1 = entry_rank_data1[entry]
        rank2 = entry_rank_data2[entry]
        rankdiff = abs(rank1 - rank2)
        rankdiff_list.append(rankdiff)

        if rankdiff > max_rank_diff:
            max_rank_diff = rankdiff

    total_rank_diff = sum(rankdiff_list)
    try:
        avg_rank_diff = total_rank_diff / (len(shared_entry) + 0.0)
    except:
        avg_rank_diff = -1

    try:
        standard_deviation_rank_diff = (sum([(rankdiff - avg_rank_diff)**2 for rankdiff in rankdiff_list]) / (len(rankdiff_list) - 1)) ** 0.5
    except:
        standard_deviation_rank_diff = -1
    
    print "="*78
    print "new items: %d" % add_entry_count
    print "ranking variation: %d" % total_rank_diff
    print "="*78
    print "OPTIONAL:"
    print "miss items: %d" % miss_entry_count
    print "max ranking variation: %d" % max_rank_diff
    print "average ranking variation: %f" % avg_rank_diff
    print "standard deviation of ranking variation: %f" % standard_deviation_rank_diff


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print "python qadiff.py fpath1 fpath2"
        sys.exit(2)
    filepath1 = sys.argv[1]
    filepath2 = sys.argv[2]
    statistics(filepath1, filepath2)

