#!/usr/bin/python3

import numpy as np

# AUXILIAR FUNCTIONS

def sample_one_element(array):
    idx = np.random.randint(len(array))
    return array[idx]

def merge(left,right):
    i,j,final = 0,0,[]
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            final.append(left[i])
            i += 1
        else:
            final.append(right[j])
            j += 1
    return final + left[i:] + right[j:]

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
    #print(k,left,elements_like_pivot,'x',pivot,right)
    if k < len(left):
        return qselect(k,left)
    elif k >= len(left)+elements_like_pivot:
        return qselect(k-len(left)-elements_like_pivot,right)
    else:
        return pivot

def rmedian():
    return False

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

if __name__ == '__main__':
    size = 5000
    idx = np.random.randint(size)
    print(idx)
    array = np.random.randint(100,size=size)
    selected = qselect(idx,array)
    print('qselect: %d'%selected)
    sorted_array = merge_sort(array) 
    print('real: %d'%sorted_array[idx])
    print(len(sorted_array),len(array))
