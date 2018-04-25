'''
A simple checker script that made by G. E. Oscar Toreh

This work is licensed under the Creative Commons Attribution 4.0 Unported License. To view a copy of this license, visit https://creativecommons.org/licenses/by/4.0/ or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.
'''

import sys
import traceback

def getInfo(ref=None):
	print(' ----------- Error found ------------ ')
	exc_type, exc_obj, exc_tb = sys.exc_info()
	print(sys.exc_info())
	print('pada baris {0}'.format(exc_tb.tb_lineno))
	traceback.print_exc()
	if ref is not None:
		print('referensi:')
		print(ref)
	print(' ------------------------------------ ')
	
	