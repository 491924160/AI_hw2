#!/usr/bin/python2.7
import sys

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

def addlist(list1, andlist, orlist, newkey):
    if checkatomic(list1):
        if newkey == 'or':
            orlist.append(list1)
        else:
            andlist.append(list1)
        return 
    key = list1[0]
    isFalse = True
    if key != newkey:
        isFalse = True
    else:
        isFalse = False
    if isFalse:
        if newkey == 'or':
            for element in list1[1:]:
                andlist.append(element)
        else:
            for element in list1[1:]:
                orlist.append(element)
    else:
        if newkey == 'or':
            for element in list1[1:]:
                orlist.append(element)
        else:
            for element in list[1:]:
                andlist.append(element)

def or_and_distribution(andlist, orlist, flag):
    list1 = list(andlist)
    resultlist = []
    while len(orlist) != 0:
        temp_list = []
        var = orlist.pop()
        list2 = []
        if flag:
            if checkatomic(var):
                list2.append(var)
            else:
                list2 = var[1:]
        else:
            list2.append(var)
        for tempvalue in list2:
            for element in list1:
                if checkatomic(element):
                    if element != tempvalue:
                        temp =['or']
                        temp.append(element)
                        temp.append(tempvalue)
                        temp_list.append(temp)
                    else:
                        temp_list.append(element)
                else:
                    element.append(tempvalue)
                    temp_list.append(element)
        resultlist += temp_list
    return resultlist

def implieslist(list1, list2):
    temp_list = ['implies']
    temp_list.append(list1)
    temp_list.append(list2)
    return temp_list

def mergelist(total, part):
    if checkatomic(part):
        total.append(part)
        return
    key = part[0]
    org_key = total[0]
    if key == org_key:
        total +=part[1:]
    else:
        total.append(part)    

def notconversion(current_list):
    newlist = []
    key = current_list[0]
    if not key in keywords:
        newlist.append('not')
        newlist.append(key)
        return newlist
    if key == 'not':
        return current_list[1]
    if key == 'and':
        newlist.append('or')
        for temp_list in current_list[1:]:
#             newlist.append(notconversion(temp_list))
            newlist.append(conversion(temp_list, 'not'))
                
        return newlist
    if key == 'or':
        newlist.append('and')
        for temp_list in current_list[1:]:
#             newlist.append(notconversion(temp_list))
            newlist.append(conversion(temp_list, 'not'))
        return newlist
    if key == 'implies':
        newlist2 = conversion(current_list, '')
        return notconversion(newlist2)
    if key == 'iff':
        newlist2 = conversion(current_list, '')
        return notconversion(newlist2)

def conversion(currentlist, key):
    if checkatomic(currentlist):
        if key != '':
            if key != 'not':
                temp_list = []
                temp_list.append(key)
                temp_list.append(currentlist)
                return temp_list
            else:
                return notconversion(currentlist)
        else:
            return currentlist
    resultlist = []
    andlist = []
    orlist = []
    currentkey = currentlist[0]
    newkey = None
    if key == '':
        if currentkey == 'implies':
            newkey = 'or'
            list1 = conversion(currentlist[1], 'not')
            addlist(list1, andlist, orlist, newkey)
            list2 = conversion(currentlist[2], '')
            addlist(list2, andlist, orlist, newkey)
#             if len(andlist) == 0:
            resultlist.append('or')
#                 resultlist.append(list1)
#                 resultlist.append(list2)
            mergelist(resultlist, list1)
            mergelist(resultlist, list2)
            return resultlist
#             else:
#                 resultlist.append('and')
#                 resultlist +=or_and_distribution(andlist, orlist)
#                 return resultlist
        elif currentkey == 'iff':
            newkey = 'and'
            list1 = implieslist(currentlist[1], currentlist[2])
            list2 = implieslist(currentlist[2], currentlist[1])
            list1_result = conversion(list1)
            list2_result = conversion(list2)
            resultlist.append('and')
            mergelist(resultlist, list1_result)
            mergelist(resultlist, list2_result)
            return resultlist
        elif currentkey == 'not':
            list1 = notconversion(currentlist[1])
            list1_result = conversion(list1, '')
            return list1_result
        elif currentkey == 'and':
            resultlist.append('and')
            for temp_value in currentlist[1:]:
                list1 = conversion(temp_value, '')
                mergelist(resultlist, list1)
            return resultlist
        elif currentkey == 'or':
            total_list = []
            for temp_value in currentlist[1:]:
                list1 = conversion(temp_value, '')
                total_list.append(list1)
            for temp1 in total_list:    
                addlist(temp1, andlist,orlist, 'or')
            if len(andlist) == 0:
                resultlist.append('or')
                for temp in orlist:
                    mergelist(resultlist, temp)
                return resultlist
            elif len(orlist) != 0:
                resultlist.append('and')
                resultlist +=or_and_distribution(andlist, orlist, True)
                return resultlist
            else:
                del andlist[:]
                del orlist[:]
                orlist.append(total_list.pop(0))
                for temp1 in total_list:
                    addlist(temp1, andlist, orlist, 'or')
                resultlist.append('and')
                resultlist +=or_and_distribution(andlist, orlist, False)
                return conversion(resultlist, '')
    else:
        temp_list = ['not']
        temp_list.append(currentlist)
        return conversion(temp_list, '')
if '-i' in sys.argv:
    index = sys.argv.index('-i')+1
f1 = open(sys.argv[index], 'r')
linenum = int(f1.readline())
count=0
while count < linenum:
    count+=1
    line = f1.readline()
    list1 = eval(line)
    temp_list = conversion(list1, '')
#     modified_list = trim(temp_list)
    print temp_list

