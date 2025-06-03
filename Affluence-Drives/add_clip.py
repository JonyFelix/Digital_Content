import json
import uuid
from datetime import datetime

def modify_cloudinary_url(video_url, transformations=None):
    """
    Adds specified Cloudinary transformations to a video URL.
    By default, it adds 'fl_attachment' and 'ac_none'.

    Args:
        video_url (str): The original Cloudinary video URL.
        transformations (list, optional): A list of transformation strings 
                                         (e.g., ["fl_attachment", "ac_none", "e_volume:mute"]).
                                         Defaults to ["fl_attachment", "ac_none"].

    Returns:
        str: The modified Cloudinary video URL with transformations.
    """
    if transformations is None:
        transformations = ["fl_attachment", "ac_none"] # Default transformations

    active_transformations = []
    # Filter out transformations already present in the URL to avoid duplication
    # This is a simple check; more robust parsing might be needed for complex existing URLs
    for t in transformations:
        # Check if the core part of the transformation (e.g., "fl_attachment" or "ac_none")
        # is already in the URL as a segment like /fl_attachment/ or /ac_none,
        # or as part of a comma-separated list like /fl_attachment,ac_none/
        # This check is not perfect for all Cloudinary URL structures but covers common cases.
        if f"/{t}/" not in video_url and f",{t}" not in video_url and f"{t}," not in video_url:
            # A more robust check would be to parse existing transformations if any.
            # For now, we'll assume simple addition if not obviously present.
            if not any(existing_t.startswith(t.split(':')[0]) for existing_t in video_url.split('/') if ':' in existing_t): # Avoid duplicating e.g. e_volume:0 if e_volume:mute is added
                active_transformations.append(t)

    if not active_transformations: # If all desired transformations seem to be present or no new ones to add
        return video_url
    
    upload_marker = "/video/upload/"
    if upload_marker not in video_url:
        print(f"Warning: '{upload_marker}' not found in URL. Cannot automatically add transformations. URL unchanged: {video_url}")
        return video_url
    
    # Correctly find the position after "/video/upload/"
    parts = video_url.split(upload_marker, 1)
    base_url = parts[0] + upload_marker
    path_after_upload = parts[1]

    # Check if there are existing transformations (version number like v12345 is not a transformation)
    existing_transforms_and_path = path_after_upload.split('/')
    path_segments = []
    current_transformations_segment = []

    # Separate existing transformations from the actual path/version
    # This logic assumes transformations are before version numbers or the main path
    version_or_public_id_started = False
    for segment in existing_transforms_and_path:
        if segment.startswith('v') and segment[1:].isdigit(): # Likely a version number
            version_or_public_id_started = True
            path_segments.append(segment)
        elif version_or_public_id_started: # If version/id started, rest is path
            path_segments.append(segment)
        elif ',' in segment or ':' in segment or segment in ["fl_attachment", "ac_none"]: # Likely existing transformations
            current_transformations_segment.extend(s.strip() for s in segment.split(','))
        else: # Part of the public_id or folder structure
            version_or_public_id_started = True
            path_segments.append(segment)
            
    # Add new transformations, ensuring no duplicates with what was parsed
    for t in active_transformations:
        if t not in current_transformations_segment:
            current_transformations_segment.append(t)
            
    final_transform_string = ",".join(current_transformations_segment)
    
    if final_transform_string:
        return base_url + final_transform_string + "/" + "/".join(path_segments)
    else: # Should not happen if active_transformations is not empty, but as a fallback
        return base_url + "/".join(path_segments)


def generate_new_clips_json():
    """
    Prompts the user for new clip details and generates JSON text for these clips.
    """
    newly_added_clips = []
    print("\n--- Generate JSON for New Clips ---")
    print("This script will help you create JSON entries for your new video clips.")
    print("It will automatically add 'fl_attachment' (for direct download) and 'ac_none' (to remove audio).")
    print("The output will be JSON text that you can copy and paste into your clips.json file.")

    while True:
        print("\n-- Adding a new clip --")
        video_url_original = input("Enter Cloudinary Video URL (e.g., https://res.cloudinary.com/.../clip.mp4): ").strip()
        if not video_url_original:
            print("Video URL cannot be empty. Please try again.")
            continue

        # Apply default transformations: direct download and no audio
        video_url_transformed = modify_cloudinary_url(video_url_original) 
        print(f"  Modified Video URL (for download, no audio): {video_url_transformed}")

        title = input("Enter Clip Title: ").strip()
        if not title:
            print("Title cannot be empty. Please try again.")
            continue

        tags_input = input("Enter Tags (comma-separated, e.g., luxury,car,drive): ").strip()
        tags = [tag.strip().lower() for tag in tags_input.split(',') if tag.strip()]

        clip_id = f"clip_{uuid.uuid4().hex[:10]}"
        date_added = datetime.now().strftime("%Y-%m-%d")

        new_clip = {
            "id": clip_id,
            "videoSrc": video_url_transformed, # Use the modified URL
            "title": title,
            "tags": tags,
            "dateAdded": date_added
            # thumbnailSrc and description are omitted as per your request
        }
        
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
        
        json_output = json.dumps(newly_added_clips, indent=4)
        print("\n```json")
        print(json_output)
        print("```\n")
    else:
        print("\nNo clips were added.")

if __name__ == "__main__":
    generate_new_clips_json()
    # Adding this line to keep the session alive until user presses Enter
    input("\nPress Enter to exit the session...")
    
