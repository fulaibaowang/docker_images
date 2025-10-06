import argparse
import os
import subprocess
import sys
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError

def safe_title(s: str) -> str:
    return s.replace("/", "_").replace("\\", "_").strip()

def run_ffmpeg(args):
    print("Running:", " ".join(args))
    subprocess.run(args, check=True)

def main():
    p = argparse.ArgumentParser(
        description=("Download 1080p video+audio with yt-dlp. "
                     "Default: no re-encode (copy). "
                     "--remux: rewrap to .mov (no re-encode). "
                     "--convert: re-encode to H.264/AAC .mov.")
    )
    p.add_argument("url", help="YouTube URL")
    p.add_argument("--convert", action="store_true",
                   help="Re-encode to MOV (H.264/AAC) with ffmpeg")
    p.add_argument("--remux", action="store_true",
                   help="Remux to MOV (no re-encode) with ffmpeg")
    p.add_argument(
        "--format",
        # more tolerant selector with fallbacks
        default=("bestvideo[height<=1080][vcodec!=none]+bestaudio[acodec!=none]/"
                 "best[height<=1080]/best"),
        help="yt-dlp format selector (default: robust <=1080p fallback chain)"
    )
    p.add_argument("--cookies", default="cookies.txt",
                   help="Cookie file path (optional, default: cookies.txt if present)")
    args = p.parse_args()

    ydl_opts = {
        "format": args.format,
        "outtmpl": "%(title)s.%(ext)s",
        # Stability/resilience knobs
        "forceipv4": True,
        "retries": 10,
        "fragment_retries": 10,
        "concurrent_fragment_downloads": 4,
        # Use the Android client, which often avoids nsig breakage
        "extractor_args": {"youtube": {"player_client": ["android"]}},
    }

    # Use cookies if the file exists (for age/region/consent walls)
    if os.path.isfile(args.cookies):
        ydl_opts["cookiefile"] = args.cookies

    # 1) Download
    try:
        with YoutubeDL(ydl_opts) as ydl:
            print("Downloading video and audio streams...")
            info = ydl.extract_info(args.url, download=True)
    except DownloadError as e:
        print("\nyt-dlp failed to fetch the requested format.", file=sys.stderr)
        print("Tip: list available formats with:", file=sys.stderr)
        print(f"  yt-dlp -F {args.url}\n", file=sys.stderr)
        raise

    title = safe_title(info.get("title", "output"))
    requested = info.get("requested_downloads", [])

    # Try to determine file paths
    video_path, audio_path, single_path = None, None, None

    if requested:
        # Separate or single files listed by yt-dlp
        for d in requested:
            fp = d.get("filepath")
            if not fp:
                continue
            if d.get("acodec") == "none":
                video_path = fp
            elif d.get("vcodec") == "none":
                audio_path = fp
            else:
                # already merged or single container
                single_path = fp
    else:
        # Fallback: yt-dlp returned a single output
        single_path = info.get("requested_formats", None) or info.get("filepath", None)
        if isinstance(single_path, list) and single_path:
            single_path = single_path[0]
        # If still None, try title-based guess with common extensions
        if not single_path:
            for ext in (".mp4", ".mkv", ".webm", ".m4a"):
                guess = f"{title}{ext}"
                if os.path.exists(guess):
                    single_path = guess
                    break

    # 2) Decide action based on flags and what we have
    if args.convert:
        # Re-encode to H.264/AAC .mov from either separate streams or a single file
        output_mov = f"{title}.mov"

        if video_path and audio_path:
            run_ffmpeg([
                "ffmpeg", "-y",
                "-i", video_path,
                "-i", audio_path,
                "-c:v", "libx264",
                "-c:a", "aac",
                "-movflags", "+faststart",
                output_mov
            ])
        elif single_path:
            run_ffmpeg([
                "ffmpeg", "-y",
                "-i", single_path,
                "-c:v", "libx264",
                "-c:a", "aac",
                "-movflags", "+faststart",
                output_mov
            ])
        else:
            print("Could not determine downloaded files to convert.", file=sys.stderr)
            sys.exit(2)

        print(f"Finished (converted): {output_mov}")
        return

    if args.remux:
        # Remux (no re-encode) to .mov
        output_mov = f"{title}.mov"
        if video_path and audio_path:
            run_ffmpeg([
                "ffmpeg", "-y",
                "-i", video_path,
                "-i", audio_path,
                "-c:v", "copy",
                "-c:a", "copy",
                "-movflags", "+faststart",
                output_mov
            ])
        elif single_path:
            run_ffmpeg([
                "ffmpeg", "-y",
                "-i", single_path,
                "-c:v", "copy",
                "-c:a", "copy",
                "-movflags", "+faststart",
                output_mov
            ])
        else:
            print("Could not determine downloaded files to remux.", file=sys.stderr)
            sys.exit(2)

        print(f"Finished (remuxed): {output_mov}")
        return

    # Default behavior: merge without re-encode (to MP4) if separate streams; else do nothing
    if video_path and audio_path:
        output_mp4 = f"{title}.mp4"
        run_ffmpeg([
            "ffmpeg", "-y",
            "-i", video_path,
            "-i", audio_path,
            "-c:v", "copy",
            "-c:a", "copy",
            "-movflags", "+faststart",
            output_mp4
        ])
        print(f"Finished (merged, no re-encode): {output_mp4}")
    else:
        print("No separate streams to merge (yt-dlp likely produced a single playable file).")

if __name__ == "__main__":
    main()
