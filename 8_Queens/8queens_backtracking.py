n=8
def print_table(board):
    for i in range(0,n):
        for j in range(0,n):
            print(board[i][j],end="")
        print("\n")

def safe(board,r,c):
    for i in range(0,c):
        if board[r][i] :
            return False
    i=r
    j=c
    while i>=0 and j>=0:
        if board[i][j]:
            return False
        i-=1
        j-=1
    i=r
    j=c
    while j>=0 and i< n :
        if board[i][j]:
            return False
        i+=1
        j-=1
    return True

def solve8Queen(board,c):
    if c >=n:
        return True
    for i in range(0,8):
        if safe(board,i,c):
            board[i][c]=1
            if solve8Queen(board,c+1):
                return True
            board[i][c]=0
    return False

board=[[0 for i in range(n)] for j in range(n)]

solve8Queen(board,0)
print_table(board)

'''OUtput:
10000000

00000010

00001000

00000001

01000000

00010000

00000100

00100000
'''