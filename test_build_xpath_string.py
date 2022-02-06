from build_xpath_string import build_xpath_string
# params 1 is yang absolute path ,n12:peer-group[{}] is list,  n12:import-policy[{}] is leaf-list. params 2 is dimension. 
# this is build single leaf-list import-policy in openconfig-yang bgp module 
path_list = build_xpath_string("nc:rpc/nc:edit-config/nc:config/n12:bgp/n12:peer-groups/n12:peer-group[{}]/n12:apply-policy/n12:config/n12:import-policy[{}]=zzz",['2','3'])
for i in path_list:
    print(i)

