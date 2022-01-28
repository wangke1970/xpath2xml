#!/usr/bin/env python3
# change https://stackoverflow.com/questions/5661968/how-to-populate-xml-file-using-xpath-in-python
__author__ = 'Wang Ke'
# └┕┖┗ ┘┙┚┛╘╙ 
from xml.etree import ElementTree as ET
import re
from itertools import chain
class xpath2xml:
    def __init__(self,ns,root=None,root_name='nc:rpc'):
        for k,v in ns.items():
            ET.register_namespace(k,v)    
        self.root = ET.Element(root_name)
        self.root.attrib = {'xmlns:'+k:v for k,v in ns.items()}
        self.ns = ns
        self.parent = None
        self.xml = None
    
#    def __call__(self,path,ns):
#        self._build(self.root,path,ns)
#        self.xml = ET.tostring(self.root,xml_declaration=True,encoding = 'utf-8')
#        self.xml = str(self.xml,encoding = "utf-8")
#        return self
    
    # add path string
    def add(self, path):
        self._build(self.root,path)
        self.xml = ET.tostring(self.root,xml_declaration=True,encoding = 'utf-8')
        self.xml = str(self.xml,encoding = "utf-8")
        return self

    # add path list
    def adds(self, path_list):
        for i in path_list:
            self = self.add(i)
        return self
    
    def _build(self, node, path):
        components = path.split("/")
        if components[0] == node.tag:
            components.pop(0)
#        identifier = r"[_A-Za-z][._\-A-Za-z0-9]*"
#        prefix = identifier
#        node_step = r'((' + prefix + r'):)?(' + identifier + r')'        
#        node_step_assign = r'((' + prefix + r'):)?(' + identifier + r')=.+'
#        node_step_predicates_num = node_step + r'\[\d+\]'
#        node_step_predicates_attrib = node_step + r'\[(@'+ node_step + r'=.+)+\]'
#        node_step_predicates_attrib_value = node_step + r'\[(@'+ node_step + r'=.+)+\]=.+'
        while components:
            value_end = None
            attrib_value = None
            components[0] = components[0].replace(' ','')
            if "[" in components[0]:
                if ']=' in components[0]:
                    value_end = components[0].split(']=',1)[1]
                    components[0] = components[0].split(']=',1)[0]+']'
                component, trail = components[0].split("[",1)
                pred = trail.split("=")[0].strip("]")
                if pred.isdigit():
                    target_index = int(pred)
                    try:
                        assert(int(pred) >= 0)
                    except AssertionError as asser:
                        print('[n] n must >= 0')
                        return
                    if "=" in trail:
                        value_end = trail.split("=")[-1].strip("]")
                else:
                    attrib_list = trail.strip("]").split("@")
                    attrib_list = list(filter(None,attrib_list)) 
                    attrib_list_dict = {i.split("=",1)[0]:i.split("=",1)[1] for i in attrib_list}
                    attrib_value = attrib_list_dict
                    target_index = 0
            
            elif "=" in components[0]:
                component, value_end = components[0].split("=",1)
                target_index = 0
            # if re.match(node_step,components[0]):
            else:
                component = components[0]
                target_index = 0
            
            components.pop(0)
            found_index = -1
            for child in node:
                if child.tag == component:
                    found_index += 1
                    if found_index == target_index:
                        if value_end:
                            child.text = value_end
                        node = child
                        if attrib_value :
                            child.attrib = attrib_value
                        break
            else:
                for i in range(target_index - found_index):
                    if value_end:
                        new_node = ET.Element(component)
                        new_node.text = value_end
                        if attrib_value :
                            new_node.attrib = attrib_value                    
                    else:
                        new_node = ET.Element(component)
                        if attrib_value :
                            new_node.attrib = attrib_value                    
                    node.append(new_node)
                node = new_node
    
    def remove(self,path):
        data = ET.tostring(self.root,xml_declaration=True,encoding='utf-8')
        data_root = ET.fromstring(str(data,encoding = "utf-8"))
        path = re.sub('(?P<num>\[[0-9]+\])',self._num_matched,path)        
        xml_node = data_root.find(path,self.ns)
        if xml_node!=None:
            self._node_find(data_root,xml_node)
        else:
            return 
        if self.parent:
            self.parent.remove(xml_node)
        self.xml = str(ET.tostring(data_root,xml_declaration=True,encoding='utf-8'),encoding="utf-8")
        return self        

    def _num_matched(self,matched):
        index_str = matched.group('num')
        index = index_str.replace('[','').replace(']','')
        index=int(index)+1
        index_str = '['+str(index)+']'
        return index_str
    
    def _node_find(self,node,sub_node):
        for i in node:
            if i == sub_node:
                self.parent=node
                break
            else:
                self._node_find(i,sub_node)
    

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
            
