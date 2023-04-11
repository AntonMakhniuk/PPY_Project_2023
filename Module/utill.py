def sum(x,y):
    return x+y


def minus(x,y):
    return x-y


def division(x,y):
    return x/y


def multiply(x,y):
    return x*y



con = "y"
while con=="y" :
    print("what you want to do?\n"
          "1 - add\n"
          "2 - minus\n"
          "3 - division\n"
          "4 - multiply\n")
    choise = int(input("please : "))
    if(choise>4 or choise<1):
        print("Incorrect operation, try again")
        continue
    first  =  int(input("first : "))
    second =  int(input("second : "))
    if(choise == 1):
     print("Res = " ,sum(first,second))
    elif(choise==2):
     print("Res = " ,minus(first,second))
    elif(choise==3):
        if(second!=0):
            print("Res = " ,division(first,second))
        else:
            print("Error: Division by 0!")
    elif(choise==4):
     print("Res = " ,multiply(first,second))
    con = input("Continue?y/n: \n").strip()
    if con == "n":
        break