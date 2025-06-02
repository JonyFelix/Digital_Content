import json
import os
import uuid

# Define the path to your clips.json file
CLIPS_FILE = 'clips.json'

def get_thumbnail_url(video_url):
    """
    Derives a Cloudinary thumbnail URL from a Cloudinary video URL.
    Assumes standard Cloudinary URL structure.
    """
    if "res.cloudinary.com" in video_url and "/video/upload/" in video_url:
        # Replace /video/upload/ with /image/upload/f_jpg,pg_auto/
        # This tells Cloudinary to deliver an image (jpg) from the video
        # and automatically pick the best frame (pg_auto) as the thumbnail.
        return video_url.replace("/video/upload/", "/image/upload/f_jpg,pg_auto/")
    else:
        # Fallback if it's not a Cloudinary video URL or not in expected format
        print("Warning: Not a Cloudinary video URL. You might need to provide a custom thumbnail.")
        return input("Please paste the direct thumbnail URL for this video: ").strip()

def add_new_clip():
    """
    Prompts the user for new clip details and adds it to clips.json.
    """
    clips_data = []
    if os.path.exists(CLIPS_FILE):
        with open(CLIPS_FILE, 'r', encoding='utf-8') as f:
            try:
                clips_data = json.load(f)
            except json.JSONDecodeError:
                print(f"Warning: {CLIPS_FILE} is empty or malformed. Starting with an empty list.")
                clips_data = []

    print("\n--- Add New Clip ---")

    while True:
        video_url = input("Enter Cloudinary Video URL (e.g., https://res.cloudinary.com/.../clip.mp4): ").strip()
        if not video_url:
            print("Video URL cannot be empty. Please try again.")
            continue

        # Automatically generate thumbnail URL
        thumbnail_url = get_thumbnail_url(video_url)
        print(f"Generated/Provided Thumbnail URL: {thumbnail_url}")

        title = input("Enter Clip Title: ").strip()
        if not title:
            print("Title cannot be empty. Please try again.")
            continue

        description = input("Enter Clip Description: ").strip()
        tags_input = input("Enter Tags (comma-separated, e.g., luxury,car,drive): ").strip()
        tags = [tag.strip().lower() for tag in tags_input.split(',') if tag.strip()]

        # Generate a unique ID (simple UUID for uniqueness)
        clip_id = f"clip_{uuid.uuid4().hex[:10]}" # Unique ID, shortened for brevity

        new_clip = {
            "id": clip_id,
            "thumbnail": thumbnail_url,
            "videoSrc": video_url,
            "title": title,
            "description": description,
            "tags": tags
        }

        clips_data.insert(0, new_clip) # Add new clip at the beginning (making it appear newest)

        print("\n--- Clip Added Successfully ---")
        print(f"ID: {clip_id}, Title: {title}")

        add_another = input("\nAdd another clip? (yes/no): ").strip().lower()
        if add_another != 'yes':
            break

    # Save the updated data back to the JSON file
    with open(CLIPS_FILE, 'w', encoding='utf-8') as f:
        json.dump(clips_data, f, indent=4) # indent=4 for pretty printing

    print(f"\n{CLIPS_FILE} has been updated with new clips.")
    print("Remember to commit and push this change to GitHub to update your live website!")

if __name__ == "__main__":
    add_new_clip()
