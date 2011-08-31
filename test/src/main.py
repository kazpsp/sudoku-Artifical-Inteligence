
'''
Created on Aug 24, 2011

@author: Amparo Luna y Rodrigo Zurek
'''

import sudoku

if __name__ == '__main__':
    msudoku=sudoku.sudoku()
    msudoku.readSudoku()
    msudoku.cycleSudoku()
