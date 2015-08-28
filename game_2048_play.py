__author__ = 'mismirno'
import game_2048

game = game_2048.TwentyFortyEight(3, 4)
print game
while True:
    print "Suggested move:", game.get_suggestion()
    str_dir = raw_input("Enter up(u), down(d), left(l) or right(r):")
    print "Moving", str_dir
    if str_dir == "up" or "up".startswith(str_dir):
        game.move(game_2048.UP)
    elif str_dir == "down" or "down".startswith(str_dir):
        game.move(game_2048.DOWN)
    elif str_dir == "left" or "left".startswith(str_dir):
        game.move(game_2048.LEFT)
    elif str_dir == "right" or "right".startswith(str_dir):
        game.move(game_2048.RIGHT)
    else:
        print "Incorrect input. Try again"
        continue
    print "Number of moves:", game.get_number_of_moves()
    print game
    if game.is_won or game.is_stuck:
        break
