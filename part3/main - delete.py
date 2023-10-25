import pandas as pd 
import os
import flask 
from flask_restful import Api, Resource, reqparse

app = flask.Flask(__name__)
api = Api(app)

comp_args = reqparse.RequestParser()
comp_args.add_argument('comp_num', type=int, help='The 8 digit ID of the company')
comp_args.add_argument('pers_num', type=int, help='The 12 digit ID of the person')
comp_args.add_argument('country', type=str, help='The Country of residence for the person (UPPERCASE)')

data =  pd.read_csv('./Q3/data/officers_20231023_175246.csv')
data.convert_dtypes()

@app.route('/')
def home():
    return 'hello world'

@app.route('/companies')
def companies():
    page = flask.request.args.get('page', default=1, type=int)
    start_idx = 10 * (page - 1)
    end_idx = 10 * page
    out = data.iloc[start_idx:end_idx]
    if len(out) > 0:
        return out.to_json(orient='records')
    else:
        return {'Reponse': 'Page out of range'}

@app.route('/company')
def company():
    page = flask.request.args.get('page', default=1, type=int)
    filter = flask.request.args.get('id', default=None, type=int)
    out = data[data['comp_num']==filter]
    if len(out) >= 1:
        return data[data['comp_num']==filter].to_json(orient='records')
    else:
        return {'Response': 'Company not found'}

@app.route('/get')
def get():
    return str(data)

if __name__ == '__main__':
    app.run()
