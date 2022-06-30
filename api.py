# import the "requests" library if you don't already have it installed
# python -m pip install requests

# load required libraries
import os
import sys
import re
import warnings
import requests
from requests.structures import CaseInsensitiveDict
import datetime

import pandas as pd
import json

# TODO remove all printing except for error messages and which dates are currently running

# store the URL of the API in a object
url = "https://5rxy4xetnd.execute-api.us-west-2.amazonaws.com/production/messages"

headers = CaseInsensitiveDict()

headers["Content-Type"] = "application/json"

# read in the configuration JSON from the project directory
# this is read in as a dictionary
with open('config/config.json') as file:
    json_config_dict = json.load(file)

# use the dict to interate through the start time and end time
# index the dictionary to get the start time inside of the json file
# we will leave the start time unchanged in the JSON file and change the date inside of Python
json_start_date_string = json_config_dict['start_time']
print(json_start_date_string)

# do the same for the end date inside of the json file
json_end_date_string = json_config_dict['end_time']
print(json_end_date_string)

# convert the start date string into a datetime object
json_start_date_datetime = datetime.datetime.strptime(json_start_date_string, '%Y-%m-%d %H:%M:%S.%f')
print(json_start_date_datetime)

# convert the end date string into a datetime object
json_end_date_datetime = datetime.datetime.strptime(json_end_date_string, '%Y-%m-%d %H:%M:%S.%f')
print(json_end_date_datetime)

# TODO I can either use the JSON config file to pass in a start date and then begin iterating based on that date OR I can basically ignore the dates in the config file and specify my own dates

# TODO I can specify the date input as a sys.arg to accept inputs from the command line interface
# specify your start time here in the format Year,Month,Day,Hour,Minute,Seconds,Microseconds
my_start_date_datetime = datetime.datetime(2022, 4, 2, 0, 0, 0, 000)
print(my_start_date_datetime)

# specify your end time here in the format Year,Month,Day,Hour,Minute,Second(s,Microseconds
my_end_date_datetime = datetime.datetime(2022, 4, 3, 0, 0, 0, 000)
print(my_end_date_datetime)

# compare the difference in time between the start and end dates
time_difference_days = (my_end_date_datetime - my_start_date_datetime).days
# print the total time difference (in days) between the start and end dates
print(time_difference_days)

# intermediate_end_date_datetime = start_date_datetime + datetime.timedelta(days = 0.5)

# print(intermediate_end_date_datetime)

# need to split the time delta into 12 hours chunks to be safe (avoid timeout)
# my_end_date_datetime

time_delta = datetime.timedelta(days = 0.5)

print(time_delta)

print(my_start_date_datetime + time_delta)

# initialize an empty list to store our list of dates to feed to the API
dates_to_call = [my_start_date_datetime]

print(dates_to_call)

date = my_start_date_datetime

while(date < my_end_date_datetime):
    print("iteration", date)
    date = date + time_delta
    dates_to_call.append(date)

# note that this list stores each element as a datetime
print(dates_to_call)

# initialize an empty pandas data frame
all_data = pd.DataFrame()

window_size = 2

for i in range(len(dates_to_call) - window_size + 1):
    print(dates_to_call[i: i + window_size])

# dates_to_call[0: 0 + window_size][0]
# dates_to_call[0: 0 + window_size][1]

