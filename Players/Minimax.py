import math


def best_minimax(game, depth, is_maximizing, limited_tree):  # True for positive(first player)
    if is_maximizing:
        best_score = -math.inf
        move = None
        for space in game.available_moves():
            game.make_move(space)
            score = minimax(game, depth - 1, False, limited_tree)
            game.undo_move(space)
            if score > best_score:
                best_score = score
                move = space
        return move
    else:
        best_score = math.inf
        move = None
        for space in game.available_moves():
            game.make_move(space)
            score = minimax(game, depth - 1, True, limited_tree)
            game.undo_move(space)
            if score < best_score:
                best_score = score
                move = space
        return move


def minimax(game, depth, is_maximizing, limited_tree):
    game.check_move()
    if game.evaluation is not None:
        return game.evaluation
    if limited_tree and depth == 0:
        return 0

    if is_maximizing:
        best_score = -math.inf
        for space in game.available_moves():
            game.make_move(space)
            score = minimax(game, depth - 1, False, limited_tree)
            game.undo_move(space)
            best_score = max(score, best_score)
        return best_score

    else:
        best_score = math.inf
        for space in game.available_moves():
            game.make_move(space)
            score = minimax(game, depth - 1, True, limited_tree)
            game.undo_move(space)
            best_score = min(score, best_score)
        return best_score

