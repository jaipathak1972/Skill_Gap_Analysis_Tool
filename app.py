import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots

# Load the Excel file
file_path = r'C:\Users\Dell\OneDrive\Desktop\advance web scraping\Nakri_data_set\Skill_Gap_Analysis_Tool\notebooks\result.xlsx'
df = pd.read_excel(file_path)

# Drop the 'is_remote' column
df.drop(columns=['is_remote'], inplace=True)

# Summary Statistics
total_jobs = df.shape[0]
avg_salary = df['job_pay'].mean()
avg_review = df['review'].mean()
min_salary = df['job_pay'].min()
max_salary = df['job_pay'].max()

# Initialize the Dash app
app = dash.Dash(__name__)

# Function to generate skill demand plot
def create_skill_demand_plot(df):
    skills = df[['skill_1', 'skill_2', 'skill_3', 'skill_4', 'skill_5', 'skill_6', 'skill_7', 'skill_8']].melt()
    skill_counts = skills['value'].value_counts().reset_index()
    skill_counts.columns = ['skill', 'count']
    fig = px.bar(skill_counts, x='skill', y='count', title='Skill Demand')
    return fig

# Function to generate salary distribution plot
def create_salary_dist_plot(df):
    fig = px.box(df, x='Job_role', y='job_pay', title='Salary Distribution by Job Role')
    return fig

# Layout of the Dash app
app.layout = html.Div([
    html.H1("Job Market Dashboard"),
    
    
    # Summary statistics cards
    html.Div([
        html.Div([
            html.H3('Total Jobs'),
            html.P(f'{total_jobs}')
        ], className='card'),
        
        html.Div([
            html.H3('Average Salary'),
            html.P(f'₹{avg_salary:,.2f}')
        ], className='card'),
        
        html.Div([
            html.H3('Minimum Salary'),
            html.P(f'₹{min_salary:,.2f}')
        ], className='card'),
        
        html.Div([
            html.H3('Maximum Salary'),
            html.P(f'₹{max_salary:,.2f}')
        ], className='card'),
        
        html.Div([
            html.H3('Average Review'),
            html.P(f'{avg_review:.2f}')
        ], className='card'),
    ], style={'display': 'flex', 'justifyContent': 'space-around', 'padding': '20px'}),
    
    # Pie chart for job role ratio
    dcc.Graph(id='job-role-pie'),
    
    # Bar chart for skill demand
    dcc.Graph(id='skill-demand-bar'),
    
    # Box plot for salary distribution
    dcc.Graph(id='salary-dist-box'),

        # Dropdown for job role selection
    dcc.Dropdown(
        id='job-role-dropdown',
        options=[{'label': role, 'value': role} for role in df['Job_role'].unique()],
        value=df['Job_role'].unique()[0],
        clearable=False,
        style={'width': '50%'}
    )
])

@app.callback(
    [Output('job-role-pie', 'figure'),
     Output('skill-demand-bar', 'figure'),
     Output('salary-dist-box', 'figure')],
    [Input('job-role-dropdown', 'value')]
)
def update_charts(selected_role):
    filtered_df = df[df['Job_role'] == selected_role]

    job_role_pie = px.pie(df, names='Job_role', title='Job Role Ratio')
    skill_demand_bar = create_skill_demand_plot(filtered_df)
    salary_dist_box = create_salary_dist_plot(filtered_df)
    
    return job_role_pie, skill_demand_bar, salary_dist_box

if __name__ == '__main__':
    app.run_server(debug=True)
