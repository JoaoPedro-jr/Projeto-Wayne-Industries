
from flask import Blueprint, render_template, redirect, url_for, flash


# Cria o blueprint principal
index_bp = Blueprint('index', __name__)

@index_bp.route('/')

def index_view():
    return render_template('index.html', title='Bem-vindo ao Sistema Wayne Industries, camarada!')

