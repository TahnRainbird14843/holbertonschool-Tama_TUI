import curses
import os

def main(stdscr):
    stdscr.nodelay(True)
    key = ""
    stdscr.clear()
    stdscr.addstr("Detected key:")
    while True:
        try:
            key = stdscr.getkey()
            stdscr.clear()
            stdscr.addstr("Detected key:")
            stdscr.addstr(key)
            if key == os.linesep:
                break
        except Exception as e:
            pass


if __name__ == "__main__":
    curses.wrapper(main)
