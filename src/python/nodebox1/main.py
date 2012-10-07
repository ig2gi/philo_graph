#!/usr/bin/env python
# encoding: utf-8
"""
main.py

Created by Gilbert Perrin on 2007-12-20.
Copyright (c) 2007 __G2G__. All rights reserved.
"""

import sys
import os
from nodebox.graphics import Context
from nodebox.util import random, choice, grid, files
from AppKit import NSApplication
NSApplication.sharedApplication().activateIgnoringOtherApps_(0)

import philo2


def main():
  
  global _ctx
  _ctx = Context()
  philo.__main__(_ctx)


if __name__ == '__main__':
	main()