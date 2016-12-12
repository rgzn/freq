"""
Example program to demonstrate Gooey's presentation of subparsers
"""

import argparse

from gooey import Gooey, GooeyParser
from message import display_message

running = True


@Gooey(optional_cols=2, program_name="Subparser Layout Demo")
def main():
  settings_msg = 'Subparser example demonstating bundled configurations ' \
                 'for liege, hurl, and peg'
  parser = GooeyParser(description=settings_msg)
  parser.add_argument('--verbose', help='be verbose', dest='verbose',
                      action='store_true', default=False)
  subs = parser.add_subparsers(help='commands', dest='command')

  hurl_parser = subs.add_parser('hurl', help='hurl is a tool to transfer data from or to a server')
  hurl_parser.add_argument('Path',
                           help='URL to the remote server',
                           type=str, widget='FileChooser')



  # ########################################################
  liege_parser = subs.add_parser('liege', help='liege is an http/https regression testing and benchmarking utility')
  liege_parser.add_argument('--get',
                            help='Pull down headers from the server and display HTTP transaction',
                            type=str)



  # ########################################################
  peg_parser = subs.add_parser('peg', help='liege is an http/https regression testing and benchmarking utility')
  peg_parser.add_argument('Output',
                             help='Pull down headers from the server and display HTTP transaction',
                             widget='FileSaver', type=argparse.FileType)

  parser.parse_args()

  display_message()




if __name__ == '__main__':
  main()
