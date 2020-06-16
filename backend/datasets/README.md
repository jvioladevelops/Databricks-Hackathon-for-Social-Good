## Datasets

Countries are labeled by the **ISO 3166-1 alpha-2**. <br>

**Remember!** All countries should be identified by these codes for better integrity 
within the project. <br>

_Examples_:

| Country name          | Country code|
| ----------------------| ----------- |
| United Arab Emirates  | AE          |
| Bulgaria              | BG          |
| ...                   |             |

_Full country list_: https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2 <br>


![iso_3_codes_alpha_2](https://gist.githubusercontent.com/eli-halych/908ca870a39bbbf0348f253ec7b0270e/raw/a39d2369830dc823495b2d50a1c61297e963aed5/iso-3-countries-alpha-2.png) 



### 1. Global mobility report
_View_: [`global_mobility_report.csv`](global_mobility_report.csv)

_Description_: <br>
The reports chart movement trends over time by geography, across different 
categories of places such as retail and recreation, groceries and pharmacies, 
parks, transit stations, workplaces, and residential.
 
_Source_: https://www.google.com/covid19/mobility/



### 2. IHME COVID-19 cases/deaths dataset (NOT USED for predictions yet)
_View_: [`summary_stats_all_locs.csv`](summary_stats_all_locs.csv)

_Description_: <br>
IHME has produced forecasts which show hospital bed use, need for intensive care beds, and
ventilator use due to COVID-19 based on projected deaths for the United States, at the country and
subnational level, and countries in the European Economic Area (EEA). Forecasts at the subnational
level are included for three EEA countries: Germany, Italy, and Spain. These projections are produced
by models based on observed death rates from COVID-19, and include uncertainty intervals. 

_Source_: http://www.healthdata.org/covid/data-downloads



### 3. WHO Coronavirus Disease (COVID-19) dataset

_View_: [`who_cases_deaths.csv`](who_cases_deaths.csv)

_Description_: <br>
Shows new cases and deaths grouped by date, country and sub regions.
Also contains cumulative number of cases and deaths grouped by date, country 
and sub regions.

_Source_: https://data.humdata.org/dataset/coronavirus-covid-19-cases-and-deaths


## Analysis
#### #1 - residential search correlation (US)

![residential-corona-cases-correlation](https://gist.githubusercontent.com/eli-halych/908ca870a39bbbf0348f253ec7b0270e/raw/9d34ac124cda54650e99f6f7d8321296b3aac010/Residential-search-new-cases-graph.png) 


_Description_: <br>
The spikes you see indicate Monday-Friday. 
That makes sense, because since the lockdown started, people would not visit public places.
Instead, based on the global mobility report, people would search for residential places more.

Spikes means increased search from the regular search (baseline).
It goes down on the weekends, since normally on the weekend people always go out more.

Spikes of residential searches on Mon-Fri correlate with spikes in new coronavirus cases.
There's a noticable shift in new coronavirus cases after the highest peaks in residential searches 
that happen on Mon-Fri. Which makes sense since it take a few days for corona virus
to develop inside of a human body.


_Technical details_: <br>
_Country (code)_: US <br>
_Normalization_: MinMaxScaler -> 0..1 <br> 
Dates: 2020-03-01 to 2020-05-01 <br>
![us-lockdown-start](https://gist.githubusercontent.com/eli-halych/908ca870a39bbbf0348f253ec7b0270e/raw/9fb2a3e1fc3c452066ce7d45bbcfc96e08880c4f/US-lockdown-start-date.png) 








