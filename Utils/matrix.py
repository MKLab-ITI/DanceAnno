#  Low Level Functions
import types
import random
import math
import time

euler =  2.718281828


##############################################
# 1. Matrix Initializations ---
##############################################

def size(matrix):
    return len(matrix),len(matrix[0]) 

def zeros(m,n):
    # Create zero matrix
    return [[0.0 for row in range(n)] for col in range(m)]

def T(matrix):
    # Transpose of a Matrix
    return [list(tup) for tup in zip(*matrix)]
 
def TList(ListIn):
    # Transpose of a list
    return [[ListIn[i]] for i in range(len(ListIn))]


def zerosSWCol(D,N,SWCol):
    # Create zero sparse matrix
    # The rows correspond to features
    
    matrix = D*[None]    
    for d in range(D):    
        if SWCol[d]==1: matrix[d] = N*[0] 
                 
    return matrix

def complexzeros(m,n):
    # Create zero matrix
    return [[0.0+0.0j for row in range(n)] for col in range(m)]

def zeros3D(d,m,n):
    # Create zero matrix 3D
    return ([[[0.0 for row in range(n)] for col in range(m)]
                                                 for dim in range(d)])

def ones(m,n):
    # Create ones matrix
    return [[1.0 for row in range(n)] for col in range(m)]


def eye(n):
    # Create eye matrix
    new_matrix = [[0 for row in range(n)] for col in range(n)]
    for i in range(n):
        new_matrix[i][i]=1.0
    return new_matrix

def randuni(m,n):
    # Create random matrix from uniform distribution at [0,1]
    return [[random.random() for row in range(n)] for col in range(m)]

def randuniVec(n,s):
    # Create random matrix from uniform distribution at [0,1]
    return [s*random.random() for i in range(n)]


def rand(m,n,s):
    #s = s/2.0
    # Create random matrix
    # normal distribution 0 mean 1 var
    return [[random.gauss(0,s) for row in range(n)] for col in range(m)]

def rotrand(mat,RotMat):
    # Rotate a Guassian random matrix mat with rotmat matrix
    N       = len(mat)
    new_mat = zeros(N,2)
        
    for i in range(N):
        new_mat[i] = Mat2Vec(multMat([mat[i]],RotMat))
    
    return new_mat

def show(matrix):
    # Print out matrix
    for col in matrix: print (col)

def drange(a,b,c):
    # Decimal range  a,a+c,a+2c,...,b
    L = int(round((b-a)/c + 1))
    Out = L*[0]
    
    Out[0] = a
    
    for i in range(L):
        if i==0:
            continue
        Out[i] = Out[i-1] + c
        
    return Out

def Factorial(n):
    # Factorial of an integer < 30
    n   = int(n)
    Out = 1 
    for i in range(n):  Out = Out*(i+1)
    
    return Out

def realVec(vec):
    # return the real part of a list (vector)
    N   = len(vec)
    Out = vec
     
    for i in range(N):
        if type(vec[i])==complex:
           Out[i] = vec[i].real
         
    return Out    

def cmp(a, b):
    return (a > b) - (a < b)

        
def sign(number):
    # The sign of a number
    return cmp(number, 0)

def sortOrd(list):
    # return the ordered index of a list
    #Indx = range(len(list))
    #Indx.sort(lambda x,y: cmp(list[x],list[y]))

    Indx = sorted(range(len(list)), key=lambda k: list[k])

    return Indx

def signVec(vec):
    return list(map(sign,vec))

def tanh(x):
    return (euler**(2.0*x)-1.0)/(euler**(2.0*x)+1.0)


###############################################
# 2. Matrix Algebraic functions ---                 
#----------------------------------------------
#              ADDITIONSs
#     ADDITION:  Matrix with Matrix 

def add(matrix1,matrix2):
    N,D = size(matrix1)
    return [[matrix1[i][j] + matrix2[i][j] for j in range(D)] 
                                           for i in range(N)]  

#===========================================
#      Add: vec1 +  vec2 
#===========================================
def addVec(vec1,vec2):
    return list(map(lambda x,y:x+y,vec1,vec2))

#===========================================
#      AddTract: Fl +  vec 
#===========================================
def addFlVec(NumFl,vec):
    N = len(vec)
    NumFl = float(NumFl)
    
    new_vec = N*[0]
    for i in range(N):
        new_vec[i]= vec[i] + NumFl
        
    return new_vec

#===========================================
#      AddTract: Int +  vec 
#===========================================
def addIntVec(NumInt,vec):
    N = len(vec)
        
    new_vec = N*[0]
    for i in range(N):
        new_vec[i]= vec[i] + NumInt
        
    return new_vec

