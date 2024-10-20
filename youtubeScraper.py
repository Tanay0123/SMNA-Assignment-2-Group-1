import requests
import json


API_KEY = "AIzaSyA16rhj5Cq7wywIQaz6562_ABe4VOX2Lto"
BASE_URL = "https://www.googleapis.com/youtube/v3/search"
CHANNEL_URL = "https://www.googleapis.com/youtube/v3/channels"


# Function to search for videos
def get_videos(query, max_results=50):
    params = {
        'key': API_KEY,
        'q': query,
        'part': 'snippet',
        'maxResults': max_results,
        'type': 'video'
    }
    response = requests.get(BASE_URL, params=params)
    return response.json()


# Function to get comments for a specific video
def get_comments(video_id, max_results=100):
    comment_url = "https://www.googleapis.com/youtube/v3/commentThreads"
    params = {
        'key': API_KEY,
        'videoId': video_id,
        'part': 'snippet',
        'maxResults': max_results,
    }
    response = requests.get(comment_url, params=params)
    return response.json()


# Function to get channel (influencer) details
def get_channel_details(channel_id):
    params = {
        'key': API_KEY,
        'id': channel_id,
        'part': 'snippet,statistics'
    }
    response = requests.get(CHANNEL_URL, params=params)
    return response.json()


# Function to save videos and comments to a JSON file
def save_videos_to_json(videos, filename="western_youtube.json"):
    data_to_save = []

    for video in videos['items']:
        video_id = video['id']['videoId']
        channel_id = video['snippet']['channelId']
        channel_info = get_channel_details(channel_id)

        # Get channel (influencer) details
        subscriber_count = "N/A"
        total_views = "N/A"
        topics_frequently_covered = "Diversity, Racial Inclusivity"

        if 'items' in channel_info:
            channel_statistics = channel_info['items'][0]['statistics']
            subscriber_count = channel_statistics.get('subscriberCount', 'N/A')
            total_views = channel_statistics.get('viewCount', 'N/A')

        # Get comments for the video
        comments = get_comments(video_id)
        video_comments = []

        if 'items' in comments:
            for comment in comments['items']:
                comment_text = comment['snippet']['topLevelComment']['snippet']['textDisplay']
                comment_author = comment['snippet']['topLevelComment']['snippet']['authorDisplayName']
                video_comments.append({
                    "author": comment_author,
                    "text": comment_text
                })

        # Append video data with comments
        data_to_save.append({
            "title": video['snippet']['title'],
            "channel": video['snippet']['channelTitle'],
            "published_date": video['snippet']['publishedAt'],
            "description": video['snippet']['description'],
            "video_id": video_id,
            "subscriber_count": subscriber_count,
            "total_views": total_views,
            "topics_frequently_covered": topics_frequently_covered,
            "comments": video_comments
        })

    # Save to JSON file
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(data_to_save, json_file, ensure_ascii=False, indent=4)


#query = "TIRTIR inclusivity OR Shiseido inclusivity OR korean brand cushion shade range"
query = "Fenty Beauty inclusivity OR urbandecay inclusivity OR Tarte Cosmetics inclusivity"
racial_videos = get_videos(query)
save_videos_to_json(racial_videos)
