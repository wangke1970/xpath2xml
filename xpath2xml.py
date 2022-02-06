#!/usr/bin/env python3
# change https://stackoverflow.com/questions/5661968/how-to-populate-xml-file-using-xpath-in-python
__author__ = 'Wang Ke'
# └┕┖┗ ┘┙┚┛╘╙ 
from xml.etree import ElementTree as ET
import re
from itertools import chain
class xpath2xml:
    def __init__(self,ns,root_name='nc:rpc'):
        for k,v in ns.items():
            ET.register_namespace(k,v)    
        self.root = ET.Element(root_name)
        self.root_tree = TreeNode(root_name)
        self.root_tree.data = self.root
        self.ns = ns
        self.parent = None
    
    @property
    def xml(self):
        xml_str = ET.tostring(self.root,xml_declaration=True,encoding='utf-8')
        xml_str = str(xml_str,encoding="utf-8")
        return xml_str
    
    # add path string    
    def add(self, path):
        self._build(self.root,path)
        return self

    def append(self,insert_path_point,path):
        insert_path_point = re.sub('(?P<num>\[[0-9]+\])',self._num_matched,insert_path_point)
        node = self.root.find(insert_path_point,self.ns)
        self._build(node,path)
        return self
    
    def extend(self,insert_path_point,paths):
        insert_path_point = re.sub('(?P<num>\[[0-9]+\])',self._num_matched,insert_path_point)
        node = self.root.find(insert_path_point,self.ns)
        for i in paths:
            self._build(node,i)
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
            components[0] = re.sub('(?P<ns>[_A-Za-z][._\-A-Za-z0-9]*:)',self._ns_matched,components[0])
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
                self.point = node
    
    def _tree(self,node_tree,node_xml):
        def chang_ns(name):
            ns = {v:k for k,v in self.ns.items()}
            name = ns[name.lstrip('{').split('}')[0]]+':'+name.lstrip('{').split('}')[1]
            return name
        for i in node_xml:
            ret = node_tree.add_child(chang_ns(i.tag),i)
            self._tree(ret,i)
    
    @property
    def tree(self):    
        self._tree(self.root_tree,self.root)
        self.root_tree.index_node()
        return self.root_tree
        
    def find(self,path):
        path = re.sub('(?P<num>\[[0-9]+\])',self._num_matched,path)
        xml_node = self.root.find(path,self.ns)
        return xml_node
    
    def findall(self,path):
        path = re.sub('(?P<num>\[[0-9]+\])',self._num_matched,path)
        xml_node_list = self.root.findall(path,self.ns)
        return xml_node_list
    
    def remove(self,path):
        path = re.sub('(?P<num>\[[0-9]+\])',self._num_matched,path)        
        xml_node = self.root.find(path,self.ns)
        if xml_node!=None:
            self._node_find(self.root,xml_node)
        else:
            return 
        if self.parent:
            self.parent.remove(xml_node)
        return self        

    def _num_matched(self,matched):
        index_str = matched.group('num')
        index = index_str.replace('[','').replace(']','')
        index=int(index)+1
        index_str = '['+str(index)+']'
        return index_str
    
    def _ns_matched(self,matched):
        node_str = matched.group('ns')
        try:
            node_str = '{'+self.ns[node_str[:-1]]+'}'
        except Exception as e:
            print('Error Lose namespaces check and add it !',e)
        return node_str    
    
    def _node_find(self,node,sub_node):
        for i in node:
            if i == sub_node:
                self.parent=node
                break
            else:
                self._node_find(i,sub_node)
    
