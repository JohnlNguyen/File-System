class foo():
    x = 1
    l = []


m = {}
def f(m):
    a = foo()
    b = foo()
    m["key"] = []
    m["key"].append(a)
    m["key"].append(b)
    return
f(m)
print m
del m["key"]
print m
