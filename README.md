# Fluent API SQL Server Integration

This project is for integrating Fluent's data via API to Fluent customer's SQL server.  
Primarily using Python 3.11 to communicate and facilitate the data flow between API and MySQL. Also using Docker to relieve compatibilty issues between older and newer systems.   
There is a slack notification setup with potential for emails to be setup as well. 

### To Install

- Clone repo.  
- rename the SECRETS.py to config.py and replace all of the default info. 
- run `docker build -t yourreponame/FluentAPI . `  
- run `docker run -d -v host/path/to/logging:/app/Logs`    
  
SQL tables will need to be setup properly. I will include templates in repo eventually.   


### Message Me  
  
Feel free to email me at info@alderautomation.ca or message me on any of my social media that can be found on my website: https://www.alderautomation.ca
