import hashlib
import random
import string
import os
import json
from flask import Flask, render_template, send_from_directory, request, jsonify, redirect, make_response, Blueprint
from config import Config
from src.database import db
from src.database import  User, Post, Board, Permission, Session, FileTracker, get_thread_post, FileRefference
from src.utils import Utils
from src.server.utils import Utils as ServerUtils
from src.engine import Engine

app = Blueprint('backend', __name__, template_folder=Config.TEMPLATES_DIR)


@app.route('/<board_short>/make_post')
@ServerUtils.check_query_args({'parent_post_id', 'head', 'body', 'files'})

def board_make_post_handle(board_short):
    board = Engine.get_board_by_short(board_short)
    parent_post_id = int(request.args.get('parent_post_id'))
    body = request.args.get('body')
    head = request.args.get('head')
    files = json.loads(request.args.get('files'))

    parent_post = None
    if parent_post_id == 1:
        parent_post = Post.query.filter_by(
            id=parent_post_id
        ).first()
    else:
        parent_post = Post.query.filter_by(
            id=parent_post_id,
            board=board
        ).first()

    if not parent_post:
        return "<h1>There is no such post :|</h1>"

    new_post = Post(
        parent=parent_post,
        head=head, 
        body=body,
        board=board
    )
    db.session.add(new_post)
    db.session.commit()

    Engine.associate_with_post(files, new_post)

    thread_post = get_thread_post(new_post)
    return redirect('/%s/thread/%s' % (board.short, thread_post.id))

"""
@app.route('/<board_short>/make_thread_post')
@ServerUtils.check_query_args({'head', 'body'})

def board_make_thred_post(board_short):
    current_board = Board.query.filter_by(  
        short=board_short
    ).first()

    if not current_board:
        return "<h1>There is no such</h1>"

    body = request.args.get('body')
    head = request.args.get('head')
    files = json.loads(request.args.get('files'))

    genesis_post = Post.query.filter_by(
        id=GENESIS_POST_ID
    ).first()

    new_post = Post(
        parent=genesis_post,
        head=head, 
        body=body,
        board=current_board
    )
    db.session.add(new_post)
    db.session.commit()

    Engine.associate_with_post(files, new_post)

    return redirect('/%s' % (current_board.short))
"""

@app.route('/files/public/<path:filename>')
def public_handle(filename):
    return send_from_directory(
        Config.PUBLIC_DIR, 
        filename, 
        as_attachment=True)


@app.route('/files/uploads/<path:filename>')
def files_handle(filename):
    return send_from_directory(
        Config.UPLOAD_DIR,
        filename
    )


"""
get resolution of video and image file:
>>ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 uoloads/9.webm
>>1280x1080
get size of any file:
>>ls -lh ./uploads/1.png | awk '{print $5}'
>>228
"""
@app.route('/<board_short>/upload', methods=['POST'])
def upload_handle(board_short):
    filedata = None
    try:
        filetracker = Engine.upload_file(request.files, board_short)
    except Exception as exc:
        raise exc
        return jsonify({
            'Response': 'ERR'
        })

    res = {
        'Response': 'OK',
        'file': filetracker
    }
    return jsonify(res)
