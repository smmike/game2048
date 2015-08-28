__author__ = 'smmike'

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


class Game2048AIPlayer:

    DIRECTIONS = [LEFT, RIGHT, UP, DOWN]
    DIRECTION_NAMES = {LEFT: 'left', RIGHT: 'right', UP: 'up', DOWN: 'down'}
    OTHER_DIRS = {UP: [LEFT, RIGHT, DOWN], DOWN: [LEFT, RIGHT, UP], LEFT: [RIGHT, DOWN, UP], RIGHT: [LEFT, DOWN, UP]}

    def __init__(self, game):
        self._game = game

    @staticmethod
    def merge_with_metrics(line):
        """
        This method merges a line towards its start and return a list consisting of 2 elements:
            * number of individual cells merges happened, where shift_factor of a number at 1 cell to replace 0 is counted
                as 1 and actual merge of 2 equal values is counted as floating number between 1 and 2 calculated as
                follows: 1 + (len(line) - merged_index)/len(line), i.e. the closer a merge to the beginning the more
                score it gets
            * new merged line if there were any merges
        """
        output = []
        merge_factor = 0
        shift_factor = 0
        merged = False
        for index in range(len(line)):
            if index == 0:
                if line[index] != 0:
                    output.append(line[index])
                else:
                    shift_factor += 1
            elif line[index] != 0:
                if len(output) > 0 and line[index] == output[-1] and not merged:
                    merge_factor += 1 + 1.0 * (float(len(line)) - len(output)) / len(line)
                    output[-1] += line[index]
                    merged = True
                else:
                    output.append(line[index])
                    merged = False
                    # else:
                    #     # self.log index, shift_factor, index - 1 - shift_factor, output
                    #     print index, shift, line, output
                    #     if line[index] != 0:
                    #         shift += 1
                    #     elif
                    #     elif line[index] == output[index - 1 - shift]:
                    #         output[index - 1 - shift] += line[index]
                    #         merge_factor += 1 #+ 4.0*(float(len(line)) - (index - 1 - shift_factor))/len(line)
                    #         output.append(0)
                    #     elif output[index - 1 - shift] == 0:
                    #         output[index - 1 - shift] += line[index]
                    #         shift += 1
                    #     else:
                    #         output.append(line[index])

        # we should pad output array with 0 to the length of input
        # while len(output) < len(line):
        #    output.append(0)
        shift_factor += len(line) - len(output)
        decrease_factor = 0
        if len(output) > 1:
            for index in range(1, len(output)):
                if output[index] < output[index - 1]:
                    decrease_factor += (len(output) - index) / (1.0 * len(output))
        return [merge_factor, shift_factor, decrease_factor,
                output]  # return [merges + (len(line) - len(output)), output]

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
            merge_result = Game2048AIPlayer.merge_with_metrics(line)
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
            for other_dir in Game2048AIPlayer.OTHER_DIRS[direction]:
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
                             self.get_tile(self._grid_height - 1, self._grid_width - 1) + self.get_tile(
            self._grid_height - 1, 0)
        for starting_cell in self._starting_cells[direction]:
            line = self.get_line(starting_cell, direction)
            merge_result = Game2048AIPlayer.merge_with_metrics(line)
            # print "merge result:", merge_result[0]
            changes += merge_result[0] + merge_result[1]  # * 1.0 / (2 + starting_cell[0] + starting_cell[1])
        # print "changes:", changes
        return changes

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
        # self._suppress_output = True
        directions_score = {}
        for direction in Game2048AIPlayer.DIRECTIONS:
            direction_name = Game2048AIPlayer.DIRECTION_NAMES[direction]
            merge_score = self.check_move(direction)
            if merge_score == 0:
                continue
            directions_score[direction_name] = merge_score
        # self._suppress_output = False
        if len(directions_score) == 0:
            self._stuck = True
            self.log("No legal moves. You lost the game")
            return "stuck"
        return key_of_max(directions_score)
