# unique-username-finder

Creates random usernames, asynchronously checks Google for zero results returned to filter out names in use

## Usage

1. Install Python 3.4.x or later
1. Run the file with `python main.py i` where `i` is the number of usernames you want to attempt to generate (the actual number will be smaller, as non-unique ones -- those found to have google results -- will be filtered out)

It'll (over)write the results to `results.txt`.

Output will look something like:

    Checking [ 5 ] usernames

    Started async check for ManateeReality
    Started async check for CornyPopulation
    Started async check for SnowPuma
    Started async check for UntrueChamois
    Started async check for OchreMouse
    Finished async check for UntrueChamois
    Finished async check for ManateeReality
    Finished async check for OchreMouse
    Finished async check for CornyPopulation
    Finished async check for SnowPuma

    Checked 5 usernames
    1 usernames were found to be unique
    Username generation took this much time: 0:00:00.801511
