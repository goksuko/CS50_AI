import sys
import string

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency() # ensuring that every value in a variable’s domain satisfy the unary constraints
        self.ac3() #  enforce arc consistency, ensuring that binary constraints are satisfied
        return self.backtrack(dict()) # on an initially empty assignment (the empty dictionary dict()) to try to calculate a solution to the problem

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for var in self.domains.copy(): # if not copied, it gives "RuntimeError: Set changed size during iteration"
            for word in self.domains[var].copy():
                if var.length != len(word):
                    self.domains[var].remove(word)
        return
        raise NotImplementedError

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revision_made = False
        
        # If there's no overlap, no revision needed
        if self.crossword.overlaps[x, y] is None:
            return False
        
        i, j = self.crossword.overlaps[x, y]
        
        # Create a copy to iterate over while modifying the original
        words_to_remove = set()
        
        for word_x in self.domains[x]:
            # Check if there exists ANY word_y that satisfies the constraint
            if not any(word_x[i] == word_y[j] for word_y in self.domains[y]):
                words_to_remove.add(word_x)
                revision_made = True
        
        # Remove all invalid words
        self.domains[x] -= words_to_remove
        
        return revision_made
        raise NotImplementedError

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs is None:
            all_arcs = []
            for x in self.crossword.variables:
                for y in self.crossword.neighbors(x):
                    all_arcs.append((x, y))
        else:
            all_arcs = arcs
        while len(all_arcs) > 0:
            (x, y) = all_arcs.pop(0)
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                for z in (self.crossword.neighbors(x) - {y}):
                    all_arcs.append((z, x))
        return True        
        raise NotImplementedError

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for var in self.crossword.variables:
            if var not in assignment:
                return False
        return True
        raise NotImplementedError

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        if not assignment:
            return True
            
        # An assignment is consistent if it satisfies all of the constraints of the problem: that is to say, 
        # all values are distinct,
        for var in assignment:
            for other_var in assignment:
                if var != other_var and assignment[var] == assignment[other_var]:
                        return False
        
        # every value is the correct length, and 
        for var in assignment:
            if len(assignment[var]) != var.length:
                return False
            
        # there are no conflicts between neighboring variables.
        for var in assignment:
            for neighbor in self.crossword.neighbors(var):
                if neighbor in assignment:
                    i, j = self.crossword.overlaps[var, neighbor]
                    if assignment[var][i] != assignment[neighbor][j]:
                        return False
        return True
        raise NotImplementedError

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        ## least-constraining values heuristic ##
        value_elimination_counts = {}
        for value in self.domains[var]:
            elimination_count = 0
            for neighbor in self.crossword.neighbors(var):
                if neighbor not in assignment and self.crossword.overlaps[var, neighbor] is not None:
                    i, j = self.crossword.overlaps[var, neighbor]
                    for neighbor_value in self.domains[neighbor]:
                        if value[i] != neighbor_value[j]:
                            elimination_count += 1
            value_elimination_counts[value] = elimination_count
        return sorted(value_elimination_counts)
        raise NotImplementedError

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        ## minimum remaining value heuristic and then the degree heuristic ##
        remaining_to_variables = {} # int : []
        for variable in self.crossword.variables:
            if variable not in assignment:
                if len(self.domains[variable]) not in remaining_to_variables:
                    remaining_to_variables[len(self.domains[variable])] = []
                remaining_to_variables[len(self.domains[variable])].append(variable)
        if remaining_to_variables:
            min_remaining_nb = min(remaining_to_variables.keys())
            if len(remaining_to_variables[min_remaining_nb]) == 1:
                return remaining_to_variables[min_remaining_nb][0]
            else:
                degree_to_variables = {} # int : []
                for variable in remaining_to_variables[min_remaining_nb]:
                    degree = len(self.crossword.neighbors(variable))
                    if degree not in degree_to_variables:
                        degree_to_variables[degree] = []
                    degree_to_variables[degree].append(variable)
                max_degree = max(degree_to_variables.keys())
                return degree_to_variables[max_degree][0]
        return []
        raise NotImplementedError
    
        # from collections import defaultdict
    
        # # Get all unassigned variables
        # unassigned = [v for v in self.crossword.variables if v not in assignment]
        
        # if not unassigned:
        #     return None
        
        # # Sort by: (1) fewest remaining values, (2) most neighbors (degree)
        # def sort_key(var):
        #     remaining_values = len(self.domains[var])
        #     degree = len(self.crossword.neighbors(var))
        #     return (remaining_values, -degree)  # negative degree for descending order
        
        # return min(unassigned, key=sort_key)

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            if self.consistent(assignment):
                assignment[var] = value
                result = self.backtrack(assignment)
                if result is not None:
                    return result
                assignment.pop(var)
        return None
        raise NotImplementedError


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()


# we have four variables:
# representing the four words we need to fill into this crossword puzzle 

# Each variable is defined by four values: 
# the row it begins on (its i value), 
# the column it begins on (its j value), 
# the direction of the word (either down or across), and 
# the length of the word. 
# Variable 1, for example, would be a variable represented by a row of 1 (assuming 0 indexed counting from the top), a column of 1 (also assuming 0 indexed counting from the left), a direction of across, and a length of 4.