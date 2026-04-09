# README

## Introduction

A site to plan races with friends.

Plan the running races you want to do, either marking yourself as interested or going. Set targets and record how you did. Add friends and sign up to races with them. Manage your profile, restricting access to personal details and making the experience nicer.

![Alt text](race-planner.png?raw=true "site")

## Getting started

The settings are currently pointing to the dev.py. In the dev environment emails are sent to the console. The production environment was setup originally to deploy to Heroku but needs re-testing. The production environment also requires environment variables.

We are using a Postgres database, once this is installed run:
```
python manage.py migrate
python manage.py runserver
```

The emails are queued using Redis:
https://redis.io/docs/latest/operate/oss_and_stack/install/archive/install-redis/

The queue requires us to start a worker for email:
```
python manage.py rqworker email
```

Insert some distances for the dropdown:
```
insert into main_distance (description) values ('10k');
insert into main_distance (description) values ('10 Mile');
insert into main_distance (description) values ('Half Marathon');
insert into main_distance (description) values ('Marathon');
```

## The pages

### Create an account and login

*Create an account*
![Create an account](screenshots/create-account.png)

Once you have created an account (note registration confirmation email sent to console in dev environment) you can login.

*Login screen*
![Login screen](screenshots/login-screen.png)

### User menu

*User menu*
![User menu](screenshots/user/user-menu.png)

*User profile*
![User profile](screenshots/user/user-profile.png)

Here you can set your favourite distance.

*User settings*
![User settings](screenshots/user/user-settings.png)

A privacy setting and whether to default the distance dropdowns to your favourite distance.

### Races

*Races*
![Races](screenshots/races/races.png)

Here you can:
- See the available races, filter by distance and suggest a new race.
- Mark as being interested in or going to a race. This moves the race to the appropriate tab.

*Suggest Races*
![Suggest races](screenshots/races/suggest_a_race.png)

Suggestions are emailed (sent to console in dev environment) to be added.

### Interested

*Interested*
![Interested](screenshots/interested/interested.png)

Here you can either mark yourself as no longer interested (moves back to Races tab) or mark yourself as going.

### Going

*Going*
![Going](screenshots/going/going-notime.png)
![Going with target time](screenshots/going/going-time.png)

Shows the races you are going to. You can either choose to run for fun or set a target time.

### Completed

*Completed*
![Completed](screenshots/completed/completed.png)

Shows the races you have completed. Clicking on the name shows more details such as your time, whether any friends went e.t.c.

![Completed race details](screenshots/completed/completed-race-details.png)
![Completed race details with extra details](screenshots/completed/completed-race-details-extradetails.png)

### Friends

*Friends*
![Friends](screenshots/friends/friends.png)

Here you can add friends to see what they have entered (need their email address).

![Friend races](screenshots/friends/friends_races.png)

Here you also have the option to remove the friend.