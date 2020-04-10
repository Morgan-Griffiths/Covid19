# #!/bin/sh
kaggle datasets download sudalairajkumar/novel-corona-virus-2019-dataset
kaggle datasets download sudalairajkumar/covid19-in-italy
kaggle datasets download sudalairajkumar/covid19-in-usa
kaggle datasets download kimjihoo/coronavirusdataset

$(rm -rf covid19-in-usa)
$(rm -rf covid19-in-italy)
$(rm -rf novel-corona-virus-2019-dataset)
$(rm -rf coronavirusdataset)
$(rm states.csv)
$(rm time_series.csv)

wget http://covidtracking.com/api/states/daily.csv -O states_daily.csv
wget https://covidtracking.com/api/us/daily.csv -O us_daily.csv
wget http://coronavirusapi.com/states.csv
wget http://coronavirusapi.com/time_series.csv

unzip novel-corona-virus-2019-dataset -d novel-corona-virus-2019-dataset
unzip covid19-in-italy -d covid19-in-italy
unzip covid19-in-usa -d covid19-in-usa
unzip coronavirusdataset -d coronavirusdataset

rm covid19-in-usa.zip
rm covid19-in-italy.zip
rm novel-corona-virus-2019-dataset.zip
rm coronavirusdataset.zip