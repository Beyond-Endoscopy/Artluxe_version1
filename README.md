# Artluxe_version1

## Motivation of the project
Artluxe is a startup company offering machine learning service for art enthusiasts and collectors. To enable the machine learning jobs, an auction artworks database including text information and pictures is needed. Previously this was done manually on local computers. \
In this project, I built an **AWS based** data pipeline which can be fully automated using Apache Airflow. This data pipeline freed us from staring at the computer screen and taking notes. 

## **The structure of this repository 

```bash
.
├── README.md
├── airflow
│   └── upcoming_work.py
├── artworks
│   ├── artwork.py
│   ├── artworks_getter.py
│   ├── auctions.py
│   ├── nlp_model
│   │   └── nlp_model.py
│   ├── past_artwork.py
│   └── past_artworks_getter.py
├── images
│   ├── Automated_Auction_Information_Pipeline-2.jpg
│   └── Automated_Auction_Information_Pipeline-3.jpg
├── new_auctions_collector.py
├── new_link_monitor.txt
├── offline_auctions.txt
├── online_auctions.txt
├── past_auctions.txt
├── past_auctions_collector.py
├── past_link_monitor.txt
├── results.py
├── to_database
│   ├── Insert_into_db.py
│   ├── img_to_s3.py
│   ├── monitor_to_db.py
│   └── update_db.py
├── upcoming_offline.py
└── upcoming_online.py
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
