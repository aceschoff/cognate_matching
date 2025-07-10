import numpy as np
import pandas as pd

ins_ali = 1.0
del_ali = 0.5
sub_ali = 1.0

# set alignment here
ali = {}

def min_cost_path_ali(cost, operations):
    
    # operation at the last cell
    path = [operations[cost.shape[0]-1][cost.shape[1]-1]]
    
    # cost at the last cell
    min_cost = cost[cost.shape[0]-1][cost.shape[1]-1]
    
    row = cost.shape[0]-1
    col = cost.shape[1]-1
    
    while row >0 and col > 0:
            
        if cost[row-1][col-1] <= cost[row-1][col] and cost[row-1][col-1] <= cost[row][col-1]:
            path.append(operations[row-1][col-1])
            row -= 1
            col -= 1
        elif cost[row-1][col] <= cost[row-1][col-1] and cost[row-1][col] <= cost[row][col-1]:
            path.append(operations[row-1][col])
            row -= 1
        else:
            path.append(operations[row][col-1])
            col -= 1
                    
    return "".join(path[::-1][1:])


def edit_distance_ali(seq1, seq2, ali):
    
    # create an empty 2D matrix to store cost
    cost = np.zeros((len(seq1)+1, len(seq2)+1))
    
    # fill the first row
    cost[0] = [i for i in range(len(seq2)+1)]
    
    # fill the first column
    cost[:, 0] = [i for i in range(len(seq1)+1)]
    
    # to store the operations made
    operations = np.asarray([['-' for j in range(len(seq2)+1)] \
                                 for i in range(len(seq1)+1)])
    
    # fill the first row by insertion 
    operations[0] = ['I' for i in range(len(seq2)+1)]
    
    # fill the first column by insertion operation (D)
    operations[:, 0] = ['D' for i in range(len(seq1)+1)]
    
    operations[0, 0] = '-'
    
    #set changeable sub cost
#     temp_sub = sub_ali
    
    # now, iterate over earch row and column
    for row in range(1, len(seq1)+1):
        
        for col in range(1, len(seq2)+1):
            
            # if both the characters are same then the cost will be same as 
            # the cost of the previous sub-sequence
#             if seq1[row-1] == seq2[col-1]:
#                 cost[row][col] = cost[row-1][col-1]
            
            # if chars align, cost will be same as cost of prev sub-seq
            if seq2[col-1] == ali[str(seq1[row-1])]:
                cost[row][col] = cost[row-1][col-1]
#                 temp_sub = 0

                
            else:
                
                insertion_cost = cost[row][col-1] + ins_ali
                deletion_cost = cost[row-1][col] + del_ali
                substitution_cost = cost[row-1][col-1] + sub_ali #temp_sub
                
                # calculate the minimum cost
                cost[row][col] = min(insertion_cost, deletion_cost, substitution_cost)
                
                # get the operation
                if cost[row][col] == substitution_cost:
                    operations[row][col] = 'S'
                    # if char aligns, remove cost
                    
                elif cost[row][col] == ins_ali:
                    operations[row][col] = 'I'
                else:
                    operations[row][col] = 'D'
#             temp_sub = sub_ali
                
    return cost[len(seq1), len(seq2)], min_cost_path_ali(cost, operations)


###################### make into function ########################

scores_ali = [ [0]*len(linb) for i in range(len(gk))]

for i, gk_word in enumerate(gk):
    for j, myc_word in enumerate(linb):
        score_ali, operations = edit_distance_ali(gk_word, myc_word, ali)
        scores_ali[i][j] = score_ali

cognates_ali = []
for i in range(len(scores_ali)):
    cogz = []
    mini = min(scores_ali[i])
    for j in range(len(scores_ali[i])):
        if scores_ali[i][j] == mini:
            cogz.append(linb[j])
    cognates_ali.append((gk[i], cogz))
    
cog_ali_dict = {key: value for key, value in cognates_ali}

##################################################################


def print_eval(gk, linb, cognates_dict):
    '''
    Takes the lists of words in each language and the cognates dict
    Long short: need to make cognates a dictionary before running this
    Precision = TP / (TP + FP)
    Recall = TP / (TP + FN)
    '''
    TP = 0
    FP = 0
    FN = 0

    for i, word in enumerate(gk):
        if linb[i] not in cognates_dict[word]:
            FN += 1
            FP += len(cognates_dict[word])
        else:
            for cog in cognates_dict[word]:
                if cog == linb[i]:
                    TP += 1
                else:
                    FP += 1
    prec = TP + FP
    rec = TP + FN
    F = (2*TP) + FP + FN
    
    print("Precision: ", TP/prec)
    print("Recall: ", TP/rec)
    print("F1: ", (2*TP)/F)
