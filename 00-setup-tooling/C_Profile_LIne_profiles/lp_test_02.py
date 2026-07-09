@profile
def process(data):
    x = load(data)
    y = augment(x)
    z = normalize(y)
    return z

# load()       5%

# augment()   80%

# normalize() 15%