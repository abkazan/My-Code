# Built a website that displays JSON data and accepts donation
### TLDR: flask, pandas, A/B testing
For this project I created a flask application with 3 pages: home, browse, and and donate
1. Home: contains a brief intro as well as links to the donation page (with A/B testing) and browse page
3. Browse: displays the chosen dataset, and also implements rate limiting to 1 request per minute
4. Donate: allows visitors to submit their email which is then handled with a post request
