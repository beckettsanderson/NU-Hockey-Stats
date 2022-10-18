# -*- coding: utf-8 -*-
"""
Homework 1:
    Due January 28th
    
Problems and graph relating to the Northeastern Women's Hockey team.

@author: Beckett Sanderson
"""

import csv
import matplotlib.pyplot as plt

HOCKEY_FILE = "huskies_hockey_stats.csv"

def read_csv(file_name):
    """
    Reads in the csv into a 2d list
    
    Parameters
    ----------
    file_name : string
        the file name to open.

    Returns
    -------
    data_list : 2d list
        2d list containing the data from the csv.

    """
    # initializes empty list
    data_list = []
    
    # opens the csv file
    with open(file_name, "r") as file:
        
        # creates a reader to go through the lines of the csv
        reader = csv.reader(file)
        
        # loops through the rows of the reader
        for row in reader:
            
            # adds the data to the empty list
            data_list.append(row)
        
    return data_list


def transform_hockey(game_data, date_col):
    """
    Sets the 2d list into a dictionary containing all the data
    
    Parameters
    ----------
    game_data : 2d list
        the data input
    date_col : int
        column holding the date

    Returns
    -------
    date_dict : dictionary
        a nested dictionary containing the games based on a key by date

    """
    # initializes the empty dictionary
    dictionary = {}
    
    # remove the labels to use to fill the dictionary
    headers = game_data.pop(0)
    
    # loops through each row int he 2d list
    for row in game_data:
        
        # sets the date and empty nested dictionary
        date = row[date_col]
        nested_dict = {}
        
        # loops through each index in the row and assigns them to the dict
        for idx in range(len(row)):
            
            nested_dict[headers[idx]] = row[idx]
        
        # assigns the nested dicts to the dictionary
        dictionary[date] = nested_dict

    return dictionary


def clean_data(dictionary, fields_list):
    """
    Organizes the dictionary to contain the values requested in the 
    fields list
    
    Parameters
    ----------
    dictionary : dictionary
        nested dictionary containing the data by date
    fields_list : list of strings
        list of strings containing the fields the user is looking for

    Returns
    -------
    new_dict : dictionary
        dictionary contianing only the info requested in fields list

    """
    # initializes a dict to hold the nested dictionary
    new_dict = {}
    # set up the fields that hold integers into a list for initialization
    num_based_fields = ["G", "A", "PP", "BLK", "P"]
    
    # loops through each date in the dictionary
    for date in dictionary:
        
        # creates the dictionary to nest inside the new dict
        nested_dict = {}
        
        # loops through every field in the fields list
        for field in fields_list:
            
            # checks if the field has to be an int and casts as int if needed
            if field in num_based_fields:
                
                nested_dict[field] = int(dictionary[date][field])
            
            # assigns values normally if not needed to be casted
            else:
                
                nested_dict[field] = dictionary[date][field]
                
        # fills the new dictionary with the assigned nested dictionary
        new_dict[date] = nested_dict
        
    return new_dict


def max_nested(cleaned_dict, field_of_interest):
    """
    Finds the max value of a field and returns the date and value in a tuple
    
    Parameters
    ----------
    cleaned_dict : dictionary
        dictionary contianing only the info requested in fields list
    field_of_interest : string
        field of interest to search for in the dictionary

    Returns
    -------
    max_tup : tuple
        tuple containing the date and the max value of what was requested.

    """
    # initializes max trackers
    max_date = None
    max_field = None
    
    # loops through each game in the dictionary
    for game in cleaned_dict:
        
        # gets the value of the requested field for that game
        cur_value = cleaned_dict[game][field_of_interest]
        
        # checks if the new value is higher than the max
        if max_field == None or cur_value > max_field:
            
            # replaces the max values with the new values
            max_field = cur_value
            max_date = game
    
    # sets the max to a tuple for returning
    max_tup = (max_date, max_field)
    
    return max_tup


def count_wins(cleaned_dict):
    """
    Counts the number of games that resulted in wins
    
    Parameters
    ----------
    cleaned_dict : dictionary
        dictionary contianing only the info requested in fields list

    Returns
    -------
    num_wins : integer
        number of wins in the dictionary

    """
    num_wins = 0
    
    # loops through each game in the dictionary
    for game in cleaned_dict:
        
        # checks if the game resulted in a win and if so adds to the count
        if cleaned_dict[game]["W/L"] == "W":
            
            num_wins += 1
    
    return num_wins


