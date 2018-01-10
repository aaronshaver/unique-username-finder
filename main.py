from datetime import datetime
import requests
import random
import sys
import time

# ******************************************************************************
# This is ugly code, just hacked together for a quick solution. No unit tests
# or anything nice like that.
# ******************************************************************************

start_time = datetime.now()

MAX_LENGTH = 15
DELAY = 0.05
MAX_USERNAMES = 800

if len(sys.argv) < 2:
    print('put number of users you want to try for as a commandline arg')
    sys.exit()

num_usernames_to_make = int(sys.argv[1])
if num_usernames_to_make > MAX_USERNAMES:
    print('Google gets mad if you do too many queries. If you still  want to do this, edit the .py file and run again.')
    sys.exit()

with open('colors.txt') as f:
    colors = f.readlines()

with open('animals.txt') as f:
    animals = f.readlines()

with open('adjectives.txt') as f:
    adjectives = f.readlines()

with open('nouns.txt') as f:
    nouns = f.readlines()

with open('coin_terms.txt') as f:
    coin_terms = f.readlines()

def write_usernames():
    usernames_sorted = sorted(usernames_final, key=len)  # shortest first
    print("\nFound {} unique and short usernames\n".format(len(usernames_sorted)))

    with open('results.txt', 'w') as f:
        for username in usernames_sorted:
            f.write(username + '\n')

    print('Username generation took this much time: ' +
        str(datetime.now() - start_time))

def get_username():
    for _ in range(10):  # in case username too long and have to try again
        prefix_list_item = random.choice([coin_terms])
        prefix = random.choice(prefix_list_item)

        suffix_list_item = random.choice([coin_terms])
        suffix = random.choice(suffix_list_item)
        if suffix == prefix:
            continue

        username = prefix.title() + suffix.title()
        username = ''.join(c for c in username if c.isalnum())  # strip special
        if len(username) <= MAX_LENGTH:
            return username

usernames = []
for _ in range(num_usernames_to_make):
    username = get_username()
    if username not in usernames:
        usernames.append(username)

def is_username_unique(username):
    url = 'https://www.google.com/search?q={}&tbs=li:1'.format(username)
    time.sleep(DELAY)  # to avoid Google blacklisting us
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
    }
    response = requests.get(url, headers=headers)
    html = response.text
    if 'detected unusual traffic' in html:
        print('Google is not happy with the traffic we are sending; abort')
        write_usernames()
        sys.exit()
    return 'did not match any documents' in response.text

num_users = len(usernames)
print('\nChecking [ {} ] usernames'.format(num_users))

usernames_final = []
count = 0
for username in usernames:
    if is_username_unique(username):
        usernames_final.append(username)
    count += 1
    if count % 100 == 0:
        print('Checked {} usernames'.format(count))
