import copy
import random

from Atom import Atom


class Formula:
    def __init__(self):
        self.clauses = []
        self.witness = {}
        self.bifurcation_counter = 0

    def __copy__(self):
        f = Formula()
        f.witness = self.witness
        f.bifurcation_counter = self.bifurcation_counter + 1
        for c in self.clauses:
            f.clauses.append(c.__copy__())
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

    def davis_and_putnam(self):
        empty_clause = False
        for clause in self.clauses:
            if not clause.clause_atoms:
                empty_clause = True
                break
        if empty_clause:
            if self.bifurcation_counter == 1:
                return self.bifurcation()
            else:
                return False
        elif self.clauses:
            unit_clause = self.unit_clause()
            pure_literal = self.pure_literal()
            if unit_clause or pure_literal:
                return self.davis_and_putnam()
            else:
                return self.bifurcation()
        else:
            return True

    def bifurcation(self):
        clause = random.choice(self.clauses)
        atom = random.choice(clause.clause_atoms)
        f_copy = self.__copy__()
        atom = atom.__copy__()
        f_copy.witness[atom.name] = atom.neg
        f_copy.simplifly(atom)
        if f_copy.davis_and_putnam():
            return True
        f_copy = self.__copy__()
        atom = atom.__copy__()
        atom = atom.not_atom()
        f_copy.witness[atom.name] = atom.neg
        f_copy.simplifly(atom)
        return f_copy.davis_and_putnam()


    def simplifly(self, atom):
        simplifly_clauses = []
        for clause in self.clauses:
            atom_index = clause.find_atom_index(atom)
            if atom_index == -1:
                simplifly_clauses.append(clause)
            elif atom.neg != clause.clause_atoms[atom_index].neg:
                del clause.clause_atoms[atom_index]
                simplifly_clauses.append(clause)
        self.clauses = simplifly_clauses

    def pure_literal(self):
        pure_literal_valid = False
        witness = {}
        for clause in self.clauses:
            for atom in clause.clause_atoms:
                if atom.name in witness:
                    if atom.neg != witness[atom.name]:
                        witness[atom.name] = None
                else:
                    witness[atom.name] = atom.neg
        for name,neg in witness.items():
            if neg is not None:
                pure_literal_valid = True
                atom = Atom(name)
                atom.neg = neg
                self.witness[name] = atom.neg
                self.simplifly(atom)
        return pure_literal_valid

    def unit_clause(self):
        unit_clause_valid = False
        uc = [c for c in self.clauses if len(c.clause_atoms) == 1]
        while uc:
            unit_clause_valid = True
            atom = list(uc[0].clause_atoms)[0]
            self.witness[atom.name] = atom.neg
            self.simplifly(atom)
            uc = [c for c in self.clauses if len(c.clause_atoms) == 1]
        return unit_clause_valid

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

    def format(self, witness):
        certificado = []
        for name, value in witness.items():
            string = '-' + name if value else name
            certificado.append(string)
        return certificado

    def get_atoms(self):
        atoms = {}
        for clause in self.clauses:
            for atom in clause.clause_atoms:
                if atom not in atoms:
                    atoms[atom.name] = True if random.random() >= 0.5 else False
        return atoms