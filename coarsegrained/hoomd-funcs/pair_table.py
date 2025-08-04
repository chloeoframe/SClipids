import os
import itertools

def set_pair_potentials(table, ff_dir):
    all_types = ['water', 'head', 'tail', 'ter2', 'amide', 'mhead2', 'oh1',
            'oh2', 'oh3', 'oh4', 'chead', 'ring', 'ctail', 'cterm', 'chme', 'ester','sticky','taild','tail2']
    for t1, t2 in itertools.product(all_types, repeat=2):
        try:
            table.set_from_file(t1, t2,
                    filename=os.path.join(ff_dir, '%s-%s.txt' % (t1, t2)))
        except:
            pass
