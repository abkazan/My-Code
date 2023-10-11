# In this project, I made predictions about census data for Wisconsin using linear regression models
### TLDR: pandas, geopandas, matplotlib, machine learning, linear regression, sklearn, sql
1. I extracted geographic data about the Wisconsin counties from a geojson file to a geopandas dataframe
2. I extracted data from a provided database using the sql3 connector for python to make queries, and added a feature from this database to the previously created geopandas dataframe
3. I then constructed a linear regression model to predict the population of a county in Wisconsin, based off its area.
4. Next, I extracted housing unit data and made another model to predicted housing units based off population, and plotted this relationship.
5. Finally I chose an individual county to analyze, and made another model to predict its population based off geographical features.
### I tried to upload the datasets used, however they where too big in size. To see my findings, please view the p6.ipynb file
