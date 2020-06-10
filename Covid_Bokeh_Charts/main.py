# Pandas for data management
import pandas as pd

# os methods for manipulating paths
from os.path import dirname, join

# Bokeh basics 
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs
from bokeh.plotting import figure, output_file
from bokeh.resources import CDN
from bokeh.embed import file_html


#from scripts.histogram import histogram_tab
from scripts.searches import searches_tab
from scripts.table import table_tab



from bokeh.sampledata.us_states import data as states

# Read data into dataframes
countries = pd.read_csv(join(dirname(__file__), 'data', 'Global_Mobility_Report2.csv'), 
	                                          index_col=0).dropna()

# Create each of the tabs

tab1 = searches_tab(countries)
tab2 = table_tab(countries)


# Put all the tabs into one application

tabs = Tabs(tabs = [tab1, tab2])

# Put the tabs in the current document for display
curdoc().add_root(tabs)



