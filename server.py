from flask import Flask,render_template,request,jsonify
import requests
import json
import codecs
app=Flask(__name__)
@app.route('/req',methods=["GET","POST"])
def index():
	#data=dict()
	#data["info"]=list()
	i=0;
	info=[]
	if request.method=="POST":
		access=request.get_json(force=True)
		response = requests.get('https://graph.facebook.com/v2.12/me?fields=posts&access_token='+access["token"])
		#print(json.loads(response.text)["posts"])
		try:
			info.append(json.loads(response.text)["posts"]["data"])
			response=requests.get(json.loads(response.text)["posts"]["paging"]["next"])
			#return response.text
			
			while(True):
				
				if("paging" in json.loads(response.text)):
					#print("i=",i)
					i=i+1
					response=requests.get(json.loads(response.text)["paging"]["next"])
					for d in json.loads(response.text)["data"]:
						info.append(d)
					#print(info)

				else :
					for d in json.loads(response.text)["data"]:
						info.append(d)
					break
			#print(info)
			with codecs.open('userinfo.tsv', 'a+',"utf-8") as users_file:
				users_file.write("story\tmessage")
				for item in info:
					if "story" in item:
						users_file.write(item["story"]+"\t")
					if "message" in item:
						users_file.write(item["message"]+"\t")
					users_file.write("\n")
				
			return jsonify(data=info)
		except:
			with codecs.open('userinfo.tsv', 'a+',"utf-8") as users_file:
				for item in info:
					if "story" in item:
						users_file.write(item["story"]+"\t")
					if "message" in item:
						users_file.write(item["message"]+"\t")
					users_file.write("\n")
			return jsonify(data=info)
		
	return render_template("index.html")
@app.route('/')
def func():
	return render_template("index.html")
if __name__=='__main__':
	app.run(debug=True)