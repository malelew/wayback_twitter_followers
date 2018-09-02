import sys
import subprocess
import pandas
import requests
import logging
from bs4 import BeautifulSoup

twitter_url = "https://twitter.com/"
arg_num = 4

if (len(sys.argv) != arg_num):
    raise ValueError("Incorrect number of arguemts please pass three arugments: twitte handle, from_date formatted as YYYYMMDDhhss, to_date formatted as YYYYMMDDhhss")

twitter_handle = str(sys.argv[1])
from_date = str(sys.argv[2])
to_date = str(sys.argv[3])

twitter_handle_url = twitter_url + twitter_handle

# waybackpack pull arugments
directory_arg = "-d ./" + twitter_handle + " "# where to save the archived pages
raw_arg = "--raw " # fetch archives in their original state
from_date_arg = "--from-date " + from_date + " " # first archive to pull
to_date_arg = "--to-date " + to_date + " " # last archive to pull
follow_redirects_arg = "--follow-redirects " # follow redirects
uniques_only_arg = "--uniques-only " # Download only the first version of duplicate filesself.
quiet_arg = "--quiet " # Don't log progress to stderr. improves run time

waybackpack_call = "waybackpack " + directory_arg + raw_arg + from_date_arg + to_date_arg + follow_redirects_arg + uniques_only_arg + quiet_arg + twitter_handle_url

subprocess.call(waybackpack_call, shell=True)
