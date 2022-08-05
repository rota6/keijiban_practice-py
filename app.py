from flask import Flask, redirect, url_for, session
from flask import render_template, request
import os, json, datetime
import bbs_login #ログイン管理モジュール
import bbs_data #データ入出力用モジュール

#Flaskインスタンスと暗号化キーの指定
app = Flask(__name__)
app.secret_key = 'U1sMNeUkZSuuX2Zn'

#掲示板のメイン画面
@app.route('/')
def index():
    #ログインが必要
    if not bbs_login.is_login():
        return redirect('/login')
    #ログ一覧を表示
    return render_template('index.html',
            user=bbs_login.get_user(),
            data=bbs_data.load_data())

#ログイン画面を表示
@app.route('/login')
def login():
    return render_template('login.html')

#ログイン処理
@app.route('/try_login', methods=['POST'])
def try_login():
    user = request.form.get('user', '')
    pw = request.form.get('pw', '')
    #ログインに成功したらルートページへ飛ぶ
    if bbs_login.try_login(user, pw):
        return redirect('/')
    #失敗したときはメッセージを表示
    return show_msg('ログインに失敗しました')

#ログアウト処理
@app.route('/logout')
def logout():
    bbs_login.try_logout()
    return show_msg('ログアウトしました')

#書き込み処理
@app.route('/write', methods=['POST'])
def write():
    #ログインが必要
    if not bbs_login.is_login():
        return redirect('/login')
    #フォームのテキストを取得
    ta = request.form.get('ta', '')
    if ta== '': return show_msg('書き込みが空でした。')
    #データに追記保存
    bbs_data.save_data_append(
        user=bbs_login.get_user(),
        text=ta
    )
    return redirect('/')

#テンプレートを利用してメッセージを出力
def show_msg(msg):
    return render_template('msg.html', msg=msg)

#新規登録画面
@app.route('/register')
def regi():
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)