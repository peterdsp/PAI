""" ----------------------------------------------------------------------------
******** Τελικός Κώδικας 
******** Συγγραφέας: Πέτρος Δεσπολλάρι ΑΜ: 18390189 
"""
 

import copy
import sys  
sys.setrecursionlimit(10**6)
# **** The Parking Spaces Diagram
# **** Διάγραμμα των Χώρων του Πάρκινγκ
#   +-------+-------+
#   |   6   |   5   |
#   +-------+-------+
#   |   4   |   3   |
#   +-------+-------+
#   |   1   |   2   |
#   +-------+-------+
#       ^
#    entrance
# spaces [5][0]
spaces = {
    1: [2, 4],
    2: [1, 3],
    3: [2, 4, 5],
    4: [1, 3, 6],
    5: [3, 6],
    6: [4, 5],
}
counter=0
# **** The Parking Initial State Diagram
# **** Διάγραμμα Αρχικής Κατάστασης του Πάρκινγκ
#
#   +--------+--------+
#   |  P5 NO |  P4 NO |
#   +--------+--------+
#   |  P3 NO |  P2 NO |
#   +--------+--------+
#   |   E    |  P1 NO |
#   +--------+--------+
#       ^
#   5 vehicles waiting


# **** The problem's initial state
# **** Αρχική Κατάσταση Προβλήματος
#
# 1ο στοιχείο : πλήθος αυτοκινήτων εκτος parking
# 2ο στοιχείο : χώρος 1 (που ειναι και ο χώρος εισόδου)
# 3ο στοιχείο : χώρος 2
# 4ο στοιχείο : χώρος 3
# 5ο στοιχείο : χώρος 4
# 6ο στοιχείο : χώρος 5
# 7ο στοιχείο : χώρος 6
# state= [5, ['E', 'NO'], ['P1', 'NO'], ['P2', 'NO'], ['P3', 'NO'],['P4', 'NO'], ['P5', 'NO']]


# ******** Operators
# ******** Τελεστές

'''
 **** Τελεστής IN:
 **** Είσοδος αυτοκινήτου και τοποθέτηση σε άδεια πλατφόρμα στο χώρο εισόδου (1)
'''
def enter(state):
    if state[0]!=0 and state[1][0][0]=='P' and state[1][1]=='NO':
        # υπάρχει πλατφόρμα στο χώρο εισόδου χωρίς αυτοκίνητο (NO)
        new_state=[state[0]-1] + [[state[1][0], 'YES']] + state[2:] # είσοδος αυτοκινήτου στο parking  
        return new_state

'''
 **** Βοηθητικη συναρτηση swap: 
 **** Αντιμεταθέτει μέσα σε μια λιστα state τα δυο στοιχεία της που βρίσκονται στις θέσεις i & j
'''
def swap(state_l, i, j): 
    state_l[i], state_l[j] = state_l[j], state_l[i] 
    return state_l

'''
 **** Τελεστής neighbour1:
 **** Μετακίνηση 1ης πλατφόρμας που συνορεύει με κενό χώρο προς το γειτονικό της κενό χώρο 
 **** αντιμετάθεση e με πλατφόρμα, π.χ. [3, ['P1', 'NO'], ['P2', 'NO'], ['E', 'NO'], ['P3', 'NO'], ['P4', 'NO'], 
 ['P5', 'NO']] ---> [3, ['P1', 'NO'], ['E', 'NO'], ['P2', 'NO'], ['P3', 'NO'], ['P4', 'NO'], ['P5', 'NO']]
'''
def neighbour1(state):    
    
    elem=['E','NO']
    i=state.index(elem) if elem in state else -1
    if i >=0:
        swap(state, i, spaces[i][0])
        return state
        
'''
 **** Τελεστής neighbour2:
 **** Μετακίνηση 2ης πλατφόρμας που συνορεύει με κενό χώρο προς τον γειτονικό της κενό χώρο
 **** αντιμετάθεση e με πλατφόρμα, π.χ. [3, ['P1', 'NO'], ['P2', 'NO'], ['E', 'NO'], ['P3', 'NO'], 
 ['P4', 'NO'], ['P5', 'NO']] ---> [3, ['P1', 'NO'], ['P2', 'NO'], ['P3', 'NO'], ['E', 'NO'], ['P4', 'NO'], ['P5', 'NO']]
'''      
def neighbour2(state):
    print
    elem=['E','NO']
    i=state.index(elem) if elem in state else -1
    if i>=0:
        swap(state, i, spaces[i][1])
        return state