#================================================
#     SUM: all values of a matrix   
#================================================
def SumVal(matrix):
    SUM = 0
    for d in range(len(matrix)):
        SUM += sum(matrix[d])
            
    return SUM        

#================================================
#   Sum of matrix vertically 1 or Horizontally 2   
#================================================
def sumMat(matrix,Dim):
    if Dim==2:
       matrix = T(matrix)    
    N = len(matrix)

    M = zeros(N,1)
    
    for i in range(N):
        M[i][0] += sum(matrix[i])

    if Dim==2: M = T(M) 
    return M 
       
#===========================================
#   Mean of matrix vertically 1 or Horizontally 2   
#===========================================
def mean(matrix,Dim):
    M = sumMat(matrix,Dim)

    if Dim==1:
       DivFactor = len(matrix[0])    
    elif Dim==2:
       DivFactor = len(matrix)
        
    return multFlMat(1.0/DivFactor,M)       
       
#======================================================
#  Sum of complex matrix vertically 1 or Horizontally 2   
#=====================================================
def complexsum(matrix,Dim):
    if Dim==2:
       matrix = T(matrix)    
    N = len(matrix)

    M = complexzeros(N,1)
    
    for i in range(N):
        M[i][0] += sum(matrix[i])

    if Dim==2: M = T(M) 
    return M 

#===========================================
#      Matrix subtraction
#===========================================
def subMat(matrix1,matrix2):
    N,D = size(matrix1)
    
    new_matrix = zeros(N,D)
    
    for i in range(N):
        new_matrix[i] = subVec(matrix1[i],matrix2[i])
    return new_matrix

#===========================================
#      Matrix subtraction
#===========================================
def subVec(vec1,vec2):
    return list(map(lambda x,y:x-y,vec1,vec2))

#===========================================
#      SubTract: vec - Fl
#===========================================
def subVecFl(vec,NumFl):
    N     = len(vec)
    NumFl = float(NumFl)
    
    new_vec = N*[0]
    for i in range(N):
        new_vec[i]= vec[i] - NumFl
        
    return new_vec

#===========================================
#      SubTract: Matrix - Fl
#===========================================
def subMatFl(matrix,NumFl):
    N,D   = size(matrix)
    NumFl = float(NumFl)
    
    new_matrix = zeros(N,D)
    for i in range(N):
        new_matrix[i]= subVecFl(matrix[i],NumFl)
        
    return new_matrix

#===========================================
#      SubTract: Fl - vec 
#===========================================
def subFlVec(NumFl,vec):
    N,NumFl = len(vec),float(NumFl)
   
    new_vec = N*[0]
    for i in range(N): new_vec[i]= NumFl - vec[i]
        
    return new_vec

#===========================================
#   Multiply Float to matrix    
#===========================================
def multFlMat(FlNum,matrix):
      
    if type(matrix)==int or type(matrix)==float:
        return FlNum*matrix
    else:            
        R,C = size(matrix)
        return [[FlNum*matrix[i][j] for j in range(C)] for i in range(R)]

#===========================================
#   Multiply Float to vec
#===========================================
def multIntVec(Num,vec):
    return [vec[i]*Num for i in range(len(vec))]

#===========================================
#   Multiply Float to vec
#===========================================
def multFlVec(FlNum,vec):
   
    if type(vec)==int or type(vec)==float:
        # Case vec is a value 
        return FlNum*vec
    else:
        return [vec[i]*FlNum for i in range(len(vec))]

#===========================================
#   Multiply Complex to vec
#===========================================
def multComplexVec(CNum,vec):
    
    # Complex with Matrix multiplication
      
    if type(vec)==int or type(vec)==float:
        Out = FlNum*vec
        return Out
    
    N = len(vec)
    Out = N*[0+0j]    
    
    for i in range(N):
        Out[i] = CNum*vec[i]

    return Out

#===========================================
#      Matrix multiplication
#===========================================
def multMat(matrix1,matrix2):
    # Matrix multiplication
    if len(matrix1[0]) != len(matrix2):
        # Check matrix dimensions
        print ('Matrices must be m*n and n*p to multiply!')
    else:
        # Multiply if correct dimensions
        new_matrix = zeros(len(matrix1),len(matrix2[0]))
        for i in range(len(matrix1)):
            for j in range(len(matrix2[0])):
                for k in range(len(matrix2)):
                    new_matrix[i][j] += matrix1[i][k]*matrix2[k][j]
        
        return new_matrix

#===========================================
#   Element wise multiplication of matrices   
#===========================================
def multMatElw(mat1,mat2):
    N,D = size(mat1)
