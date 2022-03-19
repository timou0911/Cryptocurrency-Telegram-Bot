#　
def func(min_,max_):
    
    import random
    
    answer = random.randint(min_,max_)
    
    print("the range is between",min_,"and",max_)
     
    while True:
        guess = input("enter your guess: ")
        
        if int(guess) > int(answer) :
            max_ = guess
            print("the answer is between",min_,"and",max_)
        elif int(guess) < int(answer) :
            min_ = guess
            print("the answer is between",min_,"and",max_)
        else :
            break
        
    print("you're right.")


    
min_ = input()
max_ = input()
print()
    
func(int(min_), int(max_))