if __name__  == "__main__":
    #Example add leaf-list out xml string
    ns = {'yang': 'urn:ietf:params:xml:ns:yang:ietf-yang-types', 'nc': 'urn:ietf:params:xml:ns:netconf:base:1.0', 'n1': 'http://openconfig.net/yang/bgp-policy', 'n2': 'http://openconfig.net/yang/types/inet', 'n3': 'http://openconfig.net/yang/bgp-types', 'n4': 'http://openconfig.net/yang/policy-types', 'n5': 'http://openconfig.net/yang/openconfig-types', 'n6': 'http://openconfig.net/yang/types/yang', 'n7': 'urn:ietf:params:xml:ns:yang:ietf-inet-types', 'n8': 'urn:ietf:params:xml:ns:yang:ietf-yang-types', 'n9': 'urn:ietf:params:xml:ns:yang:ietf-interfaces', 'n10': 'http://openconfig.net/yang/interfaces', 'n11': 'http://openconfig.net/yang/openconfig-ext', 'n12': 'http://openconfig.net/yang/bgp', 'n13': 'http://openconfig.net/yang/routing-policy'}
    xxx = xpath2xml(ns)
    
    path_list = ["nc:rpc/nc:edit-config/nc:config/n12:bgp/n12:peer-groups/n12:peer-group[2]/n12:apply-policy/n12:config/n12:import-policy[@nc:operation=create @yang:insert=after]=z",
                 "nc:rpc/nc:edit-config/nc:config/n12:bgp/n12:peer-groups/n12:peer-group[3]/n12:apply-policy/n12:config/n12:import-policy[2]=zzzzz",
                 "nc:rpc/nc:edit-config/nc:config/n12:bgp/n12:peer-groups/n12:peer-group[1]/n12:apply-policy/n12:config/n12:import-policy[0]=zz",
                 "nc:rpc/nc:edit-config/nc:config/n12:bgp/n12:peer-groups/n12:peer-group[1]/n12:apply-policy/n12:config/n12:import-policy[1]=zzz",
                 "nc:rpc/nc:edit-config/nc:config/n12:bgp/n12:peer-groups/n12:peer-group[0]/n12:apply-policy/n12:config/n12:import-policy[1]=zzz_000"
                ]
    
    # params 1 is yang absolute path ,n12:peer-group[{}] is list,  n12:import-policy[{}] is leaf-list. params 2 is dimension. 
    # this is build single leaf-list import-policy in openconfig-yang bgp module 
    path_list_tp = build_xpath_string("nc:rpc/nc:edit-config/nc:config/n12:bgp/n12:peer-groups/n12:peer-group[{}]/n12:apply-policy/n12:config/n12:import-policy[{}]=zzz",['2','3'])
    for i in path_list_tp:
        print(i)
        
    # add multi paths
    xxx = xxx.adds(path_list)
    # add single path
    xxx = xxx.add("nc:rpc/nc:edit-config/nc:config/n12:bgp/n12:peer-groups/n12:peer-group[0]/n12:apply-policy/n12:config/n12:import-policy[2]=zzz_111")
    # update zzz_111 to zzz_222
    xxx = xxx.add("nc:rpc/nc:edit-config/nc:config/n12:bgp/n12:peer-groups/n12:peer-group[0]/n12:apply-policy/n12:config/n12:import-policy[2]=zzz_222")
    
    print(xxx.xml)
    # current xml object nc:rpc is root. python xml.etree xpath not support Absolute path. so example remove one node
    tp = xxx.remove('./nc:edit-config/nc:config/n12:bgp/n12:peer-groups/n12:peer-group[0]/n12:apply-policy/n12:config/n12:import-policy[0]')
    print(tp.xml)

    path_str = 'nc:edit-config/nc:config/n12:bgp/n12:peer-groups/n12:peer-group[0]/n12:apply-policy/n12:config/n12:import-policy[0]={para}'
    path_str = path_str.format(para = 'aaaaa')
    tp  = tp.add(path_str)
    print(tp.xml)

    print('end')

