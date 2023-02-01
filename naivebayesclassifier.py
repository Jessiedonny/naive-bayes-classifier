import csv
from itertools import count
from operator import indexOf
import os
import sys
from pyexpat.errors import XML_ERROR_DUPLICATE_ATTRIBUTE


#arg1="data/breast-cancer-training.csv"
#arg2="data/breast-cancer-test.csv"
try:
    arg1 = sys.argv[1]
    arg2 = sys.argv[2]
except IndexError:
    raise SystemExit(f"Usage: {sys.argv[0]} <argument missing - check readme.txt>")

#read andd store training data
training_instances=[]   
with open('data/'+str(arg1),newline='') as training_data_csv:
    csvreader=csv.reader(training_data_csv,delimiter=',')
    header=next(csvreader)
    #print(header)
    for row in csvreader:
        training_instances.append(row)

training_rows=len(training_instances)
number_of_features=len(header)-2

label=[]
for i in range(len(training_instances)):
    label.append(training_instances[i][1])

#print(training_rows)
#print(number_of_features)

#read and store test data 
test_instances=[]
with open ('data/'+str(arg2),newline='') as test_data_csv:
    csvreader=csv.reader(test_data_csv,delimiter=',')
    header=[]
    header=next(csvreader)
    #print(header)
    for row in csvreader:
        test_instances.append(row)
test_rows=len(test_instances)


#initialise the count numbers to 1
#2 class label store in count_y
count_y=[1,1]

#9 attributes - define counter for each feature
count_att=[]
for i in range(number_of_features):
    count_att.append([])
    for j in range(2):
        count_att[i].append([])

    

#initialise the labels for each feature
labels=[]
label_age=['10-19','20-29','30-39','40-49','50-59','60-69','70-79','80-89','90-99'] 
labels.append(label_age)
label_menopause=['lt40','ge40','premeno']
labels.append(label_menopause)
label_tumorsize=['0-4','5-9','10-14','15-19','20-24','25-29','30-34','35-39','40-44','45-49','50-54','55-59']
labels.append(label_tumorsize)
label_invnodes=['0-2','3-5','6-8','9-11','12-14','15-17','18-20','21-23','24-26','27-29','30-32','33-35','36-39']
labels.append(label_invnodes)
label_node_caps=['yes','no']
labels.append(label_node_caps)
label_degmalig=['1','2','3']
labels.append(label_degmalig)
label_breast=['left','right']
labels.append(label_breast)
label_breastquad=['left_up','left_low','right_up','right_low','central']
labels.append(label_breastquad)
label_irradiat=['yes','no']
labels.append(label_irradiat)


#initialise the count numbers to 1
for j in range(2):
    for k in range(9): #9 values of age
        count_att[0][j].append(1)
    for k in range(3): #3 values of menopause
        count_att[1][j].append(1)
    for k in range(12): #12 values of tumor size
        count_att[2][j].append(1)
    for k in range(13): #13 values of inv-nodes
        count_att[3][j].append(1)
    for k in range(2): #2 values of node-caps
        count_att[4][j].append(1)
    for k in range(3): #3 values of deg-malig
        count_att[5][j].append(1)
    for k in range(2): #2 values of breast
        count_att[6][j].append(1)
    for k in range(5): #5 values of brest-quad
        count_att[7][j].append(1)
    for k in range(2): #2 values of irradiat
        count_att[8][j].append(1)


#count the numbers of each class and feature value based onn the training instances
def att_counter(label,index,y,instance):
    for lb in label:
        if (instance==lb):
            id=label.index(lb)
            count_att[index][y][id]+=1

for i in range(len(training_instances)):
    if(label[i]=='no-recurrence-events'):
        count_y[0]+=1

        att_counter(label_age,0,0,training_instances[i][2])       
        att_counter(label_menopause,1,0,training_instances[i][3])  
        att_counter(label_tumorsize,2,0,training_instances[i][4])       
        att_counter(label_invnodes,3,0,training_instances[i][5])  
        att_counter(label_node_caps,4,0,training_instances[i][6])       
        att_counter(label_degmalig,5,0,training_instances[i][7])  
        att_counter(label_breast,6,0,training_instances[i][8])       
        att_counter(label_breastquad,7,0,training_instances[i][9])  
        att_counter(label_irradiat,8,0,training_instances[i][10])  

       
    else:
        count_y[1]+=1
        att_counter(label_age,0,1,training_instances[i][2])       
        att_counter(label_menopause,1,1,training_instances[i][3])  
        att_counter(label_tumorsize,2,1,training_instances[i][4])       
        att_counter(label_invnodes,3,1,training_instances[i][5])  
        att_counter(label_node_caps,4,1,training_instances[i][6])       
        att_counter(label_degmalig,5,1,training_instances[i][7])  
        att_counter(label_breast,6,1,training_instances[i][8])       
        att_counter(label_breastquad,7,1,training_instances[i][9])  
        att_counter(label_irradiat,8,1,training_instances[i][10])  

print('--------counting section------------')
print('count of y=0 (no-recurrence-events)', count_y[0])
print('count of y=1 (recurrence-events)', count_y[1])
print("count of each attribute :")
for i in range(number_of_features):
    print('att',i)
    for j in range(2):
        print('  y=',j,':',count_att[i][j])

