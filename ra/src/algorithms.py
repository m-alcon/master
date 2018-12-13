#!/usr/bin/python3

import numpy as np

# AUXILIAR FUNCTIONS

def sample_one_element(array):
    idx = np.random.randint(len(array))
    return array[idx]

def sample_with_replacement(array,size):
    return np.random.choice(array,size,replace=True)

def merge(left,right):
    i,j,final = 0,0,[]
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            final.append(left[i])
            i += 1
        else:
            final.append(right[j])
            j += 1
    while i < len(left):
        final.append(left[i])
        i += 1
    while j < len(right):
        final.append(right[j])
        j += 1
    return final

# SELECT ALGORITHMS

def qselect(k,array):
    pivot = sample_one_element(array)
    left,right,elements_like_pivot = [],[],0
    for element in array:
        if element < pivot:
            left.append(element)
        elif element > pivot:
            right.append(element)
        else:
            elements_like_pivot += 1
    if k < len(left):
        return qselect(k,left)
    elif k >= len(left)+elements_like_pivot:
        return qselect(k-len(left)-elements_like_pivot,right)
    else:
        return pivot

def rmedian(S):
    n = len(S)
    sample_size = np.power(n,0.75)
    R = quick_sort(sample_with_replacement(S,int(np.ceil(sample_size))))
    d = R[int(np.floor(sample_size/2 - np.sqrt(n)))]
    u = R[int(np.floor(sample_size/2 + np.sqrt(n)))]
    C,Id,Iu = [],0,0
    for x in S:
        if x < d:
            Id += 1
        elif x > u:
            Iu += 1
        else:
            C.append(x)
    if Id > n/2 or Iu > n/2:
        return False
    if len(C) > 4*n:
        return False
    C = quick_sort(C)
    idx = int(np.floor(n/2)) - Id + 1
    return C[idx]

def rmedian_qselect(S):
    n = len(S)
    sample_size = np.power(n,0.75)
    R = quick_sort(sample_with_replacement(S,int(np.ceil(sample_size))))
    d = R[int(np.floor(sample_size/2 - np.sqrt(n)))]
    u = R[int(np.floor(sample_size/2 + np.sqrt(n)))]
    C,Id,Iu = [],0,0
    for x in S:
        if x < d:
            Id += 1
        elif x > u:
            Iu += 1
        else:
            C.append(x)
    if Id > n/2 or Iu > n/2:
        return False
    if len(C) > 4*n:
        return False
    return qselect(int(np.floor(n/2)) - Id + 1,C)

# SORT ALGORITHMS

def quick_sort(array):
    if len(array) <= 1:
        return array
    pivot = sample_one_element(array)
    left,middle,right = [],[],[]
    for element in array:
        if element < pivot:
            left.append(element)
        elif element > pivot:
            right.append(element)
        else:
            middle.append(element)
    return quick_sort(left) + middle + quick_sort(right)

def merge_sort(array):
    if len(array) <= 1:
        return array
    idx = int(len(array)/2)
    return merge(merge_sort(array[:idx]),merge_sort(array[idx:]))
