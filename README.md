# Covid-19 Time Series
This project looks at how Covid-19 cases changed over time. It pulls data from two main sources. The first is the global confirmed, death, and recovered figures from the [JHU CSSE](https://github.com/CSSEGISandData/COVID-19) dataset. The second is the UK death records by age and region from the [ONS](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/weeklyprovisionalfiguresondeathsregisteredinenglandandwales). We clean the data so that the dates, locations and case numbers are consistent, then group them into useful time series. Once the data is in a good state, we produced a set of charts that show how the virus spread, how case numbers changed, and how different areas and age groups were affected.

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
