# Spotilight

The goal of Spotilight is to better create and manage your own playlists, as well as discover more about your music
listening history on Spotify.

## Technical Decisions

Spotilight will be a create, read, update, and delete (CRUD) app that makes calls to the
[Spotify Web API](https://developer.spotify.com/documentation/web-api).

The client/front-end will be built with Vue.js. This framework will come in handy with it's flexibility in integration. 
Vue.js' high interactivity can be utilized to create a Single Page-Application (SPA), handling data updates to content
on the screen without requiring for the whole page to be reloaded. On top of Vue.js, Bootstap will be implemented to
quickly spin-up styling on the front-end and make use of it's modular UI components.

Flask will be used for communication between the front-end and the Spotify API. Originally, I had though of making Spotify
API calls directly from the front-end, although this poses as a security risk - such as exposing `oath` and the
`access_token` header to the client. With back-end operations being fairly small-scale, I think a lightweight web framework,
like Flask, will fit well.

## Workflow

Despite being spearheaded by a single developer and a one-man team, Spotilight will be run from an Agile/SCRUM mindset.
Issue tracking will be a major focus of this project to stay organized and meet deadlines. Sprints will be held weekly with
issues to be refined, planned, and added to each sprint before or at the start of a sprint.

Project development launched on January, 31st 2024 with the first sprint (Sprint 0) being focused on research and setting-up
the project in Github. The project view will outline the progress of tasks on the
["Current Sprint" tab](https://github.com/users/Bronstrom/projects/1/views/1), the list of uncompleted tasks remain in the
["Backlog"](https://github.com/users/Bronstrom/projects/1/views/2), and the
["Roadmap" tab](https://github.com/users/Bronstrom/projects/1/views/3) shows the progress of major feature stories and
overarching epics. Milestones will also be capalized on to capture larger scoped progress goals.

## Challenges & Lessons Learned
