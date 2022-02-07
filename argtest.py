import sys
import argparse
import json
parser = argparse.ArgumentParser()


subparser = parser.add_subparsers(dest='action')
subparser_add = subparser.add_parser('add', help='Add a show to the schedule')
subparser_delete = subparser.add_parser('delete', help='Delete a show from the schedule')
subparser_stop = subparser.add_parser('stop', help='Send a signal to the daemon to stop')
subparser_readme = subparser.add_parser('readme', help='Display important information about EpiGet')
subparser_license = subparser.add_parser('license', help='Display the Epiget License')

subparser_add.add_argument(
    '-t',
    required=True,
    action='store',
    nargs='*',
    type=str,
    help='Show title')

subparser_add.add_argument(
    '-y',
    action='store',
    nargs=1,
    type=str,
    help='The year the show premired')

subparser_add.add_argument(
    '-n',
    action='store',
    nargs='*',
    type=str,
    help='The network that produced the show')

subparser_delete.add_argument(
    '-id',
    required=True,
    action='append',
    type=int,
    help='The ID value of the show you wish to delete')

args = parser.parse_args(['add', '-t', 'Married', 'with', 'Children', '-y', '1988', '-n', 'Paramount', 'Network'])
if isinstance(args, argparse.Namespace):


print(args.__class__)