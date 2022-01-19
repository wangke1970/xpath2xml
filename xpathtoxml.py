# -*- coding: utf-8 -*-
# change https://stackoverflow.com/questions/5661968/how-to-populate-xml-file-using-xpath-in-python
__author__ = 'Wang Ke'
from xml.etree import ElementTree as ET
import re
from itertools import chain
class xpath2xml:
    def __init__(self,ns,root=None,root_name='nc:rpc'):
        for k,v in ns.items():
            if v=='urn:ietf:params:xml:ns:netconf:base:1.0':
                ET.register_namespace('',v)
                ET.register_namespace('nc',v)
            else:
                ET.register_namespace(k,v)    
        self.root = ET.Element(root_name)
        self.parent = None
        self.xml = None
    
    def __call__(self,path,ns):
        self._build(self.root,path,ns)
        self.xml = ET.tostring(self.root,xml_declaration=True,encoding = 'utf-8')
        self.xml = str(self.xml,encoding = "utf-8")
        return self
    
    def _build(self,node,path,ns):
        components = path.split("/")
        if components[0] == node.tag:
            components.pop(0)
        node.attrib = ns
        while components:
            value_end = None
            attrib_value = None
            if "[" in components[0]:
                component, trail = components[0].replace(' ','').split("[",1)
                pred = trail.split("=")[0].strip("]")
                if pred.isdigit():
                    target_index = int(pred)
                    try:
                        assert(int(pred) >= 0)
                    except AssertionError as asser:
                        print('[n] n must >= 0')
                        return
                    if "=" in trail:
                        value_end = trail.replace(' ','').split("=")[-1].strip("]")
                else:
                    attrib_list = trail.replace(' ','').strip("]").strip("@").split("=",1)
                    attrib_value = {attrib_list[0]:attrib_list[1]}
                    target_index = 0
            elif "=" in components[0]:
                component, value_end = components[0].replace(' ','').split("=",1)
                target_index = 0
            else:
                component = components[0].replace(' ','')
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
                    else:
                        new_node = ET.Element(component)
                        if attrib_value :
                            new_node.attrib = attrib_value                    
                    node.append(new_node)
                node = new_node
    
    def remove(self,path,ns):
        data = ET.tostring(self.root,xml_declaration=True,encoding = 'utf-8')
        data_root = ET.fromstring(str(data,encoding = "utf-8"))
        path = re.sub('(?P<num>\[[0-9]+\])',self._num_matched,path)        
        xml_node = data_root.find(path,ns)
        if xml_node!=None:
            self._node_find(data_root,xml_node)
        else:
            return
        if self.parent:
            self.parent.remove(xml_node)
        return str(ET.tostring(data_root,xml_declaration=True,encoding = 'utf-8'),encoding = "utf-8")        

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
    
def change_ns(ns):
    ns_ns = {}
    for k,v in ns.items():
        if v == 'urn:ietf:params:xml:ns:netconf:base:1.0':
            ns_ns['xmlns'] = v
            ns_ns['xmlns:nc'] = v
        else:
            ns_ns['xmlns:'+k] = v
    return ns_ns    

def bulid(path_list,ns,root_name='nc:rpc'):
    if isinstance(ns,dict):
        ns_ns = change_ns(ns)  
    # ns_ns = {'xmlns:'+k:v for k,v in ns.items() if v!='urn:ietf:params:xml:ns:netconf:base:1.0'}
    obj = xpath2xml(ns,root_name=root_name)
    for i in path_list:
        ret = obj(i,ns_ns)
    return ret

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
    #Example

    ns = {'nc': 'urn:ietf:params:xml:ns:netconf:base:1.0', 'n1': 'http://openconfig.net/yang/bgp-policy', 'n2': 'http://openconfig.net/yang/types/inet', 'n3': 'http://openconfig.net/yang/bgp-types', 'n4': 'http://openconfig.net/yang/policy-types', 'n5': 'http://openconfig.net/yang/openconfig-types', 'n6': 'http://openconfig.net/yang/types/yang', 'n7': 'urn:ietf:params:xml:ns:yang:ietf-inet-types', 'n8': 'urn:ietf:params:xml:ns:yang:ietf-yang-types', 'n9': 'urn:ietf:params:xml:ns:yang:ietf-interfaces', 'n10': 'http://openconfig.net/yang/interfaces', 'n11': 'http://openconfig.net/yang/openconfig-ext', 'n12': 'http://openconfig.net/yang/bgp', 'n13': 'http://openconfig.net/yang/routing-policy'}

#    path_list = ["nc:rpc/nc:edit-config/nc:config/n12:bgp/n12:peer-groups/n12:peer-group[3]/n12:apply-policy/n12:config/n12:import-policy[2]=zzz1",
#                 "nc:rpc/nc:edit-config/nc:config/n12:bgp/n12:peer-groups/n12:peer-group[0]/n12:apply-policy/n12:config/n12:import-policy[0]=zzz",
#                 "nc:rpc/nc:edit-config/nc:config/n12:bgp/n12:peer-groups/n12:peer-group[0]/n12:apply-policy/n12:config[@nc:operation=merge]",
#                 "nc:rpc/nc:edit-config/nc:config/n12:bgp/n12:peer-groups/n12:peer-group[0]/n12:apply-policy/n12:config/n12:import-policy[1]=zzz",]
    
    # params 1 is yang absolute path ,n12:peer-group[{}] is list,  n12:import-policy[{}] is leaf-list. params 2 is dimension. 
    # this is build single leaf-list import-policy in openconfig-yang bgp module 
    path_list = build_xpath_string("nc:rpc/nc:edit-config/nc:config/n12:bgp/n12:peer-groups/n12:peer-group[{}]/n12:apply-policy/n12:config/n12:import-policy[{}]=zzz",['2','3'])
    xxx = bulid(path_list,ns,root_name ='nc:rpc')
    print(xxx.xml)
    # current xml path is nc:rpc ,nc:rpc is root. example remove one node
    tp = xxx.remove('./nc:edit-config/nc:config/n12:bgp/n12:peer-groups/n12:peer-group[0]/n12:apply-policy/n12:config/n12:import-policy[0]',ns)

    print(tp)

    print('end')

