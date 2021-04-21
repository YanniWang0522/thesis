# README
## Dry_wet_weather_extractor_behzad.py
#### output1: if only dry/wet is needed: Rain_Flow_Heathmont_Apr19_Apr20_dry.csv
#### output2: if both dry and wet are needed (0 for dry; 1 for wet): Dry_or_wet_Rain_Flow

## Average_daily_flow_weekday.py
#### input: output from Dry_wet_weather_extractor_behzad.py
#### output average daily flow chart for catchments based on weekday, weekends, all

## Storm_event_properties.py
#### input: wet from Dry_wet_weather_extractor_behzad.py
#### output: calculate Number of rainfall events, Mean evet duration (min), Mean event intensity (mm/hr) for MIT selection

## hydrograph_month_or_week.py
#### input: both dry and wet from Dry_wet_weather_extractor_behzad.py
#### output: automatically draw weekly or monthly hydrographs

## dry_weather_daily_extractor.py
#### input: output from Dry_wet_weather_extractor_behzad.py
#### output: dry weather data longer than 1 day + summary table for each event
