import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

# Load and prepare data
df = pd.read_csv("layoffs_data.csv")
df['Year'] = pd.to_datetime(df['Date']).dt.year
grouped = df.groupby(['Year', 'Industry'])['Laid_Off_Count'].sum().reset_index()

# sunburst
grouped_company = df.groupby(['Industry', 'Company'])['Laid_Off_Count'].sum().reset_index()
top_industries = grouped_company.groupby('Industry')['Laid_Off_Count'].sum().nlargest(10).index
filtered_industries = grouped_company[grouped_company['Industry'].isin(top_industries)]
top_companies = filtered_industries.groupby('Industry').apply(lambda x: x.nlargest(10, 'Laid_Off_Count'))
top_companies.reset_index(drop=True, inplace=True)

df['Date'] = pd.to_datetime(df['Date'])
weekly_layoffs = df.resample('W', on='Date')['Laid_Off_Count'].sum().reset_index()

# Create Dash app
app = dash.Dash(__name__)
server = app.server

# Define CSS styles
#body_style = {'backgroundColor': '#f6f6f6', 'fontFamily': 'Arial, sans-serif'}
header_style = {'textAlign': 'center', 'fontSize': '2em', 'margin': '20px', 'color': '#353535'}
#main_style = {'width': '60%', 'margin': '0 auto', 'backgroundColor': '#ffffffc1', 'padding': '50px', 'boxShadow': '0 0 10px rgba(0,0,0,0.1)', 'minHeight': 'calc(100vh - 300px)'}
footer_style = {'textAlign': 'center', 'padding': '20px 0', 'color': '#777'}

body_style = {
    'backgroundColor': '#f6f6f6',
    'fontFamily': 'Arial, sans-serif',
    'textAlign': 'center'  # Add this line to center everything
}

main_style = {
    'width': '60%',
    'margin': '0 auto',
    'backgroundColor': '#ffffffc1',  # Change the background color here
    'padding': '50px',
    'boxShadow': '0 0 10px rgba(0,0,0,0.1)',
    'minHeight': 'calc(100vh - 300px)',
    'textAlign': 'left',
    'color': '#353535',
    'font-size': '1.2em'
}

"""
html.Div([
            html.H2("Total Layoffs by Industry", style={'textAlign': 'center'}),
            dcc.Dropdown(
                id='year-dropdown',
                options=[{'label': i, 'value': i} for i in grouped['Year'].unique()],
                value=grouped['Year'].min(),
            ),
            dcc.Graph(id='bar-chart'),
        ], style={'textAlign': 'center'}), 
"""

