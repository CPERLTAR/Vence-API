# 2022-08-19-08-16-09 API Development Discussion SDSU
Created: 2022-08-19 08:16:09

- [ ] #task figure out if the string returned is datetime.datetime() is UTC or if is a local time zone
- [ ] #task Google Collab notebook for the API script
- [ ] #task write the API data to a Google Drive from a Jupyter Notebook
- [ ] #task look into scheduling the API to run either via Google Collab or AWS Lambda
- [ ] #task take a look at the rate of travel function by Jamie that uses the rate of travel to clean GPS points if they exceed a threshold (moving window algorithm)
- [ ] #task calculate centroid from GPS point cluster. How to know what is just GPS error and what is movement?
- [ ] #task we share a series of shared or common processing steps for cleaning GPS points, calculating travel distance and rate of travel. Can we agree on a series of of shared processing steps that are common to groups that work with GPS data?
	1. Identify metrics or calculations from the literature
	2. Write code that processes or cleans the data
	3. Write code that calculates metric
	4. Review and Refine
- [ ] #task the column matching and column naming procedure for each message type could be more rigorous. RegEx/keyword search to split into message types?
- [ ] #task take a look at the offending messages from Jamie that has a column mis-match problem and figure out what went wrong. Figure out how to safely handle mismatch. Write data to separate df? Fill in missing values as NA?
- [ ] #task fix deprecation warning for Pandas pd.concat() 
- [ ] #task re-writing or reducing the number of objects created during cleaning process

## Tags
#dev #api

## References
1. 