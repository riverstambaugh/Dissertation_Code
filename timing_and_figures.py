from check_isomorphic import *
from brute_force import *
from check_isomorphic_graphwise import *
import itertools
import time
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
import csv
import random
import timeit
import statistics
import  os
from matplotlib.colors import ListedColormap

############################################################################################

############################ GENERATING PRESENTATIONS ######################################

#This code takes an alphabet A and generates all words of length min_length
#up to length 'max_length' using letters in the alphabet. 
#It then creates tuples containing every possible 
#combination of these words, and creates presentations with relation size n
#Then, all of these presentations are stored in a dictionary. 

def get_words(A, min_length, max_length, n):

    if n > 2:
        print("Too many presentations to feasibly examine.")
        return None

    if min_length > max_length:
        print('Invalid min/max arguments for word length.')
        return None

    allwords = []
    for length in range(min_length, max_length + 1):
        for word_tuple in itertools.product(A, repeat = length):
            if type(A[0]) == str:
                word = ''.join(word_tuple)
                allwords.append(word)
            else:
                allwords.append(word_tuple)

    pairs = sorted(list(itertools.product(allwords, repeat=2))) 
    pres_dict = dict()

    if type(A[0]) == str:
        pres_alph = ''.join(A)
    
    else:
        pres_alph = A

    #Create presentations for each pair of words
    ctr = 0
    for i in range(len(pairs)):
        if n == 1:
            presname = str(i)
            presname = Presentation(pres_alph)

            presentation.add_rule(presname, pairs[i][0], pairs[i][1])

            pres_dict[str(i)] = presname
            continue

        
        for j in range(len(pairs)):
            presname = str(ctr)
            presname = Presentation(pres_alph)
          
            presentation.add_rule(presname, pairs[i][0], pairs[i][0])
            presentation.add_rule(presname, pairs[j][0], pairs[j][1])

            pres_dict[str(ctr)] = presname

            ctr += 1

    #Prints the number of presentations stored in the dictionary
    print('Number of presentations with alphabet size', len(A), 'and relation word size(s)', min_length, 'to', max_length)
    print('with one relation:', len(pres_dict))
    return pres_dict


#Helper function for presentation generation. Does the same as 
#itertools.combinations(), but also includes self-pairs. Unused in results.
def generate_pairs(allwords):

    pairs = set()
    for i in range(len(allwords)):
        for j in range(i, len(allwords)):
            pairs.add((allwords[i], allwords[j]))

    return sorted(list(pairs))


#Takes in an alphabet and a word length range in the same way as the above, and generates
#number_of_words random words from the word length range, then creates random relation length
#presentations using these random words, returning a dictionary containing all of them.
def get_random_word_pres(A, min_length, max_length, number_of_words, number_of_pres, relation_min, relation_max):

    random_words = []
    for i in range(number_of_words):
        wordlength = random.sample(list(range(min_length, max_length + 1)), 1) 
        rand_letters = random.sample(A, wordlength[0])
        if type(A[0]) == str:
            rand_letters = ''.join(rand_letters)
        random_words.append(rand_letters)#rand_word)

    random_pres_dict = dict()

    if type(A[0]) == str:
        pres_alph = ''.join(A)
    else:
        pres_alph = A
  
    pairs = list(itertools.product(random_words, repeat = 2))

    for j in range(number_of_pres):
        random_relation_word_length = random.sample(list(range(relation_min, relation_max+1)), 1) 
        pres_words = random.sample(pairs, random_relation_word_length[0])

        #Create presentations for each pair of words
    
        presname = str(j+1)
        pres_obj = Presentation(pres_alph)
        for i in range(len(pres_words)):
            presentation.add_rule(pres_obj, pres_words[i][0], pres_words[i][1])

        random_pres_dict[presname] = pres_obj


    #for key in random_pres_dict.keys():
    #    p = random_pres_dict[key]

    print('\nGenerating presentations with alphabet size', len(A), 'and word length(s)', min_length, '-', max_length)
    print('The range of lengths of relations is:', relation_min,  '-', relation_max)
    print('The number of words generated is', number_of_words,)
    print('We  choose to take a sample of', number_of_pres, 'presentations')

    return random_pres_dict

