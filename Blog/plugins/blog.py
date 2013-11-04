import os
import datetime
import logging

Global = {"config": {}, "posts": []}

Global["config"]["path"] = "posts"
Global["config"]["date_format"] = "%d-%m-%Y"

def _convertDate(date_string, path):
	try: 
		return datetime.datetime.strptime(date_string, 
			Global["config"]["date_format"])
	except Exception, e:
		logging.warning("Date format not correct for page %s, should be %s\n%s" \
			% (path, Global["config"]["date_format"], e))


def preBuild(site):
	
	global Global

	# Check if the posts path exists
	page_path = os.path.join(site.page_path, Global["config"]["path"])

	if not os.path.isdir(page_path):
		logging.warning("No posts folder found at: %s", page_path)

	for page in site.pages():
		
		if page.path.startswith("%s/" % Global["config"]["path"]):
			
			if not page.path.endswith('.html'):
				continue

			context = page.context()
			context_post = {"path": page.path}

			# Check if we have the required keys
			for field in ["title", "author", "date"]:
				
				if not context.has_key(field):
					logging.warning("Page %s is missing field: %s" % (page.path, field))
				else:
					
					if field == "date":
						context_post[field] = _convertDate(context[field], page.path)
					else:
						context_post[field] = context[field]

			Global["posts"].append(context_post)

	# Sort the posts by date and add the next and previous page indexes
	Global["posts"] = sorted(Global["posts"], key=lambda x: x.get("date"))
	Global["posts"].reverse()
	
	indexes = xrange(0, len(Global["posts"]))
	
	for i in indexes:
		if i+1 in indexes: Global["posts"][i]['prevPost'] = Global["posts"][i+1]
		if i-1 in indexes: Global["posts"][i]['nextPost'] = Global["posts"][i-1]


def preBuildPage(site, page, context, data):
	
	context['posts'] = Global["posts"]
	
	for post in Global["posts"]:
		if post["path"] == page.path:
			context.update(post)
	
	return context, data