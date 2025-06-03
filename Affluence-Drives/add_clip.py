import json
import uuid
from datetime import datetime

def add_fl_attachment_to_url(video_url):
    """
    Adds 'fl_attachment/' to a Cloudinary video URL for direct download.
    Example:
    Input:  https://res.cloudinary.com/demo/video/upload/dog.mp4
    Output: https://res.cloudinary.com/demo/video/upload/fl_attachment/dog.mp4

    Input:  https://res.cloudinary.com/demo/video/upload/w_200,h_150/cat.mp4
    Output: https://res.cloudinary.com/demo/video/upload/fl_attachment/w_200,h_150/cat.mp4
    (Cloudinary is flexible; fl_attachment generally works well when inserted like this,
    even before other transformations. It signals the intent to download.)
    """
    if "fl_attachment" in video_url:  # Check if already present
        return video_url
    
    upload_marker = "/video/upload/"
    if upload_marker not in video_url:
        print(f"Warning: '{upload_marker}' not found in URL. Cannot automatically add fl_attachment. URL unchanged: {video_url}")
        return video_url
    
    # Replace the first occurrence of '/video/upload/' 
    # with '/video/upload/fl_attachment/'
    return video_url.replace(upload_marker, upload_marker + "fl_attachment/", 1)

def generate_new_clips_json():
    """
    Prompts the user for new clip details and generates JSON text for these clips.
    """
    newly_added_clips = []
    print("\n--- Generate JSON for New Clips ---")
    print("This script will help you create JSON entries for your new video clips.")
    print("The output will be JSON text that you can copy and paste into your clips.json file.")

    while True:
        print("\n-- Adding a new clip --")
        video_url_original = input("Enter Cloudinary Video URL (e.g., https://res.cloudinary.com/.../clip.mp4): ").strip()
        if not video_url_original:
            print("Video URL cannot be empty. Please try again.")
            continue

        video_url_for_download = add_fl_attachment_to_url(video_url_original)
        print(f"  Modified Video URL (for download): {video_url_for_download}")

        title = input("Enter Clip Title: ").strip()
        if not title:
            print("Title cannot be empty. Please try again.")
            continue

        tags_input = input("Enter Tags (comma-separated, e.g., luxury,car,drive): ").strip()
        tags = [tag.strip().lower() for tag in tags_input.split(',') if tag.strip()]

        # Generate a unique ID
        clip_id = f"clip_{uuid.uuid4().hex[:10]}"

        # Get current date for dateAdded
        date_added = datetime.now().strftime("%Y-%m-%d")

        new_clip = {
            "id": clip_id,
            "videoSrc": video_url_for_download, # Use the modified URL
            "title": title,
            "tags": tags,
            "dateAdded": date_added
            # thumbnailSrc and description are intentionally omitted as per your request
        }
        
        # Store the original URL if you want it for other purposes, 
        # but videoSrc should be the one for download.
        # new_clip["originalVideoUrl"] = video_url_original # Optional: if you want to keep it

        newly_added_clips.append(new_clip)

        print(f"\n  Clip '{title}' (ID: {clip_id}) prepared.")

        add_another = input("Add another clip? (yes/no): ").strip().lower()
        if add_another != 'yes':
            break

    if newly_added_clips:
        print("\n--- Generated JSON for New Clips ---")
        print("Copy the JSON array below and add it to your clips.json file.")
        print("If your clips.json is empty, you can use this as the entire content.")
        print("If you have existing clips, you'll need to manually merge this array into your existing JSON array structure.")
        
        # Output the list of newly added clips as a JSON array string
        json_output = json.dumps(newly_added_clips, indent=4)
        print("\n```json")
        print(json_output)
        print("```\n")
    else:
        print("\nNo clips were added.")

if __name__ == "__main__":
    generate_new_clips_json()