#Takes in a pres_dict containing all possible presentation combinations of relation
#word length n for an alphabet of size k and gets a random sample of m of these
def get_random_pres(pres_dict, m):

    #Ensures the number of random pairs is at most the length of the dictionary
    num_pairs = min(len(pres_dict), m)

    random_keys = random.sample(list(pres_dict.keys()), num_pairs)

    random_dict = {key: pres_dict[key] for key in random_keys}

    return random_dict

#######################################################################################

########################### VISUALIZING ISOMORPHISMS ##################################
  
#Takes in a dictionary of presentations and checks isomorphisms between them,
#Storing results as colored points in a grid. The grid is then saved as a PNG file.
def generate_isomorphism_grid(pres_dict):

    pres_keys = list(pres_dict.keys())
    num_pres = len(pres_keys)

    pres_range = range(num_pres)

    results = defaultdict(list)

    grid = np.zeros((num_pres, num_pres), dtype = int)

    output_to_color = defaultdict(lambda: len(output_to_color))
    output_counter = 0

    for i, key1 in enumerate(pres_keys):
        for j, key2 in enumerate(pres_keys):
            pres1 = pres_dict[key1] 
            pres2 = pres_dict[key2]

            #This is to ensure all algorithms work on each combination and are not returning 
            #different outputs. However, some presentations will have more than one isomorphism,
            #so the outputs may not be identical. This is OK.

            assert bool(check_isomorphic(pres1, pres2)) == bool(check_isomorphic_graphwise(pres1, pres2)) #== bool(brute_force_checker(pres1, pres2))
         
            res = check_isomorphic(pres1, pres2)

            if res == None:  
                res = 1

            elif res == False:
                res = 0

            else:
                res = 2
       
            if res not in output_to_color:
                output_to_color[res] = output_counter
                output_counter += 1

            grid[i, j] = output_to_color[res]


    #Saves a colored plot showing which one-relation presentations with relation word
    #size 3 and alphabet 'abc' are isomorphic to one another.
    num_colors = len(output_to_color)
    
    #custom color map is isomorphic color first, non-isomorphic second, and 
    #invalid presentation pairs 3rd.
    custom_colors = ['#ffeb3b', '#880e4f']#,'#000000']  #['#23E9F2', '#862d5c', '#388E3C']
    custom_cmap = ListedColormap(custom_colors, name='custom_cmap')

    #Generate plot and save to the 'isomorphisms' directory in 'visualizations'
    plt.figure(figsize = (20, 20), dpi = 1000)
    plt.imshow(grid, cmap=custom_cmap, origin='lower', extent=(pres_range.start, pres_range.stop-1, pres_range.start, pres_range.stop-1)) 
    plt.axis('off')

    directory = 'visualizations/isomorphism_bitmaps'

    #Make sure to change this every time to reflect what plot you want to generate!
    filename = 'OneRelationWord_Size2_3alph_Isomorphism_final.png'

    plt.savefig(os.path.join(directory, filename), bbox_inches='tight', pad_inches=0, dpi=1000)

    plt.close()
    
    return grid
#####################################################################################################

################################## VISUALIZING TIME TAKEN ###########################################

#The following code takes every combination of presentations from allpres and 
#compares the time it takes each method to run on them. It then creates a grid
#displaying a color for each pair representing which method was the fastest for 
#that pair.
def generate_time_grid(pres_dict):

    pres_keys = list(pres_dict.keys())
    num_pres = len(pres_keys)

    times_grid = np.zeros((num_pres, num_pres, 3))

    for i, key1 in enumerate(pres_keys):
        for j, key2 in enumerate(pres_keys):
            pres1 = pres_dict[key1]
            pres2 = pres_dict[key2]

            start_time = time.perf_counter()
            brute_force_checker(pres1, pres2)
            times_grid[i, j, 0] = time.perf_counter() - start_time

            start_time = time.perf_counter()
            check_isomorphic(pres1, pres2)
            times_grid[i, j, 1] = time.perf_counter() - start_time

            start_time = time.perf_counter()
            check_isomorphic_graphwise(pres1, pres2)
            times_grid[i, j, 2] = time.perf_counter() - start_time

    fastest_function = np.argmin(times_grid, axis = 2)


    fig, ax = plt.subplots(figsize=(30, 30), dpi=1000)
    cax = ax.imshow(fastest_function, cmap = 'cool', interpolation = 'nearest')
    ax.axis('off')

    filename = 'OneWordLength3_3alph_timing.png' 
    directory = 'visualizations/time_bitmaps'

    plt.savefig(os.path.join(directory, filename), bbox_inches='tight', pad_inches=0, dpi=1000)

    plt.close()

