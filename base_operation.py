import numpy as np
def list_union(list1, list2):
    return list(set(list1) | set(list2))

def list_filter_by_prefix(list, prefix):
   return [s for s in list if s.startswith(prefix)]
    
def list_unique(list):
    return list(dict.fromkeys(list))

def float_equal(a,b,eps=0.0001):
    return abs(a-b)<eps

def getElementIndexByFunc(list, func):
    return func((v,i) for i, v in enumerate(list))

def getSortListIndex(list,ascend = 1):
    s = np.array(list)
    if ascend:
        return np.argsort(s).tolist()
    else:
        return np.flip(np.argsort(s)).tolist()