#    for i in range(N):
#        for j in range(D):
#            new_matrix[i][j] =  matrix1[i][j] * matrix2[i][j]
    return [[mat1[i][j]*mat2[i][j] for i in range(N)] for j in range(D)]

#===========================================
#   Element wise multiplication of vectors   
#===========================================
def multVecElw(vec1,vec2):
    N = len(vec1)
    new_vec = N*[0]
    for i in range(N):
        new_vec[i]=vec1[i]*vec2[i]
    return new_vec

#===========================================
#   Power Float to matrix    
#===========================================
def powFlMat(FlNum,matrix):
    
    if type(matrix)==int or type(matrix)==float:
        Out = pow(FlNum,matrix)
        return Out
    
    R,C = size(matrix)
        
    new_matrix = zeros(R,C)
    for i in range(R):
        for j in range(C):
            new_matrix[i][j] = FlNum**matrix[i][j]
    return new_matrix

#===========================================
#   Power matrix to float    
#===========================================
def powMatFl(matrix,FlNum):
    
    
    if type(matrix)==int or type(matrix)==float:
        Out = pow(matrix,FlNum)
        print (Out)
        return Out
    
    R = len(matrix)
    C = len(matrix[0])
    
    new_matrix = zeros(R,C)
    for i in range(R):
        for j in range(C):
            new_matrix[i][j] = matrix[i][j]**FlNum
    return new_matrix

#===========================================
#   Power vector to float    
#===========================================
def powVecFl(vec,FlNum):
    
    if type(vec)==int or type(vec)==float:
       return vec**FlNum
    else:     
       return [vec[i]**FlNum for i in range(len(vec))]

#===========================================
#   Power float to vector    
#===========================================
def powFlVec(FlNum,vec):
    
    if type(vec)==int or type(vec)==float:
        return FlNum**vec
    else:    
        return [FlNum**vec[i] for i in range(len(vec))]

#=============================================
#   Element wise power for matrices   
#=============================================
def powElwMat(matrix,Number):
    n,d = size(matrix)
               
    powMat = zeros(n,d)
    for i in range(n):
        for j in range(d):
            powMat[i][j] = matrix[i][j]**Number 
    return powMat  


#===========================================
#   Exp of matrix    
#===========================================
def exp(matrix):
    return [expVec(matrix[i]) for i in range(len(matrix))]

#===========================================
#    Exp of Complex matrix    
#===========================================
def expComplexMat(matrix):
    R,C = size(matrix)
   
    new_matrix = complexzeros(R,C)
    for i in range(R):
        for j in range(C):
            new_matrix[i][j] =  euler**matrix[i][j] 
    
    return new_matrix

#===========================================
#   Exp of vec (float) 
#===========================================
def expVec(vec):
    return list(map(math.exp,vec))

#===========================================
#   Logarithms 
#===========================================

#   Log10 of a vec    
def log10Vec(vec):
    return list(map(math.log10,vec))

#   LogNormal of a vec    
def logNVec(vec):
    return list(map(math.log,vec))

#   Log10 of a Matrix    
def log10Mat(mat):
    return [log10Vec(mat[i]) for i in range(len(mat))]

#   LogN of a Matrix    
def logNMat(mat):
    return [logNVec(mat[i]) for i in range(len(mat))]


#===========================================
#      Divide Float to matrix    
#===========================================
def divFlMat(FlNum,matrix):
    N,D = size(matrix)
    
    new_matrix = zeros(N,D)
    for i in range(N):
        for j in range(D):
            new_matrix[i][j] = FlNum/matrix[i][j]
    return new_matrix

#===========================================
#      Divide Float to vector    
#===========================================
def divFlVec(FlNum,vec):
    return [FlNum/vec[i] for i in range(len(vec))]

#===========================================
#   Element wise division of matrices   
#===========================================
def divElw(matrix1,matrix2):
    N,D  =size(matrix1)    
    return [[matrix1[i][j] / matrix2[i][j] for j in range(D)] 
                                           for i in range(N)]    

#===========================================
#   Element wise division of vectors   
#===========================================
def divElwVec(vec1,vec2):
    return list(map(lambda x,y: x/y, vec1, vec2))#

#===========================================
#   Element wise absolute value for vectors   
#===========================================
def absElwVec(vector):
    return list(map(abs,vector))

#=============================================
#   Element wise absolute value for matrices   
#=============================================
def absElwMat(matrix):
    return [absElwVec(matrix[i]) for i in range(len(matrix))]


#=============================================
#        Product of a vector elements 
#=============================================
def prod(vector):
    p = 1
    for i in vector:
        p *= i
    return p

#=============================================        
# 3. SORTING: MAX and SORT ---
#=============================================
    
