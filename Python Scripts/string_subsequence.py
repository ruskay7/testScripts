
new = ['hereiamstackerrank','hackerworld']
string1 = "hackerrank"
for y in new:
    def is_subseq(string1, y):
        iterator = iter(y)
        return all(any(d == da for d in iterator) for da in string1)
#check if string is a sub-sequence of another string
    is_subseq(string1, y)
    if is_subseq(string1, y) == True:
        print("YES")
    else:
        print("NO")




