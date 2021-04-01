"""Generate CDR's for a virtual user scenario:

N persons form a criminal collaborating group.
They have a constant physical relation of M friends with which they make calls.

Missing in the model is a hierarchy

To ensure their privacy the persons hold P phones with a certain number.

During a certain amount of time they will make calls.

"""

import random
import names as nameslib

N = 20
M1 = 2
M2 = 4
REPLACE = 1

names={}
for i in range(0, N):
    names[i]=nameslib.get_full_name()

def make_friends():
    relations = {}
    for personnr in range(0,N):
        friends = []
        nrfriends=random.randint(M1,M2)
        while len(friends)<nrfriends:

            friend = random.randint(0,N-1)
            if friend == personnr:
                continue
            if names[friend] in friends:
                continue
            friends.append(names[friend])
        relations[personnr]=friends

    return relations

givennrs = set()

def generatenr():
    nr = random.randint(3160000000,3169999999)
    if nr in givennrs:
        return generatenr()
    return "%d" % nr

personnrs = {}

def person_nrs():
    for personnr in range(0, N):
        personnrs[personnr] = generatenr()

def update_nrs():
    for personcnt in range(0, REPLACE):
        personnr = random.randint(0,N-1)
        personnrs[personnr] = generatenr()

def generate_call():
    A = random.randint(0, N-1)
    B = random.randint(0, N-1)
    return names[A],names[B],personnrs[A],personnrs[B]

person_nrs()
for i in range(0,1000):
    print (( i ,) + generate_call())
person_nrs()
for i in range(1000,2000):
    print (( i ,) + generate_call())
person_nrs()
for i in range(2000,3000):
    print (( i ,) + generate_call())



# print(make_friends())