'''
 **** Τελεστής neighbour3:
 **** Μετακίνηση 3ης πλατφόρμας που συνορεύει με κενό χώρο προς τον γειτονικό της κενό χώρο για τις 2 νέες πλατφόρμες
 **** αντιμετάθεση e με πλατφόρμα, π.χ. [3, ['P1', 'NO'], ['P2', 'NO'], ['P3', 'NO'], ['E', 'NO'], ['P4', 'NO'], ['P5', 'NO']] ---> [3, ['P1', 'NO'], ['P2', 'NO'], ['P3', 'NO'], ['P4', 'NO'], ['E', 'NO'], ['P5', 'NO']]

'''
def neighbour3(state):  
    elem=['E','NO']
    i=state.index(elem) if elem in state else -1
    if i >=0 and (i==3 or i==4):
        swap(state, i, spaces[i][2])
        return state
'''
Συνάρτηση εύρεσης απογόνων της τρέχουσας κατάστασης
'''

def find_children(state):   
    children=[]      #Αρχικοποίηση της λίστας children
    enter_state=copy.deepcopy(state)    #Αντιγραφή του state
    enter_child=enter(enter_state)      
    tr1_state=copy.deepcopy(state)      
    tr1_child=neighbour1(tr1_state)  
    tr2_state=copy.deepcopy(state)      
    tr2_child=neighbour2(tr2_state)
    tr3_state=copy.deepcopy(state)      
    tr3_child=neighbour3(tr3_state)   
    if enter_child is not None: 
        children.append(enter_child) 
    if tr1_child is not None: 
        children.append(tr1_child)          
    if tr2_child is not None:
        children.append(tr2_child)
    if tr3_child is not None:   #εαν την βαλω πριν απο την tr1-child καθοριζει σε μεγαλο βαθμο την αποδοτικοτητα του κωδικα οσον αφορα τον αλγοριθμο DFS
        children.append(tr3_child)       
    return children

""" ----------------------------------------------------------------------------
**** FRONT
**** Διαχείριση Μετώπου
"""

""" ----------------------------------------------------------------------------
** initialization of front
** Αρχικοποίηση Μετώπου
"""

def make_front(state):
    return [state]

""" ----------------------------------------------------------------------------
**** expanding front
**** επέκταση μετώπου    
"""

def expand_front(front, method):  
    if method=='DFS':       #Αν επιλεχθεί ο αλγ΄όριθμος DFS 
        if front:
            print("Front:")
            print(front)
            node=front.pop(0)   #Αρχικοποίηση της μεταβλητής με το 1ο στοιχείο του μετώπου
            for child in find_children(node):     
                front.insert(0,child)   #Προσθήκη του κάθε παιδιού στο μέτωπο
    elif method=='BFS':     #Αν επιλεχθεί ο αλγ΄όριθμος BFS
        if front:
            print("Front:")
            print(front)
            node=front.pop(0)
            for child in find_children(node):     
                front.append(child)
    elif method=='BestFS':      #Αν επιλεχθεί ο αλγ΄όριθμος BestFS
        if front:
            print("Front:")
            print(front) # Εκτύπωση μετώπου
            node=front.pop(0) 
            for child in find_children(node):
                front.insert(0,child)
            front=sort_front(front)        
    return front

""" ----------------------------------------------------------------------------
**** QUEUE
**** Διαχείριση ουράς
"""

""" ----------------------------------------------------------------------------
** initialization of queue
** Αρχικοποίηση ουράς
"""

def make_queue(state):
    return [[state]]

""" ----------------------------------------------------------------------------
**** expanding queue
**** επέκταση ουράς
"""
def sort_front(front):
    if front:   #Έλεγχος για να βρίσκει εαν στο front υπάρχουν στοιχεία
        temp_front=front    
        distances=[]
        for i in  range(len(front)):
            platf_position=-1
            for j in range(1,len(front[i])):    #Επανάληψη (for) που τρέχει μέχρι το len του front
                if front[i][j][0][0]=='P' and front[i][j][1]=='NO' and platf_position==-1:    #Έλεγχος ορθότητας για τον μη υπολογισμό του position, τον χώρο εάν δεν είναι πλατφόρμα & αν δεν έχει αμάξι
                    platf_position=j%3+j//2
            if platf_position !=-1:
                distance=abs(platf_position)    #Αρχικοποίηση του distance με την απόλυτη τιμή του position
            else:
                distance=-1
            distances.append(distance)      #Προσθήκη της απόστασης στο τέλος της λίστας
        for i in range (len(front)):
            for j in range(0, len(front)-i-1):
                if distances [j]>distances [j+1]:
                    temp_front[j], temp_front[j+1]=temp_front[j+1], temp_front[j]
                    distances[j], distances[j+1]=distances[j+1], distances[j]
        return temp_front
    else:
        return front        