####################################################################################################

#################################### TIMING THE METHODS ############################################

#The following code times each isomorphism algorithm on presentations p and q.
#The amount of times each algorithm is tested can be changed using the 
#input parameter amount_runs. The average time it takes each algorithm 
#to compute isomorphism for each presentation is returned as a 
#tuple containing times for each algorithm whether or not the two presentations
#compared were isomorphic is also returned.
def average_time_data(p, q, amount_runs):

    #This is to ensure all algorithms work on each combination and are not returning 
    #different outputs. However, some presentations will have more than one 
    #isomorphism, so the outputs may not be identical. This is OK. If you are running
    #time tests on large presentations, make sure to comment out the 
    #brute_force_checker portion of this code!
    assert bool(check_isomorphic_graphwise(p, q)) == bool(check_isomorphic(p, q)) == bool(brute_force_checker(p, q))

    isomorphism_check = check_isomorphic_graphwise(p, q)

    def backtrack_method():
        check_isomorphic(p, q)

    def graphwise_method():
        check_isomorphic_graphwise(p, q)

    def bruteforce_method():
        brute_force_checker(p, q)

    #Again, if code is being run on large presentations, make sure to 
    #comment out brute_time or backtrack_time if necessary and replace them 
    #to simply be zero. The code will still produce averages for the 
    #algorithms you are interested in.
    backtrack_time = timeit.timeit(backtrack_method, number=amount_runs)
    graph_time = timeit.timeit(graphwise_method, number=amount_runs)
    brute_time = timeit.timeit(bruteforce_method, number=amount_runs)  
  
    return ((brute_time)/amount_runs, (backtrack_time)/amount_runs, (graph_time)/amount_runs, isomorphism_check)

#This takes in a dictionary pres_dict containing a multitude of presentations, and uses 
#average_time_data on each pair of presentations in pres_dict, returning the average time 
#over n runs for each one. This data is then averaged to compute average times for each 
#algorithm on the random sample overall. Prints output to console.
def average_time_overall(pres_dict, num_runs):

    time_dict = {x : [] for x in range(3)}
    pres_combos = []
    invalid_combos = []

    total_compares = 0
    isomorphisms = 0
    non_isomorphisms = 0
    invalids = 0

    pres_keys = list(pres_dict.keys()) 

    for i in range(len(pres_keys)):
        key1 = pres_keys[i]
        #If desired, examine what the random presentations are
        #print(pres_dict[key1].alphabet())
        #print(pres_dict[key1].rules)
        for j in range(i, len(pres_keys)):
            key2 = pres_keys[j]
            pres1 = pres_dict[key1]
            pres2 = pres_dict[key2]
         
            pres_combos.append((key1, key2))

            pair_averages = average_time_data(pres1, pres2, num_runs)
            time_dict[0].append(pair_averages[0])
            time_dict[1].append(pair_averages[1])
            time_dict[2].append(pair_averages[2])
        
            #if-else block that will increment counters that are
            #printed to the terminal displaying the number of 
            #isomorphic, non-isomorphic, and invalid pairs.
            if pair_averages[3] is not None:
                if pair_averages[3]:
                    isomorphisms += 1
                else:
                    non_isomorphisms += 1

            else:
                invalids += 1
                invalid_combos.append((key1, key2))

            total_compares += 1

    print('\nNumber of random presentations:', len(pres_dict))
    print('\nTotal comparisons:', total_compares, 'Invalid comparisons:', invalids, 'they were:', invalid_combos)
    print('Number of presentation pairs that were isomorphic:', isomorphisms, 'not isomorphic:', non_isomorphisms, '\n')

    average_list = [0]*3
    std_dev_list = [0]*3
    for i in range(3):
        std_dev_list[i] = statistics.stdev(time_dict[i])
        average_list[i] = sum(time_dict[i]) / total_compares
        
    print('Each presentation was run for each algorithm', num_runs, 'time(s)\n')

    print('Average time for brute force in random sample of', total_compares, 'presentation comparisons:')
    print(average_list[0])
    print('Standard deviation of times in the random sample:', std_dev_list[0], '\n')

    print('Average time for backtrack in random sample of', total_compares, 'presentation comparisons:')
    print(average_list[1])
    print('Standard deviation of times in the random sample:', std_dev_list[1], '\n')

    print('Average time for graphwise in random sample of', total_compares, 'presentation comparisons:')
    print(average_list[2])
    print('Standard deviation of times in the random sample:', std_dev_list[2], '\n')

    return (time_dict, pres_combos)


