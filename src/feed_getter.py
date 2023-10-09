import os
import requests

def get_and_save_feed():
	output_file = "output/feed.xml"
	if not os.path.exists("output"):
		# ディレクトリが存在しない場合、ディレクトリを作成する
		os.makedirs("output")
	
	try:
		# フィードをダウンロード
		response = downloadFeed()
		response.raise_for_status()  # エラーチェック
		# ダウンロードしたフィードをファイルに保存
		with open(output_file, 'wb') as file:
			file.write(response.content)
		#
		print(f'フィードを {output_file} に保存しました。')
	except requests.exceptions.HTTPError as e:
		print(f'HTTPエラーが発生しました: {e}')

def downloadFeed():
	# 気象庁feed
	feedurl = 'https://www.data.jma.go.jp/developer/xml/feed/regular.xml'
	ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
	headers = {'User-Agent': ua}
	res = requests.get(feedurl, headers = headers)
	return res

if __name__ == "__main__":
	get_and_save_feed()
