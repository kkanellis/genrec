
def chunks(l, chunk_size):
    for i in range(0, len(l), chunk_size):
        yield l[i:i+chunk_size]

