#!/bin/bash

SOURCE_DIR="opensora_videos"
DEST_DIR="merged_videos" 

mkdir -p "$DEST_DIR"

for sub_dir in "$SOURCE_DIR"/*/; do
    
    folder_name=$(basename "$sub_dir")

    mp4_file=$(find "$sub_dir" -maxdepth 1 -type f -name "*.mp4")

    if [[ -n "$mp4_file" ]]; then
 
        new_mp4_name="$DEST_DIR/${folder_name}.mp4"


        cp "$mp4_file" "$new_mp4_name"
        echo "Moved: $mp4_file -> $new_mp4_name"
    fi
done

echo "All videos have been moved to $DEST_DIR."
