# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 16:24:18 2016

@author: jweissman
"""

from gooey import Gooey, GooeyParser
from message import display_message

@Gooey(program_name="Frequency Finder",
       optional_cols=2)

def main():
  desc = "VHF Collar Frequency Availability" 
  parser = GooeyParser(description = desc)
  parser.add_argument('--verbose', help='be verbose', dest='verbose',
                      action='store_true', default=False)
  
  subs = parser.add_subparsers(help='commands', dest='command')
 
  # Pop finder:
  popfinder_parser = subs.add_parser('popfinder', help='Input a frequency, find populations where it could be placed')
  popfinder_parser.add_argument('frequency', 
                                help='Enter a VHF frequency in KHz to find where it could be placed',
                                type='float')
  # Frequency finder: 
  freqfinder_parser = subs.add_parser('freqfinder', help='Input populations, find frequencies that are available')

  
  
  parser.parse_args()
  
  display_message()
  
if __name__ == '__main__':
  main()