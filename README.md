# README
## Dry_wet_weather_extractor_behzad.py
#### output1: if only dry/wet is needed: (if dry):RG_Rain_Flow_Heathmont_Apr19_Apr20_dry.csv
#### output2: if both dry and wet are needed (0 for dry; 1 for wet): RG_Dry_or_wet_Rain_Flow.csv

## Average_daily_flow_weekday.py
#### input: RG_Rain_Flow_Heathmont_Apr19_Apr20_dry (from Dry_wet_weather_extractor_behzad.py)
#### output: average daily flow chart for catchments based on weekday, weekends, all

## Storm_event_properties.py
#### input: RG_Rain_Flow_Heathmont_Apr19_Apr20_wet (from Dry_wet_weather_extractor_behzad.py)
#### output: calculate Number of rainfall events, Mean evet duration (min), Mean event intensity (mm/hr) for MIT selection

## hydrograph_month_or_week.py
#### input: RG_Dry_or_wet_Rain_Flow.csv (from Dry_wet_weather_extractor_behzad.py)
#### output: automatically draw weekly or monthly hydrographs

## dry_weather_daily_extractor.py
#### input: RG_Rain_Flow_Heathmont_Apr19_Apr20_dry (from Dry_wet_weather_extractor_behzad.py)
#### output1: dry weather data longer than 1 day: RG_Dry_Weather_Heatmont.csv
#### output2: summary table for each event: RG_Dry_Weather_Heatmont_summary.csv
