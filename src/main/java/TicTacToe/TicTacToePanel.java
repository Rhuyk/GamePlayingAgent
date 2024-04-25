/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package TicTacToe;

/**
 *
 * @author pj
 */
import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class TicTacToePanel extends JPanel implements ActionListener {
    private JButton[][] buttons;
    private GameBoard gameBoard;
    private AIPlayer aiPlayer;
    private char currentPlayer;

    public TicTacToePanel(int numRows, int numCols) {
        setLayout(new GridLayout(numRows, numCols));
        buttons = new JButton[numRows][numCols];
        gameBoard = new GameBoard(numRows, numCols);
        aiPlayer = new AIPlayer('O', 'X');
        currentPlayer = 'X'; // Human player starts first
        initializeButtons();
    }

    private void initializeButtons() {
        for (int i = 0; i < gameBoard.getNumRows(); i++) {
            for (int j = 0; j < gameBoard.getNumCols(); j++) {
                JButton button = new JButton();
                button.setFont(new Font("Arial", Font.PLAIN, 40));
                button.addActionListener(this);
                buttons[i][j] = button;
                add(button);
            }
        }
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        JButton clickedButton = (JButton) e.getSource();
        int row = -1;
        int col = -1;

        // Find which button was clicked
        for (int i = 0; i < gameBoard.getNumRows(); i++) {
            for (int j = 0; j < gameBoard.getNumCols(); j++) {
                if (buttons[i][j] == clickedButton) {
                    row = i;
                    col = j;
                    break;
                }
            }
        }

        // Make player move
        if (gameBoard.makeMove(row, col, currentPlayer)) {
            clickedButton.setText(String.valueOf(currentPlayer));
            clickedButton.setEnabled(false); // Disable button after making move

            if (gameBoard.isGameOver()) {
                JOptionPane.showMessageDialog(this, getGameResultMessage());
                resetGame();
            } else {
                // Switch turns between players
                currentPlayer = (currentPlayer == 'X') ? 'O' : 'X';

                // AI player's turn
                if (currentPlayer == 'O') {
                    int[] aiMove = aiPlayer.findBestMove(gameBoard);
                    buttons[aiMove[0]][aiMove[1]].setText("O");
                    gameBoard.makeMove(aiMove[0], aiMove[1], 'O'); // AI plays as 'O'
                    buttons[aiMove[0]][aiMove[1]].setEnabled(false);
                    currentPlayer = 'X'; // Switch back to human player
                }
                if (gameBoard.isGameOver()) {
                    JOptionPane.showMessageDialog(this, getGameResultMessage());
                    resetGame();
                }
            }
        } else {
            JOptionPane.showMessageDialog(this, "Invalid move! Try again.");
        }
    }

    private String getGameResultMessage() {
        if (gameBoard.isWinner('X')) {
            return "Congratulations! You win!";
        } else if (gameBoard.isWinner('O')) {
            return "AI wins! Better luck next time.";
        } else {
            return "It's a draw! Good game.";
        }
    }

    private void resetGame() {
        gameBoard = new GameBoard(gameBoard.getNumRows(), gameBoard.getNumCols());
        currentPlayer = 'X';
        for (int i = 0; i < gameBoard.getNumRows(); i++) {
            for (int j = 0; j < gameBoard.getNumCols(); j++) {
                buttons[i][j].setText("");
                buttons[i][j].setEnabled(true);
            }
        }
    }
}
