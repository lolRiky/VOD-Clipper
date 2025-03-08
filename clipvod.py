import os, json, subprocess, sys, argparse

root = os.getcwd()
slash = '\\' if sys.platform == 'win32' else '/'

def clip_create():
    clipj = dict()
    files = [f for f in os.listdir(root) if os.path.isfile(f)]
    # Keep only files ending with .mp4 or .mkv 
    for f in files:
        n = f.split('.')
        if n[1] == 'mkv' or n[1] == 'mp4':
            clipj[f] = {}

    print('vods to clip', clipj)
    with open('clipvods.json', 'w') as f:
        f.write(json.dumps(clipj, indent=4))

def create_dir(dir):
    if not os.path.exists(dir):
            os.makedirs(os.getcwd() + slash + dir)

def clip_vods():
    vods = dict()
    paths = dict({})
    count = 0
    with open('clipvods.json', 'r') as f:
        vods = f.read()

    vods = json.loads(vods)
    for vod, timestamps in vods.items():
        if (timestamps == [] or timestamps == {}):
            continue
        cvod = vod[:-4]
        create_dir(cvod)
        paths[cvod] = {}

        # clip individual clips for a keyword
        for name, to_clip in timestamps.items():
            if to_clip == []:
                continue
            create_dir(cvod + slash + name)
            count = 0
            for time in to_clip:
                count += 1
                clip_name = f'{cvod  + slash + name +  slash + name + str(count)}.mp4'
                if name in paths[cvod]:
                    paths[cvod][name].append(clip_name)
                else:
                    paths[cvod][name] = []
                    paths[cvod][name].append(clip_name)

                tr1 = time[0].split(':')
                tr2 = time[1].split(':')
                
                cfrom = int(tr1[0]) * 3600 + int(tr1[1]) * 60 + int(tr1[2])
                cto = int(tr2[0]) * 3600 + int(tr2[1]) * 60 + int(tr2[2]) - cfrom

                ffmpeg_cmd = f'ffmpeg -ss {cfrom} -i {vod} -c copy -t {cto} {clip_name}'.split(' ')
                p = subprocess.run(ffmpeg_cmd, shell=True)
                print('stderr', p.stderr)

    if args.compile:
        for vod, keywords in paths.items():
            # Skip non timestamped vod
            if keywords == {}:
                continue
            for keyword, clips in keywords.items():
                sdir = vod + slash + keyword
                lc = sdir + slash + 'c.txt'
                for clip in clips:
                    clip_full_path = root + slash + clip
                    with open(f'{lc}', 'a') as f:
                        f.writelines(f"file \'{clip_full_path}\'\n")

                ffmpeg_cmd = f'ffmpeg -f concat -safe 0 -i {lc} -c copy {sdir + slash + keyword}.mp4'.split(' ')
                p = subprocess.run(ffmpeg_cmd, shell=True)
                print('stderr', p.stderr)


parser = argparse.ArgumentParser(description="Script to clip vods.")
parser.add_argument("--compile", action="store_true", help="Compiles all clips for each topic")
args = parser.parse_args()

clip_vods()