from bokeh.plotting import figure, output_file, show
import pandas

#df=pandas.read_csv("stock.csv", parse_dates=["Date"])
df=pandas.read_csv("initial.csv", parse_dates=["date"])
p=figure(width=750,height=250,x_axis_type="datetime",sizing_mode='scale_both')

#p.line(df["Date"],df["Close"], color="Orange", alpha=0.5)
p.line(df["date"],df["residential_percent_change_from_baseline"], color="Green", alpha=0.5)


output_file("initial2.html")

#show(p)