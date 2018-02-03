from datetime import datetime
from enum import Enum
import requests
import random
import sys
import time
import words
import asyncio

start_time = datetime.now()


class Settings(Enum):
    MAX_LENGTH = 15
    MAX_USERNAMES = 800
    PREFIXES_LISTS = [words.adjectives, words.colors]
    SUFFIXES_LISTS = [words.nouns, words.animals]
    DELAY = 0.05


if len(sys.argv) < 2:
    print('put number of users you want to try as a numeric commandline arg')
    sys.exit()

num_usernames_to_make = int(sys.argv[1])
if num_usernames_to_make > Settings.MAX_USERNAMES.value:
    print('Google gets mad if you do too many queries. If you still  want to do this, edit MAX_USERNAMES in the .py file and run again.')
    sys.exit()


def print_time_taken():
    print('Username generation took this much time: ' + str(datetime.now() - start_time))


async def get_google_response(username):
    await asyncio.sleep(Settings.DELAY.value)  # try to avoid Google blacklisting us
    future1 = loop.run_in_executor(None, requests.get, 'https://www.google.com/search?q={}&tbs=li:1'.format(username))
    response = await future1
    return response


async def check_and_add_unique_username(username):
    print("Started async check for {}".format(username))
    response = await get_google_response(username)
    html = response.text
    if 'detected unusual traffic' in html:
        print('Google is not happy with the traffic we are sending; aborting')
        write_usernames()
        print_time_taken()
        sys.exit()
    if 'did not match any documents' in response.text:
        unique_usernames.append(username)
    print("Finished async check for {}".format(username))


def write_usernames():
    usernames_sorted = sorted(unique_usernames, key=len)  # shortest first

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


usernames = []
for _ in range(num_usernames_to_make):
    username = get_username()
    if username not in usernames:
        usernames.append(username)

print('\nChecking [ {} ] usernames\n'.format(len(usernames)))

loop = asyncio.get_event_loop()

tasks = []
for username in usernames:
    tasks.append(
        asyncio.ensure_future(check_and_add_unique_username(username))
    )

unique_usernames = []
loop.run_until_complete(asyncio.wait(tasks))  
loop.close()

write_usernames()

print("\nChecked {} usernames".format(len(usernames)))
print('{} usernames were found to be unique'.format(len(unique_usernames)))
print_time_taken()
