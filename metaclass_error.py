import inspect 
import types
import builtins

def skip_redundant(iterable, skipset=None): 
    if skipset is None: skipset = set()
    for item in iterable: 
        if item not in skipset: 
            skipset.add(item)
            yield item 

def remove_redundant(metaclasses): 
    skipset = set([types.ClassType])
    for meta in metaclasses: 
        skipset.update(inspect.getmro(meta)[1:])
    return tuple(skip_redundant(metaclasses, skipset))

memoized_metaclasses_map = {}

def get_noconflict_metaclass(bases, left_metas, right_metas): 

    metas = left_metas + tuple(map(type,bases)) + right_metas
    needed_metas = remove_redundant(metas)

    if needed_metas in memoized_metaclasses_map: 
        return memoized_metaclasses_map[needed_metas]
    elif not needed_metas: 
        meta = type
    elif len(needed_metas) == 1: 
        meta = needed_metas[0]
    elif needed_metas == bases: 
        raise TypeError("Incompatible Root Metatypes", needed_metas)
    else: # unfinished
        metaname = '_' + ''.join([m.__name__ for m in needed_metas])
        meta = classmaker()(metaname, needed_metas, {})
    memoized_metaclasses_map[needed_metas] = meta 
    return meta 

def classmaker(left_metas=(), right_metas=()):
    def make_class(name, bases, adict): 
        metaclass = get_noconflict_metaclass(bases, left_metas, right_metas) 
        return metaclass(name, bases, adict) 
    return make_class 

    
    