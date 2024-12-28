import os
import json
from datetime import datetime

def save_metadata(video_file, folderdate):
    metadata_file = os.path.join(os.path.dirname(folderdate), "feed-list.json")
    metadata_entry = {
        "id": os.path.splitext(os.path.basename(video_file))[0],
        "path": f"/feed/{os.path.basename(folderdate)}/{os.path.basename(video_file)}",
        "filename": os.path.basename(video_file),
        "date": datetime.now().strftime('%Y-%m-%d'),
        "timestamp": datetime.now().isoformat(),
        "favorite": False,
        "type": "video"
    }

    # Load existing metadata
    if os.path.exists(metadata_file):
        with open(metadata_file, 'r') as f:
            metadata_list = json.load(f)
    else:
        metadata_list = []

    # Add new entry
    metadata_list.append(metadata_entry)

    # Save updated metadata
    with open(metadata_file, 'w') as f:
        json.dump(metadata_list, f, indent=4)
    print(f"Metadata saved: {metadata_file}")