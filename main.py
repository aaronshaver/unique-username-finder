from datetime import datetime
from enum import Enum
import requests
import random
import sys
import time
import words

start_time = datetime.now()

class Settings(Enum):
    MAX_LENGTH = 15
    MAX_USERNAMES = 800
    PREFIXES_LISTS = [words.adjectives, words.colors]
    SUFFIXES_LISTS = [words.nouns, words.animals]
    DELAY = 0.05
    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'

if len(sys.argv) < 2:
    print('put number of users you want to try for as a numeric commandline arg')
    sys.exit()

num_usernames_to_make = int(sys.argv[1])
if num_usernames_to_make > Settings.MAX_USERNAMES.value:
    print('Google gets mad if you do too many queries. If you still  want to do this, edit MAX_USERNAMES in the .py file and run again.')
    sys.exit()

def print_time_taken():
    print('Username generation took this much time: ' + str(datetime.now() - start_time))

def is_username_unique(username):
    url = 'https://www.google.com/search?q={}&tbs=li:1'.format(username)
    time.sleep(Settings.DELAY.value)  # to avoid Google blacklisting us
    headers = {
        'User-Agent': Settings.USER_AGENT.value,
    }
    response = requests.get(url, headers=headers)
    html = response.text
    if 'detected unusual traffic' in html:
        print('Google is not happy with the traffic we are sending; aborting')
        write_usernames()
        print_time_taken()
        sys.exit()
    return 'did not match any documents' in response.text

def write_usernames():
    usernames_sorted = sorted(unique_usernames, key=len)  # shortest first
    print("\nFound {} unique and short usernames\n".format(len(usernames_sorted)))

    with open('results.txt', 'w') as f:
        for username in usernames_sorted:
            f.write(username + '\n')

def get_username():
    for _ in range(10):  # in case username too long and have to try again, kind of a hack
        prefix_list_item = random.choice(Settings.PREFIXES_LISTS.value)
        prefix = random.choice(prefix_list_item)

        suffix_list_item = random.choice(Settings.SUFFIXES_LISTS.value)
        suffix = random.choice(suffix_list_item)
        if suffix == prefix:
            continue  # don't want repeats

        username = prefix.title() + suffix.title()
        username = ''.join(c for c in username if c.isalnum())  # strip special
        if len(username) <= Settings.MAX_LENGTH.value:
            return username

def print_num_users_checked(count):
    print('Checked {} usernames'.format(count))

usernames = []
for _ in range(num_usernames_to_make):
    username = get_username()
    if username not in usernames:
        usernames.append(username)

num_users = len(usernames)
print('\nChecking [ {} ] usernames\n'.format(num_users))

unique_usernames = []
count = 0
for username in usernames:
    if is_username_unique(username):
        unique_usernames.append(username)
    count += 1
    if count % 100 == 0:
        print_num_users_checked(count)

write_usernames()

print_num_users_checked(count)
print('{} usernames were found to be unique'.format(len(unique_usernames)))
print_time_taken()
