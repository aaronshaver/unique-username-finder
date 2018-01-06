import requests
import random
import sys

# ******************************************************************************
# This is ugly code, just hacked together for a quick solution. No unit tests
# or anything nice like that.
# ******************************************************************************

if len(sys.argv) < 2:
    print('put number of users you want to try for as a commandline arg')
    sys.exit()

num_usernames_to_make = int(sys.argv[1])

with open('colors.txt') as f:
    colors = f.readlines()

with open('animals.txt') as f:
    animals = f.readlines()

def get_username():
    for _ in range(20):
        color = random.choice(colors)
        animal = random.choice(animals)
        username = color.title() + animal.title()
        username = ''.join(c for c in username if c.isalnum())  # strip special
        if len(username) <= 15:
            return username

usernames = []
for _ in range(num_usernames_to_make):
    username = get_username()
    usernames.append(username)

def is_username_unique(username):
    url = 'https://www.google.com/search?q={}&tbs=li:1'.format(username)
    result  = requests.get(url)
    return 'did not match any documents' in result.text

num_users = len(usernames)
print('\nChecking [ {} ] usernames\n'.format(num_users))

usernames_final = []
count = 0
for username in usernames:
    if is_username_unique(username):
        usernames_final.append(username)
    count += 1
    if count % 100 == 0:
        print('Checked {} usernames'.format(count))

usernames_sorted = sorted(usernames_final, key=len)  # shortest first
print("\nFound {} unique and short usernames\n".format(len(usernames_sorted)))

with open('results.txt', 'w') as f:
    for username in usernames_sorted:
        f.write(username + '\n')
