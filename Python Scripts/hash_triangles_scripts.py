
#right triangle left aligned
def sum(num1,num2):
    for a in range(num2):
        print(" "*(7-a)+"#"*(a+1))

sum(1, 8)

#triangle inverted pyramid
def triangle(i, t=0):
    if i == 0:
        return 0
    else:
        print(' ' * ( t + 1 ) + '*' * ( i * 2 - 1 ))
        return triangle( i - 1, t + 1 )
triangle(5)