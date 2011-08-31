'''
Created on Aug 24, 2011

@authors   : Amparo Luna
             Rodrigo Zurek
          
@Email     : lunita980@hotmail.com
             rodrigozurek@hotmail.com
          
@Date      : August 30, 2011

@Versions  : 1.0 
'''

from xlrd import open_workbook
from xlwt.Workbook import Workbook
import copy

class sudoku(object):

    '''
    classdocs
    '''

    def __init__(self):
        self.sudoku=[]
        self.sudokuCheck=[]
        self.elements=[]
        self.elementInit()
        self.wb = Workbook()
        self.ws0 = self.wb.add_sheet('sudoku1',cell_overwrite_ok=True) 
        self.sw=1
        self.cont=0
        self.var=[]
        self.stack=[]
        self.file= open('log.txt','w')
        
    def elementInit(self):
        self.elements=[1,2,3,4,5,6,7,8,9]
        
    def writeExcel(self):
        for i in range(0,9):
            for j in range(0,9):
                if len(self.sudokuCheck[i][j]) == 1:
                    n=self.sudokuCheck[i][j][0]                        
                    self.sudoku[i][j]=n
                    self.ws0.write(i,j,n)
                else:                    
                    self.ws0.write(i,j,0.0)
                    self.sudoku[i][j]=0.0  
        
    def readSudoku(self):
        wb = open_workbook('test.xls')
        for s in wb.sheets():
            print 'Sheet:',s.name   
            for row in range(s.nrows):
                values = []
                for col in range(s.ncols):
                    values.append(int(s.cell(row,col).value))
                self.sudoku.append(values)   
        
                
    def globalCheck(self):
        self.mostConstrainedVariable()
        ng=30
        value=0
        for l in self.var:
            cons=0
            cons2=0
            if len(self.sudokuCheck[l[0]][l[1]])>1:                
                for k in self.sudokuCheck[l[0]][l[1]]:
                    cons += self.checkRowConstrains(l[0], l[1], k) 
                    cons += self.checkColumnConstrains(l[0], l[1], k)
                    cons += self.checkBoxConstrains(l[0], l[1], k)
                    cons2+=1
                    self.sw=1
                                       
            else:
                cons += self.checkRowConstrains(l[0], l[1], self.sudokuCheck[l[0]][l[1]][0]) 
                cons += self.checkColumnConstrains(l[0], l[1], self.sudokuCheck[l[0]][l[1]][0])
                cons += self.checkBoxConstrains(l[0], l[1], self.sudokuCheck[l[0]][l[1]][0])
                self.sw=1
            if cons<ng  :
                ng=cons
                cons3=cons2
                value=copy.deepcopy(l)
          
        if(value!=0):                
            sc=copy.deepcopy(self.sudokuCheck)
            self.file.writelines("----Introduccion de Elemento----\n")
            self.file.writelines("se introdujo el valor:" + str(self.sudokuCheck[value[0]][value[1]][cons3-1]) +" En la posicion: "+ str(value[0]+1)+","+str(value[1]+1)+ " ya que es la variable mas restringida y menos restrictora\n") 
            self.file.writelines( "--------------------------------\n")            
            self.file.writelines( "----Sudoku----\n")
            self.file.writelines( str(self.sudoku)+"\n")
            self.sudoku[value[0]][value[1]]=self.sudokuCheck[value[0]][value[1]][cons3-1]            
            stackItem=[value[0],value[1],sc[value[0]][value[1]]]            
            self.stack.append(stackItem)       
            sc[value[0]][value[1]].pop(cons3-1)             
        self.file.writelines( str(self.sudoku )+"\n")
        self.file.writelines( "----Sudoku----\n")
        
             
    def checkSudokuCheck(self):
        for i in range(0,9):
            for j in range(0,9):
                if(len(self.sudokuCheck[i][j])==0):
                    self.file.writelines( "----- Backtrack -----\n"  )                                            
                    return 0                
        return 1                                            
       
    def cycleSudoku(self):
        cont=0
        while self.sw:
            self.sudokuCheck=[]
            self.sw=0
            self.checkSudoku()
            cont+=1           
        self.file.writelines( "---- Numero de Iteraciones ----\n")
        self.file.writelines(str( cont)+"\n")
        self.file.writelines( "-------------------------------\n")
        self.writeExcel()
        self.wb.save('sudoku.xls')
        self.file.close()
        print "El sudoku a sido resuelto\n...\n...\n...\nlog.txt creado\nsudoku.xls creado"
                
    def checkSudoku(self):        
        for i in range(0,9):
            jcheck=[]
            for j in range(0,9):
                v=[]
                if self.sudoku[i][j]==0.0:                                           
                    self.checkRow(i, j)
                    self.checkColumn(i, j)
                    self.checkBox(i, j)
                    v=self.elements                    
                    self.elementInit()                    
                else:
                    v.append(self.sudoku[i][j])
                jcheck.append(v)
            self.sudokuCheck.append(jcheck)
        self.file.writelines( "----- Matriz de Posibilidades -----\n")
        for k1 in range(0,9):
            s=[]
            for k2 in range(0,9):
                s.append(self.sudokuCheck[k1][k2])           
            self.file.writelines( str(s)+"\n")
        self.file.writelines( "-------------------------\n")
        if(self.checkSudokuCheck()):
            self.globalCheck()
        else:
            self.sudokuBacktrack()
        
    def sudokuBacktrack(self):
        sw1=1
        while sw1:                 
            b=self.stack.pop()
            if len(b[2])!=0:
                self.file.writelines( "backtracking en la posicion: "+str(b[0]+1)+","+str(b[1]+1)+"... Posibilidades disponibles: "+str(b[2])+"\n")
                sw1=0
            else:
                self.sudoku[b[0]][b[1]]=0
        maxc=30
        i2=0
        for i in range(0,len(b[2])):
            conti=0
            conti+=self.checkRowConstrains(b[0], b[1], b[2][i])
            conti+=self.checkColumnConstrains(b[0], b[1], b[2][i])
            conti+=self.checkBoxConstrains(b[0], b[1], b[2][i])
            if conti<maxc:
                maxc=conti 
                i2=i
        self.sudoku[b[0]][b[1]]=b[2].pop(i2)   
        self.stack.append(b)      
        self.sw=1
        
     
    def checkRow(self,i,j):
        for k in  range(0,9):       
            if(self.elements.count((self.sudoku[i][k]))>0):
                self.elements.remove(self.sudoku[i][k])
                    
    def checkColumn(self,i,j):
        for k in  range(0,9):
            if(self.elements.count((self.sudoku[k][j]))>0):
                self.elements.remove(self.sudoku[k][j])
                    
    def checkBox(self,i,j):
        if i<3:
            if j<3:
                i2=0    
                j2=0
            elif j>=3 and j<6:
                i2=0
                j2=3
            else:
                i2=0
                j2=6
            
        elif i>=3 and i<6:
            if j<3:
                i2=3
                j2=0                
            elif j>=3 and j<6:
                i2=3
                j2=3
            else:
                i2=3
                j2=6 
                     
        else:
            if j<3:
                i2=6
                j2=0
            elif j>=3 and j<6:
                i2=6
                j2=3
            else:
                i2=6
                j2=6
        
        for i3 in range(i2,i2+3):
            for j3 in range(j2,j2+3):
                if(self.elements.count((self.sudoku[i3][j3]))>0):
                    self.elements.remove(self.sudoku[i3][j3])
            
    def checkRowConstrains(self,i,j,n):
        rowConst=0
        for k in  range(0,9):       
            if(k!=j and self.sudokuCheck[i][k].count(n)==1):
                rowConst += 1
        return rowConst        
                
                    
    def checkColumnConstrains(self,i,j,n):
        columnConst=0
        for k in  range(0,9):
            if(k!=i and self.sudokuCheck[k][j].count(n)==1):
                columnConst += 1
        return columnConst    
                    
    def checkBoxConstrains(self,i,j,n):
        boxConst=0
        if i<3:
            if j<3:
                i2=0    
                j2=0
            elif j>=3 and j<6:
                i2=0
                j2=3
            else:
                i2=0
                j2=6
            
        elif i>=3 and i<6:
            if j<3:
                i2=3
                j2=0                
            elif j>=3 and j<6:
                i2=3
                j2=3
            else:
                i2=3
                j2=6 
                     
        else:
            if j<3:
                i2=6
                j2=0
            elif j>=3 and j<6:
                i2=6
                j2=3
            else:
                i2=6
                j2=6
        
        for i3 in range(i2,i2+3):
            for j3 in range(j2,j2+3):
                if i3!=i and j3!=j and self.sudokuCheck[i3][j3].count(n)==1:                    
                    boxConst+=1
        return boxConst     


    def mostConstrainedVariable(self):
        m=10
        var=[]
        for i in range(0,9):
            for j in range(0,9):
                if self.sudoku[i][j]==0:
                    if len(self.sudokuCheck[i][j]) <= m:
                        m=len(self.sudokuCheck[i][j])
                        var.append([i,j])
        var2=copy.deepcopy(var)
        for v in var2:
            if len(self.sudokuCheck[v[0]][v[1]])>m:
                var.remove(v)
        self.var=copy.deepcopy(var)
        
