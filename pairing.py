import copy

def mk_pair(player, i, pod, npod,stand):
    found_pair = False
    pos_to_move = 0
    while not found_pair:
        found_pair = True
        tpod = copy.deepcopy(pod)
        nplayer = stand[i + 1 + pos_to_move][0]
        
        if nplayer in npod[player]:
            #print "player {} has already played {}".format(player, nplayer)
            found_pair = False
            pos_to_move += 1
            continue
        
        tpod.pop(player, None)
        tpod.pop(nplayer, None)
        
        for key in tpod:
            if player in tpod[key]:
                tpod[key].remove(player)
            if nplayer in tpod[key]:
                tpod[key].remove(nplayer)
        
        no_good = False
        option_dict = {}
        for key in tpod:
            # number of options
            n_options = len(tpod[key])
            
            # Check to see if there are any players left with no options
            if not tpod[key]:
                no_good = True
                break
            
            try:
               option_dict[n_options]
               #now try to see if the option set is in the dict
               if (set(tpod[key]) in option_dict[n_options]):
                   #check to see if there already are n other elements with only the same n choices:
                   if len(option_dict[n_options]) >= n_options:
                       #not a good pair.. blow up;
                       no_good = True
                       break
                   else:
                       option_dict[n_options].append(set(tpod[key]))
            except KeyError:
                option_dict[n_options] = [set(tpod[key])]
            
        if no_good:
            found_pair = False
            pos_to_move += 1
            print "Pair cannot be set, would create a gridlock ({}, {})".format(player, nplayer)
            continue
        
        
        pod.pop(player,None)
        pod.pop(nplayer,None)
        for key in pod:
            if player in pod[key]:
                pod[key].remove(player)
            if nplayer in pod[key]:
                pod[key].remove(nplayer)
        
        
        my_pair = False   
        if found_pair:
            # Add pair to list
            my_pair = (player,nplayer)
            # Move people in standings
            print "Found Pair {0} {1}".format(player,nplayer)
            oldindex = i + 1 + pos_to_move
            stand.insert(i + 1, stand.pop(oldindex))
    return (my_pair, stand)

def complex_pairing(matches, stand):
    
    # Create new vars Player Option Dictionary (pod) and player matches dictionary (npod)
    pod = {}
    npod = {}
    # Here we store all the players(values - list) that the player(key) has played.
    for row in matches:
        if row[0] in npod:
            npod[row[0]].append(row[1])
        else:
            npod[row[0]]=[row[1]]
    
    # Here we store all the options(values - list) that the player(key) has.
    for player in stand:
        if not player[0] in pod:
            pod[player[0]]=[];
        for potential in stand:
               if potential[0]==player[0]:
                   continue
               if not potential[0] in npod[player[0]]:
                   pod[player[0]].append(potential[0])
    
    # New variable List Of Pairs(lop)
    lop = []
    
    # Loop through all the players and find a pair for each.
    i = 0
    while i < (len(stand)):
        player = stand[i][0];
        found_pair=False
        pos_to_move = 0
        my_pair, stand = mk_pair(player, i, pod, npod, stand);
        lop.append(my_pair)
        i+=2
        if not my_pair:
            raise Error("Cannot find a possible pair for player {}".format(player))
    
    return lop

m1 = [['a', 'j'], ['a', 'c'], ['a', 'h'], ['a', 'i'], ['a', 'g'], ['a', 'b'], ['b', 'c'], ['b', 'd'], ['b', 'a'], ['b', 'h'], ['b', 'e'], ['b', 'f'], ['c', 'b'], ['c', 'a'], ['c', 'f'], ['c', 'g'], ['c', 'j'], ['c', 'h'], ['d', 'b'], ['d', 'j'], ['d', 'e'], ['d', 'f'], ['d', 'g'], ['d', 'i'], ['e', 'h'], ['e', 'd'], ['e', 'b'], ['e', 'f'], ['e', 'g'], ['e', 'i'], ['f', 'c'], ['f', 'd'], ['f', 'i'], ['f', 'e'], ['f', 'g'], ['f', 'b'], ['g', 'c'], ['g', 'a'], ['g', 'j'], ['g', 'd'], ['g', 'f'], ['g', 'e'], ['h', 'e'], ['h', 'a'], ['h', 'c'], ['h', 'b'], ['h', 'j'], ['h', 'i'], ['i', 'a'], ['i', 'f'], ['i', 'h'], ['i', 'j'], ['i', 'd'], ['i', 'e'], ['j', 'a'], ['j', 'c'], ['j', 'd'], ['j', 'g'], ['j', 'h'], ['j', 'i']]
m2 = [['a', 'd'], ['a', 'e'], ['a', 'i'], ['a', 'f'], ['a', 'h'], ['a', 'g'], ['b', 'i'], ['b', 'c'], ['b', 'j'], ['b', 'e'], ['b', 'h'], ['b', 'f'], ['c', 'b'], ['c', 'g'], ['c', 'f'], ['c', 'e'], ['c', 'j'], ['c', 'd'], ['d', 'a'], ['d', 'i'], ['d', 'h'], ['d', 'j'], ['d', 'c'], ['d', 'e'], ['e', 'a'], ['e', 'c'], ['e', 'b'], ['e', 'd'], ['e', 'f'], ['e', 'h'], ['f', 'g'], ['f', 'c'], ['f', 'a'], ['f', 'i'], ['f', 'e'], ['f', 'b'], ['g', 'f'], ['g', 'c'], ['g', 'h'], ['g', 'j'], ['g', 'a'], ['g', 'i'], ['h', 'd'], ['h', 'j'], ['h', 'g'], ['h', 'a'], ['h', 'e'], ['h', 'b'], ['i', 'b'], ['i', 'd'], ['i', 'j'], ['i', 'a'], ['i', 'f'], ['i', 'g'], ['j', 'i'], ['j', 'h'], ['j', 'b'], ['j', 'd'], ['j', 'g'], ['j', 'c']]

b = [['a'],['b'],['c'],['d'],['e'],['f'],['g'],['h'],['i'],['j']]

print complex_pairing(m2,b)