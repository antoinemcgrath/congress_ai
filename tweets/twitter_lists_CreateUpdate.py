#### A script for copying the twitter users you follow into one of your twitter lists
#### Specify your destination list

import json
import tweepy
import time
import re
import sys
from datetime import datetime

priv_pub = "public" #mode="public" OR "private"
start_ahead_at = "dk"
start = False

#### Load API keys file
keys_json = json.load(open('/usr/local/keys.json'))

#### Specify key dictionary wanted (generally [Platform][User][API])
Keys = keys_json["Twitter"]["AGreenDCBike"]["HearHerVoice"]

#### Access API using key dictionary definitions
auth = tweepy.OAuthHandler( Keys['Consumer Key (API Key)'], Keys['Consumer Secret (API Secret)'] )
auth.set_access_token( Keys['Access Token'], Keys['Access Token Secret'] )
api = tweepy.API(auth)
user = Keys['Owner']

def require_enter():
    python2 = sys.version_info[0] == 2
    if python2:
        raw_input("Press ENTER to continue.")
    else:
        input("Press ENTER to continue.")


#### Define twitter rate determining loop
#Follow add rate limited to 1000 per 24hrs: https://support.twitter.com/articles/15364
def twitter_rates():
    stats = api.rate_limit_status()  #stats['resources'].keys()
    for akey in stats['resources'].keys():
        if type(stats['resources'][akey]) == dict:
            for anotherkey in stats['resources'][akey].keys():
                if type(stats['resources'][akey][anotherkey]) == dict:
                    #print(akey, anotherkey, stats['resources'][akey][anotherkey])
                    limit = (stats['resources'][akey][anotherkey]['limit'])
                    remaining = (stats['resources'][akey][anotherkey]['remaining'])
                    used = limit - remaining
                    if used != 0:
                        print("  Twitter API used:", used, "requests used,", remaining, "remaining, for API queries to", anotherkey)
                    else:
                        pass
                else:
                    pass  #print("Passing")  #stats['resources'][akey]
        else:
            print(akey, stats['resources'][akey])
            print(stats['resources'][akey].keys())
            limit = (stats['resources'][akey]['limit'])
            remaining = (stats['resources'][akey]['remaining'])
            reset = (stats['resources'][akey]['reset'])
            used = limit - remaining
            if used != 0:
                print("  Twitter API:", used, "requests used,", remaining, "remaining, for API queries to", akey)
            if remaining < 2:
                print("  Twitter requests remaining are just", remaining, "for API queries to", akey)
                print("Reset is:", reset)



twitter_rates()


def test_rate_limit(api, wait=True, buffer=.1):
    """
    Tests whether the rate limit of the last request has been reached.
    :param api: The `tweepy` api instance.
    :param wait: A flag indicating whether to wait for the rate limit reset
                 if the rate limit has been reached.
    :param buffer: A buffer time in seconds that is added on to the waiting
                   time as an extra safety margin.
    :return: True if it is ok to proceed with the next request. False otherwise.
    """
    #Get the number of remaining requests
    remaining = int(api.last_response.header('x-rate-limit-remaining'))
    #Check if we have reached the limit
    if remaining == 0:
        limit = int(api.last_response.header('x-rate-limit-limit'))
        reset = int(api.last_response.header('x-rate-limit-reset'))

        #Parse the UTC time
        reset = datetime.fromtimestamp(reset)
        #Let the user know we have reached the rate limit
        print("0 of {} requests remaining until {}.".format(limit, reset))

        if wait:
            #Determine the delay and sleep
            delay = (reset - datetime.now()).total_seconds() + buffer
            print ("Sleeping for {}s...".format(delay))
            sleep(delay)
            #We have waited for the rate limit reset. OK to proceed.
            return True
        else:
            #We have reached the rate limit. The user needs to handle the rate limit manually.
            return False

    #We have not reached the rate limit
    return True









