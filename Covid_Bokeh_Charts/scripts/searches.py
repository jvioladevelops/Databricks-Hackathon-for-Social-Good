# pandas and numpy for data manipulation
import pandas as pd
import numpy as np
from bokeh.io import curdoc
from bokeh.plotting import figure, output_file
from bokeh.resources import CDN
from bokeh.embed import file_html

from scipy.stats import gaussian_kde

from bokeh.plotting import figure
from bokeh.models import (CategoricalColorMapper, HoverTool, 
						  ColumnDataSource, Panel, 
						  FuncTickFormatter, SingleIntervalTicker, LinearAxis)
from bokeh.models.widgets import (CheckboxGroup, Slider, RangeSlider, 
								  Tabs, CheckboxButtonGroup, 
								  TableColumn, DataTable, Select)
from bokeh.layouts import column, row, WidgetBox, gridplot, Spacer
from bokeh.palettes import Category20_16

def searches_tab(countries):
	
	# Dataset for density plot based on carriers, range of delays,
	# and bandwidth for density estimation
	def make_dataset(country_list, range_start, range_end, bandwidth):

		xs = []
		ys = []
		colors = []
		labels = []

		for i, country in enumerate(country_list):
			subset = countries[countries['country_region'] == country]
			subset = subset[subset['residential'].between(range_start, 
														range_end)]



			kde = gaussian_kde(subset['residential'], bw_method=bandwidth)

			
			# Evenly space x values
			x = np.linspace(range_start, range_end, 100)
			# Evaluate pdf at every value of x
			y = kde.pdf(x)

			# Append the values to plot
			xs.append(list(x))
			ys.append(list(y))

			# Append the colors and label
			colors.append(country_colors[i])
			labels.append(country)

		new_src = ColumnDataSource(data={'x': xs, 'y': ys, 
								   'color': colors, 'label': labels})

		return new_src

	def make_plot(src):
		p = figure(plot_width = 700, plot_height = 700,
				   title = 'Plot of Residential Searches by Country',
				   x_axis_label = 'Number of Searches', y_axis_label = 'Scaled Value')


		p.multi_line('x', 'y', color = 'color', legend = 'label', 
					 line_width = 3,
					 source = src)

		# Hover tool with next line policy
		hover = HoverTool(tooltips=[('Country', '@label'), 
									('Searches', '$x'),
									('Scaled Value', '$y')],
						  line_policy = 'next')

		# Add the hover tool and styling
		p.add_tools(hover)

		p = style(p)

		return p
	
	def update(attr, old, new):

		country_to_plot = [country_selection.labels[i] for i in 
							country_selection.active]
		
		# If no bandwidth is selected, use the default value
		if bandwidth_choose.active == []:
			bandwidth = None
		# If the bandwidth select is activated, use the specified bandwith
		else:
			bandwidth = bandwidth_select.value
			
		
		new_src = make_dataset(country_to_plot,
									range_start = range_select.value[0],
									range_end = range_select.value[1],
									bandwidth = bandwidth)
		
		src.data.update(new_src.data)
		
	def style(p):
		# Title 
		p.title.align = 'center'
		p.title.text_font_size = '20pt'
		p.title.text_font = 'serif'

		# Axis titles
		p.xaxis.axis_label_text_font_size = '14pt'
		p.xaxis.axis_label_text_font_style = 'bold'
		p.yaxis.axis_label_text_font_size = '14pt'
		p.yaxis.axis_label_text_font_style = 'bold'

		# Tick labels
		p.xaxis.major_label_text_font_size = '12pt'
		p.yaxis.major_label_text_font_size = '12pt'

		return p
	

	available_countries = list(set(countries['country_region']))
	available_countries.sort()

	country_colors = Category20_16
	sorted(country_colors)



	country_selection = CheckboxGroup(labels=available_countries, 
									   active = [0, 1])
	country_selection.on_change('active', update)
	
	range_select = RangeSlider(start = -60, end = 180, value = (-60, 120),
							   step = 5, title = 'Range of Delays (min)')
	range_select.on_change('value', update)
	

	initial_countries = [country_selection.labels[i] for 
						i in country_selection.active]
	
	# Bandwidth of kernel
	bandwidth_select = Slider(start = 0.1, end = 5, 
							  step = 0.1, value = 0.5,
							  title = 'Bandwidth for Density Plot')
	bandwidth_select.on_change('value', update)
	
	# Whether to set the bandwidth or have it done automatically
	bandwidth_choose = CheckboxButtonGroup(
		labels=['Choose Bandwidth (Else Auto)'], active = [])
	bandwidth_choose.on_change('active', update)

	# Make the density data source
	src = make_dataset(initial_countries, 
						range_start = range_select.value[0],
						range_end = range_select.value[1],
						bandwidth = bandwidth_select.value) 
	
	# Make the density plot
	p = make_plot(src)
	
	# Add style to the plot
	p = style(p)
 

	
	# Put controls in a single element
	controls = WidgetBox(country_selection)
	
	# Create a row layout
	layout = row(controls, p)
	
	# Make a tab with the layout 
	tab = Panel(child=layout, title = 'Density Plot')

	return tab