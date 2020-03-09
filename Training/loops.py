#Map is a function (not a method) that apply a set of action on a list of elements. It returns a "map" that can be converted in a set, list,...
my_list=[1,2,3,4]

def getSquare(number):
    ret= number*number
    return ret

a=list(map(getSquare, my_list))
print(a)

a=list(map(lambda n:n*n, my_list))
print(a)

#This can be applied to multiple entries
num1 = [4, 5, 6]
num2 = [5, 6, 7]
result = list(map(lambda n1, n2: n1+n2, num1, num2))
print(result)

    

#Map, filter and reduce can do awesome things written quickly
from functools import reduce
numbers = [1,2,3,4,5,6]
odd_numbers=filter(lambda n :n%2==1,numbers)
squared=map(lambda n: n*n,odd_numbers)
total=reduce(lambda sum,n:sum+n,squared)
