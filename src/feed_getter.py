import os
import requests
import xmltodict

class RegularFeedEntry:
	def __init__(self, title, id, updated, author, link, content):
		self.title = title
		self.id = id
		self.updated = updated
		self.author = author
		self.link = link
		self.content = content
		print(title)
		print(id)
		print(updated)
		print(author)
		print(link)
		print(content)
		print('')

# 高頻度フィード（定時）
class RegularFeed:
	def __init__(self):
		self.USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
		self.Feed_Url = 'https://www.data.jma.go.jp/developer/xml/feed/regular.xml'
		self.Input_File = 'output/feed.xml'
		self.getAndSaveFeed(self.Feed_Url, self.Input_File)
		with open(self.Input_File) as file:
			self.entries = []
			self.parseFeed(xmltodict.parse(file.read()))

	def downloadFeed(self, url):
		# 気象庁feed
		headers = {'User-Agent': self.USER_AGENT}
		res = requests.get(url, headers = headers)
		return res

	def getAndSaveFeed(self, url, output_file):	
		try:
			# フィードをダウンロード
			response = self.downloadFeed(url)
			response.raise_for_status()  # エラーチェック
			# ダウンロードしたフィードをファイルに保存
			with open(output_file, 'wb') as file:
				file.write(response.content)
			#
			print(f'フィードを {output_file} に保存しました。')
		except requests.exceptions.HTTPError as e:
			print(f'HTTPエラーが発生しました: {e}')
			
	def parseFeed(self, dictobj):
		feed = dictobj['feed']
		for entry in feed['entry']:
			if '府県天気予報' entry['title']:
				newObj = RegularFeedEntry(
					entry['title'],
					entry['id'],
					entry['updated'],
					entry['author']['name'],
					entry['link']['@href'],
					entry['content']['#text'])
				output_name = basename = os.path.basename(entry['link']['@href'])
				print(output_name)
				#getAndSaveFeed(entry['link']['@href'], 'output/' + output_file)
				self.entries.append(newObj)

			if '府県週間天気予報' in entry['title']:
				newObj = RegularFeedEntry(
					entry['title'],
					entry['id'],
					entry['updated'],
					entry['author']['name'],
					entry['link']['@href'],
					entry['content']['#text'])
				output_name = basename = os.path.basename(entry['link']['@href'])
				print(output_name)
				#getAndSaveFeed(entry['link']['@href'], 'output/' + output_file)
				self.entries.append(newObj)

if __name__ == "__main__":
	if not os.path.exists("output"):
		# ディレクトリが存在しない場合、ディレクトリを作成する
		os.makedirs("output")

	parser = RegularFeed()
