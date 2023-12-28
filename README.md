# This is a small twitch lurker that runs as a discord bot

You will need a twitch app token and a discord app token

## USAGE
Needs a database for the config that looks like : 
|column_name|data_type  |                                      
|------------------------------|------------------------------|
|pid|integer            |                                      
|db_ip|inet             |                                      
|should_run|boolean     |                                      
|db_username|text       |                                      
|db_passw|text          |                                      
|guild_id|text          |                                      
|person_ids|text        |                                      
|cmd_chann|text         |                                      
|db_name|text           |                                      
|stream_chann|text      |                                      
|temp_streamer|text     |                                      
|temp_streamer_msg|text |                                      
|tok|text               |                                      
|twitch_token|text      |            



### For the goog workingness, the bot will need a database (specified in the db_username, db_passw, db_name, db_ip) that looks like :

**Streamers:**
|column_name|data_type|
|------------------------------|------------------------------|
|id|text      |
|name|text    |
|pp|text      |
|added_by|text|

**Streams:**
|column_name|data_type|
|------------------------------|------------------------------|
|stream_mture|boolean  |
|stream_id|text        |
|game_id|text          |
|stream_name|text      |
|stream_thumbnail|text |
|stream_language|text  |
|streamer_id|text      |
|msg_id|text           |



                                                               
