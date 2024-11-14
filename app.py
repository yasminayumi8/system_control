from flask import Flask, render_template, request, redirect, url_for, flash
from models import Categoria, Produto, db_session, Funcionario, Movimentacao
from sqlalchemy import select

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret!'


@app.route('/')
def index():
    return redirect('home')


@app.route('/home', methods=['GET'])
def home():

    return render_template('template.html')