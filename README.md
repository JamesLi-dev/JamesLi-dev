# Todoist Stats

<!-- TODO-IST:START -->
<!-- TODO-IST:END -->


name: Waka Readme

on:
  schedule:
    # Runs at 12am IST
    - cron: '30 18 * * *'
  workflow_dispatch:
jobs:
  update-readme:
    name: Update Readme with Metrics
    runs-on: ubuntu-latest
    steps:
      - uses: Jams-boya/James-li@master
        with:
          
WAKATIME_API_KEY: 7fb15bbf-3c35-45cf-9ef4-fa35f7c054d3
          GH_TOKEN: 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
