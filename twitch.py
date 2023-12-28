from itertools import repeat
import requests as r
import os

print("\n")

# -----------------------------global-------------------------------- #
global client_secret
url_oauth = "https://id.twitch.tv/oauth2/"
url_api = 'https://api.twitch.tv/helix/users'
client_id =
client_secret = ''
oauth_token = ''
# ----------------------------end global----------------------------- #

def setup(tok):
	global client_secret
	client_secret = tok
	get_oauth_token()
	get_token_validation()



class Streamer:
	def __init__(self, id, name, pic, desc):
		self.id = id
		self.name = name
		self.pic = pic
		self.desc = desc
	class Stream:
		def __init__(self, id, sid, tags, game_name, title, lang, nsfw, thumb):
			self.id = id
			self.sid = sid
			self.tags = tags
			self.game_name = game_name
			self.title = title
			self.lang = lang
			self.nsfw = nsfw
			self.thumb = thumb
	def to_dict(self):
		return {
			'id': self.name,
			'name': self.desc,
			'pic': self.pic,
			'desc' : self.desc
		}

def get_oauth_token():
	"""
	Retrieves the OAuth token for API authentication.

	:return: The OAuth token.
	"""
	global oauth_token, client_secret
	req_oauth = r.post(f'{url_oauth}token', data={
		'client_id': client_id,
		'client_secret': client_secret,
		'grant_type': 'client_credentials',
	})
	credential = req_oauth.json()
	oauth_token = credential['access_token']
	return oauth_token


def get_token_validation():
	"""
	Perform token validation.

	:return: The response from the validation request.
	"""
	global oauth_token
	request_v = r.get(f'{url_oauth}validate', headers=create_headers())
	return request_v


def create_headers():
	"""
	Creates headers for an HTTP request.

	:return: the headers dictionary
	"""
	global oauth_token
	print(oauth_token)
	headers = {
		'Content-Type': 'application',
		"Client-Secret": client_secret,
		"Client-Id": client_id,
		"Authorization": "Bearer " + oauth_token
	}
	return headers


def get_user(user):
	"""
	:return: The response from the API request.
	"""
	# Envoi requête API
	req = r.get(f'{url_api}?login={user}', headers=create_headers())
	jreq = req.json()
	if req.status_code != 200 or len(jreq["data"]) != 1:
		return False
	return traitement(jreq)

def get_user_by_id(user):
	"""
	:return: The response from the API request.
	"""
	# Envoi requête API
	req = r.get(f'{url_api}?id={user}', headers=create_headers())
	jreq = req.json()
	if req.status_code != 200 or len(jreq["data"]) != 1:
		return False
	return traitement(jreq)

def traitement(data_to_parse) -> Streamer:
	"""
	:param data_to_parse: The data that needs to be parsed and processed. It should be a dictionary with the following structure:
	    {
	        "data": [
	            {
	                "id": <id_value>,
	                "display_name": <display_name_value>,
	                "profile_image_url": <image_url_value>
	            },
	            ...
	        ]
	    }
	:return: string with the id

	This method takes the provided data and performs some processing on it. It prints out the following information:
	- Test print from the traitement function followed by the input data.
	- The type of the input data.
	- The ID of the first element in the "data" list.
	- The login name of the first element in the "data" list.
	- The image URL of the first element in the "data" list.

	Note: This method does not return any value.
	"""
	data = Streamer(id=data_to_parse["data"][0]["id"], name=data_to_parse["data"][0]["display_name"], pic=data_to_parse["data"][0]["profile_image_url"], desc=data_to_parse["data"][0]["description"])
	return data


def get_stream(ids):
	url = 'https://api.twitch.tv/helix/streams?'
	for i in ids:
		url = url + f'user_id={i}&'
	req = r.get(f'{url}', headers=create_headers())
	return stream_traitement(req.json(), ids)

def stream_traitement(data, streamers_id) -> dict:
	l_streams = {i["user_id"]:Streamer.Stream(id=i["id"], sid=i["user_id"], tags=i["tags"], game_name=i['game_name'], title=i['title'], lang=i['language'], nsfw=i['is_mature'], thumb=i['thumbnail_url']) for i in data["data"]}
	print(l_streams)
	l_streams_keys = list(l_streams.keys())
	print(l_streams_keys)
	to_ret = {"yes":{}, "no":[]}
	for i in streamers_id:
		if str(i) in l_streams_keys:
			print(f"Stream {i} is live!")
			print(data["data"][0])
			print(l_streams[i])
			to_ret["yes"][i]=l_streams[i]
		else:
			print(f"Stream {i} is not live.")
			to_ret["no"].append(i)
	return to_ret


if __name__ == "__main__":
	pass

