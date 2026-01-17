from googleapiclient.discovery import build
import pandas as pd

API_KEY = "AIzaSyCKSzTbjHujlh_wXk8kpy7T_TF_PxiQS-g"

youtube = build("youtube", "v3", developerKey=API_KEY)

SEARCH_QUERY = "book review"
MAX_VIDEOS = 5
COMMENTS_PER_VIDEO = 50

comments_data = []

# Search for videos
search_request = youtube.search().list(
    q=SEARCH_QUERY,
    part="snippet",
    type="video",
    maxResults=MAX_VIDEOS
)
search_response = search_request.execute()

video_ids = [item["id"]["videoId"] for item in search_response["items"]]

# Fetch comments for each video
for video_id in video_ids:
    video_response = youtube.videos().list(
        part="snippet",
        id=video_id
    ).execute()

    video_title = video_response["items"][0]["snippet"]["title"]

    comment_request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=COMMENTS_PER_VIDEO,
        textFormat="plainText"
    )

    comment_response = comment_request.execute()

    for item in comment_response["items"]:
        snippet = item["snippet"]["topLevelComment"]["snippet"]

        comments_data.append({
            "video_title": video_title,
            "comment_text": snippet["textDisplay"],
            "author": snippet["authorDisplayName"],
            "like_count": snippet["likeCount"],
            "published_at": snippet["publishedAt"],
            "source": "youtube"
        })

df = pd.DataFrame(comments_data)
df.to_csv("data/raw/youtube_book_comments.csv", index=False)

print(f"Collected {len(df)} YouTube comments")
