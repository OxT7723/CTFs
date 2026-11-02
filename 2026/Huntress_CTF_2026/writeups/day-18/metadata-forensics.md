# Frame of Reference

Day 18 · Metadata forensics · **Session note**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

## Later Homebase account

### Day 18 Metadata Forensics: Frame of Reference

The challenge asks for primary video stream dimensions. Start the current mode
through the metadata runner, download the assigned bundle, and inspect the
question's named video file from those bytes. The reusable runner reads the
first video stream's width and height with `ffprobe` or MediaInfo and formats
them as `WIDTHxHEIGHT`.

Single Solve used `video-001.mp4` with dimensions `320x180`. The runner's
candidate was accepted. Time Trial and all five Mastery sets also completed
with every answer accepted using the same deterministic helper.

## Retained sources

- [later/writeups/day-18/metadata-forensics-frame-of-reference.md](../../source-notes/later/writeups/day-18/metadata-forensics-frame-of-reference.md)
