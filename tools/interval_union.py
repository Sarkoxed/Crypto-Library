class tp:
    def __repr__(self):
        return "(%d,%d)" % (self.start, self.end)

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __iter__(self):
        yield self.start
        yield self.end


def union(s):
    s.sort(key=lambda self: self.start)
    y = [s[0]]
    for x in s[1:]:
        if y[-1].end < x.start:
            y.append(x)
        elif y[-1].end == x.start:
            y[-1].end = x.end
    return y