#The following creates a plot, using each pair of presentations compared as the dots on the x-axis.
#The plot is a scatter plot that will display the time each presentation takes as an individually 
#colored and shaped dot for each presentation pair.
def get_time_scatter(time_dict, pres_combos):

    x = np.arange(len(pres_combos))

    markers = ['o', 's', '^']

    colors = ['blue', 'green', 'red']

    plt.figure(figsize=(20, 10))

    #comment out / change marker and color indexing as necessary.
    plt.scatter(x, time_dict[0], label='BFA', marker=markers[0], color=colors[0])
    plt.scatter(x, time_dict[1], label='BTA', marker=markers[1], color=colors[1])
    plt.scatter(x, time_dict[2], label='GWA', marker=markers[2], color=colors[2])

    plt.xticks(x, pres_combos, rotation=45, ha='right')
    plt.xlabel('Pairs of Presentations')
    plt.ylabel('Time (seconds)')
    plt.title('Algorithm Time Comparison')

    plt.legend()
    plt.grid(True)

    #Change title of PNG as necessary given random presentation
    #generation parameters.
    plt.savefig('All3_A{size of alphabet}_RW{sizes of rel. words}_RL{sizes of rel. list}_{Number of comparisons}')

##########################################################################################

############################ RUN THE CODE HERE ###########################################

#Define alphabet A here, either as integers or strings

#A = ['a', 'b', 'c']#, 'd', 'e', 'f', 'g', 'h', 'i', 'k']
A = list(range(3))

#Define the max length of word you desire here
max_length = 2
min_length = 2

#relation_length_max = 250
#relation_length_min = 100

#Get the dictionary of all presentations with relation length n
#with words of the specified word sizes

#Define relation length. CAREFUL! anything larger than 2 or 3 
#on large word sizes will be very big.
n = 1
pres_dict = get_words(A, min_length, max_length, n)
if pres_dict == None:
    print('specified n was too large. Try again with n < 2.')
#Get a random set of these presentations of length rand_length:
#number_of_pres = 10
#Specify the amount of times each algorithm should be run for each presentation pair:
#num_runs = 1

#Specify the number of random words ranging from length min_length to max_length
#we desire to generate:
#number_of_words = 1000

#Get the random dictionary for each presentation
#rand_dict = get_random_word_pres(A, min_length, max_length, number_of_words, number_of_pres, relation_length_min, relation_length_max)

#Compute the average times overall for each algorithm
#res = average_time_overall(rand_dict, num_runs) 

#Scatter plot of the times for each comparison in the above
#get_time_scatter(res[0], res[1])

#Get the average time for each method to compute whether every pair in rand_dict
#is isomorphic or not when running it 

#Generate plot of isomorphisms between the presentations
#if pres_dict is not None:
#    grid = generate_isomorphism_grid(pres_dict)

#with open("3x3PresentationMatrix", "w") as f:
#    f.write(str(grid))

#Generate plot of fasted method for each pair of presentations
generate_time_grid(pres_dict)