class TreeNode(object):
    def __init__(self, name, parent=None):
        super(TreeNode, self).__init__()
        self.name = name
        self.parent = parent
        self.child = []
        self.data = None

    def __repr__(self) :
        return 'TreeNode(%s)' % self.name

    def __contains__(self, item):
        return item in self.child

    def __len__(self):
        """return number of children node"""
        return len(self.child)

    def __bool__(self):
        """always return True for exist node"""
        return True

    @property
    def path(self):
        # return path string (from root to current node) recursion
        if self.parent:
            ret = '%s/%s' % (self.parent.path.strip(), self.name)
            return ret
        else:
            return self.name

    def get_child(self, name):
        # get a child node of current node
        for i in self.child:
            if i[0] == name:
                return i[1]        

    def add_child(self, name, data):
        obj = TreeNode(name)
        obj.data = data
        obj.parent = self
        self.child.append([name,obj])
        return obj

    def del_child(self, name):
        #remove a child node from current node include xml node
        ll = []
        for i in self.child:
            if i[0] == name:
                sub_xml_node = i[1].data
            else:    
                ll.append(i)
        self.child = ll
        #self.child = [i for i in self.child if i[0]!=name]
        self.data.remove(sub_xml_node)
        
    def find_child(self, path):
        # find child node by ['a','b','c'] or 'a/b/c', return None if not found"""
        path = path if isinstance(path, list) else path.split('/')
        cur = self
        for sub in path:
            # search
            obj = cur.get_child(sub)
            # check if search done
            if obj is None:
                break
            cur = obj
        return obj

    def _dump(self,ss,indent):
        # tree to string
        # ╚ ∟ ┗ └
        tab = '    '*(indent-1) + ' ├ ' if indent > 0 else ''
        if self.data.text:
            ret = '%s%s%s%s' % (tab, str(self.name) + ':',self.data.text,'\n')
            ss[0] += ret
        else:    
            ret = '%s%s%s' % (tab, str(self.name),'\n')
            ss[0] += ret
        for i in self.child:
            i[1]._dump(ss,indent+1)
    
    @property 
    def dump(self):
        dump_dict = {0:''}
        indent=0
        self._dump(dump_dict,indent)
        return dump_dict[0]
    
    def index_node(self):
        if self.child == []:
            return
        d = {}
        for i in self.child:
            d[i[0]] = [ii[0] for ii in enumerate(self.child) if ii[1][0]==i[0]]
        for k,v in d.items():
            num=0
            for i in self.child:
                if i[0]==k and len(v)>1:
                    i[0]=i[0]+'['+str(num)+']'
                    i[1].name = i[0]
                    num+=1        
        for i in self.child:
            i[1].index_node()
    
    @property            
    def get_xml_node(self):
        return {'tag':self.data.tag,'attrib':self.data.attrib,'value':self.data.text}
    
    def set_xml_tag(self, tag):
        self.data.tag = tag
        return self
    
    def set_xml_attrib(self, attrib):
        if isinstance(attrib,dcit):
            self.data.attrib = attrib
        else:
            print('Error attrib must dict !')
        return self    
    
    def set_xml_text(self, text):
        self.data.text = text
        return self
    
    def get_parent(self):
        if isinstance(self.parent.name,str):
            return self.parent

            
