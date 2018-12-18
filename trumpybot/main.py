
################################################################################
## Main                                                                       ##
## Entry point for running TrumpyBotPi                                        ##
################################################################################

from Brain.Brain import Brain


def main():
    trumpybot = Brain()

    while trumpybot.active:
        trumpybot.listen()
        trumpybot.interpret()


if __name__ == "__main__":
    main()
