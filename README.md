
# Auto Practice Room

This repository contains a script that automatically reserves a practice room for me using a selenium browser automation script. The script is run on github actions every day at 1am to make a reservation one week in advance.

A separate script running in Google Apps Script polls my email for automatic reservation confirmation emails and adds a corresponding event into my google calendar.

Running selenium in github actions uses a setup based on <https://github.com/jsoma/selenium-github-actions>
