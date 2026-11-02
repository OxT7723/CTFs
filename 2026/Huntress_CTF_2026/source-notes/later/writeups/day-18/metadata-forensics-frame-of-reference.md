> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Day 18 Metadata Forensics: Frame of Reference

The challenge asks for primary video stream dimensions. Start the current mode
through the metadata runner, download the assigned bundle, and inspect the
question's named video file from those bytes. The reusable runner reads the
first video stream's width and height with `ffprobe` or MediaInfo and formats
them as `WIDTHxHEIGHT`.

Single Solve used `video-001.mp4` with dimensions `320x180`. The runner's
candidate was accepted. Time Trial and all five Mastery sets also completed
with every answer accepted using the same deterministic helper.
