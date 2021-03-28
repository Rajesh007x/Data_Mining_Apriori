#!/usr/bin/env python
# coding: utf-8

# In[87]:


import sys
import time
import numpy as np
import pandas as pd

print("Welcome to the simulation of the apriori algorithms. \n Please choose the dataSet you want: \n 1. Test \n 2. GroceryStore \n 3. Cars List \n 4. Games \n 5. Costco \n 6. Nike")
while True:
    choice_of_data=input()
    if(choice_of_data=='1'):
        dataList=pd.read_csv('test.csv')
        print('User chose Test dataset')
        break
    elif(choice_of_data=='2'):
        dataList=pd.read_csv('GroceryStoreDataSet.csv')
        print('User chose GroceryStore dataset')
        break
    elif(choice_of_data=='3'):
        dataList=pd.read_csv('Cars_List.csv')
        print('User chose Cars List dataset')
        break
    elif(choice_of_data=='4'):
        dataList=pd.read_csv('Games_Transaction_List.csv')
        print('User chose Games dataset')
        break
    elif(choice_of_data=='5'):
        dataList=pd.read_csv('Costco.csv')
        print('User chose Costco dataset')
        break
    elif(choice_of_data=='6'):
        dataList=pd.read_csv('Nike.csv')
        print('User chose Nike dataset')
        break
    else:
        print("Invalid data, please enter the number corresponding to the data")
        break     
    

#Games_List = pd.read_csv('GroceryStoreDataSet.csv')
#Test_List = pd.read_csv('Games_Transaction_List.csv')


# In[78]:


print("Enter the Minimum Support (in percentage) : ", end=" ")
minsupport = input()
print("Enter the Minimum Confidence (in percentage) : ", end=" ")
minconfidence = input()
min_support = float(minsupport)/100
min_conf = float(minconfidence)/100
print('\n')
print("The minimum support is :", minsupport)
print("The minimum confidence is :",minconfidence)


# In[79]:


def load_transactions(dataList):
    Transactions = []
    df_items = dataList['TransactionList']
    comma_splitted_df = df_items.apply(lambda x: x.split(','))
    for i in comma_splitted_df:
        Transactions.append(i)
    return Transactions
load_transactions(dataList)

Transactions = load_transactions(dataList)
Transactions


# In[80]:


class Rule:

    def __init__(self, left, right, all):
        self.left = list(left)
        self.left.sort()
        self.right = list(right)
        self.right.sort()
        self.all = all

    def __str__(self):
        return ",".join(self.left)+" ==> "+",".join(self.right)

    def __hash__(self):
        return hash(str(self))


# In[81]:


def scan(Transactions, Ck):
    count = {s: 0 for s in Ck}
    n = len(Transactions)
    for t in Transactions:
        for fset in Ck:
            if fset.issubset(t):
                count[fset] += 1
    
    return {fset: support/n for fset, support in count.items() if support/n>=min_support}


# In[82]:


def calculateCandidate(Lk):
    res = []
    print("len Lk", len(Lk))
    for i in range(len(Lk)):
        for j in range(i+1, len(Lk)):
            it1 = Lk[i]
            it2 = Lk[j]
            it11 = list(it1)
            it22 = list(it2)
            it11.sort()
            it22.sort()
            print("it11",it11)
            print("it22",it22)
            if it11[:len(it1)-1] == it22[:len(it1)-1]:
                res.append(it1 | it2)
                print("Res: ", res)
    return res


# In[83]:


def calculate_frequency_support():
    support = {}
    candidate = [[]]
    Lk = [[]]
    C1 = set()
    for t in Transactions:
        for item in t:
            C1.add(frozenset([item]))
            #print(C1)
            #print("*****")
    #print("-----------------------------------------------")
    #print("C1: ", C1)
    candidate.append(C1)
    #print(candidate)
    #print("-----------------------------------------------")
    #print("Transactions: ",Transactions)
    count = scan(Transactions, C1)
    #print("-----------------------------------------------")
    #print("Count: ", count)
    Lk.append(list(count.keys()))
    #print("-----------------------------------------------")
    #print("Lk: ", Lk)
    support.update(count)
    print("-----------------------------------------------")
    print("support: ", support)
    print("-----------------------------------------------")
    print("candidate: ",candidate)
    k = 1
    while len(Lk[k]) > 0:
        print("+++++++++++++++++++++++++++++++++++++++++++")
        print("k=", k)
        print("Lk[k]: ", Lk[k])
        candidate.append(calculateCandidate(Lk[k]))
        print("candidate: ", candidate)
        print("candidate[k+1]: ",candidate[k+1])
        count = scan(Transactions, candidate[k+1])
        support.update(count)
        Lk.append(list(count.keys()))
        k += 1
    return Lk, support


# In[84]:


def EvaluateSecondaryRules(fs, rights, fresult, support):
    rlength = len(rights[0])
    totlength = len(fs)
    if totlength-rlength > 0:
        rights = calculateCandidate(rights)
        new_right = []
        for right in rights:
            left = fs - right
            if len(left) == 0:
                continue
            confidence = support[fs] / support[left]
            if confidence >= min_conf:
                fresult.append([Rule(left, right, fs), support[fs],  confidence])
                new_right.append(right)

        if len(new_right) > 1:
            EvaluateSecondaryRules(fs, new_right, fresult, support)


# In[85]:


def EvaluateAssociationRules(frequent, support):
    fresult = []
    for i in range(2, len(frequent)):
        if len(frequent[i]) == 0:
            break
        freq_sets = frequent[i]

        for fs in freq_sets:
            for right in [frozenset([x]) for x in fs]:
                left = fs-right
                confidence = support[fs] / support[left]
                if confidence >= min_conf:
                    fresult.append([Rule(left, right, fs), support[fs], confidence])

        if len(freq_sets[0]) != 2:

            for fs in freq_sets:
                right = [frozenset([x]) for x in fs]
                EvaluateSecondaryRules(fs, right, fresult, support)

    fresult.sort(key=lambda x: str(x[0]))
    return fresult


# In[86]:


if __name__ == '__main__':

    start_time = time.time()
    freq, supp = calculate_frequency_support()
    print("Frequency: ",freq)
    print("Support: ", supp)
    fresult = EvaluateAssociationRules(freq, supp)
    end_time = time.time()
    
    print("\n----- > Association With Support and Confidence: < -------\n")
    for x in fresult:
        print("Rule: ",x[0])
        print("Support: ", x[1])
        print("Confidence: ", x[2])
        print("\n")
        
    print("--------------------------- RUNNING TIME:-----------------------------------")
    print("The Runtime of the program is: " + str(end_time - start_time) + "seconds")
    
    print("---------------------------------------------------------------------------\n")

