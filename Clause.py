from Formula import Formula

class Clause:
    def __init__(self):
        self.clause_atoms = []

    def __copy__(self):
        c = Clause()
        for atom in self.clause_atoms:
            c.clause_atoms.append(atom.__copy__())
        return c

    def __str__(self):
        str_clause = '('
        for index, atom in enumerate(self.clause_atoms):
            str_clause += atom.__str__()
            if index != len(self.clause_atoms) - 1:
                str_clause += ' | '
        str_clause += ')'
        # str_clause += '1' if self.is_tautology() else '0'
        return str_clause

    def is_tautology(self):
        check_atom = {}
        for atom in self.clause_atoms:
            if atom.name in check_atom:
                if atom.neg != check_atom[atom.name]:
                    return True
            else:
                check_atom[atom.name] = atom.neg
        return False

    def not_clause(self):
        f = Formula()
        for atom in self.clause_atoms:
            c = Clause()
            a = atom.__copy__()
            a = a.not_atom()
            c = c.or_atom(a)
            f = f.and_clause_formula(c)
        return f

    def get_atom(self):
        return self.clause_atoms[0]

    def comparate_atom(self, obj_atom):
        for a in self.clause_atoms:
            if obj_atom.name == a.name:
                if obj_atom.neg == a.neg:
                    return False
        return True

    def or_atom(self,obj_atom):
        c = Clause()
        for atom in self.clause_atoms:
            c = c.or_atom(atom.__copy__())
        if self.comparate_atom(obj_atom):
            c.clause_atoms.append(obj_atom.__copy__())
        return c

    def and_atom(self,obj_atom):
        f = Formula()
        f = f.and_clause_formula(self.__copy__())
        c = Clause()
        c = c.or_atom(obj_atom.__copy__())
        f = f.and_clause_formula(c)
        return f

    def and_clause(self,clause):
        f = Formula()
        f = f.and_clause_formula(self.__copy__())
        f = f.and_clause_formula(clause.__copy__())
        return f

    def or_clause(self,obj_clause):
        c = Clause()
        for atom in self.clause_atoms:
            c = c.or_atom(atom.__copy__())
        for atom in obj_clause.clause_atoms:
            c = c.or_atom(atom.__copy__())
        return c

    def delete_atom(self, del_atom):
        for atom in self.clause_atoms:
            if atom.name == del_atom.name:
                self.clause_atoms.remove(atom)

    def literal(self, del_atom):
        for atom in self.clause_atoms:
            if atom.name == del_atom.name:
                if atom.neg != del_atom.neg:
                    self.clause_atoms.remove(atom)
                    return False
                else:
                    return True
