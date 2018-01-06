# unique-username-finder

Creates random usersnames, checks against Google for zero results returned

## Usage

1. Install Python 3.x
1. Run the file with `python main.py i` where `i` is the number of usernames you want to attempt to generate (the actual number will be smaller as non-unique ones -- those found to have google results -- are filterd out)

It'll (over)write the results to `results.txt`.

The code's super ugly and hacked together, but it got the job done.

Output will look something like:

    Checking [ 10 ] usernames

    Found 3 unique and short usernames