#calculate total/denominators
class_total=count_y[0]+count_y[1]
#9 total count - define counter for each feature
total_att=[]
for i in range(number_of_features):
    total_att.append([])
    for j in range(2):
        total_att[i].append(0)

for j in range(2):
    for i in range(len(label_age)):
        total_att[0][j]+=count_att[0][j][i]
    for i in range(len(label_menopause)):
        total_att[1][j]+=count_att[1][j][i]
    for i in range(len(label_tumorsize)):
        total_att[2][j]+=count_att[2][j][i]
    for i in range(len(label_invnodes)):
        total_att[3][j]+=count_att[3][j][i]
    for i in range(len(label_node_caps)):
        total_att[4][j]+=count_att[4][j][i]
    for i in range(len(label_degmalig)):
        total_att[5][j]+=count_att[5][j][i]
    for i in range(len(label_breast)):
        total_att[6][j]+=count_att[6][j][i]
    for i in range(len(label_breastquad)):
        total_att[7][j]+=count_att[7][j][i]
    for i in range(len(label_irradiat)):
        total_att[8][j]+=count_att[8][j][i]

print("Total count of y for each attribute :")
for i in range(number_of_features):
    print('att',i,':')
    for j in range(2):
        print( '  Total y=',j,':',total_att[i][j])

#calculate the probabilities from the couting numbers
prob_y=[]
for i in range(2):
    prob_y.append(round(count_y[i]/class_total,4))

print('-------probability section---------')
print('Prob(y=0):',prob_y[0])
print('Prob(y=1):',prob_y[1])

def att_prob(prob_att,label,index):
    for j in range(2):
        prob_att.append([])
        for i in range(len(label)):
            prob_att[j].append([])
            prob_att[j][i]=round(count_att[index][j][i]/total_att[index][j],4)




prob_att=[[],[],[],[],[],[],[],[],[]]
att_prob(prob_att[0],label_age,0)
att_prob(prob_att[1],label_menopause,1)
att_prob(prob_att[2],label_tumorsize,2)
att_prob(prob_att[3],label_invnodes,3)
att_prob(prob_att[4],label_node_caps,4)
att_prob(prob_att[5],label_degmalig,5)
att_prob(prob_att[6],label_breast,6)
att_prob(prob_att[7],label_breastquad,7)
att_prob(prob_att[8],label_irradiat,8)

print('Probibilities of each attribute are stored in a list the same order as the label')
print('Age: ',label_age)
print('   Prob(age|y=0): ',prob_att[0][0],'\n   Prob(age|y=1:) ',prob_att[0][1])
print('Menopause: ',label_menopause)
print('   Prob(menopause|y=0):', prob_att[1][0],'\n   Prob(menopause|y=1):', prob_att[1][1])
print('Tumor-size: ',label_tumorsize)
print('   Prob(tumor-size|y=0):',prob_att[2][0],'\n   Prob(tumor-size|y=1):',prob_att[2][1])
print('Inv-nodes: ',label_invnodes)
print('   Prob(inv-nodes|y=0):',prob_att[3][0],'\n    Prob(inv-nodes|y=1):',prob_att[3][1])
print('Node-caps: ', label_node_caps)
print('   Prob(node-caps|y=0):',prob_att[4][0],'\n    Prob(node-caps|y=1):',prob_att[4][1])
print('Deg-malig: ', label_degmalig)
print('   Prob(deg-malig|y=0):',prob_att[5][0],'\n    Prob(deg-malig|y=1):',prob_att[5][1])
print('Breast: ',label_breast)
print('   Prob(breast|y=0):',prob_att[6][0],'\n   Prob(breast|y=1):',prob_att[6][1])
print('Breast-quad: ',label_breastquad)
print('   Prob(breast-quad|y=0):',prob_att[7][0],'\n  Prob(breast-quad|y=1):',prob_att[7][1])
print('Irradiat: ',label_irradiat)
print('   Prob(irradiat|y=0):',prob_att[8][0],'\n   Prob(irradiat|y=1):',prob_att[8][1])



def calculate_score(score_y, prob_att,label,insts,j):
    score=score_y
    for i in range(number_of_features):
        id=label[i].index(insts[i+2])
        #print(id,insts[i+2])
        score=score*float(prob_att[i][j][id])
    return score


#calculation of the class score for test instances
score_att=[]

for i in range(len(test_instances)):
    score_att.append([])
    for j in range(2):
        score_att[i].append(calculate_score(prob_y[j],prob_att,labels,test_instances[i],j))

print('----------test instances prediction-----------')
        

for j in range(len(test_instances)):
    print('test instance ',j,':')
    largest_score=0
    predict_y=''
    for i in range(2):
        print('  Score of y =',i,':',score_att[j][i])
        if(float(score_att[j][i])>largest_score):
            largest_score=score_att[j][i]
            predict_y=i
    if(predict_y==0):
        predict_y='no-recurrence-events'
    else:
        predict_y='recurrence-events'
    #print('  largest_score:',largest_score)
    print('  Predicted class:', predict_y)



