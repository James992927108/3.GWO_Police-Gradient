# -*- coding:utf-8 -*-

from copy import deepcopy 
# l =[0,1,2,3,4]
# print l
# print '向后移动4格'
# '''
# l1=l
# print id(l1)
# print id(l)
# for i in range(4,9):
#     l[i]=l1[i-4]
# print l
# for i in range(4):
#     l[i]=l1[i+6]
# #print l
# '''
# l1 = [0,1,2,3,4]
# for i in range(1,5):
#     l[i] = l1[i-1]

# print l

# l =[0,1,2,3,4]
# print l
# l1 = [0,1,2,3,4]
# for i in range(1,5):
#     l[i] = l1[i-1]
# print l


l = [0, 1, 2, 3, 4]
print l

l1 = deepcopy(l)
for i in range(1,5):
    l[i] = l1[i-1]
print l
print "******************"