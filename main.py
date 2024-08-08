from flask import Flask, jsonify, request
from flask_cors import CORS
import random

app = Flask(__name__)
cors = CORS(app, origins='*')  # This will enable CORS for all routes

@app.route("/api/users", methods=['GET'])
def users():
    return jsonify({
        "users": ['grover', 'ben', 'enigma']
    })

def validMove(board, row, col, num):
    """Check if placing num in board[row][col] is valid according to Sudoku rules."""
    if num in board[row]:  # Check row
        return False
    
    if num in [board[r][col] for r in range(9)]:  # Check column
        return False
    
    startRow = 3 * (row // 3)
    startCol = 3 * (col // 3)
    
    for r in range(startRow, startRow + 3):
        for c in range(startCol, startCol + 3):
            if board[r][c] == num:
                return False
            
    return True

def solve(board):
    """Solve the Sudoku board using backtracking."""
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if validMove(board, row, col, num):
                        board[row][col] = num
                        if solve(board):
                            return True
                        board[row][col] = 0
                return False
    return True

def generateSudoku():
    """Generate a complete Sudoku board."""
    board = [[0] * 9 for _ in range(9)]
    solve(board)
    return board

def calcDifficulty(level):
    """Determine the number of cells to remove based on difficulty level."""
    if level == "hard":
        return 60
    elif level == "medium":
        return 40
    else:
        return 20

def removeNums(board, num_removed):
    """Remove a number of cells from the Sudoku board to create a puzzle."""
    count = 0
    while count < num_removed:
        row, col = random.randint(0, 8), random.randint(0, 8)
        if board[row][col] != 0:
            board[row][col] = 0
            count += 1

def generatePuzzle(num_removed=40):
    """Generate a Sudoku puzzle by removing numbers from a complete board."""
    board = generateSudoku()
    removeNums(board, num_removed)
    return board

@app.route("/api/sudoku", methods=['GET'])
def sudoku():
    """API endpoint to generate a Sudoku puzzle."""
    level = request.args.get('level', 'medium')  # Get difficulty level from query params, default to 'medium'
    puzzle = generatePuzzle(level)
    return jsonify(puzzle)

if __name__ == '__main__':
    app.run(debug=True, port=8080)
