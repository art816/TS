#!/usr/bin/env python3

import sys
sys.path.append('.')
sys.path.append('..')

from web_parameters import show_device_from_NMS
import web_parameters

if __name__=='__main__':
    if len(sys.argv) == 1:
        show_device_from_NMS.main()
    else:
        if sys.argv[1] == '-v':
            print('version: ', web_parameters.__version__)
            sys.exit(0)
