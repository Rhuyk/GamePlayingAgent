/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package TicTacToe;

/**
 *
 * @author pj
 */
import java.util.ArrayList;
import java.util.List;

public class AIPlayer {
    private char aiPlayer;
    private char humanPlayer;

    public AIPlayer(char aiPlayer, char humanPlayer) {
        this.aiPlayer = aiPlayer;
        this.humanPlayer = humanPlayer;
    }

    public int[] findBestMove(GameBoard gameBoard) {
        int[] bestMove = new int[]{-1, -1};
        int bestScore = Integer.MIN_VALUE;
        int alpha = Integer.MIN_VALUE;
        int beta = Integer.MAX_VALUE;

        List<int[]> emptySpaces = getEmptySpaces(gameBoard);

        for (int[] space : emptySpaces) {
            int row = space[0];
            int col = space[1];
            gameBoard.makeMove(row, col, aiPlayer);
            int score = minimax(gameBoard, 0, false, alpha, beta);
            gameBoard.undoMove(row, col);

            if (score > bestScore) {
                bestScore = score;
                bestMove[0] = row;
                bestMove[1] = col;
            }
            alpha = Math.max(alpha, bestScore);
            if (beta <= alpha) {
                break;
            }
        }

        return bestMove;
    }

    private List<int[]> getEmptySpaces(GameBoard gameBoard) {
        List<int[]> emptySpaces = new ArrayList<>();
        char[][] board = gameBoard.getBoard();
        int numRows = gameBoard.getNumRows();
        int numCols = gameBoard.getNumCols();

        for (int i = 0; i < numRows; i++) {
            for (int j = 0; j < numCols; j++) {
                //System.out.println("Board[" + i + "][" + j + "] = " + board[i][j]);
                if (board[i][j] == ' ') {
                    
                    //System.out.println("Test1");
                    emptySpaces.add(new int[]{i, j});
                }
            }
        }
        return emptySpaces;
    }

    private int minimax(GameBoard gameBoard, int depth, boolean isMaximizingPlayer, int alpha, int beta) {
        if (gameBoard.isGameOver()) {
            if (gameBoard.isWinner(aiPlayer)) {
                return 10;
            } else if (gameBoard.isWinner(humanPlayer)) {
                return -10;
            } else {
                return 0;
            }
        }

        List<int[]> emptySpaces = getEmptySpaces(gameBoard);

        if (isMaximizingPlayer) {
            int bestScore = Integer.MIN_VALUE;
            for (int[] space : emptySpaces) {
                int row = space[0];
                int col = space[1];
                gameBoard.makeMove(row, col, aiPlayer);
                int score = minimax(gameBoard, depth + 1, false, alpha, beta);
                gameBoard.undoMove(row, col);
                bestScore = Math.max(bestScore, score);
                alpha = Math.max(alpha, bestScore);
                if (beta <= alpha) {
                    break;
                }
            }
            return bestScore;
        } else {
            int bestScore = Integer.MAX_VALUE;
            for (int[] space : emptySpaces) {
                int row = space[0];
                int col = space[1];
                gameBoard.makeMove(row, col, humanPlayer);
                int score = minimax(gameBoard, depth + 1, true, alpha, beta);
                gameBoard.undoMove(row, col);
                bestScore = Math.min(bestScore, score);
                beta = Math.min(beta, bestScore);
                if (beta <= alpha) {
                    break;
                }
            }
            return bestScore;
        }
    }
}