import os
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import plotly.figure_factory as ff

app = dash.Dash(__name__,title='Company Name')

os.chdir()

files = os.listdir()
numfiles=0;
numfiles=len(files)
data_combined=[]
for x in range(10):
     # opening the CSV file 
         with open(files[x], mode ='r') as file:
       # reading the CSV file 
           data = pd.read_csv(file,skiprows=[0,1,2,3,4,5,6,7,8,9,11])
           datas = data.sort_values("Time", axis = 0, ascending = True, inplace = True, na_position ='last')
data['Time']=pd.to_numeric(data['Time'], errors='coerce');
data['Time']=data['Time'].div(3600);
x1=data['Time'];

#* Background color and text colors for graphs
colors = {
    'background': '#ffffff',
    'text': '#5bb582'
}

#* Parts of csv file which is needed for graphs
############## FIGURE 1
#* Data from csv for figure 1
y1=pd.to_numeric(data['Temp.REF01_inlet'], errors='coerce');
y2=pd.to_numeric(data['Temp.REF01_middle'], errors='coerce');
y3=pd.to_numeric(data['Temp.REF01_outlet'], errors='coerce');
y4=pd.to_numeric(data['Temp.REF01_outlet2'], errors='coerce');

#* Create figure 1
fig1 = go.Figure()

#* Add tracers to fig1
fig1.add_trace(go.Scatter(x=x1, y=y1,
                    mode='lines',
                    name='Inlet'))
fig1.add_trace(go.Scatter(x=x1, y=y2,
                    mode='lines',
                    name='Middle'))
fig1.add_trace(go.Scatter(x=x1, y=y3,
                    mode='lines',
                    name='Outlet'))
fig1.add_trace(go.Scatter(x=x1, y=y4,
                    mode='lines',
                    name='Outlet 2'))

#* Update layout to add axis titles to fig1
fig1.update_layout(xaxis_title='Time [H]',
                   yaxis_title='Temperature [C]')

#* Update layout to change font color to fig 1
fig1.update_layout(
    font_color=colors['text']
)     
##############

############## FIGURE 2
y5=pd.to_numeric(data['Temp.REF01_burner'], errors='coerce');

#* Create figure 2
fig2=go.Figure()

#* Add tracers to fig2
fig2.add_trace(go.Scatter(x=x1, y=y5,
                        mode='lines',
                        name='Burner'))

#* Update layout to add axis titles to fig2
fig2.update_layout(xaxis_title='Time [H]',
                    yaxis_title='Temperature [C]')
##############


# Group data together
hist_data = [y1]
group_labels = ['Group 1']

# Create distplot with custom bin_size

fig3 = ff.create_distplot(hist_data, group_labels)
fig3.update_layout(xaxis_title='Temperature [C]',
                   yaxis_title='Time [H]')


#! not used
app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Container2 Setup - 250h test',
        style={
            'textAlign': 'center',
            'color': colors['text']

        }
    ),
    html.Div(children='Test Data', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
])

############## TABS
tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #6d6d6d',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#0c2e40',
    'color': 'white',
    'padding': '12px'
}

app.layout = html.Div([
    dcc.Tabs(
        id="tabs-example",
        value="tab-1",
        parent_className='custom-tabs',
        className='custom-tabs-container',
        children=[
            dcc.Tab(
                label='Home',
                value='tab-1',
                className='custom-tab',
                selected_className='custom-tab--selected',
                style=tab_style,
                selected_style=tab_selected_style
            ),
            dcc.Tab(
                label='Reformer',
                value='tab-2',
                className='custom-tab',
                selected_className='custom-tab--selected',
                style=tab_style,
                selected_style=tab_selected_style
            ),
            dcc.Tab(
                label='Burner',
                value='tab-3',
                className='custom-tab',
                selected_className='custom-tab--selected',
                style=tab_style,
                selected_style=tab_selected_style
            ),
            dcc.Tab(
                label='CO Slip',
                value='tab-4',
                className='custom-tab',
                selected_className='custom-tab--selected',
                style=tab_style,
                selected_style=tab_selected_style
            ),
            dcc.Tab(
                label='Dist',
                value='tab-5',
                className='custom-tab',
                selected_className='custom-tab--selected',
                style=tab_style,
                selected_style=tab_selected_style
            ),
        ]),
    html.Div(id='tabs-example-content')
])
##############



#! Callback
@app.callback(Output('tabs-example-content', 'children'),
              [Input('tabs-example', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
                        html.Div([
                            html.H1('Company name', style={"text-align": "center"}),
                            dcc.Graph(id='setup1', figure=fig1)
                            ], className="one-third column"),  
        ])
    elif tab == 'tab-2':
        return html.Div([
                        html.Div([
                            html.H2('Temperature distribution over time', style={"text-align": "center"}),
                            dcc.Graph(id='setup1', figure=fig1)
                            ], className="one-third column"),
        ])
    elif tab == 'tab-3':
        return html.Div([
                        html.Div([
                            html.H2('Burner temperature over time', style={"text-align": "center"}),
                                dcc.Graph(id='setup4', figure=fig2)
                                ], className="one-third column"),  
        ])
    elif tab == 'tab-4':
        return html.Div([
                        html.Div([
                            html.H2('CO slip over time', style={"text-align": "center"}),
                                 dcc.Graph(id='setup4', figure=fig1)
                                 ], className="one-third column"),    
        ])
    elif tab == 'tab-5':
        return html.Div([
                        html.Div([
                            html.H2('Dist', style={"text-align": "center"}),
                                 dcc.Graph(id='Dist', figure=fig3)
                                 ], className="one-third column"),    
        ])


if __name__ == '__main__':
    app.run_server(host='127.0.0.1',port='65310',debug=True)