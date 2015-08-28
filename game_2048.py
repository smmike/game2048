"""
Clone of 2048 game, with win/lose detection
"""
# import poc_2048_gui
import random
import math

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def list2d(array2d):
    """
    Helper function to create deep copy of a 2D array
    """
    result = list()
    for row in array2d:
        result.append(list(row))
    return result


def key_of_max(dictionary):
    max_value = max(dictionary.values())
    for key in dictionary.keys():
        if dictionary[key] == max_value:
            return key


def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    output = []
    shift = 0
    for index in range(len(line)):
        if index == 0:
            output.append(line[index])
        else:
            # self.log index, shift, index - 1 - shift, output
            if line[index] == 0:
                shift += 1
            elif line[index] == output[index - 1 - shift]:
                output[index - 1 - shift] += line[index]
                output.append(0)
            elif output[index - 1 - shift] == 0:
                output[index - 1 - shift] += line[index]
                shift += 1
            else:
                output.append(line[index])
                # we should pad output array with 0 to the length of input
    while len(output) < len(line):
        output.append(0)
    return output


class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    NUMBER_OF_TRIALS = 1000
    DIRECTIONS = [LEFT, RIGHT, UP, DOWN]
    DIRECTION_NAMES = {LEFT: 'left', RIGHT: 'right', UP: 'up', DOWN: 'down'}
    OTHER_DIRS = {UP: [LEFT, RIGHT, DOWN], DOWN: [LEFT, RIGHT, UP], LEFT: [RIGHT, DOWN, UP], RIGHT: [LEFT, DOWN, UP]}

    def __init__(self, grid_height, grid_width):
        self._win_count = 2048
        self._suppress_output = False
        if grid_width < 2 or grid_height < 2:
            raise ValueError("Dimensions for the game's grid should be not less than 2x2")
        self._grid_height = grid_height
        self._grid_width = grid_width
        self._grid = None
        self._cells_list = [(row, col) for col in range(grid_width) for row in range(grid_height)]
        self._stuck = False
        self._win = False
        self._number_of_moves = 0
        self.reset()
        self._starting_cells = {}
        self._lines = {}
        # Initialize dictionary of starting cells for each direction
        for direction in OFFSETS.keys():
            self._starting_cells[direction] = self.get_starting_cells(direction)
            self._lines[direction] = {}
            for starting_cell in self._starting_cells[direction]:
                self._lines[direction][starting_cell] = self.get_line_cells(starting_cell, direction)
        # print self._starting_cells

    @staticmethod
    def merge_with_metrics(line):
        """
        This method merges a line towards its start and return a list consisting of 2 elements:
            * number of individual cells merges happened, where shift of a number at 1 cell to replace 0 is counted
                as 1 and actual merge of 2 equal values is counted as floating number between 1 and 2 calculated as
                follows: 1 + (len(line) - merged_index)/len(line), i.e. the closer a merge to the beginning the more
                score it gets
            * new merged line if there were any merges
        """
        output = []
        merge_factor = 0
        shift_factor = 0
        shift = 0
        for index in range(len(line)):
            if index == 0:
                output.append(line[index])
            else:
                # self.log index, shift, index - 1 - shift, output
                if line[index] == 0:
                    shift += 1
                elif line[index] == output[index - 1 - shift]:
                    output[index - 1 - shift] += line[index]
                    merge_factor += 1 #+ 4.0*(float(len(line)) - (index - 1 - shift))/len(line)
                    output.append(0)
                elif output[index - 1 - shift] == 0:
                    output[index - 1 - shift] += line[index]
                    shift += 1
                    shift_factor += 1
                else:
                    output.append(line[index])
        # we should pad output array with 0 to the length of input
        # while len(output) < len(line):
        #    output.append(0)
        trailing_zeroes_factor = len(line) - len(output)
        return [merge_factor, shift_factor, trailing_zeroes_factor, output] #return [merges + (len(line) - len(output)), output]

    def set_win_count(self, number):
        """
        Sets the number that should be obtained to win, which is by default 2048
        """
        power = math.log(number, 2)
        if int(power) != power:
            raise ValueError("Win number should be power of 2, e.g. 512 or 1024")
        self._win_count = number

    def log(self, output):
        if not self._suppress_output:
            print output

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self._stuck = False
        self._win = False
        self._number_of_moves = 0
        self._grid = [[0 for _ in range(self._grid_width)] for _ in range(self._grid_height)]
        for _ in (0, 1):
            self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        output = "  "
        for col in range(self._grid_width):
            output += "  " + str(col) + "  "
        output += "\n    "
        for col in range(self._grid_width):
            output += "-----"
        output += "\n "
        for row in range(self._grid_height):
            output += str(row) + " |"
            for col in range(self._grid_width):
                output += str(self._grid[row][col])
                for dummy_space_count in range(5 - len(str(self._grid[row][col]))):
                    output += " "
            output += "|\n "
        output += "  "
        for col in range(self._grid_width):
            output += "-----"
        return output

    @property
    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._grid_height

    @property
    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._grid_width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        if self._stuck:
            self.log("There's no more legal moves. You lost the game.")
        elif self._win:
            self.log("You won the game")
        changed = False
        for starting_cell in self._starting_cells[direction]:
            line = self.get_line(starting_cell, direction)
            merge_result = TwentyFortyEight.merge_with_metrics(line)
            if merge_result[0] + merge_result[1] != 0:
                changed = True
                self.replace_line(merge_result[-1], starting_cell, direction)
                if self._win_count in merge_result[-1]:
                    self._win = True
        if self._win:
            if not self._suppress_output:
                self._number_of_moves += 1
            self.log("Congratulations! You  won the game!")
        elif changed:
            if not self._suppress_output:
                self._number_of_moves += 1
            self.new_tile()
        else:
            legal_moves = 0
            for other_dir in TwentyFortyEight.OTHER_DIRS[direction]:
                # if other_dir != direction:
                legal_moves += self.check_move(other_dir)
                # if has_legal_moves:
                # break
            if legal_moves == 0:
                self._stuck = True
                self.log("There's no more legal moves. You lost the game.")
            self.log("Illegal move")

    def check_move(self, direction):
        """
        Checks how many changes would happen if move in the given direction.
        If this number is 0 it means that move is illegal
        """
        changes = 0
        initial_corner_sum = self.get_tile(0, 0) + self.get_tile(0, self._grid_width - 1) + \
            self.get_tile(self._grid_height - 1, self._grid_width - 1) + self.get_tile(self._grid_height - 1, 0)
        for starting_cell in self._starting_cells[direction]:
            line = self.get_line(starting_cell, direction)
            merge_result = TwentyFortyEight.merge_with_metrics(line)
            #print "merge result:", merge_result[0]
            changes += merge_result[0] + merge_result[1]#* 1.0 / (2 + starting_cell[0] + starting_cell[1])
        #print "changes:", changes
        return changes

    @property
    def is_won(self):
        """
            Returns whether user won the game, i.e. there's 2048 in some cell
        """
        return self._win

    @property
    def is_stuck(self):
        """
            Returns whether user is stuck with no legal moves in any direction
        """
        return self._stuck

    def get_number_of_moves(self):
        """
            Returns number of moves
        """
        return self._number_of_moves

    def get_starting_cells(self, direction):
        """
            Provided a direction in which a user would like to merge tiles
            this method returns a list of starting cells of all lines
            (that could be rows or columns) that need to be merged
        """
        starting_cells = []
        if OFFSETS[direction][1] == 0:
            for col in range(self._grid_width):
                starting_row = int(-0.5 + 0.5 * OFFSETS[direction][0])
                starting_cells.append((starting_row, col))
        else:
            for row in range(self._grid_height):
                starting_col = int(-0.5 + 0.5 * OFFSETS[direction][1])
                starting_cells.append((row, starting_col))
        return starting_cells

    def get_line_cells(self, starting_cell, direction):
        """
            Returns a list of cell co-ordinates traversing from a given 'starting_cell'
            in a given direction
        """
        if OFFSETS[direction][1] == 0:
            # row = starting_cell[0]
            return [(row, starting_cell[1]) for row in range(starting_cell[0], starting_cell[0] + OFFSETS[direction][0] * self._grid_height, OFFSETS[direction][0])]
        else:
            return [(starting_cell[0], col) for col in range(starting_cell[1], starting_cell[1] + OFFSETS[direction][1] * self._grid_width, OFFSETS[direction][1])]

    def get_line(self, starting_cell, direction):
        """
            Returns a list of values traversing from a given 'starting_cell'
            in a given direction
        """
        return [self._grid[pos[0]][pos[1]] for pos in self._lines[direction][starting_cell]]

    def replace_line(self, new_line, starting_cell, direction):
        """ Replace a line in the game grid starting with a given 'starting_cell'
            in a given 'direction' with the line provided in a 'new_line'
        """
        if OFFSETS[direction][1] == 0:
            row = starting_cell[0]
            for new_row in range(self._grid_height):
                if new_row < len(new_line):
                    self._grid[row][starting_cell[1]] = new_line[new_row]
                else:
                    self._grid[row][starting_cell[1]] = 0
                row += OFFSETS[direction][0]
        else:
            col = starting_cell[1]
            for new_col in range(self._grid_width):
                if new_col < len(new_line):
                    self._grid[starting_cell[0]][col] = new_line[new_col]
                else:
                    self._grid[starting_cell[0]][col] = 0
                col += OFFSETS[direction][1]

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        value = 2
        if random.random() > 0.9:
            value = 4
        empty_cells = [pos for pos in self._cells_list if self._grid[pos[0]][pos[1]] == 0]
        random_tile = random.choice(empty_cells)
        self.set_tile(random_tile[0], random_tile[1], value)

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._grid[row][col]

    def get_cell_value(self, pos):
        """
        Return the value of the tile at given cell position
        """
        return self._grid[pos[0]][pos[1]]

    def set_grid(self, grid):
        """
        Sets game's grid to the specified values
        """
        self._grid = list2d(grid)

    def get_suggestion(self):
        """
        Calculates the best move for given state
        :return: Returns direction of the best move according to AI player
        """
        if self._stuck:
            self.log("No legal moves")
            return
        if self._win:
            return
        #self._suppress_output = True
        directions_score = {}
        for direction in TwentyFortyEight.DIRECTIONS:
            direction_name = TwentyFortyEight.DIRECTION_NAMES[direction]
            merge_score = self.check_move(direction)
            if merge_score == 0:
                continue
            directions_score[direction_name] = merge_score
        #self._suppress_output = False
        if len(directions_score) == 0:
            self._stuck = True
            self.log("No legal moves. You lost the game")
            return "stuck"
        return key_of_max(directions_score)


# def test_merge(input, expected_output):
#     output = merge(input)
#     if output != expected_output:
#         self.log "Test failed for input:", input, "expected output:", expected_output, ", but was", output
#     else:
#         self.log "Test passed for input:", input, ". Output:", output


# test_merge([2, 0, 2, 4], [4, 4, 0, 0])
# test_merge([0, 0, 2, 2], [4, 0, 0, 0])
# test_merge([2, 2, 0, 0], [4, 0, 0, 0])
# test_merge([2, 2, 2, 2, 2], [4, 4, 2, 0, 0])
# test_merge([8, 16, 16, 8], [8, 32, 8, 0])


# poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
