from xpath2xml import xpath2xml
ns = {'yang':'urn:ietf:params:xml:ns:yang:ietf-yang-types','nc':'urn:ietf:params:xml:ns:netconf:base:1.0','oc-bgp':'http://openconfig.net/yang/bgp'}
bgp_x = xpath2xml(ns,'nc:rpc')
example_str_1 = 'nc:edit-config/nc:config/' + 'oc-bgp:bgp/oc-bgp:peer-groups/oc-bgp:peer-group[0]/oc-bgp:apply-policy/oc-bgp:config'
example_str_2 = 'nc:edit-config/nc:config/' + 'oc-bgp:bgp/oc-bgp:peer-groups/oc-bgp:peer-group[1]/oc-bgp:apply-policy/oc-bgp:config'

bgp_x.add(example_str_1)
bgp_x.add(example_str_2)
#注意 oc-bgp:default-import-policy','oc-bgp:export-policy[0]','oc-bgp:export-policy[1]','oc-bgp:default-export-policy' 次序先入的node先生成xml 
bgp_x.insert(example_str_1,'oc-bgp:import-policy[0]')
bgp_x.insert(example_str_1,'oc-bgp:import-policy[1]')

bgp_x.inserts(example_str_1,['oc-bgp:default-import-policy','oc-bgp:export-policy[0]','oc-bgp:export-policy[1]','oc-bgp:default-export-policy'])
bgp_x.insert(example_str_2,'oc-bgp:import-policy[0]')
bgp_x.inserts(example_str_2,['oc-bgp:default-import-policy','oc-bgp:export-policy[0]','oc-bgp:default-export-policy'])
print(bgp_x.xml)
tree = bgp_x.tree
ss = tree.dump
print(ss)
