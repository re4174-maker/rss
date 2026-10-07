# Discord Feed Bots 🚀

[![Push GitHub Trending to Discord](https://github.com/re4174-maker/rss/actions/workflows/trending.yml/badge.svg)](https://github.com/re4174-maker/rss/actions/workflows/trending.yml)
[![Push Alpaca Financial News to Discord](https://github.com/re4174-maker/rss/actions/workflows/alpaca_news.yml/badge.svg)](https://github.com/re4174-maker/rss/actions/workflows/alpaca_news.yml)

Automated GitHub Actions workers that push deduplicated alerts to Discord via webhooks.

| Workflow | Schedule | What it posts | Secrets |
|---|---|---|---|
| `trending.yml` | hourly | New global GitHub trending repositories | `DISCORD_WEBHOOK_URL` |
| `alpaca_news.yml` | every 5 min | Financial news from the Alpaca News API | `APCA_API_KEY_ID`, `APCA_API_SECRET_KEY`, `DISCORD_WEBHOOK_NEWS` |

Each workflow keeps its "already seen" state on a background branch, so nothing is posted twice.

## Setup

Add the secrets above under Settings → Secrets and variables → Actions.
