class Formula:
    def __init__(self):
        self.clauses = []

    def __str__(self):
        string = '['
        for index,clauses in enumerate(self.clauses):
            string += clauses.__str__()
            if index != len(self.clauses) - 1:
                string += ' \n '
        string += ']'
        return string

    def delete_tautology(self):
        f = Formula()
        for clause in self.clauses:
            if not clause.is_tautology():
                f.clauses.append(clause.__copy__())
        return f

    def and_clause_formula(self, obj_clause):
        f = Formula()
        for clause in self.clauses:
            f.clauses.append(clause.__copy__())
        f.clauses.append(obj_clause.__copy__())
        return f

    def or_formula(self, obj_formula):
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
            f = f.or_formula(not_clause) if f.clauses else not_clause
        return f

    def get_david_putman(self):
        f = Formula()
        f = self.delete_tautology()
        witness = {}

        if self.clauses:
            print('evalular')
            while self.clauses:
                for c in self.clauses:
                    print(f'formula:\n{self}')
                    print(f'clasula:\n{c}\n')
                    if c.clause_atoms:
                        if self.clauses:
                            # aplicar clausula unitaria
                            if len(c.clause_atoms) == 1:
                                a = c.get_atom()
                                witness[a.name] = not a.neg
                                for c_clear in self.clauses:
                                    if c_clear != c:
                                        c_clear.delete_atom(a)
                                self.clauses.remove(c)
                            # aplicar LP
                            else:
                                # el primer atomo de la clausula que estemos evaluando
                                a_lp = c.get_atom()
                                witness[a_lp.name] = not a_lp.neg
                                for c_clear in self.clauses:
                                    if c_clear != c:
                                        if c_clear.literal(a_lp):
                                            self.clauses.remove(c_clear)
                                self.clauses.remove(c)
                        else:
                            print('SAT verdad')
                    else:
                        print('lado izq del diagrama')
                    print(f'clausula:\n{c}')
                    print(f'formula:\n{self}\n')
        else:
            print('SAT verdad')

        return witness