#=============================================
#  Estimate Max and Arg Max of Mat Rows 
#=============================================
def maxRow(matrix): 
    N,M = size(matrix)
    
    ArgMaxVec = N*[0]
    MaxVec    = N*[0] 
    
    MaxVec  = list(map(max,matrix))
        
    for i in range(N):
        ArgMaxVec[i] = matrix[i].index(MaxVec[i])
                
    return MaxVec,ArgMaxVec

#=============================================
#  Estimate Max and Arg Max of a vec  
#=============================================
def maxVec(vec): 
    MaxVal = max(vec)
    return MaxVal, vec.index(MaxVal)

#=============================================
#  Estimate Min and Arg Min of Vec list 
#=============================================
def minVec(vec): 
    MinVal = min(vec)
    return MinVal, vec.index(MinVal)
    

# REM: HERE
    
    
#=============================================
#   Median of matrix vertically 1 or Horizontally 2
#=============================================
def median(matrix,Dim):
    N,D = size(matrix)
                  
    if Dim==1:
       M = zeros(N,1)
       for i in range(N):
           A = sorted(Mat2Vec(getRow(matrix,i))) 
           M[i][0] = A[int(N/2)]    
    elif Dim==2:
       M = zeros(1,D)
       Matrix2 = T(matrix)
       for i in range(D):
           A = sorted(Mat2Vec(getRow(Matrix2,i)))
           M[0][i] = A[int(N/2)]    
    
    return M
#======================================
# Differentiate Lines of a matrix
#======================================
def diffMat(matrix):
    N,K = size(matrix)
        
    new_mat = zeros(N,K)
    
    for i in range(N-1):
        new_mat[i] = subVec(matrix[i+1],matrix[i])
    
    new_mat[N-1] = new_mat[N-2]    
    
    return new_mat
#----------------------------------------------------
#       Replications, gets, and rotations
#----------------------------------------------------    
    
#=============================================
#   Repeat a vertical vec DTimes to Horizontal   
#=============================================
def repvecCOL(vec,DTimes):
    # vec is a Nx1 vector
    N = len(vec)
    
    M = zeros(N,DTimes)
    for i in range(N):
        for j in range(DTimes):
            M[i][j] = vec[i][0]
    
    return M

#=============================================
#   Repeat a horizontal vec NTimes to vertical   
#=============================================
def repvecROW(vec,NTimes):
    # vec is a 1xD vector
    D = len(vec[0])
                
    M = zeros(NTimes,D)
    for i in range(NTimes):
        for j in range(D):
            M[i][j] = vec[0][j]
    
    return M

#=============================================
#        Get Column of a matrix
#=============================================
def getCol(matrix,j):
    N = len(matrix)
    ColVec = zeros(N,1)
    
    for i in range(N): ColVec[i][0] = matrix[i][j]
    
    return ColVec

#=============================================
#        Get Row of a matrix
#=============================================
def getRow(matrix,i):
    D = len(matrix[0])
    RowVec = zeros(1,D)
    
    for j in range(D):
        RowVec[0][j] = matrix[i][j]
    
    return RowVec

#=============================================
#        Get Diag of a matrix nxn
#=============================================
def getDiag(matrix):
    n = len(matrix)
    DiagVec = zeros(1,n)
        
    for j in range(n):
        DiagVec[0][j] = matrix[j][j]
    
    return DiagVec


#=============================================
#     Transform matrix to vector 
#=============================================
def Mat2Vec(matrix):
    N,D = size(matrix)
        
    if D == 1:
        M = [0 for i in range(N)]
        for i in range(N):
            M[i] = matrix[i][0]
    else:
        M = [0 for i in range(D)]
        for i in range(D):
            M[i] = matrix[0][i]        
    
            
    return M



 

#=========================================================
#           Handle Inconsistencies of EM
#             written for Python 2.5 
#=========================================================
def Incs(ProbMixtInit,IndexMixt): 
    eps = 2.2 * 10e-10
    Inf = 10  * 10e+10
     
    ZeroProbMixt = (FindMatLNum(ProbMixtInit,eps)+ \
                              FindMatGNum(ProbMixtInit,Inf))
    
    for IndPat in ZeroProbMixt:                
           ProbMixtInit[IndPat][IndexMixt] = eps;
       
    return ProbMixtInit
                           
    # REM: only in P2.6 availabe                
    # math.isnan 
    # math.isinf
    #ZeroProbMixt= [find( ProbMixtInit(1:NPatterns) < eps)' ...
    #               find( isnan(ProbMixtInit(1:NPatterns)))' ...
    #               find( ProbMixtInit(1:NPatterns) == Inf)'];
    
    return Out    

