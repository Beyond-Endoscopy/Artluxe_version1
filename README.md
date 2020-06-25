# Artluxe_version1

## Motivation of the project
Artluxe is a startup company offering machine learning service for art enthusiasts and collectors. To enable the machine learning jobs, an auction artworks database including text information and pictures is needed. Previously this was done manually on local computers. \
In this project, I built an **AWS based** data pipeline which can be fully automated using Apache Airflow. This data pipeline freed us from staring at the computer screen and taking notes. 

## **The structure of this repository 

```bash
.
├── README.md
├── airflow
│   ├── histo_work.py
│   └── upcoming_work.py
├── histo_scraper
│   ├── histo_auctions.txt
│   ├── histo_auctions_collector.py
│   ├── histo_scraper_job.py
│   └── update_database.py
├── images
│   ├── Automated_Auction_Information_Pipeline-2.jpg
│   └── Automated_Auction_Information_Pipeline-3.jpg
└── upcoming_scraper
    ├── img_to_s3.py
    ├── monitor_to_db.py
    ├── nb_model
    │   ├── MultinomialNBClassifier_v1.0.pkl
    │   └── nlp_ml_models.py
    ├── new_auctions_collector.py
    ├── new_auctions_monitor.txt
    ├── new_offline_null_counter.txt
    ├── new_online_null_counter.txt
    ├── offline_auctions.txt
    ├── online_artwork_getter.py
    ├── online_auctions.txt
    ├── preprocess.py
    ├── to_database.py
    └── upcoming_scraper_job.py
```


## Running environment and softwares used
Amazon EC2 t2-micro (ubuntu 18.04), S3, Amazon RDS db.t2.micro.\
Softwares: Python 3.6; Google Chrome driver 83.0.4103.39; Selenium Python 3.141.0; Scikit Learn 0.23.1; Pycharm Professional 2020.1

## The pipeline

![Alt text](/images/Automated_Auction_Information_Pipeline-2.jpg?raw=true "Optional Title")


## The inner pipeline of scraping 
To make the pipeline automatable, a good inner workflow in the scraping part is needed. 

![Alt text](/images/Automated_Auction_Information_Pipeline-3.jpg?raw=true "Optional Title")

## Further work
In collaboration with the owner of Artluxe, I'm incorporating the image preprocessing into the pipeline and hopefully, the machine learning part can also be included into the automated workflow.
