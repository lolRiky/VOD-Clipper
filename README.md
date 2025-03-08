# VOD Clipper

A python script which clips a video files based on a timestamps provided a json file. Script will organize clips into folders per VOD. Optionally, every clip per topic can be merged into a single larger clip using `--compile`.

## Prerequisites
- Python3.11 
- ffmpeg in path

## Example JSON
```json
{
    "2023-10-11_new.mkv": {
        "introduction": [ ["00:00:00", "00:01:00"], ["00:03:00", "00:04:00"], ["00:04:00", "00:05:00"] ],
        "outro": [ ["01:27:00", "01:28:00"], ["01:30:00", "01:31:00"] ],
    },
    "2023-05-03_meeting.mkv": {
        "topic1": [ ["00:05:23", "00:13:58"]],
        "topic2": [ ["00:15:27", "00:31:03"]]
    }
}
```

## Usage
```bash
python clipvod.py [--compile]
```

Expected folder structure
```
root_dir_with_script/
├── 2023-10-11_new/
│   ├── introduction/
│   │   ├── introduction1.mp4
│   │   ├── introduction2.mp4
│   │   ├── introduction3.mp4
│   │   ├── introduction.mp4  (if --compile is used)
│   ├── outro/
│       ├── outro1.mp4
│       ├── outro2.mp4
│       ├── outro.mp4  (if --compile is used)
│
├── 2023-05-03_meeting/
│   ├── topic1/
│   │   ├── topic11.mp4
│   ├── topic2/
│       ├── topic21.mp4
```