#===== Normalize NxM matrix lines (Probs) to [0,1] =======  
def NormProb(matrix):
    SumCols = list(map(sum,matrix))
            
    return [[matrix[i][m]/SumCols[i] 
             for m in range(len(matrix[0]))] for i in range(len(matrix))]


#==== Estimate likelihood of a model =========
def EstLikelyhood(ProbMixtNorm,ProbMixtInit):
    N,M = size(ProbMixtNorm)
    LTotal = 0
        
    log = math.log
     
    for m in range(M):
        for i in range(N):
            if ProbMixtInit[i][m]!=0:
              LTotal += ProbMixtNorm[i][m]*log(ProbMixtInit[i][m])
        
    return LTotal 
  


#####################################################
#          Comparisons and Finds 
#####################################################

#===========================================
#       Compare Mat1 >= Mat2
#===========================================
def matCompGE(matrix1,matrix2):
    N,D = size(matrix1)
        
    Out = zeros(N,D)
    
    for i in range(N):
        for j in range(D):
            if matrix1[i][j]>=matrix2[i][j]:
               Out[i][j] = 1
    return Out

#===========================================
#       Compare Mat1 >= Mat2
#===========================================
def matCompL(matrix1,matrix2):
    N,D = size(matrix1)
        
    Out = zeros(N,D)
    
    for i in range(N):
        for j in range(D):
            if matrix1[i][j]<matrix2[i][j]:
               Out[i][j] = 1
    return Out

#===========================================
#       Compare vector > number
#===========================================
def CompVecGNum(vector,number):
    n = len(vector)
    Out = n*[0]
    for i in range(n):
        if vector[i]>number:
            Out[i] = 1
        
    return Out

#===========================================
#       Compare vector <= number
#===========================================
def CompVecLENum(vector,number):
    n = len(vector)
    Out = n*[0]
    for i in range(n):
        if vector[i]<=number:
            Out[i] = 1
        else:
            Out[i] = 0  
        
    return Out

#===========================================
#       Compare vector < number
#===========================================
def CompVecLNum(vector,number):
    n = len(vector)
    Out = n*[0]
    for i in range(n):
        if vector[i]<number:
            Out[i] = 1
        
    return Out

#===========================================
#       Compare vector == number
#===========================================
def CompVecENum(vector,number):
    n = len(vector)
    Out = n*[0]
    
    OutIndex = findSTR(number,Vector)
    
    for i in range(len(OutIndex)):
        Out[OutIndex[i]] = 1
        
    return Out

#===========================================
#       Compare Mat(Nx1) < number
#===========================================
def FindMatLNum(matrix,number):
    N = len(matrix)
        
    Out = []
    for i in range(N):
        if matrix[i][0]<number:
            Out.append(i)
        
    return Out

#===========================================
#       Compare Mat(Nx1) > number
#===========================================
def FindMatGNum(matrix,number):
    N = len(matrix)
        
    Out = []
    for i in range(N):
        if matrix[i][0]>number:
            Out.append(i)
        
    return Out

#===========================================
#       Find index vector > Num
#===========================================
def FindG(vector,Num):
    n = len(vector)
    Out = []
    for i in range(n):
        if vector[i] > Num:
            Out.append(i)
        
    return Out

#===========================================
#       Find index vector > Num
#===========================================
def FindGb(vector,Num):
    n = len(vector)
    Out = []
    for i in range(n):
        if vector[i][0] > Num:
            Out.append(i)

    return Out

#===========================================
#       Find index vector < Num
#===========================================
def FindL(vector,Num):
    n = len(vector)
    Out = []
    for i in range(n):
        if vector[i]<Num:
            Out.append(i)
        
    return Out

#===========================================
#       Find index vector < Num
#===========================================
def FindLb(vector,Num):
    n = len(vector)
    Out = []
    for i in range(n):
        if vector[i][0]<Num:
            Out.append(i)

    return Out

#===========================================
#       Find index vector < Num
#===========================================
def FindLE(vector,Num):
    n = len(vector)
    Out = []
    for i in range(n):
        if vector[i]<=Num:
            Out.append(i)
        
    return Out

#===========================================
#       Find index vector == num
#===========================================
def FindE(vector,Num):
    return findSTR(Num,vector)

#===========================================
#       Find index L>=vector >= H
#===========================================
def FindIn(vector,L,H):
    n = len(vector)
    Out = []
    for i in range(n):
        if vector[i]>=L and vector[i]<=H:   
            Out.append(i)
        
    return Out

#===========================================
#       Find index vector \notin [L,H]
#===========================================
def FindOut(vector,L,H):
    n = len(vector)
    Out = []
    for i in range(n):
        if vector[i]<=L and vector[i]>=H:   
            Out.append(i)
        
    return Out

