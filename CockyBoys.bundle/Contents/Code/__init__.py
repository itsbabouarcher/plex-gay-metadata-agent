#CockyBoys
import re, os, urllib
PLUGIN_LOG_TITLE='CockyBoys'	# Log Title

VERSION_NO = '2017.02.04.1'

REQUEST_DELAY = 0					# Delay used when requesting HTML, may be good to have to prevent being banned from the site

# URLS
BASE_URL='http://cockyboys.com%s'

# Example Video Details URL
# http://cockyboys.com/scenes/introducing-max-holt-with-tegan-zayne.html?type=vids
BASE_VIDEO_DETAILS_URL='http://cockyboys.com/scenes/'

# Example Search URL:
# http://cockyboys.com/search.php?query=Hosing+Him+Down
BASE_SEARCH_URL='http://cockyboys.com/search.php?query=%s'

# Example File Name:
# http://cdn.members.cockyboys.com/content//upload/Justin-Brody-Ricky-Roman/flash1080/justin_brody_ricky_roman.mp4?type=download
# FILENAME_PATTERN = re.compile("")
# TITLE_PATTERN = re.compile("")

ENCLOSING_DIRECTORY_LIST=["CockyBoys"]

def Start():
	HTTP.CacheTime = CACHE_1WEEK
	HTTP.Headers['User-agent'] = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.2; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)'

class CockyBoys(Agent.Movies):
	name = 'CockyBoys'
	languages = [Locale.Language.NoLanguage, Locale.Language.English]
	primary_provider = False
	contributes_to = ['com.plexapp.agents.cockporn']

	def Log(self, message, *args):
		if Prefs['debug']:
			Log(PLUGIN_LOG_TITLE + ' - ' + message, *args)

	def search(self, results, media, lang, manual):
		self.Log('-----------------------------------------------------------------------')
		self.Log('SEARCH CALLED v.%s', VERSION_NO)
		self.Log('SEARCH - media.title -  %s', media.title)
		self.Log('SEARCH - media.items[0].parts[0].file -  %s', media.items[0].parts[0].file)
		self.Log('SEARCH - media.primary_metadata.title -  %s', media.primary_metadata.title)
		self.Log('SEARCH - media.items -  %s', media.items)
		self.Log('SEARCH - media.filename -  %s', media.filename)
		self.Log('SEARCH - lang -  %s', lang)
		self.Log('SEARCH - manual -  %s', manual)

		if media.items[0].parts[0].file is not None:
			path_and_file = media.items[0].parts[0].file
			self.Log('SEARCH - File Path: %s' % path_and_file)
			path_and_file = os.path.splitext(path_and_file)[0]
			enclosing_directory, file_name = os.path.split(path_and_file)
			enclosing_directory, enclosing_folder = os.path.split(enclosing_directory)
			self.Log('SEARCH - Enclosing Folder: %s' % enclosing_folder)
			# Check if enclosing directory matches an element in the directory list.
			if enclosing_folder in ENCLOSING_DIRECTORY_LIST:
				self.Log('SEARCH - File Name: %s' % file_name)
				self.Log('SEARCH - Split File Name: %s' % file_name.split(' '))

				video_url = BASE_VIDEO_DETAILS_URL + file_name + '.html?type=vids'
				html=HTML.ElementFromURL(video_url, sleep=REQUEST_DELAY)

				video_title=html.xpath('//*[@class="gothamy sectionTitle"]//text()')[0]
				results.Append(MetadataSearchResult(id = video_url, name = video_title, score = 100, lang = lang))

	def update(self, metadata, media, lang, force=False):
		self.Log('UPDATE CALLED')

		if media.items[0].parts[0].file is not None:
			file_path = media.items[0].parts[0].file
			self.Log('UPDATE - File Path: %s' % file_path)
			self.Log('UPDATE - metadata.id: %s' % metadata.id)
			url = metadata.id

			# Fetch HTML
			html = HTML.ElementFromURL(url, sleep=REQUEST_DELAY)

			# Set tagline to URL
			metadata.tagline = url

			video_title = html.xpath('//*[@class="gothamy sectionTitle"]//text()')[0]
			self.Log('UPDATE - video_title: "%s"' % video_title)

			metadata.content_rating = 'X'
			metadata.title = video_title
			metadata.studio = "CockyBoys"