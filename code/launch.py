import sys
import logging
from controller import Controller

def main():
    if len(sys.argv) > 2:
        print("USAGE: \tpython3 launch.py [loglvl]")
        print("loglvl is the level of logging of the system: ")
        print("+ 0 for ERROR level")
        print("+ 1 for WARNING level")
        print("+ 2 for INFO level")
        print("+ 3 for DEBUG level")
        print("Default is ERROR + WARNING")
        print("Example: python3 launch.py 3")
        return

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    if len(sys.argv) == 2:
        if int(sys.argv[1]) == 0:
            logger.setLevel(logging.ERROR)
            print("Logger level set to: ERROR")
        elif int(sys.argv[1]) == 1:
            logger.setLevel(logging.WARNING)
            print("Logger level set to: WARNING")
        elif int(sys.argv[1]) == 2:
            logger.setLevel(logging.INFO)
            print("Logger level set to: INFO")
        elif int(sys.argv[1]) == 3:
            logger.setLevel(logging.DEBUG)
            print("Logger level set to: DEBUG")
        else:
            print("Wrong loglvl inserted: value ranges in [0,1,2,3]")
            return

    controller = Controller()
    sys.exit(controller.run())


if __name__ == '__main__':
    main()
