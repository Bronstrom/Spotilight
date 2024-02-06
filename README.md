# Spotilight

The goal of Spotilight is to better create and manage your own playlists, as well as discover more about your music
listening history on Spotify through visualizations.

## Technical Decisions

Spotilight will be a CRUD app that makes calls to the Spotify API.

The client/front-end will be built with the Vue.js. Vue.js will come in handy with it's flexibility in integration. It's
high interactivity can also be utalized to create a Single Page-Application (SPA), handling data updates to content on the
screen without requiring for the whole page to be reloaded. which will be a great framework to use with it which is
flexiblity in integration.

Flask will be used for communication between the front-end and the Spotify API. Originally, I had though of making direct
Spotify API calls directly from the front-end, although this poses as a security risk - such as exposing `oath` and the
`access_token` header to the client. With back-end operations being fairly small-scale, I think a lightweight web framework,
like Flask will fit well.

## Workflow

Despite being spearheaded by a single developer and a one-man team, this project will be run from an Agile/SCRUM mindset.
Issue tracking will be a major focus of this project to stay organized and meet deadlines. Sprints will be held weekly with
issues to be refined, planned, and added to each sprint before or at the start of a sprint. Project development launched on
January, 31st 2024 with the first sprint (Sprint 0) being focused on research and setting-up the project in Github. The
project view will outline the progress of tasks on the "Current Sprint" tab, the list of uncompleted tasks in the "Backlog",
and the "Roadmap" tab shows the progress of storyies and overarching epics. Milestones will also be used to capture larger
scoped progress goals.

<!-- TODO: Add links above -->

## Challenges & Lessons Learned
