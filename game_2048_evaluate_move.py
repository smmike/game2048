__author__ = 'mismirno'
import game_2048
import cProfile

game = game_2048.TwentyFortyEight(3, 4)
print game


def main():
    print "Suggested move:", game.get_suggestion()

#main()
cProfile.run('main()')

