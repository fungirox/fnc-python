import random


class Formula:
    def __init__(self):
        self.clauses = []
        self.bifurcation = 0

    def __copy__(self):
        f = Formula()
        for c in self.clauses:
            f.clauses.append(c)
        return f

    def __str__(self):
        string = '['
        for index,clauses in enumerate(self.clauses):
            string += clauses.__str__()
            if index != len(self.clauses) - 1:
                string += '\n'
        string += ']'
        return string

    def delete_tautology(self):
        f = Formula()
        for clause in self.clauses:
            if not clause.is_tautology():
                f.clauses.append(clause.__copy__())
        return f

    def and_clause(self,obj_clause):
        f = Formula()
        for clause in self.clauses:
            f.clauses.append(clause.__copy__())
        f.clauses.append(obj_clause)
        return f

    def or_formula(self,obj_formula):
        f = Formula()
        for clause in self.clauses:
            for clause2 in obj_formula.clauses:
                f.clauses.append(clause.or_clause(clause2))
        return f

    def and_formula(self,obj_formula):
        f = Formula()
        for clause in self.clauses:
            f.clauses.append(clause.__copy__())
        for clause in obj_formula.clauses:
            f.clauses.append(clause.__copy__())
        return f

    def not_formula(self):
        f = Formula()
        for clause in self.clauses:
            not_clause = clause.not_clause()
            f = f.and_formula(not_clause)
        return f

    def get_david_putman(self):
        f = self.delete_tautology()
        witness = {}

        if f.clauses:
            while f.clauses:
                for clause in f.clauses:
                    clause_copy = clause.__copy__()
                    print(f'formula:\n{f}')
                    print(f'clasula:\n{clause_copy}\n')
                    if clause_copy.clause_atoms:
                        if f.clauses:
                            # aplicar clausula unitaria
                            if len(clause_copy.clause_atoms) == 1:
                                a = clause_copy.get_atom()
                                witness[a.name] = not a.neg
                                for c_clear in f.clauses:
                                    if c_clear != clause_copy:
                                        c_clear = c_clear.delete_atom(a)
                                f.clauses.remove(clause_copy)
                            # aplicar LP
                            else:
                                # el primer atomo de la clausula que estemos evaluando
                                a_lp = clause_copy.get_atom()
                                witness[a_lp.name] = not a_lp.neg
                                for c_clear in f.clauses:
                                    if c_clear != clause_copy:
                                        if c_clear.literal(a_lp):
                                            f.clauses.remove(c_clear)
                                f.clauses.remove(clause_copy)
                        else:
                            print('SAT verdad')
                    else:
                        f.bifurcation = f.bifurcation + 1
                        return {'formula': f,
                                'SAT': witness}
                    print(f'clausula:\n{clause}')
                    print(f'formula:\n{f}\n')

        else:
            print('SAT verdad')

        return {'formula': f,
                'SAT': witness}

    def GSAT(self):
        f = self.__copy__()
        witness = f.get_atoms()
        tries = 5
        print(f'witness {witness}')
        while tries > 0:
            flips = 3
            while flips > 0:
                solucion = f.solucionar_formula(witness)
                if solucion == 1:
                    return witness
                else:
                    witness[random.choice(list(witness.keys()))] = True if random.random() >= 0.5 else False
                flips = flips - 1
            tries = tries - 1
        return 'No se encontró solucion a la formula'

    def solucionar_formula(self,witness):
        clausulas_solucion = 0
        clausulas = len(self.clauses)
        for clause in self.clauses:
            for atom in clause.clause_atoms:
                if witness[atom.name] == atom.neg:
                    clausulas_solucion = clausulas_solucion + 1
                    break
        return clausulas_solucion / clausulas

    def get_atoms(self):
        atoms = {}
        for clause in self.clauses:
            for atom in clause.clause_atoms:
                if atom not in atoms:
                    atoms[atom.name] = True if random.random() >= 0.5 else False
        return atoms