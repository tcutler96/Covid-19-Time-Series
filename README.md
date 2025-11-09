# Covid-19 Time Series

We retrieve Covid-19 data including global confirmed, death and recovered cases ([JHU CSSE](https://github.com/CSSEGISandData/COVID-19)) and UK deaths by age and region ([ONS](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/weeklyprovisionalfiguresondeathsregisteredinenglandandwales)), clean it to our liking and then perform various analysis and visualisations.

## US Confirmed Daily Cases
By plotting US confirmed daily cases on a semi logarithmic plot, we can see that there was a short period of exponential growth from about 2nd March to 22nd March, which is when stay-at-orders were beginning to be announced in the US. It seems that the lockdown procedures were successful in significantly reducing transmission numbers.
![Global Analysis](demo/US_confirmed_cases.png)

## Global Confirmed Daily Cases
By plotting the daily confirmed cases for each country/ province, overlayed on a world map, we get visualisation of how the pandemic spread across the globe. We can see that it starts in Wuhan, China and then isolated hotspots appears throughout the rest of the world which gradually grow.
![Global Animation](demo/global_confirmed_cases.gif)

## UK Deaths by Age
By plotting UK deaths over time separated into age groups, we can see a big spike around April, just after lockdown was initiated, that eventually falls off but then begins to rise again from October. Also, the majority of deaths are elderly people, with over 80% of deaths being persons over the age of 70, who most likely had previous underlying health conditions.
![UK Analysis](demo/uk_deaths_age.png)

## UK Deaths by Region
By plotting the map of the UK with colour coded regions, we can see how each region was effected each day. The worst time period was during April with many regions reporting hundreds of deaths each days and the countries capital of London reaching over 300. This rapidly falls off following the lockdown procedures.
![UK Animation](demo/uk_deaths_region.gif)