#======================================================
#      Selections and Assignments
#------------------------------------------------------

#======================================
#      Normalize Tab to max value
#======================================
def NormTab(matrix):
    N,D = size(matrix)
    
    Output = zeros(N,D)
    
    for i in range(N):
        MaxValLine = max(matrix[i])
        for j in range(D):
            Output[i][j] = matrix[i][j]/MaxValLine 
    
    return Output
    




#======================================
#        3D Matrix Assignment
#======================================
def AssMat3(matrixTemp,matrixIn,DDim):
    # matrix Out DDim x N x D 
    # matrix In  N x D
    
    # Assign matIn at matOut at DDim 
    
    N,D = size(matrixIn)
            
    matrixOut = matrixTemp    
        
    for i in range(N):
        for j in range(D):
            matrixOut[DDim][i][j] = matrixIn[i][j]
    
    return matrixOut        
    
#======================================
#     2D Matrix Assignment byCol
#======================================
def AssMatCol(matrixTemp,matrixIn,d):
    # matrix Out N x D   
    # matrix In  N x 1
    
    # Assign matIn at matTemp at d Col < D
    # and return matTemp

    matrixOut = matrixTemp    
        
    for i in range(len(matrixIn)):
        matrixOut[i][d] = matrixIn[i][0]
    
    return matrixOut   
          
#======================================
#     2D Matrix Assignment byRow
#======================================
def AssMatRow(matrixTemp,VecIn,RowsIndex):
    # matrixTemp N x D   
    # VecIn      1 x D
    # RowsIndex  1 x K
    
    # Assign VecIn at matTemp[kI] where kI = RowsIndex[k] k=1,..,K 
    # and return matTemp

    matrixOut = matrixTemp    
    K         = len(RowsIndex)
        
    for k in range(K):
        matrixOut[RowsIndex[k]] = VecIn
    
    return matrixOut           

#----------------------------  
def SelVecAt(vector,Index):
    #    Select elements of vector by indexing
    return [vector[Index[i]] for i in range(len(Index))]

#----------------------------  
#def SelSTRAt(STR,Index):
#    #    Select elements of vector by indexing
#    Out = ''
#    for i in range(len(Index)):
#           Out.append(STR[Index[i]]) 
#    return Out           
#
#
#
#print SelSTRAt('abcdefghijk',[1,2])

#==========================================
#    Select rows of matrix by indexing  
#==========================================
def SelMatRowsAt(matrix,Index):
    N = len(Index)
    D = len(matrix[0])
        
    Out = zeros(N,D)
    for i in range(N):
        Out[i] = matrix[Index[i]]             
      
    return Out

#==========================================
#    Select Cols of matrix by indexing  
#==========================================
def SelMatColsAt(matrix,Index):
    N,D = len(matrix),len(Index)
    
    Out = zeros(N,D)
    
    for j in range(D):
        for i in range(N):
            Out[i][j] = matrix[i][Index[j]]             
      
    return Out

#==========================================
#    Select a (orthogonal) part of a matrix
#==========================================
def SelPart(A,SRows,SCols):
    # A matrix
    # SRows [0,2] to select first and third row
    # SCols [0,2] to select first and third col
        
    return [[A[i][j] for j in SCols] for i in SRows] 
       
######################################################
#             REM: Adapt      Advanced Statistics
#                 imported from stats.py
######################################################


#=====================================================
#       Continued fraction form of the incomplete
#                 Beta function
#       (Adapted from: Numerical Recipies in C.)
#-----------------------------------------------------

def betacf(a,b,x):
    ITMAX = 200
    EPS = 3.0e-7

    bm = az = am = 1.0
    qab = a+b
    qap = a+1.0
    qam = a-1.0
    bz = 1.0-qab*x/qap
    for i in range(ITMAX+1):
        em = float(i+1)
        tem = em + em
        d = em*(b-em)*x/((qam+tem)*(a+tem))
        ap = az + d*am
        bp = bz+d*bm
        d = -(a+em)*(qab+em)*x/((qap+tem)*(a+tem))
        app = ap+d*az
        bpp = bp+d*bz
        aold = az
        am = ap/bpp
        bm = bp/bpp
        az = app/bpp
        bz = 1.0
        if (abs(az-aold)<(EPS*abs(az))):
            return az
    print ('a or b too big, or ITMAX too small in Betacf.')
   
#=========================================================
#                incomplete beta function:
#
# I_x(a,b) = 1/Beta(a,b)* int_0^x t^(a-1)(1-t)^(b-1) dt
#
# a,b>0 
# Beta(a,b) = Gamma(a)*Gamma(b)/Gamma(a+b) using the 
# betacf function. (See Numerical Recipies in C.)
#=========================================================
   
