'''
Mid-term Problem 3 Monete Carlo Simulation
Author: Yuhao Zhao
Person I consulted: Jing
Last edit: March 17th

'''

import random
import matplotlib.pyplot as plt

score_list=[]# create a global empty list
def Monte_carlo(n:int, pass_score:int) -> float:
    '''

    '''
    class_one = ["A"]*6 +["B"]*3 +["C"]*1
    class_two = ["B"]+["C"]*4+["D"]*4+["F"]*1
    question_list=["1"]*90+["0"]*30 #1 is class one, 0 is class 2
    pass_count = 0
    #print(class_one, class_two, question_list)


    for i in range(n):
        twelve_q = random.sample(question_list,12)
        total_score = 0

        for j in range (len(twelve_q)):
            if twelve_q[j] =="1":
                score_for_question = random.choice(class_one)
                #print(score_for_question)
                if score_for_question =="A":
                    total_score += 4
                elif score_for_question =="B":
                    total_score+= 3
                elif score_for_question =="C":
                    total_score += 2

            if twelve_q[j] =="0":
                score_for_question = random.choice(class_two)
                #print(score_for_question)
                if score_for_question =="B":
                    total_score += 3
                elif score_for_question =="C":
                    total_score+= 2
                elif score_for_question =="D":
                    total_score += 1
                elif score_for_question =="F":
                    total_score += 0

        score_list.append(total_score)
        if total_score >=pass_score:
            pass_count +=1

    prob = pass_count/n
    return(prob)


def main():

    random.seed(20020131)
    #print(f"the probability you will pass this test is : {Monte_carlo(100000, 36)}")
    plt.title(f"the probability you will pass this test is(n=100000) : {Monte_carlo(100000, 36)}")
    plt.hist(score_list, bins='auto')
    plt.xlabel("score")
    plt.ylabel("frequency")
    plt.show()

    probs =[]
    for i in range(100):
        probs.append(Monte_carlo(100000, 36))
    print(f"the probabilities you will pass this test are (n=100000) : {probs}")

main()
