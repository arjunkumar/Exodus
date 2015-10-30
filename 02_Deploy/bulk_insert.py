import os
from sqlalchemy.engine import create_engine

engine = create_engine('mysql://exodusapp:exodus123@exodus.cyn9qtdt4hb5.us-west-2.rds.amazonaws.com/exodus?charset=utf8&local_infile=1')
engine.allow_local_infile=True
connection = engine.connect()


#insert into Ad table
truncate_Crawl_Raw_query="truncate table exodus_staging.Crawl_Raw"
connection.execute(truncate_Crawl_Raw_query)



filepath ='/tmp/data.csv'
#trans = connection.begin()
query = "LOAD DATA LOCAL INFILE '" + filepath +"' INTO TABLE exodus_staging.Crawl_Raw FIELDS TERMINATED BY '|||' LINES TERMINATED BY '\n'"
#connection.execute("LOAD DATA LOCAL INFILE  INTO TABLE exodus_staging.Crawl_Raw FIELDS TERMINATED BY '|||' LINES TERMINATED BY '\n'")
connection.execute(query)
#trans.commit()

#insert into Ad table
insert_Ads_query= "insert into exodus.Ad( URL, TYPE, SIZE) select LinktoAdImage, FileType, concat(Width,' X ',Height) from exodus_staging.Crawl_Raw"
connection.execute(insert_Ads_query)

#insert into Crawl table 
insert_Crawl_query ="insert into exodus.Crawl( AdID,DateID,WebsiteID,ChannelID,CompanyID) select A.Id ,d.Id, w.Id,1 , null from exodus_staging.Crawl_Raw cr inner join exodus.Ad A on A.URL = cr.LinktoAdImage inner join exodus.Date d on d.Full_Date = DATE inner join exodus.Website w on w.URL = cr.Website"


connection.execute(insert_Crawl_query)

connection.close()