def BetaInc(x,a,b):
    
    if (x<0.0 or x>1.0):
        raise Exception(ValueError, 'Bad x in lbetai')
    if (x==0.0 or x==1.0):
        bt = 0.0
    else:
        bt = math.exp(GammaLn(a+b)-GammaLn(a)-GammaLn(b)+a*math.log(x)+b*\
                      math.log(1.0-x))
    if (x<(a+1.0)/(a+b+2.0)):
        return bt*betacf(a,b,x)/float(a)
    else:
        return 1.0-bt*betacf(b,a,1.0-x)/float(b)


#=========================================================
#         Natural logarithm of Gamma function of xx.
# Gamma(z) = int_0^{\inf} t^(z-1)exp(-t) dt
# (From: Numerical Recipies in C.)
#=========================================================
def GammaLn(xx):
    coeff = [76.18009173, -86.50532033, 24.01409822, -1.231739516,
             0.120858003e-2, -0.536382e-5]
    
    x   = xx  - 1.0
    tmp = x   + 5.5
    tmp = tmp - (x+0.5)*math.log(tmp)
    ser = 1.0
    for j in range(len(coeff)):
        x  += 1.0
        ser = ser + coeff[j]/x
        
    return -tmp + math.log(2.50662827465*ser)     

#===========================================
#    Chi2 random numbers with D degFree
#===========================================
def Chi2Rnd(D):
    Out = 0
    for d in range(D):
        Out += random.gauss(0,1)**2
        
    return Out    


#===========================================
#        Estimate Covariance Matrix
#===========================================
  
def cov(Patterns):
    N,D = size(Patterns)
    CovMat = zeros(D,D)
    
    MeanVec = mean(Patterns,2)
              
            
    AvPat   = subMat(Patterns,repvecROW(MeanVec,N)) 
    
    for d1 in range(D):
       for d2 in range(d1,D):
           CovMat[d1][d2] = SumVal(multMatElw(getCol(AvPat,d1),\
                                              getCol(AvPat,d2)))
           CovMat[d2][d1] = CovMat[d1][d2]

    CovMat = multFlMat(1.0/(N-1),CovMat) 

    return CovMat            

#print show(cov(T([[1,1,1,1],[5,6,7,8],[9,10,11,12]])))

#=================================================
#   Estimate Multiple Correlation Coefficient MCC 
#   N-1 First Cols to Last Col
#=================================================
def MCC(Patterns):
    import numpy
    N,D  = size(Patterns)

    SigmaMat  = cov(Patterns)
        
    Sm        = SelPart(SigmaMat,range(D-1),range(D-1))
    sMp1vector= SigmaMat[D-1][0:D-1]
    sMp1Mp1   = SigmaMat[D-1][D-1] 
    InvSm     = numpy.linalg.inv(Sm)
       
    ResA = multMat([sMp1vector],InvSm)   
        
    ResB = multMat(ResA,T([sMp1vector]))
            
    MultCC    = ( ResB[0][0] /sMp1Mp1)**0.5
    
    return MultCC

#=================================================
#   Estimate Pearson Concordance Coefficient 
#=================================================
def PearsonConco(x,y):
    CovMat = cov(T([x,y]))
    N = len(x)
     
    vx,vy,vxy = CovMat[0][0],CovMat[1][1],CovMat[0][1]
    mx,my     = mean([x],1)[0][0],mean([y],1)[0][0]
      
    r             = vxy/ (vx*vy)**0.5
    zr            = 0.5 * math.log((1.0+r)/(1.0-r))
    fc            = 1.96*(1.0/(N-3.0)**0.5)
    
    zeta_l,zeta_u  = zr - fc, zr + fc
    r_l,r_u        = tanh(zeta_l),tanh(zeta_u)
            
    #t             = stats.t.ppf(0.95,N-2)
    #PearsonDownLim= t/np.sqrt(N-2+pow(t,2))
        
    Conco   = 2.0*vxy/(vx+vy+(mx-my)**2.0)    
    return r,r_l,r_u,Conco       
 
    
#===========================================
#        Estimate variance of a vec
#===========================================
def var(vec):
    N = len(vec)

    MeanVal = sum(vec)/float(N)
            
    AvVec = subVecFl(vec,MeanVal) 
    
    S2 = 0
    for i in range(N):
           S2 += AvVec[i]**2.0 

    return 1.0/(float(N)-1)*S2




#===========================================
# Estimate variance of a Matrix in dimension d
#===========================================
  