def count_pp(cleaned_dict, num_pp):
    """
    Counts the number of games matching the input power play
    
    Parameters
    ----------
    cleaned_dict : dictionary
        dictionary contianing only the info requested in fields list
    num_pp : int
        number of power plays to count

    Returns
    -------
    num_games : integer
        number of games with the identified number of power plays

    """
    num_games = 0
    
    # loops through each game in the dictionary
    for game in cleaned_dict:
        
        # checks if the power play number in the dictionary matches the 
        # number parameter and if so adds a count
        if cleaned_dict[game]["PP"] == num_pp:
            
            num_games += 1
    
    return num_games


def graph_goals_hist(cleaned_dict):
    """
    Graphs a histogram of goals scored in a game using a cleaned dictionary

    Parameters
    ----------
    cleaned_dict : dictionary
        dictionary contianing only the info requested in fields list.

    Returns
    -------
    None.

    """
    # initializes an empty list to fill with the goal numbers
    goals_list = []
    
    # creates a list filled with the numbers of goals scored
    for game in cleaned_dict:
        
        num_goals = cleaned_dict[game]["G"]
        goals_list.append(num_goals)
    
    # plots the historgram using the list with number of goals
    plt.hist(goals_list, bins = 13, width = .85)
    
    # graph organization
    plt.title("Goals and Frequency")
    plt.xlabel("Number of Goals Scored")
    plt.ylabel("Number of Times Scored")

    plt.show()
    

def graph_blks_assists(cleaned_dict):
    """
    Graphs a scatterplot of blocks in a game by assist in a game using a 
    cleaned dictionary

    Parameters
    ----------
    cleaned_dict : dictionary
        dictionary contianing only the info requested in fields list.

    Returns
    -------
    None.

    """
    # initializes variables for the legend
    legend_win_count = 0
    legend_loss_count = 0    
    
    # loops through every game in the dictionary
    for game in cleaned_dict:
        
        # sets colors and labels for wins versus losses
        if cleaned_dict[game]["W/L"] == "W":
            color = "green"
            label = "Win"
        
        else:
            color = "red"
            label = "Loss"
        
        # plots the points in a way that allows a legend to be created for 
        # wins and losses
        if legend_win_count == 0 and label == "Win":
            
            plt.plot(cleaned_dict[game]["BLK"], cleaned_dict[game]["A"], "s",
                 color = color, label = label)
            legend_win_count += 1
            
        elif legend_loss_count == 0 and label == "Loss":
            
            plt.plot(cleaned_dict[game]["BLK"], cleaned_dict[game]["A"], "s",
                 color = color, label = label)
            legend_loss_count += 1
            
        else:
            
            plt.plot(cleaned_dict[game]["BLK"], cleaned_dict[game]["A"], "s",
                 color = color)
    
    # graph organization
    plt.title("Blocks and Assists by Game")
    plt.xlabel("Blocks")
    plt.ylabel("Assists")
    plt.legend()
    
    plt.show()


def Main():
    
    print("Welcome to Homework 1")
    
    # gather the data from the csv
    hockey_data = read_csv(HOCKEY_FILE)
    
    # create a dictionary out of the gathered data
    hockey_dict = transform_hockey(hockey_data, 1)
    
    # creates a cleaned dictionary containing the fields requested in the list
    fields_list = ["Opponent", "W/L", "G", "A", "PP", "BLK"]
    cleaned_hockey_dict = clean_data(hockey_dict, fields_list)
    print(cleaned_hockey_dict, "\n")
    
    # date of most goals scored
    max_goals = max_nested(cleaned_hockey_dict, "G")
    print("We scored the most goals on:", max_goals[0])
    
    # date of most assists
    max_assists = max_nested(cleaned_hockey_dict, "A")
    print("We had the most assists on:", max_assists[0])
    
    # date of most blocks
    max_blocks = max_nested(cleaned_hockey_dict, "BLK")
    print("We had the most blocks on:", max_blocks[0])
    
    # number of wins
    num_wins = count_wins(cleaned_hockey_dict)
    print("We won", num_wins, "games")
    
    # number of games with one power play
    num_games_one_pp = count_pp(cleaned_hockey_dict, 1)
    print("We had", num_games_one_pp, "games with exactly one power play")
    
    # create a histogram of the number of goals scored by game
    graph_goals_hist(cleaned_hockey_dict)
    
    # create a scatterplot of blocks by assists
    graph_blks_assists(cleaned_hockey_dict)
    
Main()
