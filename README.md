# paseo-qa-recording-skill

A Claude Code skill that records QA proof videos of [Paseo](https://paseo.sh) browser sessions in the background, using the [paseo-browser-recorder](https://github.com/nickmaglowsch/paseo-browser-recorder) plugin.

Ask something like "record a QA proof of the checkout flow in the Paseo browser". The agent starts a recording, drives the flow with the `browser_*` tools, stops the recording, and reports the video path with ffprobe stats.

## Install

1. Install the plugin: `paseo plugin install github:nickmaglowsch/paseo-browser-recorder`
2. Copy the skill:

   ```bash
   git clone https://github.com/nickmaglowsch/paseo-qa-recording-skill ~/.claude/skills/paseo-qa-recording
   ```

`record.py` is a fallback for agents created before the plugin was installed, which don't have the `browser_record_*` tools.
