class Atom:
    def __init__(self,str_name):
        self.name = str_name.lower()
        self.neg = False

    def __copy__ (self):
        new_atom = Atom(self.name)
        new_atom.neg = self.neg
        return new_atom

    def __str__(self):
        str_atom = ''
        if self.neg:
            str_atom += '-'
        str_atom += self.name
        return str_atom

    def not_atom(self):
        new_atom = Atom(self.name)
        new_atom.neg = not self.neg
        return new_atom