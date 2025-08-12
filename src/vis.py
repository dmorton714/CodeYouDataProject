# %% [markdown]
# # Visualization examples
# 
# Visualizion was not turn into a class because the project will use Google Locker for dashboard creation, this notebook only works to showcase how to use the Data Manipulation classes.

# %% [markdown]
# ## Imports

# %%
import pandas as pd
import plotly.express as px
import os
import sys
parent_dir = os.path.abspath("..")
sys.path.append(parent_dir)
from dash import Dash, dcc, html, Input, Output
from most_common_pathways_taken_data import Most_common_pathways_taken_data
from completion_rate_data import Completion_rate_data
from cleaning_enrollments_data import EnrollmentsCleaning

# %% [markdown]
# ## Cleaning data
# 
# This step should be done before the use of any of the Data classes

# %%
cleaner = EnrollmentsCleaning(pd.read_excel('../../data/ARC_Enrollments.xlsx'))


# %% [markdown]
# ## Most common pathway taken:

# %%
def Dash_most_selected_path_by_cohort() -> Dash: # Need to pass the dataframe argument because of how the Data is structure
    app = Dash(__name__)
    # Const
    data_class = Most_common_pathways_taken_data(cleaner.Get_clean_data())

    dropdown_options = data_class.Get_cohorts_list()
    pathway_color = {
        'Web Development M1': 'blue',
        'Data Analysis M1': 'red', 
        'Software Development M1': 'green',
        'Quality Assurance M1': 'yellow', 
        'User Experience M1': 'purple'
    }

    # Display
    app.layout = html.Div([
        html.H2('Cohorts', style={'text-align': "center"}),
        html.P('Select Cohort:'),
        dcc.Dropdown(
            id="dropdown",
            options=dropdown_options,
            value=dropdown_options[0],
            clearable=False,
        ),
        dcc.Graph(id="graph")
        
    ], style={'backgroundColor':'white'})

    @app.callback(
        Output("graph", "figure"),
        Input("dropdown", "value"))

    # Graph
    def tt(time):
        df = data_class.Get_data_by_cohort(time)
        fig = px.pie(df, names='Service', values='count', color='Service', color_discrete_map=pathway_color)
        return fig

    return app

    # TODO: Add number of students per each cohort 
    # TODO: Fix the options on the selection 
    # TODO: make colors better

Dash_most_selected_path_by_cohort().run(debug=True, port=8052)

# %% [markdown]
# ## Compleation rates:

# %%
def Dash_completion_rates_by_path() -> Dash: # TODO: fix data structure so visualization doesn't use df
    app2 = Dash(__name__)
    # Const
    data_class = Completion_rate_data(cleaner.Get_clean_data())
    completion_df = data_class.Get_completion_percentages().round(2)
    options = data_class.Get_pathways_name(completion_df)

    # Display
    app2.layout = html.Div([
        html.H2('Pathways Completion', style={'text-align': "center"}),
        html.P('Select pathway:'),
        dcc.Dropdown(
            id="dropdown",
            options=options,
            value=options[0],
            clearable=False,
        ),
        dcc.Graph(id="graph")
        
    ], style={'backgroundColor':'white'})

    @app2.callback(
        Output("graph", "figure"),
        Input("dropdown", "value"))

    # Graph
    # TODO: Need to add an extra selection box with the cohorts
    def Display_pathway_completion(p):
        df = completion_df[completion_df['Pathway'] == p]
        fig = px.bar(df, x='Module', y='Successfully Completed')
        return fig

    return app2

Dash_completion_rates_by_path().run(debug=True, port=8053)


