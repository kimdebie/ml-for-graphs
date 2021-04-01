"""Generate CDR's for a virtual user scenario:

N persons form a criminal collaborating group.
They have a constant physical relation of M friends with which they make calls.

Missing in the model is a hierarchy

To ensure their privacy the persons hold P phones with a certain number.

During a certain amount of time they will make calls.

"""

import random
import names as nameslib

random.seed(42)

N = 20
M1 = 2
M2 = 4
REPLACE = 2                  # Number of persons that change phone number while shuffeling
NRSHUFFLES = 100             # Total number of calls is NRSHUFFLES*CALLSBETWEENSHUFFLE
CALLSBETWEENSHUFFLE = 30

names={}
for i in range(0, N):
    names[i]=nameslib.get_full_name()

givennrs = set()

def generatenr():
    nr = random.randint(3160000000,3169999999)
    if nr in givennrs:
        return generatenr()
    return "+" + "%d" % nr

personnrs = {}

def person_nrs():
    for personnr in range(0, N):
        personnrs[personnr] = generatenr()

def update_nrs():
    for personcnt in range(0, REPLACE):
        personnr = random.randint(0,N-1)
        personnrs[personnr] = generatenr()

def generate_call_no_phonebook():
    A = random.randint(0, N-1)
    friendoptions = friends[A]
    friendidx = random.randint(0, len(friendoptions)-1)
    B = friendoptions[friendidx]

    return names[A],names[B],personnrs[A],personnrs[B]

def generate_call_with_phonebook():
    A = random.randint(0, N-1)
    friendoptions = friends[A]
    friendidx = random.randint(0, len(friendoptions)-1)
    B = friendoptions[friendidx]
    phonebook = phonebooks[A]
    Bnr = phonebook[B]
    phonebook[B] = personnrs[B]  #After a call to a person the caller will update its phonebook
    return names[A], names[B], personnrs[A], Bnr

generate_call = generate_call_with_phonebook

def make_friends():
    relations = {}
    for personnr in range(0,N):
        friends = []
        nrfriends=random.randint(M1,M2)
        while len(friends)<nrfriends:

            friend = random.randint(0,N-1)
            if friend == personnr:
                continue
            if friend in friends:
                continue
            friends.append(friend)
        relations[personnr]=friends

    return relations

def make_phonebook(relations):
    phonebooks = {}
    for personnr in range(0,N):
        relation = relations[personnr]
        phonebook = {}
        for friend in relation:
            phonebook[friend]=personnrs[friend]
        phonebooks[personnr]=phonebook

    return phonebooks

friends = make_friends()


def get_cdr_data_groups():
    global phonebooks

    records = []

    person_nrs()
    phonebooks = make_phonebook(friends)
    for i in range(0,1000):
        records.append(( i ,) + generate_call())
    person_nrs()
    for i in range(1000,2000):
        records.append(( i ,) + generate_call())
    person_nrs()
    for i in range(2000,3000):
        records.append(( i ,) + generate_call())

    return records

def get_cdr_data_soft():
    global phonebooks

    records = []

    person_nrs()
    phonebooks = make_phonebook(friends)
    cnt = 0
    for shuffels in range (0, NRSHUFFLES):
        for i in range(0, CALLSBETWEENSHUFFLE):
            records.append(( cnt ,) + generate_call())
            cnt = cnt + 1
        update_nrs()

    return records

get_cdr_data = get_cdr_data_soft

if __name__ == '__main__':
    for cdr in get_cdr_data():
        print(cdr)

# print(make_friends())

