"""
Project for Week 4 of "Python Data Analysis".
Processing CSV files with baseball stastics.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""
import time
import csv

##
## Provided code from Week 3 Project
##

def read_csv_as_list_dict(filename, separator, quote):
    """
    Inputs:
      filename  - name of CSV file
      separator - character that separates fields
      quote     - character used to optionally quote fields
    Output:
      Returns a list of dictionaries where each item in the list
      corresponds to a row in the CSV file.  The dictionaries in the
      list map the field names to the field values for that row.
    """
    table = []
    with open(filename, newline='') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=separator, quotechar=quote)
        for row in csvreader:
            table.append(row)
    return table

#print(read_csv_as_list_dict('table1.csv', ",", '"'))
def read_csv_as_nested_dict(filename, keyfield, separator, quote):
    """
    Inputs:
      filename  - name of CSV file
      keyfield  - field to use as key for rows
      separator - character that separates fields
      quote     - character used to optionally quote fields
    Output:
      Returns a dictionary of dictionaries where the outer dictionary
      maps the value in the key_field to the corresponding row in the
      CSV file.  The inner dictionaries map the field names to the
      field values for that row.
    """
    table = {}
    with open(filename, newline='') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=separator, quotechar=quote)
        for row in csvreader:
            rowid = row[keyfield]
            table[rowid] = row
    return table

##
## Provided formulas for common batting statistics
##

# Typical cutoff used for official statistics
MINIMUM_AB = 500

def batting_average(info, batting_stats):
    """
    Inputs:
      batting_stats - dictionary of batting statistics (values are strings)
    Output:
      Returns the batting average as a float
    """
    hits = float(batting_stats[info["hits"]])
    at_bats = float(batting_stats[info["atbats"]])
    if at_bats >= MINIMUM_AB:
        return hits / at_bats
    else:
        return 0

def onbase_percentage(info, batting_stats):
    """
    Inputs:
      batting_stats - dictionary of batting statistics (values are strings)
    Output:
      Returns the on-base percentage as a float
    """
    hits = float(batting_stats[info["hits"]])
    at_bats = float(batting_stats[info["atbats"]])
    walks = float(batting_stats[info["walks"]])
    if at_bats >= MINIMUM_AB:
        return (hits + walks) / (at_bats + walks)
    else:
        return 0

def slugging_percentage(info, batting_stats):
    """
    Inputs:
      batting_stats - dictionary of batting statistics (values are strings)
    Output:
      Returns the slugging percentage as a float
    """
    hits = float(batting_stats[info["hits"]])
    doubles = float(batting_stats[info["doubles"]])
    triples = float(batting_stats[info["triples"]])
    home_runs = float(batting_stats[info["homeruns"]])
    singles = hits - doubles - triples - home_runs
    at_bats = float(batting_stats[info["atbats"]])
    if at_bats >= MINIMUM_AB:
        return (singles + 2 * doubles + 3 * triples + 4 * home_runs) / at_bats
    else:
        return 0


##
## Part 1: Functions to compute top batting statistics by year
##

def filter_by_year(statistics, year, yearid):
    """
    Inputs:
      statistics - List of batting statistics dictionaries
      year       - Year to filter by
      yearid     - Year ID field in statistics
    Outputs:
      Returns a list of batting statistics dictionaries that
      are from the input year.
    """
    list_of_dictionaries=[]
    length=len(statistics)

    for row in range(length):
        if(statistics[row][yearid]==str(year)):
            list_of_dictionaries.append(statistics[row])
    return list_of_dictionaries


def top_player_ids(info, statistics, formula, numplayers):
    """
    Inputs:
      info       - Baseball data information dictionary
      statistics - List of batting statistics dictionaries
      formula    - function that takes an info dictionary and a
                   batting statistics dictionary as input and
                   computes a compound statistic
      numplayers - Number of top players to return
    Outputs:
      Returns a list of tuples, player ID and compound statistic
      computed by formula, of the top numplayers players sorted in
      decreasing order of the computed statistic.
    """
    tuple1=()
    list1=[]
    final_list=[]
    for idx in range(len(statistics)):
        top_player=float(formula(info,statistics[idx]))
        tuple1=(statistics[idx][info["playerid"]],top_player)
        list1.append(tuple1)
        tuple1=()
    list1.sort(key=lambda pair: pair[1] , reverse=True)

    for jdx in range(numplayers):
        final_list.append(list1[jdx])
    return(final_list) 


def lookup_player_names(info, top_ids_and_stats):
    """
    Inputs:
      info              - Baseball data information dictionary
      top_ids_and_stats - list of tuples containing player IDs and
                          computed statistics
    Outputs:
      List of strings of the form "x.xxx --- FirstName LastName",
      where "x.xxx" is a string conversion of the float stat in
      the input and "FirstName LastName" is the name of the player
      corresponding to the player ID in the input.
    """
    master_file=read_csv_as_list_dict(info["masterfile"],info["separator"], info["quote"])
    top_plyr_ids_only=[]
    top_plyr_names_only=[]
    top_plyr_names_only_temp=()
    length_of_ids_and_stats=len(top_ids_and_stats)
    length_of_master_file=len(master_file)
    for idx in range(length_of_ids_and_stats):
        top_plyr_ids_only.append(top_ids_and_stats[idx][0])
    
    
    for idx1 in range(length_of_ids_and_stats):
        for idx2 in range(length_of_master_file):
            if(top_plyr_ids_only[idx1]==master_file[idx2][info["playerid"]]):
                top_plyr_names_only_temp=(master_file[idx2][info["firstname"]]+" "+str(master_file[idx2][info["lastname"]]))
        top_plyr_names_only.append(top_plyr_names_only_temp)
        top_plyr_names_only_temp=()

    list_of_strings=[]
    for data in range(length_of_ids_and_stats):
        stats="{:4.3f}".format(top_ids_and_stats[data][1])
        strings=(str(stats)+" --- "+top_plyr_names_only[data])

        list_of_strings.append(strings)
        strings=""
    return(list_of_strings)
    

def compute_top_stats_year(info, formula, numplayers, year):
    """
    Inputs:
      info        - Baseball data information dictionary
      formula     - function that takes an info dictionary and a
                    batting statistics dictionary as input and
                    computes a compound statistic
      numplayers  - Number of top players to return
      year        - Year to filter by
    Outputs:
      Returns a list of strings for the top numplayers in the given year
      according to the given formula.
    """
    batting_statistics=read_csv_as_list_dict(info["battingfile"],info["separator"], info["quote"])
    stats_of_given_year=filter_by_year(batting_statistics, year, info["yearid"])
    top_ids_and_stats=top_player_ids(info, stats_of_given_year, formula, numplayers)
    return lookup_player_names(info, top_ids_and_stats)


##
## Part 2: Functions to compute top batting statistics by career
##


def aggregate_by_player_id(statistics, playerid, fields):
    """
    Inputs:
      statistics - List of batting statistics dictionaries
      playerid   - Player ID field name
      fields     - List of fields to aggregate //names of columns
    Output:
      Returns a nested dictionary whose keys are player IDs and whose values
      are dictionaries of aggregated stats.  Only the fields from the fields
      input will be aggregated in the aggregated stats dictionaries.
    """

    sum1=0
    dict1={} #initial dict(temporary b4 value is stored in dict2)
    dict2={} #dicts of dicts
    length_of_fields=len(fields)
    count=0
    length=(len(statistics)) #102816
    print(length)
    start_time=time.time()
    for idx_statistics in range(length):
        for idxfield in range(length_of_fields):
            for idx in range(length):
                if((statistics[count][playerid])==statistics[idx][playerid]):
                    for key,values in statistics[idx].items():
                        if(key==fields[idxfield]):
                            sum1+=int(values)
                            dict1[fields[idxfield]]=sum1
     
            sum1=0
        dict1[playerid]=statistics[idx_statistics][playerid]
        count+=1
        dict2[statistics[idx_statistics][playerid]]=dict1
        dict1={}
    end_time=time.time()
    print(end_time-start_time) 
    return(dict2)




##aggregate_by_player_id([{'player': '1', 'stat2': '4', 'stat1': '3', 'stat3': '5'},{'player': '1', 'stat2': '1', 'stat1': '2', 'stat3': '8'},
##{'player': '1', 'stat2': '7', 'stat1': '5', 'stat3': '4'}],
##'player', ['stat1'])
###expected {'1': {'player': '1', 'stat1': 10}}        

def compute_top_stats_career(info, formula, numplayers):
    """
    Inputs:
      info        - Baseball data information dictionary
      formula     - function that takes an info dictionary and a
                    batting statistics dictionary as input and
                    computes a compound statistic
      numplayers  - Number of top players to return
      
    """
    list1=[]

    statistics=read_csv_as_list_dict(info["battingfile"],info["separator"], info["quote"])
    aggregated_stats_by_plyr_id=(aggregate_by_player_id(statistics, info["playerid"], info["battingfields"]))
    list_of_player_ids=list(aggregated_stats_by_plyr_id)
    length_of_stats=len(info["battingfields"])
    dict1={}
    for players in range(len(list_of_player_ids)):
        for idx in range(length_of_stats):
            plyridx=list_of_player_ids[players]
            dict1[info["battingfields"][idx]]=aggregated_stats_by_plyr_id[plyridx][info["battingfields"][idx]]
            #list1.append(dict1)
            #dict1={}
        dict1[info["playerid"]]=list_of_player_ids[players]
        list1.append(dict1)
        #list2.append(list1)
        #list1=[]
        dict1={}
    print(list1)
    print("")

    top_ids_and_stats=top_player_ids(info,list1,formula,numplayers)
    return lookup_player_names(info, top_ids_and_stats)

##
## Provided testing code
##

def test_baseball_statistics():
    """
    Simple testing code.
    """

    #
    # Dictionary containing information needed to access baseball statistics
    # This information is all tied to the format and contents of the CSV files
    #
    baseballdatainfo = {"masterfile": "Master_2016.csv",   # Name of Master CSV file
                        "battingfile": "Batting_2016.csv", # Name of Batting CSV file
                        "separator": ",",                  # Separator character in CSV files
                        "quote": '"',                      # Quote character in CSV files
                        "playerid": "playerID",            # Player ID field name
                        "firstname": "nameFirst",          # First name field name
                        "lastname": "nameLast",            # Last name field name
                        "yearid": "yearID",                # Year field name
                        "atbats": "AB",                    # At bats field name
                        "hits": "H",                       # Hits field name
                        "doubles": "2B",                   # Doubles field name
                        "triples": "3B",                   # Triples field name
                        "homeruns": "HR",                  # Home runs field name
                        "walks": "BB",                     # Walks field name
                        "battingfields": ["AB", "H", "2B", "3B", "HR", "BB"]}



    print("Top 5 batting averages in 1923")
    top_batting_average_1923 = compute_top_stats_year(baseballdatainfo, batting_average, 5, 1923)
    for player in top_batting_average_1923:
        print(player)
    print("")

    print("Top 10 batting averages in 2010")
    top_batting_average_2010 = compute_top_stats_year(baseballdatainfo, batting_average, 10, 2010)
    for player in top_batting_average_2010:
        print(player)
    print("")

    print("Top 10 on-base percentage in 2010")
    top_onbase_2010 = compute_top_stats_year(baseballdatainfo, onbase_percentage, 10, 2010)
    for player in top_onbase_2010:
        print(player)
    print("")

    print("Top 10 slugging percentage in 2010")
    top_slugging_2010 = compute_top_stats_year(baseballdatainfo, slugging_percentage, 10, 2010)
    for player in top_slugging_2010:
        print(player)
    print("")

    # You can also use lambdas for the formula
    #  This one computes onbase plus slugging percentage
    print("Top 10 OPS in 2010")
    top_ops_2010 = compute_top_stats_year(baseballdatainfo,
                                          lambda info, stats: (onbase_percentage(info, stats) +
                                                               slugging_percentage(info, stats)),
                                          10, 2010)
    for player in top_ops_2010:
        print(player)
    print("")

    print("Top 20 career batting averages")
    top_batting_average_career = compute_top_stats_career(baseballdatainfo, batting_average, 20)
    for player in top_batting_average_career:
        print(player)
    print("")


# Make sure the following call to test_baseball_statistics is
# commented out when submitting to OwlTest/CourseraTest.

test_baseball_statistics()
