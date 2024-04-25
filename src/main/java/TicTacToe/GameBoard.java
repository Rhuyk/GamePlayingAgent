/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package TicTacToe;

/**
 *
 * @author pj
 */
public class GameBoard {

    /**
     * @return the EMPTY
     */
    public char getEMPTY() {
        return ' ';
    }
    
    private char[][] board;
    private static final char EMPTY = ' ';
    private int numRows;
    private int numCols;

    public GameBoard(int numRows, int numCols) {
        this.numRows = numRows;
        this.numCols = numCols;
        this.board = new char[numRows][numCols];
        initializeBoard();
    }

    private void initializeBoard() {
        for (int i = 0; i < getNumRows(); i++) {
            for (int j = 0; j < getNumCols(); j++) {
                board[i][j] = getEMPTY();
            }
        }
    }

    public boolean makeMove(int row, int col, char player) {
        if (isValidMove(row, col) && board[row][col] == getEMPTY()) {
            board[row][col] = player;
            return true;
        }
        return false;
    }

    public void undoMove(int row, int col) {
        if (isValidMove(row, col)) {
            board[row][col] = getEMPTY();
        }
    }

    public boolean isGameOver() {
        return isWinner('X') || isWinner('O') || isBoardFull();
    }

    public boolean isWinner(char player) {
        // Check rows
        for (int i = 0; i < getNumRows(); i++) {
            boolean rowWin = true;
            for (int j = 0; j < getNumCols(); j++) {
                if (board[i][j] != player) {
                    rowWin = false;
                    break;
                }
            }
            if (rowWin) {
                return true;
            }
        }

        // Check columns
        for (int j = 0; j < getNumCols(); j++) {
            boolean colWin = true;
            for (int i = 0; i < getNumRows(); i++) {
                if (board[i][j] != player) {
                    colWin = false;
                    break;
                }
            }
            if (colWin) {
                return true;
            }
        }

        // Check diagonals (\ and /)
        boolean diag1Win = true;
        boolean diag2Win = true;
        for (int i = 0; i < getNumRows(); i++) {
            if (board[i][i] != player) {
                diag1Win = false;
            }
            if (board[i][getNumCols() - 1 - i] != player) {
                diag2Win = false;
            }
        }
        return diag1Win || diag2Win;
    }

    public boolean isBoardFull() {
        for (int i = 0; i < getNumRows(); i++) {
            for (int j = 0; j < getNumCols(); j++) {
                if (board[i][j] == getEMPTY()) {
                    return false; // Board is not full
                }
            }
        }
        return true; // Board is full (tie)
    }

    public char[][] getBoard() {
        return board;
    }

    private boolean isValidMove(int row, int col) {
        return row >= 0 && row < getNumRows() && col >= 0 && col < getNumCols();
    }

    
    public void displayBoard() {
        for (int row = 0; row < getNumRows(); row++) {
            for (int col = 0; col < getNumCols(); col++) {
                System.out.print(getBoard()[row][col]);
                if (col < getNumRows() - 1) {
                    System.out.print(" | ");
                }
            }
            System.out.println();
            if (row < getNumCols() - 1) {
                System.out.println("---------");
            }
        }
    }

    /**
     * @return the numRows
     */
    public int getNumRows() {
        return numRows;
    }

    /**
     * @param numRows the numRows to set
     */
    public void setNumRows(int numRows) {
        this.numRows = numRows;
    }

    /**
     * @return the numCols
     */
    public int getNumCols() {
        return numCols;
    }

    /**
     * @param numCols the numCols to set
     */
    public void setNumCols(int numCols) {
        this.numCols = numCols;
    }
    
}