app.layout = html.Div(style=body_style, children=[
    html.Header(html.H1("Recent Job Layoffs"), style=header_style),
    html.Main([
        html.P("The rise of artificial intelligence (AI) is starting yet again a significant transformation in various industries, automating many jobs. This technological advancement, while beneficial in many aspects, can lead to an increase in unemployment. In this article, we'll discuss recent job layoffs with two interactive plots and relate this to a discussion about the future directions of our current economic systems in a world with more and more automation at hand."),
        html.P("We'll start by looking at a sunburst plot that shows the top 10 industries in terms of total layoffs from 2020-2023. The data is given by layoffs.fyi and their work on tracking layoffs in various industries. In this plot, we can click on individual industries to see the top 10 companies in that industry. Big companies like Amazon, Meta, Google, Microsoft, and others lead the way. These companies often make use of extensive cost-cutting and restructuring to increase their profits. They are most likely to be the first ones to automate jobs and lay off employees. These big companies could also be put together into a 'Big Tech' group'. The biggest layoff was from Google in January 2023. In an open letter published by Google CEO Sundar Pichai, the narrative followed a similar trajectory to that of other companies that have downsized in recent months, noting that the company had 'hired for a different economic reality' than what it's up against today. This can make one think about what big megacorp CEOs mean by that. Have they decided to trust emerging AI technologies to automate a big part of their workforce?"),
        dcc.Graph(id='circle-packing-plot', style={'textAlign': 'center', 'margin': '0 auto', 'width': '550px'}), 
         # Add a width here"""
        # Add another interactive plot here
        html.P("Across the different industries, we see highly digitalized companies being layoff count leaders. We can also see an increasing trend by looking at the visualization below of the total amount of layoffs over time. We can't say if this trend is due to AI since the super Chatbot hype has only been around since around February or March of 2023 but we should be allowed to speculate."),
        dcc.Graph(id='weekly-layoffs-plot'),  # Add a width here # Add a width here
        # Add a hidden interval component
        html.P("The plots show a dangerously high amount of job layoffs in recent months(!). In 'How Artificial Intelligence Could Kill Capitalism' Bernard Marr talks about how the benefits of AI could be accruing to the owners of the technology, leading to a potential rise in economic inequality. He notes that humans will find themselves in a situation where they have to compete for whatever paid jobs are still available to them in a robot-dominated workforce. Since the existence of a 'Star-Trek-like' utopia is not feasible without a transition period."),
        html.P("There is an obvious need for a modern economic system that allows us to transition to a post-work-friendly world. Marr argues that if we can produce goods at a far cheaper cost the owner is still selling his goods to the highest bidder. In a post-work world, it is hard to grasp the concept of a 'highest bidder' due to the new economic situation."),
        html.P("We can argue that these big companies lead the way for a post-work society. They aren't necessarily concerned about human safety even though OpenAI CEO Sam Altman is known for his 'AI-safety' quotes, one of my favorites being 'AI will probably most likely lead to the end of the world, but in the meantime, there'll be great companies.' Sam Altman is also someone who promotes universal basic income which might be a good direction for a post-work society. People aren't sure about the real intentions of Sam Altman and OpenAI since they went for-profit using open-source technology that was meant to be free for everyone and most importantly, free for research."),
        html.P("As consumers, we need to keep an eye on the trajectory of automation. There is a future where megacorps use AI to extend their power to dominate a dystopian cyberpunk world. We also need to keep an eye on certain key players such as ultra-rich people like Elon Musk. Back in March 2023, Musk signed a letter demanding AI research to pause. Many speculated whether Musk was doing this for the safety of humanity or his own good. In the end, it became clear that it was the latter since he opened up his own company for AI research only weeks later."),
        html.P("Sources:", style={'font-size': '0.6em'}),
        html.P("https://techcrunch.com/2023/01/21/alphabet-makes-cuts-twitter-bans-third-party-clients-and-netflixs-reed-hastings-steps-down/, https://bernardmarr.com/how-artificial-intelligence-could-kill-capitalism/, https://edition.cnn.com/2023/07/12/tech/elon-musk-ai-company/index.html", style={'font-size': '0.5em'}),
        dcc.Interval(id='interval-component', interval=1*1000, n_intervals=0)
    ], style=main_style),
    html.Footer("Bruno Kreiner 2023", style=footer_style)
])

"""@app.callback(
    Output('bar-chart', 'figure'),
    [Input('year-dropdown', 'value')]
)
def update_bar_chart(selected_year):
    filtered_df = grouped[grouped['Year'] == selected_year].head(10)
    fig = px.bar(filtered_df, x='Industry', y='Laid_Off_Count', color='Industry')
    fig.update_layout(xaxis={'categoryorder':'total descending'}, showlegend=False)
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', yaxis_title=None, xaxis_title=None)
    return fig"""

@app.callback(
    Output('circle-packing-plot', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_circle_packing_plot(n):
    fig = px.sunburst(top_companies, path=['Industry', 'Company'], values='Laid_Off_Count', title=f"Sunburst of Top Companies by Total Layoffs in Industries")
    #fig.update_layout(height=700, width=550)  # Adjust these values as needed
    return fig

@app.callback(
    Output('weekly-layoffs-plot', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_weekly_layoffs_plot(n):
    fig = px.line(weekly_layoffs, x='Date', y='Laid_Off_Count', title=f"Weekly Total Layoffs", labels={'Laid_Off_Count': "Layoffs"})
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', xaxis_title=None)
    return fig


# Add another callback here to update the other plot

if __name__ == '__main__':
    app.run_server(debug=True)
