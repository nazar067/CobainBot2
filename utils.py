"""
Module with all helper functions
"""

import sponsorblock as sb

_sb_client = sb.Client()



def get_skip_segments(video_id: str) -> list[sb.Segment] | None:
    """
    Get video skip segments using SponsorBlock.

    Used to skip sponsor inserts, intros, etc.

    :param video_id: YouTube video ID

    :return: List of SponsorBlock segments
    """

    try:
        return _sb_client.get_skip_segments(video_id)
    except sb.errors.HTTPException:
        return None



def get_ffmpeg_sponsor_filter(segments: list[sb.Segment], vid_duration_s: int) -> str:
    """
    Get ffmpeg arguments to remove SponsorBlock segments from the video.

    Works on the principle of trimming parts of the audio track
    that do not contain segments, followed by concatenation.
    """

    skipped = len(segments)
    filter_complex = ''


    # Include a gap between the beginning of the video and the first segment
    start = 0
    end = segments[0].start
    if end - start > 1:
        filter_complex += f"[0:a]atrim={start}:{end},asetpts=PTS-STARTPTS[a0];"
        skipped += 1

    # Include gaps between the rest of the segments
    for i, segment in enumerate(segments):

        # Determine the beginning and end of gap to be trimmed
        next_segment = segments[i + 1] if i + 1 < len(segments) else None
        start = segment.end
        end = next_segment.start if next_segment else vid_duration_s

        # Skip a gap if it is too short
        if end - start < 1 and len(segments) > 1:
            skipped -= 1
            continue

        segment_i = i + 1 - (len(segments) - skipped)
        filter_complex += f"[0:a]atrim={start}:{end},asetpts=PTS-STARTPTS[a{segment_i}];"


    # Add [a1][a2][...]
    for i in range(1, skipped + 1):
        filter_complex += f"[a{i}]"


    filter_complex += f"concat=n={skipped}:v=0:a=1[outa]"

    return f'-filter_complex "{filter_complex}" -map "[outa]"'
