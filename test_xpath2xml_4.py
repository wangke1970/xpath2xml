from xpath2xml import xpath2xml

ns = {'yang': 'urn:ietf:params:xml:ns:yang:ietf-yang-types', 'nc': 'urn:ietf:params:xml:ns:netconf:base:1.0', 'n1': 'http://openconfig.net/yang/bgp-policy', 'n2': 'http://openconfig.net/yang/types/inet',
 'n3': 'http://openconfig.net/yang/bgp-types', 'n4': 'http://openconfig.net/yang/policy-types', 'n5': 'http://openconfig.net/yang/openconfig-types', 'n6': 'http://openconfig.net/yang/types/yang', 'n7': '
urn:ietf:params:xml:ns:yang:ietf-inet-types','n9': 'urn:ietf:params:xml:ns:yang:ietf-interfaces', 'n10': 'http://openconfig.net/yang/interfaces', 'n11': 'http://openconfig.net/yang/openconfig-ext', 'n12'
: 'http://openconfig.net/yang/bgp', 'n13': 'http://openconfig.net/yang/routing-policy'}
xxx = xpath2xml(ns)
xxx.add("nc:edit-config/nc:config/n12:bgp/n12:peer-groups/n12:peer-group[0]/n12:apply-policy/n12:config/n12:import-policy[0]='zzz_000_000'")
xxx.add("nc:edit-config/nc:config/n12:bgp/n12:peer-groups/n12:peer-group[0]/n12:apply-policy/n12:config/n12:import-policy[1]='zzz_000_111'")
xxx.add("nc:edit-config/nc:config/n12:bgp/n12:peer-groups/n12:peer-group[0]/n12:apply-policy/n12:config/n12:import-policy[2]='zzz_000_222'")
xxx.add("nc:edit-config/nc:config/n12:bgp/n12:peer-groups/n12:peer-group[1]/n12:apply-policy/n12:config/n12:import-policy[0]='zzz_111_000'")
xxx.add("nc:edit-config/nc:config/n12:bgp/n12:peer-groups/n12:peer-group[1]/n12:apply-policy/n12:config/n12:import-policy[1]='zzz_111_111'")
print(xxx.xml)
