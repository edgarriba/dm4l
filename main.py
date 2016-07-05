import os
import sys
import logging
import argparse
from monitor import Monitor
from misc import Commands
from logger import logger
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from graphics.config import plot_conf
from dm4l import DM4L



def plot(dm4l, x, y, title, legend, plot_params):
    dm4l.plotter.multi_plot(x, y, 'all', title, legend, plot_params)

if __name__ == '__main__':
    dm4l = DM4L()
    parser = argparse.ArgumentParser(description='~ Dark Magic 4 Logs ~')

    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('--logs', type=str, nargs=2, help="""log_path1,log_path2 backend1[,backend2...]
    The backend should be in %s""" %str(dm4l.get_backends()))
    group.add_argument('--file', type=str, default='./monitors.conf', help="Reads: log_path<space>backend\\nlog_path... from here")
    group.add_argument('--path', type=str, default=None, nargs=2, help="Reads all logs in path. Ex. --from_path ./*.log")
    parser.add_argument('--safe', action='store_false', help="Ignore erroneous logs")
    parser.add_argument('--silent', action='store_true', help='Do not show warnings')
    parser.add_argument('--refresh', type=int, default=0, help="Seconds to refresh data. 0 = run once.")
    subparsers = parser.add_subparsers(dest='subcommand')
    parser_max = subparsers.add_parser('max')
    parser_max.add_argument('--format', default=[0], type=int, nargs='+',
                        help="any combination of 0,1,2 where 0 = max, 1 = argmax, 2 = maxid. Ex: 0 2 = max_value id")
    parser_plot = subparsers.add_parser('plot')
    parser_plot.add_argument('-x', type=str, default=plot_conf['x'], help="Data to show in x axis.")
    parser_plot.add_argument('-y', type=str, nargs='+', default=plot_conf['y'], help="Data to show in y axis.")
    parser_plot.add_argument('--title', type=str, default='')


    #parser_report = subparsers.add_parser('--report')

    args = parser.parse_args()

    if args.silent:
        logger.setLevel(logging.FATAL)
    else:
        logger.setLevel(logging.INFO)
        with open(os.path.join(os.path.dirname(__file__), 'logo.txt'),'r') as infile:
            logger.info(infile.read())
            [h.flush() for h in logger.handlers]

    dm4l = DM4L()
    dm4l.set_safe(True)
    if args.logs is not None:
        args.logs[0] = args.logs[0].split(',')
        args.logs[1] = args.logs[1].split(',')
        if len(args.logs[1]) == 1 and len(args.logs[1]) < len(args.logs[0]):
            args.logs[1] *= len(args.logs[0])
        assert(len(args.logs[1]) == len(args.logs[0]))
        dm4l.set_input(DM4L.FROM_LIST, args.logs)
    elif args.path is not None:
        dm4l.set_input(DM4L.FROM_FOLDER, args.path)
    elif args.file is not None:
        dm4l.set_input(DM4L.FROM_FILE, args.file)

    dm4l.update_input()

    monitor = Monitor(dm4l)
    if args.subcommand == 'max':
        monitor.set_command(Commands.MAX, {'format':args.format})
    elif args.subcommand == 'plot':
        monitor.set_command(Commands.PLOT, {'x':args.x, 'y':args.y, 'title':args.title})

    if args.refresh > 0:
        monitor.refresh = args.refresh
        monitor.run()
    else:
        monitor.run_once()


