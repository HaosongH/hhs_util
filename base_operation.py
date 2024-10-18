def list_union(list1, list2):
    return list(set(list1) | set(list2))

def float_equal(a,b,eps=0.0001):
    return abs(a-b)<eps