def varMat(Mat,d):
    N,K = size(Mat)
                
    if d == 2:
       VecVarOut = N*[0]
       for i in range(N):
           VecVarOut[i] = var(Mat[i])    
    elif d==1:
       VecVarOut = K*[0]
       for j in range(K):
           VecVarOut[j] = var(Mat2Vec(T(getCol(Mat,j))))     
            
    return VecVarOut

#===========================================
#      Estimate (x-m)Sigma^(-1)(x-m)T
#===========================================
def CleverMult(Patterns,Center,SigmaInv,N,D,G):
            
    if D==1:
         s  = SigmaInv[0][0]
         m  = Center[0]        
         return [[s*(Patterns[n][0]-m)**2] for n in range(N)]
    if D==2:
      for n in range(N):
          A,B = Patterns[n][0]-Center[0],Patterns[n][1]-Center[1]  
                      
          G[n][0] = A**2*SigmaInv[0][0] + B**2*SigmaInv[1][1] + \
                    A*B*SigmaInv[0][1]
      return G               
    else:
      DistPatIndexMixt = D*[0.0]
      Buff             = D*[0.0]
                   
      for n in range(N):
         for d in range(D): 
             DistPatIndexMixt[d] = Patterns[n][d] - Center[d]  
         
         for d in range(D):
             Buff[d] = 0
             for k in range(D):
               Buff[d] += DistPatIndexMixt[k] *SigmaInv[k][d]
         
             Buff[d] = Buff[d]*DistPatIndexMixt[d]       
      
         G[n][0] = sum(Buff)
         
      return G
    
#=================================================
#  The error function:           erf
#  Abramovitz & Stegun "Handbook of Math eq.7.1.26"
#==================================================
def erf(x):
    
    # save the sign of x
    xSign = sign(x)
    x     = abs(x)

    # constants
    a1 =  0.254829592
    a2 = -0.284496736
    a3 =  1.421413741
    a4 = -1.453152027
    a5 =  1.061405429
    p  =  0.3275911

    
    t = 1.0/(1.0 + p*x)
    y = 1.0 - (((((a5*t + a4)*t) + a3)*t + a2)*t + a1)*t*math.exp(-x*x)
    return xSign*y 

       
#===================================
#     FIR filter of Signal
#===================================
def FIRfilter(B,vec):
    N    = len(vec)
    LenF = len(B)
           
    new_vec = N*[0]
    for i in range(N):
        for j in range(LenF):
            new_vec[i] += B[j]*vec[i-j]
     
    return new_vec

#===================================
#         ShiftMinTo0  Column
#===================================
def ShiftMinTo0(Matrix,Col):
    ColData = Mat2Vec(getCol(Matrix,Col))
    MinVal = -1*min(ColData)
    
    ColData = addFlVec(MinVal,ColData)
    
    Matrix = AssMatCol(Matrix,T([ColData]),Col) 
    
    return Matrix


#----  ShiftMinTo0  Row ----
def ShiftMinTo0Row(Matrix,iRow):
    Matrix[iRow] = addFlVec(-1*min(Matrix[iRow]),Matrix[iRow])
    return Matrix

    
             
#----------------------------------------
#   Set operations ---
#========================================

# STRING OPERATIONS

# Find where str value occurs in str L
def findSTR(value, L):
    i    = -1
    Out  = []
    while 1: 
      try: 
         f = L.index(value, i+1)
         Out.append( f )
         i = Out[-1]
      except:
         return Out

# Set operations
       
#========================================
#    Intersection of two lists 
#========================================
def intersect(A,B):
    return list(set(A) & set(B))
    
#========================================
#    Unique of list of (Integ or STR)
#========================================
def Unique(A):
    Out = list(set(A))
    Out.sort()
    return Out 



######################################################
#            Performance Times
#=====================================================

def profile_mult(matrix1,matrix2):
    # A more detailed timing with process information
    # Arguments must be strings for this function
    # eg. profile_mult('a','b')
    import cProfile
    cProfile.run('matrix.mult(' + matrix1 + ',' + matrix2 + ')')

######################################################
#            Image to eps
#=====================================================
#def Im2eps(Filename,outfile):
#    import Image
#    im = Image.open(Filename)
#    im.save(outfile, "EPS")
#    
#FotoName = "NeuroTool3"    
#Im2eps(FotoName+".bmp",FotoName+".eps")    



#####------- Test Area ------------------
####
#######b = 'jimverasdsdjimversdsdsddddddddjimveraassasjimver'
#######a = 'jimver'
#######
## = [[5,15,15,2],[2,2,3,4],[5,6,7,8]]
######L  = ['asdsd','bbb','aaaa','cc','cc','asdsd']
#G = [1.0,5.0,2.0] 
###
###L = [2.3,2.3,4.5]
###
#TS = time.clock()
#divFlVec(5.0,G)
#print time.clock()-TS


