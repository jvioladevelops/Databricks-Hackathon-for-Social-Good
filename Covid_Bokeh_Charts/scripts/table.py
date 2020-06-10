# pandas and numpy for data manipulation
import pandas as pd
import numpy as np

from bokeh.models import ColumnDataSource, Panel
from bokeh.models.widgets import TableColumn, DataTable

def table_tab(countries):

	# Calculate summary stats for table
	country_stats = countries.groupby(['country_region'])['residential'].describe()
	country_stats = country_stats.reset_index().rename(
		columns={'country_region': 'country',  '50%':'median'})

	# Round statistics for display
	country_stats['mean'] = country_stats['mean'].round(2)
	country_src = ColumnDataSource(country_stats)

	# Columns of table
	table_columns = [TableColumn(field='country', title='Country'),
					 #TableColumn(field='date', title='Date'),
					 TableColumn(field='min', title='Min Residential Searches %'),
					 TableColumn(field='mean', title='Mean Residential Searches %'),
					 TableColumn(field='median', title='Median Residential Searches %'),
					 TableColumn(field='max', title='Max Residential Searches %')]

	country_table = DataTable(source=country_src, 
							  columns=table_columns, width=1000)

	tab = Panel(child = country_table, title = 'Summary Table')

	return tab