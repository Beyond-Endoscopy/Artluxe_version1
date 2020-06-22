# Artluxe_version1

## **The structure of this repository
upcoming_scraper: The py files doing scraping jobs of upcoming auctions.
histo_scraper: The py files doing scraping jobs of ended auctions.
nb_model: The naive Bayes model doing text preprocessing.
auxiliary_texts: Some txt files serves to store some information before writing into the database.


## Motivation of the project
Artluxe is a startup company offering machine learning service for art enthusiasts and collectors. To enable the machine learning jobs, an auction artworks database including text information and pictures is needed. Previously this was done manually on local computers. In this project, I built an AWS based data pipeline which can be fully automated using Apache Airflow. This data pipeline freed us from staring at the computer screen and taking notes.  

## The data pipeline 
The data pipeline starts with scraping data from the internet with selenium virtual browser, then it splits into two branches: One branch stores the images into Amazon S3 using boto3; the other preprocesses the text information with a pre-trained Naive Bayes model, then writes the data into Amazon RDS PostgresSQL. The images are named by the artwork id so that when we do the machine learning job we can easily join the image data and the SQL data. By an Airflow dag, the job of collecting data is run on a weekly basis. 

## Challenges, the inner workflow of web scraping
Automate the pipeline is by no means easy, given the intricate nature of the web scraping. To list a few, there are both online and offline auctions, their web pages (html files) are written in different formats; we also need to collect the data from auctions which just ended and updating the price realized column of our database; the scrapers may fail and need updating because of the web going down or format changing... A good design of the workflow is needed in order to resolve the difficulties.

I split the scraping job into two main workflows, one for upcoming auctions and the other for ended auctions. 

The job for the upcoming ones is done first, and it is split further into online ones and offlines. Different scrapers were used to treat the online ones and the offline ones, collecting both the images and the text information. After preprocessing the text data, I wrote them altogether into the SQL database. The images are stored all together into S3. 

Then run the job for the ended auctions. Only the artwork id and the price realized need to be collect since the price realized is the only new information, in this way I avoid lots of redundant work. Next update the SQL database using the artwork id.

For the other challenge, treating the case of failure, I added some code to the scraper so that the running information of each job is recorded. For example, I recorded how many artworks have all null values, which might be a signal that the scraper is not collecting information at all. I further created several databases to store this information so that it is very easy to check. 

## Further work
In collaboration with the owner of Artluxe, I'm incorporating the image preprocessing into the pipeline and hopefully, the machine learning part can also be included into the automated workflow.
