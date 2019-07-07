class SetInput():
    """
    This is an object that initialise the input sets
    """
    def __init__(self, i, k, t):
        self.i = i
        self.k = k
        self.t = t

class ParaInput():
    """
    This is an object that initialise the parameters
    """
    def __init__(self, p, B, Bi, precedence):
        self.p = p
        self.B = B
        self.Bi = Bi
        self.precedence = precedence
