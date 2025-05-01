## Template Code
```python
import sys

sys.stdin = open('sample_input.txt')
readline = sys.stdin.readline

if __name__ == '__main__':

    test_case_total_count = int(readline())

    for test_case in range(test_case_total_count):
        answer = int(input())

        # TODO: Implementation

        print(f'#{test_case + 1} {answer}')

```

---
## Print without space delimiter and new line (String Literal)
```python
print('''Hello
My
Wolrd~''', end='', sep='')
```
---
## How to print number with commas as thousands separators?
<details>
  <summary>Details</summary>
  <p>
    
```python
value_info = {
  "Seoul": [10312545, 91375],
  "Pusan": [3567910, 5868],
  "Incheon": [2758296, 64888],
  "Daegu": [2511676, 17230],
  "Gwangju": [1454636, 29774],
}

for key in value_info:
    print(f"{key.rjust(15)}"
          f"{f'{value_info[key][0]:,d}'.rjust(15)}"
          f"{(('+' if value_info[key][1] >= 0 else '-') + f'{value_info[key][1]:,.0f}').rjust(15)}"
          , sep="")
```
  </p>
</details>

---
## String Format -- %10d, %10.4f, %10s (Python)
<details>
  <summary>Details</summary>
  <p>

```python
# 1. %-formatting
weight = 79.12
print("%-10.4f" % weight)

# 2. format function
print(format(weight, "-10.4f"))

# 3. String 
hash_value = "1234567890"
print("%13s" % hash_value)
# print(format(hash_value, "%13s"))   # ValueError: Invalid format specifier
print(hash_value.rjust(13))

```
  </p>
</details>

---
## F String Format (Python)
<details>
  <summary>Details</summary>
  <p>
    
```python
# 1. %-formatting
arr=[1,2,3]
print("%s %s %s" % (arr[0], arr[1], arr[2]))

truple=(1,2,3)
print("%s %s %s" % truple)


# 2. str.format()
name = "rolroralra"
age = 20
print("Hello, {}. I am {}.".format(name, age))
print("Hello, {1}. You are {0}.".format(age, name))

person = {'name': 'Eric', 'age': 74}
print("Hello, {name}. You are {age}.".format(name=person['name'], age=person['age']))

# You can also use ** to do this neat trick with dictionaries
print("Hello, {name}. You are {age}.".format(**person))


# 3. f string
print(f"Hello, {name}. You are {age}.")
```
  </p>
</details>

---
## Python Operator
[https://docs.python.org/ko/3.7/library/operator.html](https://docs.python.org/ko/3.7/library/operator.html)

#### Ternary Operator (3항 연산자)
<details>
  <summary>Details</summary>
  <p>
    
```python
a = 10
b = 10

# Old Version Ternary Operation (A and B or C)
print(a == b and "TRUE" or "FALSE")
# OUTPUT: TRUE
print(a == b and a - b or a + b)    # This old version ternary operator has this problem
# OUTPUT: 20

# New Ternary Operation in python 2.5
print("TRUE" if a == b else "FALSE")
# OUTPUT: TRUE
print(a - b if a == b else a + b)
# OUTPUT: 0
```
  </p>
</details>


---
## Set
<details>
  <summary>Details</summary>
  <p>
    
```python
set1 = {1,2,3}
set2 = {3,4,5}
print(set1 & set2)
#print(set1.intersection(set2))
print(set1 | set2)
#print(set1.union(set2))
print(set1 - set2)
#print(set1.difference(set2))
print(set1 ^ set2)
#print(set1.symmetric_difference(set2))
```
  </p>
</details>

---
## Python List Comprehension
```python
a = [2, 6, 7, 8, 9]
list_even = list()
for num in a:
    if num % 2 ==0:
        list_even.append(num)
#       list_even += [num]
#       list_even.extend([num])
print(list_even)

# List Comprehension
print([num for num in a if num % 2 == 0])
```

---
## Difference between == and is
[https://www.tutorialspoint.com/difference-between-and-is-operator-in-python](https://www.tutorialspoint.com/difference-between-and-is-operator-in-python)

<details>
  <summary>Details</summary>
  <p>
    
```python
# Python program to  
# illustrate the  
# difference between 
# == and is operator 
# [] is an empty list 
list1 = [] 
list2 = [] 
list3=list1 
  
if (list1 == list2): 
   print("True") 
else: 
   print("False") 
# True

  
if (list1 is list2): 
   print("True") 
else: 
   print("False") 
# False


if (list1 is list3): 
   print("True") 
else:     
   print("False")
# True
```

  </p>
</details>

---
## Python Comprehension (TODO)
[https://mingrammer.com/introduce-comprehension-of-python/](https://mingrammer.com/introduce-comprehension-of-python/)

---
## Python Lambda (TODO)
- [https://wikidocs.net/64](https://wikidocs.net/64)
- [https://www.geeksforgeeks.org/functools-module-in-python/](https://www.geeksforgeeks.org/functools-module-in-python/)

<details>
  <summary>Details</summary>
  <p>
    
```python
import functools
```
  </p>
</details>
