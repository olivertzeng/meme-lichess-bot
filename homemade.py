"""
Some example classes for people who want to create a homemade bot.

With these classes, bot makers will not have to implement the UCI or XBoard interfaces themselves.
"""

import logging
import random

import chess
from chess.engine import Limit, PlayResult

from lib.engine_wrapper import MinimalEngine
from lib.lichess_types import HOMEMADE_ARGS_TYPE

logger = logging.getLogger(__name__)


class ExampleEngine(MinimalEngine):
    """An example engine that all homemade engines inherit."""


class Anarchy(ExampleEngine):

    def search(
        self, board: chess.Board, time_limit: Limit, *args: HOMEMADE_ARGS_TYPE
    ) -> PlayResult:

        # Get amount of legal moves
        legalMoves = list(board.legal_moves)

        # Initialise variables
        bestMove = None

        # Evaluate each move
        for move in legalMoves:

            # en passant is forced
            if board.is_en_passant(move):
                print("en passant is forced")
                return PlayResult(move, None)

            # play the ruy lopez
            if board.board_fen() == "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR":
                print("e4 best by test")
                return PlayResult(chess.Move.from_uci("e2e4"), None)

            if board.board_fen() == "rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR":
                return PlayResult(chess.Move.from_uci("q1f3"), None)

            if (
                board.board_fen()
                == "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R"
            ):
                return PlayResult(chess.Move.from_uci("f1b5"), None)

            # always play the bongcloud
            if board.san(move) in ["Ke2", "Ke7", "Kxe2", "Kxe7"]:
                return PlayResult(move, None)

            # never play rook a4
            if not (board.san(move)[0] == "R" and board.san(move)[-2:] == "a4"):
                # king stays on e2/e7
                if not (board.san(move)[0] == "K"):
                    board.push(move)
                    board.pop()
            else:
                print("I saw Ra4, I just didn't like it")

        if bestMove != None:
            return PlayResult(bestMove, None)
        else:
            return PlayResult(random.choice(list(board.legal_moves)), None)
