from flask import Flask, render_template, send_from_directory, request, jsonify, redirect, make_response, Blueprint
from config import Config
from src.engine import Engine
from src.server.utils import Utils as ServerUtils

app = Blueprint('frontend', __name__, template_folder=Config.TEMPLATES_DIR)


@app.route('/')
def index_handle():
    return render_template('index.html', boards=Engine.get_boards_dumped())


@app.route('/<board_short>')
def board_handle(board_short):
    current_board = Engine.get_board_by_short(board_short)
    return render_template(
        'board.html', 
        current_board=current_board.dump_to_dict(),
        boards=Engine.get_boards_dumped(),
        posts=Engine.get_threads_preview_dumped(current_board)
    )


@app.route('/<board_short>/thread/<thread_post_id>')
def thread_handle(board_short, thread_post_id):
    current_board = Engine.get_board_by_short(board_short)
    return render_template(
        'thread.html', 
        current_board=current_board.dump_to_dict(),
        boards=Engine.get_boards_dumped(),
        posts=[Engine.get_thread_dumped(current_board, thread_post_id)]
    )


@app.route('/<board_short>/post_constructor')
@ServerUtils.check_query_args({'parent_post_id'})
def post_constructor_handle(board_short):
    board = Engine.get_board_by_short(board_short)
    parent_post = Engine.get_post_by_id(request.args.get('parent_post_id'))
    return render_template(
        'post_constructor.html',
        boards=Engine.get_boards_dumped(),
        current_board=board,
        parent_post=parent_post
    )
