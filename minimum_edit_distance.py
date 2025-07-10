import numpy as np
import pandas as pd

# set ins/del/sub costs
ins_cost = 1
del_cost = 1
sub_cost = 2


def min_cost_path(cost, operations):
    '''
    Find the Minimum Cost Path, to be used to find the Minimum Edit Distance
    '''
    
    path = [operations[cost.shape[0]-1][cost.shape[1]-1]]   # operation at the last cell
    min_cost = cost[cost.shape[0]-1][cost.shape[1]-1]   # cost at the last cell
    
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



def edit_distance_dp(seq1, seq2):
    '''
    Find the Actual Mnimum Edit Distance using the Minimum Cost Path
    try to remember what dp stands for
    '''
    cost = np.zeros((len(seq1)+1, len(seq2)+1))     # create an empty 2D matrix to store cost
    cost[0] = [i for i in range(len(seq2)+1)]   # fill the first row
    cost[:, 0] = [i for i in range(len(seq1)+1)]    # fill the first column
    # to store the operations made
    operations = np.asarray([['-' for j in range(len(seq2)+1)] \
                                 for i in range(len(seq1)+1)])
    operations[0] = ['I' for i in range(len(seq2)+1)]   # fill the first row by insertion 
    operations[:, 0] = ['D' for i in range(len(seq1)+1)]    # fill the first column by insertion operation (D)
    operations[0, 0] = '-'
    
    # now, iterate over earch row and column
    for row in range(1, len(seq1)+1):
        for col in range(1, len(seq2)+1):
            # if both the characters are same then the cost will be same as 
            # the cost of the previous sub-sequence
            if seq1[row-1] == seq2[col-1]:
                cost[row][col] = cost[row-1][col-1]
            else:
                insertion_cost = cost[row][col-1] + ins_cost
                deletion_cost = cost[row-1][col] + del_cost
                substitution_cost = cost[row-1][col-1] + sub_cost
                
                # calculate the minimum cost
                cost[row][col] = min(insertion_cost, deletion_cost, substitution_cost)
                
                # get the operation
                if cost[row][col] == substitution_cost:
                    operations[row][col] = 'S'
                    
                elif cost[row][col] == ins_cost:
                    operations[row][col] = 'I'
                else:
                    operations[row][col] = 'D'
                
    return cost[len(seq1), len(seq2)], min_cost_path(cost, operations)





################ make into function #####################

scores = [ [0]*len(linb) for i in range(len(gk))]

for i, gk_word in enumerate(gk):
    for j, myc_word in enumerate(linb):
        score, operations = edit_distance_dp(gk_word, myc_word)
        scores[i][j] = score


cognates = []
for i in range(len(scores)):
    cogz = []
    mini = min(scores[i])
    for j in range(len(scores[i])):
        if scores[i][j] < 3.5:
             cogz.append(linb[j])
    cognates.append((gk[i], cogz))
    
print(cognates[:30])

cognates_dict = {key: value for key, value in cognates}

#########################################################


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
