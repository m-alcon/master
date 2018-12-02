import numpy as np

# AUXILIAR FUNCTIONS

def sample_one_element(array):
    idx = np.random.randint(len(array))
    element = array[idx]
    del array[idx]
    return element, array

def merge(a1,a2):
    if len(a1) < len(a2):
        small = a1
        big = a2
    else:
        small = a2
        big = a1
    i,j,final = 0,0,[]
    while i < len(small):
        if small[i] < big[j]:
            final.append(small[i])
            i += 1
        else:
            final.append(big[j])
            j += 1
    return final + big[j:]

# SELECT ALGORITHMS

def qselect(k,array):
    pivot, array = sample_one_element(array)
    left,right = [],[]
    for element in array:
        if element < pivot:
            left.append(element)
        elif element > pivot:
            right.append(element)
    if k < len(left):
        return qselect(k,left)
    elif k > len(left):
        return qselect(k-len(left)-1,right)
    else:
        return pivot

def rmedian():
    return False

# SORT ALGORITHMS

def quick_sort(array):
    if len(array) <= 1:
        return array
    pivot, array = sample_one_element(array)
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
    array = [1,5,6,3,1,3,6,8,9,2,4,1,2,6,8,9,4,3,2]
    print(merge_sort(array))