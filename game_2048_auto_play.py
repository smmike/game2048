__author__ = 'mismirno'
import game_2048


def game_attempt():
    game = game_2048.TwentyFortyEight(4, 4)
    game.set_win_count(512)
    #print game
    while True:
        # print "Suggested move:",
        str_dir = game.get_suggestion()
        #print "Moving", str_dir
        if str_dir == "up" or "up".startswith(str_dir):
            game.move(game_2048.UP)
        elif str_dir == "down" or "down".startswith(str_dir):
            game.move(game_2048.DOWN)
        elif str_dir == "left" or "left".startswith(str_dir):
            game.move(game_2048.LEFT)
        elif str_dir == "right" or "right".startswith(str_dir):
            game.move(game_2048.RIGHT)
        elif game.is_stuck:
            print "Game lost"
        else:
            assert "Unexpected output:", str_dir
        #    print "Incorrect input. Try again"
        #    continue
        #print "Number of moves:", game.get_number_of_moves()
        # print game
        if game.is_won or game.is_stuck:
            break
    return game.is_won

ATTEMPTS = 100
result = 0
for attempt in range(ATTEMPTS):
    if game_attempt():
        result += 1
print result, "wins of", ATTEMPTS, "attempts"