if __name__  == "__main__":
    #Example add leaf-list out xml string
    ns = {'yang': 'urn:ietf:params:xml:ns:yang:ietf-yang-types', 'nc': 'urn:ietf:params:xml:ns:netconf:base:1.0', 'n1': 'http://openconfig.net/yang/bgp-policy', 'n2': 'http://openconfig.net/yang/types/inet', 'n3': 'http://openconfig.net/yang/bgp-types', 'n4': 'http://openconfig.net/yang/policy-types', 'n5': 'http://openconfig.net/yang/openconfig-types', 'n6': 'http://openconfig.net/yang/types/yang', 'n7': 'urn:ietf:params:xml:ns:yang:ietf-inet-types','n9': 'urn:ietf:params:xml:ns:yang:ietf-interfaces', 'n10': 'http://openconfig.net/yang/interfaces', 'n11': 'http://openconfig.net/yang/openconfig-ext', 'n12': 'http://openconfig.net/yang/bgp', 'n13': 'http://openconfig.net/yang/routing-policy'}
    # init object and xml root nc:rpc
    xxx = xpath2xml(ns,'nc:rpc')
    xxx1 = xpath2xml(ns,'data')
    
    path_list = ["nc:edit-config/nc:config/n12:bgp/n12:peer-groups/n12:peer-group[2]/n12:apply-policy/n12:config/n12:import-policy[@nc:operation=create @yang:insert=after]=z",
                 "nc:edit-config/nc:config/n12:bgp/n12:peer-groups/n12:peer-group[3]/n12:apply-policy/n12:config/n12:import-policy[2]=zzzzz",
                 "nc:edit-config/nc:config/n12:bgp/n12:peer-groups/n12:peer-group[1]/n12:apply-policy/n12:config/n12:import-policy[0]=zz",
                 "nc:edit-config/nc:config/n12:bgp/n12:peer-groups/n12:peer-group[1]/n12:apply-policy/n12:config/n12:import-policy[1]=zzz",
                 "nc:edit-config/nc:config/n12:bgp/n12:peer-groups/n12:peer-group[0]/n12:apply-policy/n12:config/n12:import-policy[1]=zzz_000"
                ]
    
        
    # add multi paths
    for i in path_list:
        xxx = xxx.add(i)
    # add single path
    xxx = xxx.add("nc:edit-config/nc:config/n12:bgp/n12:peer-groups/n12:peer-group[0]/n12:apply-policy/n12:config/n12:import-policy[2]=zzz_111")
    # update zzz_111 to zzz_222
    xxx = xxx.add("nc:edit-config/nc:config/n12:bgp/n12:peer-groups/n12:peer-group[0]/n12:apply-policy/n12:config/n12:import-policy[2]=zzz_222")
    
    print(xxx.xml)
    # nc:rpc is root. xml.etree xpath not support Absolute path.
    tp = xxx.remove('./nc:edit-config/nc:config/n12:bgp/n12:peer-groups/n12:peer-group[0]/n12:apply-policy/n12:config/n12:import-policy[0]')
#    tp = xxx.remove('nc:edit-config/nc:config/n12:bgp/n12:peer-groups/n12:peer-group[0]/n12:apply-policy/n12:config/n12:import-policy[0]')

    print(tp.xml)

    path_str = 'nc:edit-config/nc:config/n12:bgp/n12:peer-groups/n12:peer-group[0]/n12:apply-policy/n12:config/n12:import-policy[0]={para}'
    path_str = path_str.format(para = 'aaaaa')
    tp  = tp.add(path_str)
    
    insert_point = "./nc:edit-config/nc:config/n12:bgp/n12:peer-groups/n12:peer-group[0]/n12:apply-policy/n12:config"
    tp = xxx.append(insert_point,'n12:aaaa/n12:bbbb=ccc')
    tp = xxx.extend(insert_point,['n12:aaaa[1]/n12:bbbb=ccc','n12:aaaa[2]/n12:bbbb=ccc'])
    print(tp.xml)
    # tree xml object
    tree = xxx.tree
    # find xml node by tree 
    tp_1 = tree.find_child('nc:edit-config/nc:config/n12:bgp/n12:peer-groups/n12:peer-group[0]')
    tp_2 = tree.find_child(['nc:edit-config','nc:config','n12:bgp','n12:peer-groups','n12:peer-group[0]'])
    
    # get nc:edit-config/nc:config/n12:bgp/n12:peer-groups/n12:peer-group[0] xml node retun a dict
    # return is  {'tag': '{http://openconfig.net/yang/bgp}peer-group', 'attrib': {}, 'value': None}
    # {http://openconfig.net/yang/bgp}peer-group is n12:peer-group
    xml_node_detail = tp_2.get_xml_node
    print(xml_node_detail)
    
    # set xml value
    tp_2 = tp_2.set_xml_text('aaaa')
    # del 'n12:apply-policy' in tree and del xml
    tp_2.del_child('n12:apply-policy')
    
    # show tree
    ss = tree.dump
    print(ss)
    
    # show tp_2 node path
    print(tp_2.path)
    xxx1.add("nc:rpc/nc:edit-config/nc:config/n12:bgp/n12:peer-groups/n12:peer-group[0]/n12:apply-policy/n12:config/n12:import-policy[1]=zzz_000")
    print(xxx1.xml)
    
    #show xxx1 object xml
    print(xxx1.xml)
    print('end')

