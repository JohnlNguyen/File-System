class foo():
    l = []
    def __init__(self,val):
        self.val = val
    def __cmp__(self, other):
        return self.val < other.val
a = foo(10)
b = foo(12)
l = []
l.append(a)
l.append(b)

sorted(l)

print l[0].val