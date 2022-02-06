from itertools import chain
def _gen_multlist_code(nm):
    s = ''
    l =[]
    for i in nm:
        num = int(nm[nm.index(i)])
        s = s + 'for {} in range({}) '.format('i_'+ str(i),str(num))
        l.append('i_'+ str(i))
    var = '['+','.join(l)+ ']'
    s = '[' + var + s + ']'
    code = eval(s)
    return code
    
def build_xpath_string(path,nm):
    if path.count('{') == len(nm):
        num_int = 1
        for num_nn in nm:
            num_int = num_int * int(num_nn)            
        path = (path +'```') * num_int
        mm = _gen_multlist_code(nm)
        mm = tuple(list(chain.from_iterable(mm)))
        path = path.format(*mm)
        path = path.rstrip('```')
        path_list = path.split('```')
        return path_list
    else:
        print("Dimension error or {} not in []: Example build_xpath_string('aaa/bbb[{}]/ccc[{}]',['2','3'])")