#### Create a list of the twitter users current lists
existing_lists = []
lists = api.lists_all()
for one in lists:
  existing_lists.append(one.slug)
  print(one.slug)


#### Create current_list if not listed and update existing_lists
def list_check(current_list, existing_lists, description):
  list_exists = False
# Check if current_list is on the list of existing list
  while list_exists == False:
    for list in existing_lists:
      if list==current_list:
        #print("It exists", current_list, list_exists, list)
        list_exists = True
      else:
        #print("It doesn't exist", current_list, list_exists, list)
        pass
# Create current_list & add to list
    if list_exists == False:
      print("no list found, creating list")
      api.create_list(name=current_list, description=description, mode=priv_pub) #mode="public" OR "private"
      existing_lists.append(current_list)
      print("New list created and name added to list of lists")
      list_exists = True
    else:
      pass
      #print("List found")
    return(current_list, existing_lists)


def get_user_id(name, attempt):
    id = None
    attempt += 1
    if attempt == 1:
        delay = 1
    if attempt == 2:
        delay = 61
    if attempt == 3:
        delay = 60*16
    if attempt == 4:
        delay = 60*61*3
    if attempt == 5:
        delay = 60*61*15
    if attempt == 6:
        delay = 60*61*25
    if attempt > 6:
        delay = 60*49*10*attempt
    #print("user id fetch delay:", delay)
    if delay > 60:
        print("Delay will occur for", str(round(delay/60)), "minutes.")
    time.sleep(delay)
    try:
        u = api.get_user(name)
        id = u.id
        if u.protected == True:
            print("User is protected", name, id)
            id = None
    except tweepy.error.TweepError as e:
        if e.api_code == 80:
            print("error code 80", str(e))
            require_enter()
        elif e.api_code == 50:
            print("Username no longer exists, id unavailable for", name)
            pass
        elif e.api_code == 63:
            print("User has been suspended", name)
            pass
        elif e.api_code == 88:
            print("Rate limit exceeded, id not acquired for:", name)
            test_rate_limit(api)
            get_user_id(name, attempt)
            pass
        else:
            print("Unkown error press enter to pass", e.api_code, str(e.args[0][0]['message']), name)
            require_enter()
            time.sleep(3)
            pass
    return(id)



def add_user_to_list(id, current_list, user, attempt):
    try:
        attempt += 1
        if attempt == 1:
            delay = 15
        if attempt == 2:
            delay = 61
        if attempt == 3:
            delay = 60*16
        if attempt == 4:
            delay = 60*61*3
        if attempt == 5:
            delay = 60*61*15
        if attempt == 6:
            delay = 60*61*25
        if attempt > 6:
            delay = 60*49*10*attempt
        #print("user id fetch delay:", delay)
        if delay > 60:
            print("Delay will occur for", str(round(delay/60)), "minutes.")
        time.sleep(delay)
        # Add user to list
        api.add_list_member(user_id=id, slug=current_list, owner_screen_name=user)
    except tweepy.error.TweepError as e:
        if e.api_code == 104: #Either list is not yours, or you are restricted. Either way you aren't allowed to add members to this list
            print("Pass", e.api_code, str(e.args[0][0]['message']), name, current_list, user)
            add_user_to_list(id, current_list, user, attempt)
            pass
        elif e.api_code == 88: #Rate limit exceeded
            print("Retry", e.api_code, str(e.args[0][0]['message']), name, current_list, user)
            test_rate_limit(api)
            add_user_to_list(id, current_list, user, attempt)
            pass
        else:
            print("Unkown error press enter to pass", e.api_code, str(e.args[0][0]['message']), name, current_list, user)
            print(name, id, current_list, user)
            require_enter()
            time.sleep(3)
            pass

        pass






#### PUSHES REPS FROM EVERYPOLITICIAN TO TWITTER LISTS ####
import requests
from everypolitician import EveryPolitician
ep = EveryPolitician()

