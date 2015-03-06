#!/usr/bin/python2.7
import sys
import re
keywords = ['implies', 'and', 'or', 'not', 'iff']
def checkatomic(list1):
    if list1 == None:
        return True
    if type(list1).__name__ == 'str':
        return True
    key = list1[0]
    if key == 'not' and type(list1[1]).__name__ == 'str':
        return True
    else:
        return False
def hashkey(var):
    if type(var).__name__ == 'list':
        str1 = var[0]+'_'+var[1]
    else:
        str1 = var
    return str1
def opposite(var1, var2):
    if checkatomic(var1) and checkatomic(var2):
        if type(var1).__name__ == 'list' and type(var2).__name__ == 'str':
            if var1[1] == var2:
                return True
            else:
                return False
        elif type(var2).__name__ == 'list' and type(var1).__name__ == 'str':
            if var2[1] == var1:
                return True
            else:
                return False
        else:
            return False
    return False
def unit_removeclause(var, list1, unitlist):
    for element in list1:
        if element in keywords:
            continue
        if checkatomic(element):
            if opposite(element, var):
                list1.remove(element)
                list1.append([])
                continue
        else:
            for sub_ele in element[1:]:
                if sub_ele == var:
                    list1.remove(element)
                elif opposite(sub_ele, var):
                    element.remove(sub_ele)
                    if len(element) == 2:
                        temp = element[1]
                        list1.remove(element)
                        list1.append(temp)
                        if not getopposite(temp) in unitlist:
                            unitlist.append(temp)
                    elif len(element) == 1:
                        element.pop()
                            
def purity_removecaluse(var, list1):
    for ele in list1:
        if ele == var:
            list1.remove(ele)
            continue
        if type(ele).__name__ == 'list':
            for sub_ele in ele:
                if sub_ele == var:
                    list1.remove(ele)
                    break
          
def extract(var):
    if type(var).__name__ == 'str':
        return var
    else:
        return var[1]
def assign(var):
    if type(var).__name__ == 'list':
        temp = var[1]+'='+'false'
    else:
        temp = var +'='+'true'
    return temp
def getopposite(var):
    if type(var).__name__ == 'str':
        list1 = ['not']
        list1.append(var)
        return list1
    else:
        return var[1]
def oppositekey(key):
    if re.match('not.+', key):
        result = re.split('_', key)
        return result[1]
    else:
        return 'not_'+key
def DPLL(list1, assign_list, var_list):
    # empty list
    if len(list1) == 0:
        return True
    key = list1[0]
    if key == 'or' or key == 'not':
        if key == 'or':
            ele = list1[1]
            assign_list.append(assign(ele))
            var_list.remove(extract(ele))
            while len(var_list)!= 0:
                temp = var_list.pop()
                assign_list.append(assign(temp))
            return True
        else:
            assign_list.append(assign(list1))
            var_list.remove(extract(list1))
            return True
    unitlist = []
    puritylist = []
    table = {}
    if len(var_list) == 0:
        for ele in list1:
            if type(ele).__name__ == 'list' and len(ele) == 0:
                return False
        return True
    if len(list1) <= 1:
        while len(var_list)!=0:
            var = var_list.pop()
            assign_list.append(assign(var))
        return True
    # preprocess the list

    for var in list1:
        if var in keywords:
            continue
        if type(var).__name__ == 'list' and len(var) == 0 and key == 'and':
            return False
        if checkatomic(var):
            str1 = hashkey(var)
            if str1 in table:
                table[str1]+=1
            else:
                table[str1] = 1
            if not getopposite(var) in unitlist:
                unitlist.append(var)
        else:
            for ele in var[1:]:
#                 if not ele in unitlist:
#                     unitlist.append(ele)
                str1 = hashkey(ele)
                if str1 in table:
                    table[str1]+=1
                else:
                    table[str1]=1
    for key in table.keys():
        oppo_key= oppositekey(key)
        if not oppo_key in table :
            result = None
            if re.match('not.+', key):
                result = ['not']
                temp = re.split('_', key)[1]
                result.append(temp)
            else:  
                result = key
            if not result in unitlist:
                puritylist.append(result)
#     for temp in unitlist:
#         for temp1 in puritylist:
#             if temp == temp1:
                
    if len(unitlist) !=0:
        while len(unitlist) !=0:
            var = unitlist.pop()
            assign_list.append(assign(var))
            # remove the unit clause from the list
            list1.remove(var)
            unit_removeclause(var, list1, unitlist)
            org_value = extract(var)
            if  org_value in var_list:
                var_list.remove(org_value)
    if len(puritylist) != 0:
        while len(puritylist) != 0:
            var = puritylist.pop()
            assign_list.append(assign(var))
            #remote the purity list from the list
#             list1.remove(var)
            purity_removecaluse(var, list1)
            org_value = extract(var)
            if org_value in var_list:
                var_list.remove(org_value)
    if len(var_list) != 0:
        rand_var = var_list.pop()
        temp_list = list(list1)
        temp_unitlist = list(unitlist)
        unit_removeclause(rand_var, temp_list, temp_unitlist)
        assign_list.append(assign(rand_var))
        if DPLL(temp_list,assign_list, var_list):
            return True
        else:
            assign_list.pop()
            temp_list = list(list1)
            temp_unitlist = list(unitlist)
            rand_var = ['not', rand_var]
            assign_list.append(assign(rand_var))
            unit_removeclause(rand_var, temp_list, temp_unitlist)
            if DPLL(temp_list, assign_list, var_list):
                return True
            else:
                return False
    else:
#         for ele in list1:
#             if type(ele).__name__ == 'list' and len(ele) == 0:
#                 return False
#         return True
        return  DPLL(list1, assign_list, var_list)
            
             
def extract_var(list1, var_list):       
    for ele in list1:
        if ele in keywords:
            continue
#         temp_list = []
        if checkatomic(ele):
            org_value = extract(ele)
            if not org_value in var_list:
                var_list.append(org_value)
        else:
            extract_var(ele, var_list)

if '-i' in sys.argv:
    index = sys.argv.index('-i')+1
f1 = open(sys.argv[index], 'r')
linenum = int(f1.readline())
count=0
while count < linenum:
    count+=1
    line = f1.readline()
    list1 = eval(line)
    resultlist = []
    var_list = []
    extract_var(list1, var_list)
    flag = DPLL(list1, resultlist, var_list)
    if flag:
        final = ['true']
        final+=resultlist
        print final
    else:
        resultlist=['false']
        print resultlist
#     modified_list = trim(temp_list)
#     print temp_list