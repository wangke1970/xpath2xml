from xpath2xml import xpath2xml

def test_all():
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
    tp = xxx.insert(insert_point,'n12:aaaa/n12:bbbb=ccc')
    tp = xxx.inserts(insert_point,['n12:aaaa[1]/n12:bbbb=ccc','n12:aaaa[2]/n12:bbbb=ccc'])
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
    # xxx1 oject add 
    xxx1.add("nc:rpc/nc:edit-config/nc:config/n12:bgp/n12:peer-groups/n12:peer-group[0]/n12:apply-policy/n12:config/n12:import-policy[1]=zzz_000")
    print(xxx1.xml)
    
    #show xxx1 object xml
    print(xxx1.xml)
    print('end')

test_all()