def sort_queue(queue):
    if queue:   #Έλεγχος για να βρίσκει εαν η ουρά έχει στοιχεία
        distances=[]    #Αρχικοποίηση της λίστας αποστάσεων
        for i in range(len(queue)):
            temp_queue=queue    #Αποθήκευση σε μία προσωρινή(temp_queue) μεταβλητή
            base=queue[i][-1];    #Αποθήκευση τελευταίας κατάστασης
            platf_position=-1
            for j in range(1,len(base)):      
                if base[j][0][0]=='P' and base[j][1]=='NO' and platf_position==-1:      #Έλεγχος εάν υπάρχει άδεια πλατφόρμα
                    platf_position=j%3+j//2     #Υπολογισμός απόστασης
            if platf_position!=-1:
                distance=abs(platf_position)    #Αποθήκευση της ανωτέρο απόστασης  
            else:
                distance=-1
            distances.append(distance)      #Αποθήκευση της ανωτέρο απόστασης στην λίστα
        for i in range (len(queue)):     #Bubblesort για ταξινόμηση
            for j in range(0, len(queue)-i-1):
                if distances [j]>distances [j+1]:
                    temp_queue[j], temp_queue[j+1]=temp_queue[j+1], temp_queue[j]
                    distances[j], distances[j+1]=distances[j+1], distances[j]
        return temp_queue
    else:
        return queue    #Επιστροφή ουράς
     
def extend_queue(queue, method):
    if method=='DFS':
        print("Queue:")
        print(queue)
        node=queue.pop(0)
        queue_copy=copy.deepcopy(queue)
        children=find_children(node[-1])
        for child in children:
            path=copy.deepcopy(node)
            path.append(child)
            queue_copy.insert(0,path)
    elif method=='BFS':
        print("Queue:")
        print(queue)
        node=queue.pop(0)
        queue_copy=copy.deepcopy(queue)
        children=find_children(node[-1])
        for child in children:
            path=copy.deepcopy(node)
            path.append(child)
            queue_copy.append(path)          
    elif method=='BestFS': 
        if queue:
            print("Queue:")
            print(queue) # Εκτύπωση ουράς
            node=queue.pop(0) # Αφαιρούμε το πρώτο στοιχείο από την ουρά
            queue_copy=copy.deepcopy(queue) # Δημιουργούμε ένα αντίγραφο της ουράς
            children=find_children(node[-1])
            for child in children:
                path=copy.deepcopy(node) 
                path.append(child)
                queue_copy.insert(0,path)
            # Ταξινομούμε την ουρά
            queue_copy = sort_queue(queue_copy)   
    return queue_copy
            
""" ----------------------------------------------------------------------------
**** Problem depending functions
**** ο κόσμος του προβλήματος (αν απαιτείται) και υπόλοιπες συναρτήσεις σχετικές με το πρόβλημα

  #### to be  added ####
"""

""" ----------------------------------------------------------------------------
**** Basic recursive function to create search tree (recursive tree expansion)
**** Βασική αναδρομική συνάρτηση για δημιουργία δέντρου αναζήτησης (αναδρομική επέκταση δέντρου)
"""

def find_solution(front, queue, closed, method):
    global counter
    counter=counter+1   #Μετρητής για κάθε νέο μέτωπο που δημιουργείται
    print(counter)    #Βλέπω το counter σε περίπτωση που το πρόγραμμα κλείσει από ανεπαρκή προσωρινή μνήμη
    if not front:
        print('_NO_SOLUTION_FOUND_')  
    elif front[0] in closed:
        new_front=copy.deepcopy(front)
        new_front.pop(0)
        new_queue=copy.deepcopy(queue)
        new_queue.pop(0)
        find_solution(new_front, new_queue, closed, method)
    elif is_goal_state(front[0]):
        print('_GOAL_FOUND_')
        print(front[0])  
        print(counter) 
    else:
        closed.append(front[0])
        front_copy=copy.deepcopy(front)
        front_children=expand_front(front_copy, method)
        queue_copy=copy.deepcopy(queue)
        queue_children=extend_queue(queue_copy, method)
        closed_copy=copy.deepcopy(closed)
        find_solution(front_children, queue_children, closed_copy, method)      
        
"""" ----------------------------------------------------------------------------
** Executing the code
** κλήση εκτέλεσης κώδικα
"""
def is_goal_state(front):
    if front[0]==0:
        return 1 
def main(): 
    initial_state=[5, ['E', 'NO'], ['P1', 'NO'], ['P2', 'NO'], ['P3', 'NO'], ['P4', 'NO'], ['P5', 'NO']]
    method='DFS'  
    """ ----------------------------------------------------------------------------
    **** starting search
    **** έναρξη αναζήτησης
    """
    print('____BEGIN__SEARCHING____')
    find_solution(make_front(initial_state), make_queue(initial_state), [], method)      
if __name__ == "__main__":
    main()