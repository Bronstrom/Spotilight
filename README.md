# Spotilight

The goal of Spotilight is to empower Spotify users with robust options to create and manage their own playlists, and discover more about their own music
listening history on Spotify.

## Technical Decisions

Spotilight is a web application that authentificates with and retrieves data from the
[Spotify Web API](https://developer.spotify.com/documentation/web-api).

The client/front-end wis built with Vue.js. This framework comes in handy with it's flexibility in integration. 
Vue.js' high interactivity can be utilized to create a Single Page-Application (SPA), handling data updates to content
on the screen without requiring for the whole page to be reloaded. On top of Vue.js, Bootstap is implemented to
quickly spin-up styling on the front-end and make use of it's modular UI components.

Flask will be used for communication between the front-end and the Spotify API. Originally, I had though of making Spotify
API calls directly from the front-end, although this poses as a security risk - such as exposing `oath` and the
`access_token` header to the client. With back-end operations being fairly small-scale, a lightweight web framework,
like Flask, fits well.

## Workflow

Despite being spearheaded by a single developer and a one-man team, the intial Spotilight application was run from an 
Agile / Scrum mindset. Issue tracking was a major focus of this project to stay organized to meet deadlines. Sprints
were held weekly from January to April consistently. Issues were refined, planned, and added to each sprint before or
at the start of a sprint.

Project development launched on January, 31st 2024 with the first sprint (Sprint 0) being focused on research and setting-up
the project in Github and ended on April, 2nd 2024 with the final sprint (Sprint 8) which completed the major intended
funcationality in the application. The project view outlines the progress of tasks on the
["Current Sprint" tab](https://github.com/users/Bronstrom/projects/1/views/1), the list of uncompleted tasks remain in the
["Backlog"](https://github.com/users/Bronstrom/projects/1/views/2), and the
["Roadmap" tab](https://github.com/users/Bronstrom/projects/1/views/3) shows the progress of major feature stories and
overarching epics. Milestones were capitalized on to capture larger scoped progress goals.

## Challenges & Lessons Learned
As a single developer, the pacing of the project kept me at a good pace and I was able to reach my deadline goals.
I mocked up user stories and epics early in development, and divvy up tasks in the backlog prior to the beginning of a sprint. 
I was also able to take advantage of some automation, such as issue templates for the projects and an ease to add new issues
directly to the project with generated metadata. Throughout the project I had found myself ahead of schedule, and thinking
"Oh I could do another task this Sprint." I was better at estimating my velocity towards the end of the sprint. I started by
placing down the initial infrastructure earlier in the project, starting with authentication and then handling the playlist
and metrics pages. There was a week or two where I knew work was going to drag (due to vacation) and I was able to foresee
this and plan ahead by giving myself less development heavy tasks and focus on documentation.

I found the authentication piece to be a bit of a challenge - I hadn't worked with many authentication platforms before and
this project opened me up to JWT and Bearer tokens. There were a few questions I needed to ask to get me where I wanted to be
with the persistence piece: "how should I best store these tokens?" "Should it be local or session storage in the browser?"
"Should I use a library and store it on the Flask server?" "Should I also use a refresh token?"

I also did feel like there were some challenges with limits on Spotify that I hadn't perceived until later into the development
process. Writing a genre algorithm was difficult as not every song provides a genre, instead I had to rely on the artist's genre.
Sub-genres are not a concept to Spotiy's Web API, and I came up with an algorithm that categorizes artist's genre's into smaller
sub-categories. The term length was also a tad bit of a challenge to work with Spotify's API. Spotify only gives short-term
(4 weeks) medium term (6 months) and long-term (3+ years) length timeframes. I just had to work with what Spotify gave me here
in order to show accurate metrics.

## Going Forward
I ended up going to a music concert earlier this year in the spring and found myself with a desire to add some extra automation
to this tool. I added the ability to search and add an artist's top songs. I consider adding additional features just like this
that makes playlist creation easier and with myself being a bit of an indie-head, I could see myself adding additional features
to help me explore underrated music and new artists.

I'm also a huge fan of Discover Weekly, so maybe I could make some sort of spin off of that for this app. I also want to refine
some of my algorithms and improve on them in the application. The genre algorthim could use some work to improve it and I'm
excited to return to it at some point.
