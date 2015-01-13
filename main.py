#!/usr/bin/python

import sys
import logging
import random
import string
import time
import curses
from curses import wrapper

logging.basicConfig(filename='log.log',level=logging.DEBUG)



class CursedScreen(object):
    def __init__(self,screen=None):
        self.screen = screen
        self.max_y, self.max_x = screen.getmaxyx()
        curses.noecho()
        curses.cbreak()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
        self.screen.clear()
        curses.nocbreak()
        self.file_list = []
        self.screen_list = []
        self.screen_line_format = ("{:<"+str(self.max_x)+"}")
        self.demo_file = open("test.text","wb")

    def get_file(self,filename):
        self.file_list = []
        with open(filename,"rb") as open_file:
            for line in open_file:
                self.file_list.append(line.strip())

    def print_file_by_line(self):
        self.screen_list = [("{:<"+str(self.max_x)+"}").format("") for i in range(self.max_y)]
        for index, line in enumerate(self.file_list):
            del self.screen_list[0]
            self.screen_list.append(self.screen_line_format.format(line))
            self.print_screen()
        for i in range(self.max_y):
            del self.screen_list[0]
            self.screen_list.append(self.screen_line_format.format(""))
            self.print_screen(scramble=False)

    def print_screen(self,scramble=True):
        for index, line in enumerate(self.screen_list):
            line = self.scramble_line(line, index)
            self.print_line(line, index)
        self.screen.refresh()
        time.sleep(0.1)

    def scramble_line(self, line, index):
        scramble = (float(index)/(self.max_y))**3
        output = "".join([symbol if random.random() > scramble else random.choice(string.ascii_letters) for symbol in line])
        return output

    def print_line(self, line, y_coord, colour=None):
        if y_coord >= self.max_y:
            y_coord = self.max_y
        try:
            for x_coord, symbol in enumerate(line):
                self.print_character(y_coord,x_coord, symbol, colour=colour)
        except curses.error as e:
            logging.error(e)

    def print_character(self, y_coord, x_coord, character, colour=None):
        if y_coord > self.max_y-2:
            self.screen.addch(y_coord,x_coord,character, curses.color_pair(3))
        elif y_coord > self.max_y/2:
            self.screen.addch(y_coord,x_coord,character, curses.color_pair(2))
        else:
            self.screen.addch(y_coord,x_coord,character, curses.color_pair(1))

    
    def exit(self):
        self.demo_file.close()
        self.screen.keypad(0)
        curses.echo()
        curses.endwin()

def main():
    wrapper(_main)

def _main(stdscr):
    prog = CursedScreen(stdscr)
    filename = sys.argv[len(sys.argv)-1]
    prog.get_file(filename)
    prog.print_file_by_line()
    prog.exit()

if __name__ == '__main__':
    main()
