
from flask import Flask, render_template, request, jsonify
import pandas as pd
import json
import plotly
import plotly.express as px

data = pd.read_csv('incd_cleaned.csv')

code = {'Alabama': 'AL',
            'Alaska': 'AK',
            'Arizona': 'AZ',
            'Arkansas': 'AR',
            'California': 'CA',
            'Colorado': 'CO',
            'Connecticut': 'CT',
            'Delaware': 'DE',
            'District of Columbia': 'DC',
            'Florida': 'FL',
            'Georgia': 'GA',
            'Hawaii': 'HI',
            'Idaho': 'ID',
            'Illinois': 'IL',
            'Indiana': 'IN',
            'Iowa': 'IA',
            'Kansas': 'KS',
            'Kentucky': 'KY',
            'Louisiana': 'LA',
            'Maine': 'ME',
            'Maryland': 'MD',
            'Massachusetts': 'MA',
            'Michigan': 'MI',
            'Minnesota': 'MN',
            'Mississippi': 'MS',
            'Missouri': 'MO',
            'Montana': 'MT',
            'Nebraska': 'NE',
            'Nevada': 'NV',
            'New Hampshire': 'NH',
            'New Jersey': 'NJ',
            'New Mexico': 'NM',
            'New York': 'NY',
            'North Carolina': 'NC',
            'North Dakota': 'ND',
            'Ohio': 'OH',
            'Oklahoma': 'OK',
            'Oregon': 'OR',
            'Pennsylvania': 'PA',
            'Rhode Island': 'RI',
            'South Carolina': 'SC',
            'South Dakota': 'SD',
            'Tennessee': 'TN',
            'Texas': 'TX',
            'Utah': 'UT',
            'Vermont': 'VT',
            'Virginia': 'VA',
            'Washington': 'WA',
            'West Virginia': 'WV',
            'Wisconsin': 'WI',
            'Wyoming': 'WY'}
            
data['Code'] = data['State'].map(code)

data.rename(columns={'Age-Adjusted Incidence Rate([rate note]) - cases per 100,000':'Cases per 100k'},
               inplace=True)

app = Flask(__name__)

#Using Flask, implement the 3 routes (15 points total):

@app.route("/")
def index():
    return render_template("index.html")


@app.route('/state/<string:name>')
def returnJSON(name):
    usertext = name

    if sum(data['State'].str.lower() == usertext.lower()) == True:
    
        result = data[data['State'].str.lower() == usertext.lower()].iloc[0,2]
        
        data_json = {"State" : usertext, "Cases" : result}
        
    else:
        data_json = "ERROR - Check spelling or spaces"
    

    return jsonify(data_json)
        
        
@app.route("/info", methods=["GET"])
def info() :
    usertext = request.args.get("usertext")
    
    if sum(data['State'].str.lower() == usertext.lower()) == True:
        result = data[data['State'].str.lower() == usertext.lower()].iloc[0,2]
    else:
        result = "ERROR  - Check spelling or spaces"
        
    return render_template("info.html", analysis=result, usertext=usertext)


#Extra work (5 points)
@app.route("/map")
def map():
    fig = px.choropleth(data,
                        locations='Code',
                        color='Cases per 100k',
                        color_continuous_scale='spectral_r',
                        hover_name='State',
                        locationmode='USA-states',
                        scope='usa')
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template("map.html", graphJSON=graphJSON)




if __name__ == "__main__":
    app.run(debug=True)