import time
from playwright.sync_api import sync_playwright
from yt_dlp import YoutubeDL

def play_youtube_music(search_query: str):
    """使用 Playwright 自動開啟 YouTube 並播放音樂"""
    print(f"\n[1/2] 正在開啟 YouTube 搜尋並播放：{search_query}...")
    
    with sync_playwright() as p:
        # 開啟瀏覽器 (headless=False 讓我們可以看到畫面)
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # 1. 前往 YouTube 搜尋頁面
        search_url = f"https://www.youtube.com/results?search_query={search_query}"
        page.goto(search_url)
        
        # 2. 點擊第一個影片搜尋結果
        first_video = page.locator('ytd-video-renderer a#video-title').first
        first_video.click()
        
        print("已成功進入影片頁面，開始播放音樂！(將持續播放 15 秒)")
        # 讓瀏覽器保持開啟 15 秒聆聽音樂
        page.wait_for_timeout(15000)
        browser.close()

def download_youtube_mp3(search_query: str):
    """使用 yt-dlp 自動下載音訊為 MP3 檔案"""
    print(f"\n[2/2] 正在準備下載最高音質 MP3：{search_query}...")
    
    ydl_opts = {
        'format': 'm4a/bestaudio/best', # 選擇最佳音訊格式
        'outtmpl': '%(title)s.%(ext)s', # 設定輸出檔名為影片標題
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        # 若系統無安裝 ffmpeg，退回下載預設最高品質音訊
        'ignoreerrors': True,
    }
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            # ytsearch1: 代表搜尋關鍵字並下載第一個搜尋結果
            ydl.download([f"ytsearch1:{search_query}"])
        print("\n音樂下載與轉換完成！檔案已存於目前目錄。")
    except Exception as e:
        print(f"\n下載過程中出現提示：{e}")

if __name__ == "__main__":
    # 輸入你想聽/想下載的歌名或歌手
    song_name = "Jay Chou 七里香"
    
    # 執行播放自動化
    play_youtube_music(song_name)
    
    # 執行下載功能
    download_youtube_mp3(song_name)