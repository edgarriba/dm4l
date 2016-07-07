import sys
import time
import logging
from misc import Commands


class Monitor():
    def __init__(self, dm4l_instance, command={}, options={}, safe=True, refresh=1):
        self.dm4l = dm4l_instance
        self.refresh = refresh
        self.end = False
        self.command = command
        self.options = options

    def set_command(self, command, options):
        self.command = command
        self.options = options

    def print_max(self):
        if len(self.dm4l.get_handlers()) > 0:
            max = self.dm4l.get_max()
            res = []
            for i in self.options['format']:
                res.append(str(max[i]))
            print ' '.join(res)

    def plot(self):
        self.dm4l.plotter.multi_plot(self.options['x'], self.options['y'],
                                     'all', self.options['title'])

    def update(self):
        if self.dm4l.update():
            if self.command == Commands.MAX:
                self.print_max()
            elif self.command == Commands.PLOT:
                self.plot()

    def run(self):
        logging.getLogger('dm4l').info('Running monitor...')
        try:
            while not self.end:
                self.dm4l.update_input()
                self.update()
                time.sleep(1)
        except KeyboardInterrupt:
            logging.getLogger('dm4l').warn('\nExiting by user request.\n')
            sys.exit(0)

    def run_once(self):
        self.dm4l.plotter.set_persistent(True)
        self.update()