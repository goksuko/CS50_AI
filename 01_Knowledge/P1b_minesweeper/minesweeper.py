import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """
    # We’ll only want our sentences to be about cells 
    # that are not yet known to be either safe or mines. 
    # This means that, once we know whether a cell is a mine or not, 
    # we can update our sentences to simplify them and 
    # potentially draw new conclusions.

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if self.count == len(self.cells):
            return set(self.cells)
        else:
            return set()
        raise NotImplementedError

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return set(self.cells)
        else:
            return set()
        raise NotImplementedError

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1
        return
        raise NotImplementedError

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)
        return
        raise NotImplementedError


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # print("add knowledge")
        # print(f"{cell} move made and marked safe")
        # 1) mark the cell as a move that has been made
        self.moves_made.add(cell)
        # 2) mark the cell as safe
        self.mark_safe(cell)
        # 3) add a new sentence to the AI's knowledge base
        #        based on the value of `cell` and `count`
        sent = Sentence(self.find_neighbours(cell), count)
        self.add_safes(sent)
        self.add_mines(sent)
        if sent not in self.knowledge:            
            self.knowledge.append(sent)
            # print(f"{sent} is added to the knowledge")
        # 4) mark any additional cells as safe or as mines
        #    if it can be concluded based on the AI's knowledge base
        # 5) add any new sentences to the AI's knowledge base
        #    if they can be inferred from existing knowledge
        # print("knowledge now\n----------")
        # for l in self.knowledge:
        #     print(l)
        # print("------------\n")
        for snt in self.knowledge:
            for snt2 in self.knowledge:
                if snt != snt2 and snt.cells < snt2.cells:
                    new_sent = Sentence(snt2.cells - snt.cells, snt2.count - snt.count)
                    # print(f"{new_sent} is the new sentence")
                    self.add_safes(new_sent)           
                    self.add_mines(new_sent)
                    if new_sent.count != 0  and new_sent.count != len(new_sent.cells) and new_sent not in self.knowledge:
                        self.knowledge.append(new_sent)
                        # print(f"{new_sent} is added to the knowledge")
        return
        raise NotImplementedError

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for cll in self.safes:
            if cll not in self.moves_made:
                self.moves_made.add(cll)
                return cll
        return None
        raise NotImplementedError

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        while True:
            cll = (random.randint(0, self.height - 1), random.randint(0, self.width - 1))
            if cll not in self.moves_made:
                if cll not in self.mines:
                    return cll
        raise NotImplementedError

    def find_neighbours(self, cell):
        """
        Returns a set of cell coordinates on the Minesweeper board. 
        Each tuple represents a neighbour cell.
        """
        height = self.height
        width = self.width     
        answer = set()
        i, j = cell
        # print(cell)
        for row in range(i-1, i+2):
            for col in range(j-1, j+2):
                if 0 <= row < height and 0 <= col < width:
                    answer.add((row, col))
        answer.remove((i, j))
        # print(answer)
        return answer

    def add_safes(self, sentence):
        """
        Checks the cells in the sentence, if they are safe
            1) marks them as safe
            2) adds them to the safes set()
        """
        for cll in sentence.known_safes():
            # print(f"sentence: {sentence}")
            self.mark_safe(cll)
            self.safes.add(cll)
            # print(f"{cll} is safe")
            if len(sentence.cells) > 1:
                copy = set(sentence.cells)
                copy.remove(cll)
                new_sent = Sentence(copy, sentence.count) 
                if new_sent not in self.knowledge:            
                    self.knowledge.append(new_sent) 

    def add_mines(self, sentence):
        """
        Checks the cells in the sentence, if they are mine
            1) marks them as mine
            2) adds them to the mines set()
        """
        for cll in sentence.known_mines():
            self.mark_mine(cll)
            self.mines.add(cll)
            # print(f"{cll} is mine")
            if len(sentence.cells) > 1:
                copy = set(sentence.cells)
                copy.remove(cll)
                new_sent = Sentence(copy, sentence.count - 1) 
                if new_sent not in self.knowledge:            
                    self.knowledge.append(new_sent)         
