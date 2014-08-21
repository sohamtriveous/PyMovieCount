__author__ = 'sohammondal'

import sys
import urllib
import re

def sortFunc(tuple):
    '''
    simple key comparison method for sorting
    :param tuple:
    :return:
    '''
    return tuple[-1]


def openAndCount(url):
    '''
    opens a site and finds the following movie pattern
    serial number: 1.
    movie name: The Shawshank Redemption
    year: (1994)
    rating: 9.2
    :param url: the url to parse data from
    :return: None
    '''
    opener = urllib.urlopen(url)
    data = opener.readlines()
    # assign variables so we can do a comparison
    rank = None
    filmName = None
    year = None
    rating = None
    yearDictionary = {}
    for line in data:
        # look for the rating and print the details
        # also populate a dictionary based on the year
        if year:
            rating = find('>([\d.]+)', line)
            if rating:
                print rank, filmName, year, rating
                # populate the year dictionary
                if yearDictionary.get(year):
                    yearDictionary[year] = yearDictionary[year] + 1
                else:
                    yearDictionary[year] = 1
                rank = None
                filmName = None
                year = None
                rating = None
                continue
            else:
                continue
        # look for the year
        if filmName:
            year = find(r'>\((\d+)\)', line)
            continue
        # look for the movie name
        if rank:
            filmName = find(r'>([\w\s]+)<', line)
            continue
        # look for the rank
        if rank == None:
            rank = find(r'<span name="ir".*>(\d+)\.', line)
    # sort the year dictionary
    tupleList = sorted(yearDictionary.items(), key=sortFunc, reverse=True)
    print tupleList
    return


def find(pat, string):
    '''
    Finds a regular expression match within a string
    :param pat: the regex pattern to be matched
    :param string: the string where to search
    :return: the first group match within ()
    '''
    match = re.search(pat, string)
    if match:
        return match.group(1)
    else:
        return None

# opens a url mentioned in the commandline argument and finds the frequency (whichyear)
# designed to work with http://www.imdb.com/chart/top
openAndCount(sys.argv[1])
