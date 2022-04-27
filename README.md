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
          
