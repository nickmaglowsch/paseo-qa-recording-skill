---
name: paseo-qa-recording
description: Record a video of a QA session in the Paseo browser, in the background, using the local paseo-browser-recorder plugin. Use when the user asks to record QA proof, record a video/screencast of a Paseo browser session, capture video evidence of a flow, or "record it" while driving browser_* tools. Produces an .mp4/.webm and reports its path plus ffprobe stats.
---

# Record QA proof in the Paseo browser

The `paseo-browser-recorder` plugin ([nickmaglowsch/paseo-browser-recorder](https://github.com/nickmaglowsch/paseo-browser-recorder)) records a Paseo browser tab while it sits in the background. It captures `browser_screenshot` frames on a timer and encodes them with ffmpeg. No window is focused or shown.

## 1. Check the recorder is available

- If you have the `browser_record_start` / `browser_record_stop` tools (MCP server `browser-recorder`), use them.
- Otherwise your agent was created before the plugin was installed. Use the fallback script in this skill's directory:
  `python3 ~/.claude/skills/paseo-qa-recording/record.py start <browserId> [outputPath] [fps]`
  `python3 ~/.claude/skills/paseo-qa-recording/record.py stop <browserId>`
- If both fail, run `paseo plugin ls`. The plugin must be `running`. If it isn't, check `paseo plugin logs paseo-browser-recorder` and tell the user. Do not restart the daemon.
- If the plugin isn't installed, ask the user before installing it (plugins are trusted, unsandboxed code): `paseo plugin install github:nickmaglowsch/paseo-browser-recorder`.

## 2. Record

1. Open or pick the tab: `browser_new_tab` or `browser_list_tabs`.
2. Start before the first action. Default to `outputPath: ~/Movies/paseo-qa/<short-flow-name>-<YYYYMMDD-HHMM>.mp4` (expand `~` to an absolute path; the file must not already exist), and default `fps` to 5. Use up to 15 fps for animation-heavy flows. Set `maxSeconds` above the expected session length (default 600).
3. Drive the flow with the normal `browser_*` tools.
4. Always call stop, including when the flow fails. A failed flow is still evidence. If you forget, the recorder stops by itself when the tab closes, the agent session ends, or `maxSeconds` passes.

Known Paseo quirk: in a background tab, the first `browser_type` right after a navigation can be silently dropped. Confirm typed values with `browser_snapshot` or `browser_evaluate` and retype when needed, so the video shows the real flow.

## 3. Verify and report

Run this on the output:

```bash
ffprobe -v error -count_frames -show_entries stream=codec_name,width,height,r_frame_rate,nb_read_frames:format=duration -of default=nw=1 <file>
```

Report the file path, duration, resolution, and frame count. Check that the duration is roughly the session's real length. To spot-check the content, build a contact sheet and look at it:

```bash
ffmpeg -v error -y -i <file> -vf "select='not(mod(n\,25))',scale=480:-2,tile=4x3" -frames:v 1 -update 1 /tmp/qa-contact.png
```

If the user wants to watch it, `open -R <file>` reveals it in Finder.

## Limits

- Timed screenshots, not true video: 1–15 fps, frames capped at 1280px wide.
- Needs ffmpeg on PATH, and a daemon with no password set (the plugin calls the daemon's loopback agent MCP endpoint).
