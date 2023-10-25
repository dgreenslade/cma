import pandas as pd 
import flask 
from flask_restful import Api, Resource, reqparse, abort
from waitress import serve

app = flask.Flask(__name__)
api = Api(app)

comp_args = reqparse.RequestParser()
comp_args.add_argument('comp_num', type=int, help='The 8 digit ID of the company')
comp_args.add_argument('country', type=str, help='The Country of residence for the person (UPPERCASE)')

# In memory datastore - this should be replaced with a database and the data loaded ther.
# The database server could either be a separate Docker container with mounted volume, or a db on a separate.
data =  pd.read_csv('./data/officers_input.csv')
data = data.fillna('')
data.convert_dtypes()

@app.route('/')
def home():
    return """
        <h1 id="welcome">Welcome</h1>
        <p>The following enpoints exist:</p>
        <p><a href="./company">/company</a></p>
        <ul>
        <li>list of unique company IDs</li>
        </ul>
        <p><a href="./company/88958775">/company/&ltid&gt</a></p>
        <ul>
        <li>returns a list of Officer records at that company</li>
        </ul>
        <p><a href="./country">/country</a></p>
        <ul>
        <li>a list of unique countries</li>
        </ul>
        <p><a href="./country/SCOTLAND">/country/&ltcountry&gt</a></p>
        <ul>
        <li>returns a list of Officer records with an address within that country</li>
        </ul>
    """

class Company(Resource):
    """
    List of Officer objects pulled from in memory datastore.  
    Filters by company_num and passes dict to Flask (which will return JSON)
    """
    def get(self, comp_num):
        result = data[data['comp_num']==comp_num]
        if len(result) > 0:
            # Remove NaN from result then convert to JSON
            result = result.apply(lambda x : x.dropna().to_dict(),axis=1).to_dict()
            return {'success': 'true', 'result': result}
            # return {'success': 'true', 'result': out2.to_dict('records')}
        else:
            abort(404, message=f'Company {comp_num} does not exist')


class CompanyList(Resource):
    def get(self):
        """Return list of Company Numbers (IDs), so these can be used in Company request"""
        result = data['comp_num'].to_list()
        return {'success': 'true', 'company_nums': result}
    

class Country(Resource):
    def get(self, country):
        """
        List of Officer objects filtered by country.  
        Filters by country and passes dict to Flask (which will return JSON).
        """
        result = data[data['country']==country]
        if len(result) > 0:
            return {'success': 'true', 'result': result.to_dict('records')}
        else:
            abort(404, message=f'Country {country} does not exist in the data')

class CountryList(Resource):
    def get(self):
        """Return distinct list of Countries, so these can be used in Country request"""
        result = data[data['country'].notnull()]['country'].unique().tolist()
        return {'success': 'true', 'countries': result}


api.add_resource(Company, '/company/<int:comp_num>')
api.add_resource(CompanyList, '/company')
api.add_resource(Country, '/country/<country>')
api.add_resource(CountryList, '/country')


# DEVELOPMENT SERVER
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8000)

# Use production WSGI server
if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8000)