#all_countries = ep.countries()
all_json = ep.countries_json_data()
for country in all_json:
    print(country['code'])
    if country['code'].lower() == start_ahead_at:
        start = True
        print("Starting")
    while start == True:
        branches = country['legislatures']
        for branch in branches:
            link = branch['popolo_url']
            f = requests.get(link)
            new = json.loads(f.text)
            #Loaded the json from the url specific to the branch
            for person in new['persons']:
                try:
                    for alink in person['links']:
                        if alink['note'] == 'twitter':
                            name = (alink['url'].split("/")[3])
                            list = country['code'] +"-"+ country['legislatures'][0]['slug']
                            list.replace(" ","-")
                            current_list = list.lower()
                            if len(current_list) > 25:
                                current_list = current_list.replace("representative","rep")
                            description = "A list of politicical accounts from " + str(country['name']) + " within the " + str(country['legislatures'][0]['name'])
                            #Create current_list if not listed and update existing_lists
                            response = list_check(current_list, existing_lists, description)
                            current_list = response[0]
                            existing_lists = response[1]
                            attempt = 0
                            id = get_user_id(name, attempt)
                            if id == None:
                              continue
                            attempt = 0
                            add_user_to_list(id, current_list, user, attempt)
                            count += 1
                except:
                  pass

















#### Adds Reps from OpenStates to Twitter Lists (US State Reps)####
## Creates list if none exists
from sunlight import openstates
# Get all legisilators form Openstates API
allLegs = openstates.legislators()
# Set counter
count=-1
# For each legislator in the list of legislators
for leg in allLegs:
  # Try to set values (error will result if values do not exist)
  try:
    vals = (str(count), 'us-'+str(leg['state'])+"-"+str(leg['chamber']), str(leg['+twitter']))
    list = 'us-'+str(leg['state'])+"-"+str(leg['chamber'])
    list.replace(" ", "-")
    current_list = list.lower()
    print(vals[0], vals[1])
    name = (str(str(leg['+twitter']).split("/")[3]))
    # Get twitter user_id from twitter name/handle
    attempt = 0
    id = get_user_id(name, attempt)
    if id == None:
        continue

    description = "A list of politicical accounts from the US state of " + str(leg['state']) + " within the " + str(leg['chamber'] + "chamber.")
    #Create current_list if not listed and update existing_lists
    response = list_check(current_list, existing_lists, description)
    current_list = response[0]
    existing_lists = response[1]

    # Add user to list
    attempt = 0
    add_user_to_list(id, current_list, user, attempt)
    count += 1
    # Error resulted Openstate API did not include a twitter name for this legislator
  except KeyError as e:
    if str(e) == "'+twitter'":
      # ADD FUNCTION TO CRAWL LEGISLATORS WEBSITE TO CAPTURE HANDLES IF WANTED
      # Legislators website url is here (view other variables by printing value leg)
      #print(leg['url'])
      pass      #Has no twitter handle
    elif leg['photo_url'] == 'http://www.legdir.legis.state.tx.us/FlashCardDocs/images/Senate/small/A1430.jpg':
      pass
    else:
      print ('I got a KeyError - reason "%s"' % str(e))
      #print(leg)
  except IndexError as e:
    print ('I got an IndexError - reason "%s"' % str(e))
    #print(leg)
#### DONE PUSHING STATE REPS FROM OPENSTATES TO TWITTER LISTS ####

print("Complete, number added:", str(count))






#all_json[3]['slug']
#all_json[3]['legislatures']
#all_json[3]['legislatures'][0]['slug']

#ep.country_legislature('Alderney', 'States')
#ep.country_legislature(all_json[3]['slug'], all_json[3]['legislatures'][0]['slug'])
#all_json[3]['legislatures'][0]['popolo_url']



# Create list if it does not exist
##existing_lists = list_check(current_list, existing_lists, description)
# Add user to list
##api.add_list_member(user_id=id, slug=list, owner_screen_name=user)

#### PUSHES REPS FROM EVERYPOLITICIAN TO TWITTER LISTS ####