for i in range(len(dates_to_call) - window_size + 1):
    # the time difference in and of itself doesn't matter
    # rather its the amount of time it takes the server to respond to with that much data
    # if its takes too much time, then you will get a server error

    # convert the start datetime to a string
    # the formatting part is specific to the date formatting the API expects
    start_date_datetime = dates_to_call[i: i + window_size][0]
    start_date_string = start_date_datetime.strftime("%Y-%m-%d %H:%M:%S.%f")
    print(start_date_string)

    # assign in the new start and end dates to the json converted to dictionary
    json_config_dict['start_time'] = start_date_string
    print(json_config_dict['start_time'])

    # grab the first intermediate end date from the list
    intermediate_date_datetime = dates_to_call[i: i + window_size][1]
    intermediate_date_string = intermediate_date_datetime.strftime("%Y-%m-%d %H:%M:%S.%f")
    print(intermediate_date_string)

    json_config_dict['end_time'] = intermediate_date_string

    # convert the dict to a json string
    data = json.dumps(json_config_dict)

    # make call to API, store response in a object
    response = requests.post(url, headers=headers, data=data)

    # stop execution if http response returns an error
    # there are many possible reasons that it may return an error
    if response.status_code != 200:
        sys.exit(("Error: HTTP Response" + " " + str(response.status_code) + " " + response.reason))

    print(response.status_code)

    print(response.text)

    # check the character encoding of the API response
    # it should be in utf-8
    print(response.encoding)

    # index the response variable to get the "content" of the response
    # the response text will work better than response content
    message_text = response.text

    # check the output in the console
    print(message_text)

    # drop the first and last characters from the message so string splitting will create symmetrical messages
    # first we need to know the length of the message (i.e., number of characters) to create an index
    message_length = len(message_text)

    # stop execution if the http response is empty but status code is 200
    # for whatever reason, the server returns two braces with nothing inside
    if message_length <= 3:
        sys.exit("Error: Empty Response from Server")

    # check the output in the console
    print(message_length)

    # TODO instead of creating new variables when cleaning up the message string, just overwrite the message string

    # drop the last character of the message which is an extra right brace "]"
    # this is just an extra unnecessary character
    message_text_drop_last_char = message_text[0:(message_length - 1)]

    # if it worked correctly you should see a parenthesis character instead of a brace character
    print(message_text_drop_last_char[-1])

    # print(message_text_drop_last_char)
    # print(message_text)

    # drop the first character of the message which is an extra left brace "["
    # this is just an extra unnecessary character
    message_text_drop_first_char = message_text_drop_last_char[1:]

    # if it worked correctly you should see a parenthesis character instead of a brace character
    print(message_text_drop_first_char[0])

    # drop the empty space characters too
    message_text_drop_empty_spaces = str.replace(message_text_drop_first_char, " ", "")

    # print the output in the console to check if it was successful
    # there shouldn't be any spaces between characters
    print(message_text_drop_empty_spaces)

    # the message text also has apostrophe characters that we need to drop
    # these characters are leftovers from the message data
    message_text_drop_apostrophe_char = str.replace(message_text_drop_empty_spaces, "'", "")

    # print the message text after we dropped the apostrophes to see if if worked
    print(message_text_drop_apostrophe_char)

    # drop the extra brace characters too
    message_text_drop_left_brace_char = str.replace(message_text_drop_apostrophe_char, "[", "")

    # if it worked correctly you should no longer see a left brace character alongside "sequenceNumber"
    print(message_text_drop_left_brace_char)

    # there are actually two message types returned from the beta API
    # split the message response into two separate messages on a specific combination of characters
    message_list = message_text_drop_left_brace_char.split(sep="]),")

    # print the messages and their indexes to check if each message was string split properly
    # there should be no extra characters at the beginning or end of each string
    for index, value in enumerate(message_list):
        print(index, value)

    # intialize an empty list to store the data
    regex_search = []

    # implement a for loop that reads in each element from the message_list
    # and checks for a pattern match on the regular expression
    # if there is a pattern match, the for loop will print a success message
    # if there is not a pattern match, the for loop will print an error message and stop the for loop
    # error message include the index number so you can take a look at where in the data the for loop stopped
    for i in range(len(message_list)):
        regex_search.append(re.search("datetime.datetime\(\d*,\d*,\d*,\d*,\d*,\d*,\d*\)", message_list[i]))
        if type(regex_search[i]) == re.Match:
            print("RegEx match")
        elif type(regex_search[i]) != re.Match:
            warnings.warn('Not a match: (index number = ' + str(i) + ')' + ' ' + message_list[i])
            offending_message = message_list[i]
            index = int(i)
            # print the offending message
            print(offending_message)
            break

    # you can also access the offending message by indexing the message list
    message_list[index]

    # intialize an empty list to store if the date in each message is a match to the regex
    # tis object will be used to test if the type is a re.match or none (not a match)
    missing_dates = []

    # search for dates in the message list that are missing the microseconds field
    # this regular expression may need to change if the inputs are different
    # this for loop tells you which dates are missing a field based on regular expression match

    for i in range(len(message_list)):
        missing_dates.append(re.search("datetime.datetime\(\d*,\d*,\d*,\d*,\d*,\d*\)", message_list[i]))

    # search for dates in the message list that are missing the seconds field and the microseconds field
    for i in range(len(message_list)):
        missing_dates.append(re.search("datetime.datetime\(\d*,\d*,\d*,\d*,\d*\)", message_list[i]))

    # intialize and empty list to store the messages that are missing a date field
    offending_messages = []
    offending_messages_index = []

    # this for loop will tell you which messages are missing a date by their index
    for i in range(len(missing_dates)):
        if type(missing_dates[i]) == re.Match:
            offending_messages.append(message_list[i])
            offending_messages_index.append(int(i))
            print('This message is missing a date: (index number = ' + str(i) + ')')

    # these are the offending messages
    print(offending_messages)
    print(offending_messages_index)

    # intialize an empty list to store the offending messages that have zeros added
    # the zeros are so that when we go to evaluate the date expression
    # it doesn't fail because their are uneven number of inputs
    # dates that are missing a field have 6 inputs
    # dates that aren't missing a field have 7 inputs
    offending_messages_add_zeros = []

    for i in range(len(offending_messages)):
        offending_messages_add_zeros.append(re.sub(pattern="\)", repl=",00000)", string=offending_messages[i]))

    print(offending_messages_add_zeros)

    for i in range(len(offending_messages)):
        message_list[offending_messages_index[i]] = offending_messages_add_zeros[i]

    # reinitialize an empty list to overwrite the list with the bad date
    regex_search = []

    # rerun the error message to check if our solution worked
    # important: the output from this for loop will be used to extract the date expressions
    # TODO treat this like an error message rather than a way to extract date expressions
    for i in range(len(message_list)):
        regex_search.append(re.search("datetime.datetime\(\d*,\d*,\d*,\d*,\d*,\d*,\d*\)", message_list[i]))
        if type(regex_search[i]) == re.Match:
            print("RegEx match")
        elif type(regex_search[i]) != re.Match:
            warnings.warn('Not a match: (index number = ' + str(i) + ')' + ' ' + message_list[i])
            offending_message = message_list[i]
            index = int(i)
            break

    # check the output in the console
    print(regex_search)

    # initialize an empty list to store the unevaluated date expressions
    date_expressions = []
    # TODO this breaks when then seconds parameter is missing, I fixed it for microseconds
    # extract just the date expression from the
    for i in range(len(regex_search)):
        date_expressions.append(regex_search[i].group())

    # check the output in the console
    # there should only be unevaluated Python expressions in this list
    print(date_expressions)

    # check that the length of the date list matches the length of the message list
    len(date_expressions)
    len(message_list)

    # print a warning message if there are missing dates in the message data
    # there might be problems caused by missing dates that this script currently cannot handle
    if len(date_expressions) == len(message_list):
        print("There are no missing dates in these messages. Proceed.")
    elif len(date_expressions) != len(message_list):
        warnings.warn('Warning Message: It looks like some dates might be missing. STOP.')

    # It makes more sense to store the date as string rather (in ISO format)
    # Rather than as a datetime object when writing to a csv file
    # some programs like Excel have problems displaying datetime formats
    # initialize an empty list to store the datetimes converted into isoformat 8601 date strings
    isodate_list = []

    # evaluate the string as a Python expression and temporarily store the output as a "datetime" object
    # datetime objects are a special class of objects with special properties
    # then convert the datetime object into an isoformat 8601 date string
    for i in range(len(date_expressions)):
        date_time_object = (eval(date_expressions[i]))
        isodate_list.append(date_time_object.isoformat())

    # check the output in the console to see if the dates were converted properly
    # there should a list of date strings similar to "2021-12-01T00:26:33.477000"
    print(isodate_list)

    # initialize an empty list for the cleaned dates
    message_list_cleaned_dates = []

    # for loop through the message list, replacing each unevaluated Python date expression with a date string in iso format
    # it looks like a paranthesis was dropped or changed in this message type
    for i in range(len(message_list)):
        message_list_cleaned_dates.append(
            re.sub("datetime.datetime\(\d*,\d*,\d*,\d*,\d*,\d*,\d*\)", isodate_list[i], message_list[i]))

    # check the output in the console to see if the date strings were correctly replaced
    # you should now see iso 8601 formatted dates instead of unevaluated Python expressions
    for index, value in enumerate(message_list_cleaned_dates):
        print(index, value)

    # split the message text on the comma delimiter
    # store the string split message data in a new object
    # its important to note that we are changing data formats by splitting
    # we are going from a string to a list

    # write a for loop that
    # indexes message list to extract each message
    # splits each message by every comma
    # returns a nested list with each message stored in the parent list and split apart into
    # if you run this list multiple times you will need to clear

    # initialize an empty list for storing the nested data
    message_list_split = []

    for i in range(len(message_list_cleaned_dates)):
        message_split = (message_list_cleaned_dates[i].split(sep=","))
        message_list_split.append(message_split)

    print(message_list_split)

    # initialize empty lists to store each of the message types
    GpsLocationExtIndication = []
    GpsLocationExtIndicationCowHeading = []
    ShockEventExtIndication = []
    DeviceStatusIndication = []

    # TODO this could be more efficient if I created groups of each message type based on the element length
    # separate each message type by the number elements in each list
    for element in message_list_split:
        if len(element) == 10:
            GpsLocationExtIndication.append(element)
        elif len(element) == 11:
            GpsLocationExtIndicationCowHeading.append(element)
        elif len(element) == 21:
            ShockEventExtIndication.append(element)
        elif len(element) == 27:
            DeviceStatusIndication.append(element)

    # print(GpsLocationExtIndication)
    # print(GpsLocationExtIndicationCowHeading)
    # print(ShockEventExtIndication)
    # print(DeviceStatusIndication)

    location_extent_df = pd.DataFrame(GpsLocationExtIndication,
                                      columns=['uuid',
                                               'date',
                                               'collar',
                                               'messagetype',
                                               'latitude',
                                               'longitude',
                                               'accuracy',
                                               'reliable',
                                               'more',
                                               'sequence']
                                      )
    location_extent_df.index.name = "index"

    location_extent_cow_heading_df = pd.DataFrame(GpsLocationExtIndicationCowHeading,
                                                  columns=['uuid',
                                                           'date',
                                                           'collar',
                                                           'messagetype',
                                                           'latitude',
                                                           'longitude',
                                                           'accuracy',
                                                           'cowHeading',
                                                           'tiltAngle',
                                                           'reliable',
                                                           'more',
                                                           'sequence']
                                                  )
    location_extent_cow_heading_df.index.name = "index"

    shock_event_df = pd.DataFrame(ShockEventExtIndication,
                                  columns=['uuid',
                                           'date',
                                           'collar',
                                           'messagetype',
                                           'soundDisabled',
                                           'shockDisabled',
                                           'soundSuspended',
                                           'shockSuspended',
                                           'soundEvent',
                                           'shockEvent',
                                           'latitude',
                                           'longitude',
                                           'trackingState',
                                           'headingReportingEnabled',
                                           'headingManagementEnabled',
                                           'shockCount',
                                           'soundCount',
                                           'shockCountCumulative',
                                           'reliable',
                                           'more',
                                           'sequence']
                                  )

    shock_event_df.index.name = "index"

    # this data frame does not split on an equals sign
    # instead it uses column names
    device_status_df = pd.DataFrame(DeviceStatusIndication,
                                    columns=['uuid',
                                             'date',
                                             'collar',
                                             'messagetype',
                                             'sequenceNumber',
                                             'trackingState',
                                             'headingReportingEnabled',
                                             'headingManagementEnabled',
                                             'soundDisabled',
                                             'shockDisabled',
                                             'soundSuspended',
                                             'shockSuspended',
                                             'shockCountAttempts',
                                             'soundCountAttempts',
                                             'shockCountApplied',
                                             'soundCountApplied',
                                             'shockCountSuspend',
                                             'soundCountSuspend',
                                             'shockCountCumulative',
                                             'currVoltageMv',
                                             'lastTxVoltageMv',
                                             'lastShockVoltageMv',
                                             'mmuTempDegC',
                                             'mcuTempDegC',
                                             'reliable',
                                             'more',
                                             'sequence']
                                    )

    device_status_df.index.name = "index"

    # concatenate dataframes
    combined_df = pd.concat([device_status_df, location_extent_df, location_extent_cow_heading_df, shock_event_df],
                            ignore_index=True)

    # specify the order of the column names in the combined dataframe
    column_names = ['uuid',
                    'date',
                    'collar',
                    'messagetype',
                    'latitude',
                    'longitude',
                    'trackingState',
                    'cowHeading',
                    'tiltAngle',
                    'headingReportingEnabled',
                    'headingManagementEnabled',
                    'soundDisabled',
                    'shockDisabled',
                    'soundSuspended',
                    'shockSuspended',
                    'soundEvent',
                    'shockEvent',
                    'shockCount',
                    'soundCount',
                    'shockCountAttempts',
                    'soundCountAttempts',
                    'shockCountApplied',
                    'soundCountApplied',
                    'shockCountSuspend',
                    'soundCountSuspend',
                    'shockCountCumulative',
                    'currVoltageMv',
                    'lastTxVoltageMv',
                    'lastShockVoltageMv',
                    'mmuTempDegC',
                    'mcuTempDegC',
                    'reliable',
                    'more',
                    'sequence',
                    'accuracy']

    # reorder the columns so that latitude and longitude are right after 'messagetype'
    reindex_combined_df = combined_df.reindex(columns=column_names)

    # clean up all of the rows with equals signs
    # replace the string on the left side of the equals sign with nothing ""
    reindex_combined_df.uuid = reindex_combined_df.uuid.str.replace("(", "", regex=False)

    reindex_combined_df.latitude = reindex_combined_df.latitude.str.replace("latitude=", "")

    reindex_combined_df.longitude = reindex_combined_df.longitude.str.replace("longitude=", "")

    reindex_combined_df.accuracy = reindex_combined_df.accuracy.str.replace("accuracy=", "")

    reindex_combined_df.reliable = reindex_combined_df.reliable.str.replace("reliable=", "")

    reindex_combined_df.more = reindex_combined_df.more.str.replace("more=", "")

    reindex_combined_df.sequence = reindex_combined_df.sequence.str.replace("sequence=", "")

    reindex_combined_df.cowHeading = location_extent_cow_heading_df.cowHeading.str.replace("cowHeading=", "")

    reindex_combined_df.tiltAngle = location_extent_cow_heading_df.tiltAngle.str.replace("tiltAngle=", "")

    reindex_combined_df.soundDisabled = reindex_combined_df.soundDisabled.str.replace("soundDisabled=", "")

    reindex_combined_df.shockDisabled = reindex_combined_df.shockDisabled.str.replace("shockDisabled=", "")

    reindex_combined_df.soundSuspended = reindex_combined_df.soundSuspended.str.replace("soundSuspended=", "")

    reindex_combined_df.shockSuspended = reindex_combined_df.shockSuspended.str.replace("shockSuspended=", "")

    reindex_combined_df.soundEvent = reindex_combined_df.soundEvent.str.replace("soundEvent=", "")

    reindex_combined_df.shockEvent = reindex_combined_df.shockEvent.str.replace("shockEvent=", "")

    reindex_combined_df.trackingState = reindex_combined_df.trackingState.str.replace("trackingState=", "")

    reindex_combined_df.headingReportingEnabled = reindex_combined_df.headingReportingEnabled.str.replace(
        "headingReportingEnabled=", "")

    reindex_combined_df.headingManagementEnabled = reindex_combined_df.headingManagementEnabled.str.replace(
        "headingManagementEnabled=", "")

    reindex_combined_df.shockCount = reindex_combined_df.shockCount.str.replace("shockCount=", "")

    reindex_combined_df.soundCount = reindex_combined_df.soundCount.str.replace("soundCount=", "")

    reindex_combined_df.shockCountCumulative = reindex_combined_df.shockCountCumulative.str.replace(
        "shockCountCumulative=", "")

    # reindex_combined_df.sequenceNumber = reindex_combined_df.sequenceNumber.str.replace("sequenceNumber=", "")

    reindex_combined_df.headingReportingEnabled = reindex_combined_df.headingReportingEnabled.str.replace(
        "headingReportingEnabled=", "")

    reindex_combined_df.headingManagementEnabled = reindex_combined_df.headingManagementEnabled.str.replace(
        "headingManagementEnabled=", "")

    reindex_combined_df.shockCountAttempts = reindex_combined_df.shockCountAttempts.str.replace("shockCountAttempts=",
                                                                                                "")

    reindex_combined_df.soundCountAttempts = reindex_combined_df.soundCountAttempts.str.replace("soundCountAttempts=",
                                                                                                "")

    reindex_combined_df.shockCountApplied = reindex_combined_df.shockCountApplied.str.replace("shockCountApplied=", "")

    reindex_combined_df.soundCountApplied = reindex_combined_df.soundCountApplied.str.replace("soundCountApplied=", "")

    reindex_combined_df.shockCountSuspend = reindex_combined_df.shockCountSuspend.str.replace("shockCountSuspend=", "")

    reindex_combined_df.soundCountSuspend = reindex_combined_df.soundCountSuspend.str.replace("soundCountSuspend=", "")

    reindex_combined_df.currVoltageMv = reindex_combined_df.currVoltageMv.str.replace("currVoltageMv=", "")

    reindex_combined_df.lastTxVoltageMv = reindex_combined_df.lastTxVoltageMv.str.replace("lastTxVoltageMv=", "")

    reindex_combined_df.lastShockVoltageMv = reindex_combined_df.lastShockVoltageMv.str.replace("lastShockVoltageMv=",
                                                                                                "")

    reindex_combined_df.mmuTempDegC = reindex_combined_df.mmuTempDegC.str.replace("mmuTempDegC=", "")

    reindex_combined_df.mcuTempDegC = reindex_combined_df.mcuTempDegC.str.replace("mcuTempDegC=", "")

    # the very last sequence=false has a couple extra characters that we need to remove
    reindex_combined_df.sequence = reindex_combined_df.sequence.str.replace("])", "", regex=False)

    # check that the extra characters were removed from the last row of the sequence column
    # printing to console should be "true" or "false" without any additional characters if this worked
    print(reindex_combined_df.sequence.iloc[-1])

    # add the index column name back in
    reindex_combined_df.index.name = "index"

    # arrange the data frame by date from oldest to most recent
    sort_by_date_combined_df = reindex_combined_df.sort_values('date')

    reset_index_combined_df = sort_by_date_combined_df.reset_index(drop=True)

    # fill 'nan' values with 'NA' strings so they're won't be any blank/missing values in the data
    fillna_combined_df = reset_index_combined_df.fillna('NA')

    all_data = all_data.append(fillna_combined_df)

    all_data = all_data.reset_index(drop=True)

# create a filename based on the date range you specified for the HTTP request
# convert the datetime object to a string but use a more friendly format for filenames
my_start_date_filename = my_start_date_datetime.strftime("%Y-%m-%d")
print(my_start_date_filename)

my_end_date_datetime = my_end_date_datetime.strftime("%Y-%m-%d")
print(my_end_date_datetime)

# concatenate strings to create a flexible filename
filename = "data/" + my_start_date_filename + "_" + my_end_date_datetime + "_Vence-message-data" + ".csv"

# check if the "data" directory exists,
# if it does not, create new directory
cwd = os.getcwd()

path = os.path.join(cwd, "data")

if not os.path.isdir(path):
    try:
        os.mkdir(path)
    except OSError as error:
        print(error)

    # print in the console to check the filename string
print(filename)

# write out the data frame as a csv file using the flexible filename convention
all_data.to_csv(filename)
