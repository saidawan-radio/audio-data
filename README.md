# audio-data

`audio-data` is the metadata collection component of Saidawan Radio. It connects to the configured Telegram channel with **Telethon**, scans audio messages, extracts metadata, and saves a JSON catalogue for downstream pocket repositories.

Repository: https://github.com/saidawan-radio/audio-data

## What it does

- Connects to Telegram using a Telethon `StringSession`.
- Reads audio messages from the configured channel.
- Extracts title, performer, duration, message ID, channel details, caption/message text, MIME type, file size, Telegram document ID, dates, and a generated filename.
- Assigns a stable internal ID and keeps a map from Telegram message IDs to internal IDs.
- Detects edits to existing messages and updates metadata when the Telegram edit date is newer.
- Writes the resulting data structure to the configured JSON file.

## Main files

| File | Purpose |
|---|---|
| `fetch_and_write_detail.py` | Entry point: loads configuration/data, creates the Telegram client, and starts the metadata fetch. |
| `FetchDetail.py` | Fetches Telegram messages, creates/updates audio records, and reads/writes JSON. |
| `AudioDetail.py` | Converts a Telegram audio message into a normalized metadata object and generates filenames. |
| `config.py` | Loads settings from environment variables / `.env`. |
| `requirements.txt` | Python dependencies. |
| `.github/workflows/` | Automation workflows, if enabled in the current branch. |
| `data.json` | The catalogue output when configured to use this path. |

## Data model

The JSON structure includes:

- `audio_info`: records keyed by internal audio ID.
- `map_msg_id`: mapping from Telegram message ID to internal ID.
- `general_info.last_internal_id`: the last allocated internal ID.

A record typically includes `id`, `title`, `performer`, `duration`, `date`, `author_name`, `channel`, `msg_id`, `message`, `filename`, `mime_type`, `edit_date`, `size`, and `document_id`.

## Configuration

`config.py` reads these environment variables:

- `API_ID`
- `API_HASH`
- `SESSION_STR`
- `CHANNEL_USERNAME`
- `DOWNLOAD_PATH`
- `DATA_FILE_PATH`
- `DATE_FORMAT`
- `LOAD_START_DATE`
- `DURATION_LIMIT`
- `MIN_MSG_ID`
- `DATA_FETCH_LIMIT`
- `DATA_FETCH_SIZE_LIMIT`
- `FILENAME_PATTERN`

Use GitHub Actions **Secrets** for `API_HASH` and `SESSION_STR`; do not commit them. The code expects several numeric settings to be parseable as integers.

## Local execution

Use a Python environment and install `requirements.txt`. Set the environment variables expected by `config.py`, then run:

```bash
python fetch_and_write_detail.py
```

The script needs a valid Telegram API configuration and a session authorized to read the configured channel. The configured output path must be writable.

## How it connects to the rest of the organization

`audio-data` is the catalogue source used by the pocket download/metadata processes. Pockets use the catalogue's internal IDs and Telegram message IDs to retrieve the corresponding Telegram audio, then add GitHub Raw URLs for the published media. The static web player uses the resulting metadata/media URLs to present tracks.

## Operational cautions

- Back up the JSON catalogue before changing its schema or internal-ID rules.
- Test the fetch on a copy of the data file before running a large historical scan.
- Confirm that the message has audio metadata before accessing audio attributes.
- Never expose Telegram session strings in logs, commits, or workflow artifacts.
