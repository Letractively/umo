# Description #

**Url Malware Owned** (UMO) is a mini tool for catch malware URLs.

# Objective #

The main objective of UMO is harvest URLs and detect malware in them. UMO have three logical components:

  * Collector component
  * Analysis component
  * Report component

## Collector component ##

UMO have three modes for harvest URLs now:

  * Through Google Engine
  * Through Bing Engine
  * Crawling

## Analysis component ##

In this moment UMO search the URLs in local database of Google Safebrowsing for decide if one URL is owned by
a malware.

## Report component ##

This module is the output of UMO for show url's with malware. For now text file :)

# Acknowledgements #

Thank you to the developers of:

  1. fimap: http://code.google.com/p/fimap/
  1. Pybing: http://code.google.com/p/pybing/
  1. xgoogle: http://www.catonmat.net/blog/python-library-for-google-search/
  1. safebrowsing python: http://code.google.com/p/safebrowsing-python/







