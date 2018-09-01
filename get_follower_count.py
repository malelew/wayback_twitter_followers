import sys
import subprocess
import pandas
from bs4 import BeautifulSoup
import requests
import logging

twitter_url = "https://twitter.com/"
arg_num = 3

#if (len(argv) != arg_num):
#    return "Incorrect number of arugments"

twitter_handle = str(sys.argv[0])
from_date = str(sys.argv[1])
to_date = str(sys.argv[2])

twitter_handle_url = twitter_url + twitter_handle

# waybackpack pull arugments
directory_arg = "-d " + twitter_handle + " "# where to save the archived pages
raw_arg = "--raw " # fetch archives in their original state
from_date_arg = "--from-date " + from_date + " " # first archive to pull
to_date_arg = "--to-date" + to_date + " " # last archive to pull
follow_redirects_arg = "--follow-redirects " # follow redirects
uniques_only_arg = "--uniques-only " # Download only the first version of duplicate filesself.
quiet_arg = "--quiet " # Don't log progress to stderr. improves run time

subprocess.call("waybackpack " + directory_arg + raw_arg + from_date_arg +
                 to_date_arg + follow_redirects_arg + uniques_only_arg +
                 quiet_arg + twitter_handle_url)
