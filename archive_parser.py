import time
import os
import pandas as pd
import logging
from datetime import datetime
from bs4 import BeautifulSoup

# setup debug logging
logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def compile_follower_growth(twitter_handle, pages_dir="./"):
  # start timer
  start = time.time()
  logger.info("Start...")

  # intialize dataframe
  follower_count_df = pd.DataFrame(columns=['date', 'follower_count', 'handle'])
  failed_date_len = 4

  if (type(twitter_handle) != list):
      handles = [twitter_handle]

  # loop through each handle present and extract date and corresponding follower count
  for handle in handles:
    # dict with key:value equaling date:follower_count
    follower_count_dict = {}

    print handle
    # keep a list of dates failed for debugging purposes
    failed_dates = []
    passed_dates = []

    # logger.info("Current Handle: %s", handle)

    # make a list of the dates present in the wayback archive
    dates = [date for date in os.listdir(os.path.expanduser(pages_dir + handle)) if not date.startswith('.')]

    print dates 

    # for each archive date find 'follower_count' element and extract total
    for date in dates:
      # intialize len of number and bool that keeps track of whether number has ended
      num_len = 0
      num = False

      # convert string to datetime object
      count_date = datetime.strptime(date, "%Y%m%d%H%M%S") # currently not being utilized and converted after the fact

      # get the path of the specific date's archived html
      page = pages_dir + handle + '/' + date + '/twitter.com' + '/' + handle
      # open the file as a BeuatifulSoup object then convert it to an str for easier search indexing
      soup = BeautifulSoup(open(os.path.expanduser(page)), 'html.parser')
      soup = str(soup)

      # get the index of where the follower_count element is
      init = soup.find('followers_count')

      # for debugging purposes keep track of failed follower_count search
      if (init == -1):
        failed_dates.append(date[0:failed_date_len])
        continue

      # iterate thru the string until a digit is reach
      while (not num):
        init+=1 # keep track of where the number's initial index
        num = soup[init].isdigit() # will return whether current char is a digit

      # iterate thru the number until you reach a char that is not a digit
      while (num):
        num_len+=1 # keep track of the len of the number
        num = soup[init:init+num_len].isdigit() # will return whether current char is a digit

      # slice the number out of the html string and convert to an int
      follower_count = int(soup[init:init+num_len-1])
      # store the follower count in a dict with a key:value of date:follower_count
      follower_count_dict[date] = follower_count

    # initialize a temporary dataframe to store the current handle's follower_count growth
    temp_df = pd.DataFrame.from_dict(follower_count_dict, orient='index')
    temp_df.reset_index(level=0, inplace=True)
    temp_df['handle'] = handle # add a col indicating corresponding handle
    temp_df.columns = ['date', 'follower_count', 'handle'] # rename columns

    # append the new data to the comprehensive dataframe with the growth for all present candidates
    follower_count_df = follower_count_df.append(temp_df)
  logger.info('Number of failed follower_count element searches %d',    len(failed_dates))

  follower_count_df = clean_duplicate_dates(follower_count_df)

  # convert from YYYYMMDDHHMMSS format to YYYYMMDD
  follower_count_df.date = pd.Series((follower_count_df.date)).astype(int)

  # convert from YYYYMMDDHHMMSS format to YYYYMMDD # conve
  temp_series = pd.Series((follower_count_df.date / 1000000)).astype(int)
  follower_count_df[date] = pd.to_datetime(temp_series, format="%Y%m%d")

  # sort the data by date
  follower_count_df = follower_count_df.sort_values(['date'])

  logger.info('Done!')
  return follower_count_df

def clean_duplicate_dates(follower_count_df):
  # keep a list of each row to be dropped from the dataframe
  entries_to_drop = []
  # loop through each row

  follower_count_df.date = pd.Series((follower_count_df.date)).astype(int)

  for index, row in follower_count_df.iterrows():
    # take the current date and modify it to remove time
    curr_date = int((row['date']) / 1000000) # use this line if date is saved as a int

    # curr_date = row['date'][0:8] # use this line if date is saved as a string

    # the first row cannot be compared
    if (index != 0):
      # if prev MMDDYYYY matches the current add it to be removed
      print "curr date " + str(curr_date)
      print "prev date" + str(prev_date)
      if (curr_date == prev_date[1]):
        print "dropping row"
        entries_to_drop.append(prev_date[0])
    # set prev_date to current_date for next iteration
    prev_date = (index, curr_date)

  entries_to_keep = set(range(len(follower_count_df))) - set(entries_to_drop)
  follower_count_df = follower_count_df.take(list(entries_to_keep))
  return follower_count_df
