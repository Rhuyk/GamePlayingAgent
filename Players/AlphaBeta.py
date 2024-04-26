import math


def best_alpha_beta(game, depth, is_maximizing, limited_tree):
    if is_maximizing:
        best_score = -math.inf
        move = None
        alpha = -math.inf
        beta = math.inf
        for space in game.available_moves():
            game.make_move(space)
            score = alpha_beta(game, depth - 1, False, limited_tree, alpha, beta)
            game.undo_move(space)
            if score > best_score:
                best_score = score
                move = space
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break
        return move
    else:
        best_score = math.inf
        move = None
        alpha = -math.inf
        beta = math.inf
        for space in game.available_moves():
            game.make_move(space)
            score = alpha_beta(game, depth - 1, True, limited_tree, alpha, beta)
            game.undo_move(space)
            if score < best_score:
                best_score = score
                move = space
            beta = min(beta, best_score)
            if beta <= alpha:
                break
        return move


def alpha_beta(game, depth, is_maximizing, limited_tree, alpha, beta):
    game.check_move()
    if game.game_over:
        return game.evaluation
    if limited_tree and depth == 0:
        return 0

    if is_maximizing:
        best_score = -math.inf
        for space in game.available_moves():
            game.make_move(space)
            score = alpha_beta(game, depth - 1, False, limited_tree, alpha, beta)
            game.undo_move(space)
            best_score = max(score, best_score)
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break
        return best_score

    else:
        best_score = math.inf
        for space in game.available_moves():
            game.make_move(space)
            score = alpha_beta(game, depth - 1, True, limited_tree, alpha, beta)
            game.undo_move(space)
            best_score = min(score, best_score)
            beta = min(beta, best_score)
            if beta <= alpha:
                break
        return best_score
