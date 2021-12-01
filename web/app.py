import flask
# from flask import request
from markupsafe import escape
from flask import render_template
import numpy as np
import pickle

app = flask.Flask(__name__, template_folder='templates')

model = pickle.load(open('model/model_classifier.pkl', 'rb'))
@app.route('/')
def main():
    return(flask.render_template('index.html'))




@app.route('/hello')
def hello():
    return 'Hello, world!'

@app.route('/user/<username>')
def show_user_profile(username):
    return 'User %s' % escape(username)

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return 'Post %d' % post_id

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    return 'Subpath %s' % escape(subpath)

def shutdown_server():
    func = flask.request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

@app.route('/predict', methods=['POST'])
def predict():
    int_features = [int(x) for x in flask.request.form.values()]
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)
    output = {0: "Not Placed", 1: "Placed"}
    return flask.render_template('index.html', 
    prediction_text="Student must be {} to workplace".format(output[prediction[0]]))
# @app.route('login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         return do_the_login()
#     else:
#         return show_the_login_form()


if __name__ == '__main__':
    app.run()