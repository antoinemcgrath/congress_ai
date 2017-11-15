#### A script for copying the twitter users you follow into one of your twitter lists
#### Specify your destination list

import json
import tweepy
import time
import re

#### Load API keys file
keys_json = json.load(open('/usr/local/keys.json'))

#### Specify key dictionary wanted (generally [Platform][User][API])
Keys = keys_json["Twitter"]["ClimateCong_Bot"]["ClimatePolitics"]
#Keys = keys_json["Twitter"]["AGreenDCBike"]["HearHerVoice"]

#### Access API using key dictionary definitions
auth = tweepy.OAuthHandler( Keys['Consumer Key (API Key)'], Keys['Consumer Secret (API Secret)'] )
auth.set_access_token( Keys['Access Token'], Keys['Access Token Secret'] )
api = tweepy.API(auth)
user = Keys['Owner']



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
            used = limit - remaining
            if used != 0:
                print("  Twitter API:", used, "requests used,", remaining, "remaining, for API queries to", akey)
                pass


twitter_rates()












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
      api.create_list(name=current_list, description=description)
      existing_lists.append(current_list)
      print("New list created and name added to list of lists")
      list_exists = True
    else:
      print("List found")
    return(existing_lists)


def get_user_id(name):
    id = None
    try:
        u = api.get_user(name)
        id = u.id
    except tweepy.error.TweepError as e:
        if e.api_code == 80:
            time.sleep(60*5) #Sleep for 5 minutes
        elif e.api_code == 50:
            print("Username no longer exists, id unavailable")
            pass #Sleep for 5 minutes
        else:
            print (e)
    return(id)









#### PUSHES REPS FROM EVERYPOLITICIAN TO TWITTER LISTS ####
import requests
from everypolitician import EveryPolitician
ep = EveryPolitician()

#all_countries = ep.countries()
all_json = ep.countries_json_data()
for country in all_json:
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
              description = "A list of politicical accounts from " + str(country['name']) + " within the " + str(country['legislatures'][0]['name'])
              try:
                #Create current_list if not listed and update existing_lists
                existing_lists = list_check(current_list, existing_lists, description)
                # Add user to list
                id = get_user_id(name)
                if id == None:
                    continue
                api.add_list_member(user_id=id, slug=current_list, owner_screen_name=user)
              except tweepy.error.TweepError as e:
                print("error, perhaps user is already on list")
                print(e)
                print(id, current_list, user)
                time.sleep(10)
                pass
            else:
              pass
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
    id = get_user_id(name)
    if id == None:
        continue
    try:
      description = "A list of politicical accounts from the US state of " + str(leg['state']) + " within the " + str(leg['chamber'] + "chamber.")
      #Create current_list if not listed and update existing_lists
      existing_lists = list_check(current_list, existing_lists, description)
      # Add user to list

      api.add_list_member(user_id=id, slug=current_list, owner_screen_name=user)
    except tweepy.error.TweepError as e:
      print("error, perhaps user is already on list")
      #print(e)
      pass
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
