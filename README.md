> [!CAUTION]
> This repository version of Wattle is not yet suitable for production use. Features may be incomplete, untested, or subject to breaking changes without notice.

# Project Overview

![CI](https://github.com/nickjj/docker-django-example/workflows/CI/badge.svg?branch=main)

The Wattle Cloud Platform is designed to simplify the process of searching for properties and purchasing associated certificates. Users can input parcel details, view matching property assessments, select certificates (including urgent options), provide contact information, and make payments via Stripe.

## Table of contents

- [Features](#features)
- [Running this app](#running-this-app)
- [Model Setup](#model-setup)
- [Files of interest](#files-of-interest)
  - [`.env`](#env)
  - [`run`](#run)
- [Updating dependencies](#updating-dependencies)
  - [In development](#in-development)
  - [In CI](#in-ci)
  - [In production](#in-production)
- [How Does Testing Work](#how-does-testing-work)
- [Monitoring](#monitoring)

## Features

- Property search and certificate purchase
- Order management for certificates
- Stripe payment integration
- Detailed user flows for parcel search and order fulfilment
- Infrastructure setup and testing commands

## Running this app

You'll need to have [Docker installed](https://docs.docker.com/get-docker/).
It's available on Windows, macOS and most distros of Linux. If you're new to
Docker and want to learn it in detail check out the [additional resources
links](#learn-more-about-docker-and-django) near the bottom of this README.

You'll also need to enable Docker Compose v2 support if you're using Docker
Desktop. On native Linux without Docker Desktop you can [install it as a plugin
to Docker](https://docs.docker.com/compose/install/linux/). It's been generally
available for a while now and is stable. This project uses specific [Docker
Compose v2
features](https://nickjanetakis.com/blog/optional-depends-on-with-docker-compose-v2-20-2)
that only work with Docker Compose v2 2.20.2+.

If you're using Windows, it will be expected that you're following along inside
of [WSL or WSL
2](https://nickjanetakis.com/blog/a-linux-dev-environment-on-windows-with-wsl-2-docker-desktop-and-more).
That's because we're going to be running shell commands. You can always modify
these commands for PowerShell if you want.

#### Clone this repo anywhere you want and move into the directory:

```sh
git clone https://github.com/wattlehq/mimosa.git mimosa
cd mimosa

# Optionally checkout a specific tag, such as: git checkout 0.10.0
```

#### Copy an example .env file because the real one is git ignored:

```sh
cp .env.example .env
```

#### Build everything:

_The first time you run this it's going to take 5-10 minutes depending on your
internet connection speed and computer's hardware specs. That's because it's
going to download a few Docker images and build the Python + Yarn dependencies._

```sh
docker compose up --build
```

Now that everything is built and running we can treat it like any other Django
app.

Did you receive a `depends_on` "Additional property required is not allowed"
error? Please update to at least Docker Compose v2.20.2+ or Docker Desktop
4.22.0+.

Did you receive an error about a port being in use? Chances are it's because
something on your machine is already running on port 8000. Check out the docs
in the `.env` file for the `DOCKER_WEB_PORT_FORWARD` variable to fix this.

Did you receive a permission denied error? Chances are you're running native
Linux and your `uid:gid` aren't `1000:1000` (you can verify this by running
`id`). Check out the docs in the `.env` file to customize the `UID` and `GID`
variables to fix this.

#### Setup the initial database & infrastructure:

```sh
# You can run this from a 2nd terminal.
./run manage migrate
```

Start the Stripe webhook service, copy and paste webhook secret into .env,
then stop.

```sh
docker-compose up stripe
```

Create a new admin super user.

```sh
./run manage createsuperuser
```

_We'll go over that `./run` script in a bit!_

#### Check it out in a browser:

Visit <http://localhost:8000> in your favorite browser.

#### Linting the code base:

```sh
# You should get no output (that means everything is operational).
./run lint
```

#### Sorting Python imports in the code base:

```sh
# You should see that everything is unchanged (imports are already formatted).
./run format:imports
```

#### Formatting the code base:

```sh
# You should see that everything is unchanged (it's all already formatted).
./run format
```

_There's also a `./run quality` command to run the above 3 commands together._

#### Running the test suite:

```sh
# You should see all passing tests. Warnings are typically ok.
./run manage test
```

#### Stopping everything:

```sh
# Stop the containers and remove a few Docker related resources associated to this project.
docker compose down
```

You can start things up again with `docker compose up` and unlike the first
time it should only take seconds.

## Model Setup

In order to deploy and run the Web Application successfully, you will need to setup a
few Models, particularly `Properties`, `Certificates` and `Fees`.

You can create instances of these models from within the Django Admin by browsing to the URL: http://localhost:8000/admin

## Files of interest

I recommend checking out most files and searching the code base for `TODO:`,
but please review the `.env` and `run` files before diving into the rest of the
code and customizing it. Also, you should hold off on changing anything until
we cover how to customize this example app's name with an automated script
(coming up next in the docs).

### `.env`

This file is ignored from version control so it will never be commit. There's a
number of environment variables defined here that control certain options and
behavior of the application. Everything is documented there.

Feel free to add new variables as needed. This is where you should put all of
your secrets as well as configuration that might change depending on your
environment (specific dev boxes, CI, production, etc.).

### `run`

You can run `./run` to get a list of commands and each command has
documentation in the `run` file itself.

It's a shell script that has a number of functions defined to help you interact
with this project. It's basically a `Makefile` except with [less
limitations](https://nickjanetakis.com/blog/replacing-make-with-a-shell-script-for-running-your-projects-tasks).
For example as a shell script it allows us to pass any arguments to another
program.

This comes in handy to run various Docker commands because sometimes these
commands can be a bit long to type. Feel free to add as many convenience
functions as you want. This file's purpose is to make your experience better!

_If you get tired of typing `./run` you can always create a shell alias with
`alias run=./run` in your `~/.bash_aliases` or equivalent file. Then you'll be
able to run `run` instead of `./run`._

#### Start and setup the project:

This won't take as long as before because Docker can re-use most things. We'll
also need to setup our database since a new one will be created for us by
Docker.

```sh
# Start the application.
docker compose up --build

# Then in a 2nd terminal once it's up and ready.
./run manage migrate
```

#### Sanity check to make sure the tests still pass:

It's always a good idea to make sure things are in a working state before
adding custom changes.

```sh
# You can run this from the same terminal as before.
./run quality
./run manage test
```

If everything passes now you can optionally `git add -A && git commit -m
"Initial commit"` and start customizing the app. Alternatively you can wait
until you develop more of the app before committing anything. It's up to you!

## Updating dependencies

Let's say you've customized the app and it's time to make a change to the
`requirements.txt` or `package.json` file.

Without Docker you'd normally run `pip3 install -r requirements.txt` or `yarn
install`. With Docker it's basically the same thing and since these commands
are in our `Dockerfile` we can get away with doing a `docker compose build` but
don't run that just yet.

#### In development:

You can run `./run pip3:outdated` or `./run yarn:outdated` to get a list of
outdated dependencies based on what you currently have installed. Once you've
figured out what you want to update, go make those updates in the
`requirements.txt` and / or `assets/package.json` file.

Then to update the dependencies you can run `./run pip3:install` or `./run
yarn:install`. That'll make sure any lock files get copied from Docker's image
(thanks to volumes) into your code repo and now you can commit those files to
version control like usual.

You can check out the
[run](https://github.com/nickjj/docker-django-example/blob/main/run) file to see
what these commands do in more detail.

As for the requirements' lock file, this ensures that the same exact versions
of every package you have (including dependencies of dependencies) get used the
next time you build the project. This file is the output of running `pip3
freeze`. You can check how it works by looking at
[bin/pip3-install](https://github.com/nickjj/docker-django-example/blob/main/bin/pip3-install).

You should never modify the lock files by hand. Add your top level Python
dependencies to `requirements.txt` and your top level JavaScript dependencies
to `assets/package.json`, then run the `./run` command(s) mentioned earlier.

#### In CI:

You'll want to run `docker compose build` since it will use any existing lock
files if they exist. You can also check out the complete CI test pipeline in
the [run](https://github.com/nickjj/docker-django-example/blob/main/run) file
under the `ci:test` function.

#### In production:

This is usually a non-issue since you'll be pulling down pre-built images from
a Docker registry but if you decide to build your Docker images directly on
your server you could run `docker compose build` as part of your deploy
pipeline.

## How Does Testing Work

There is a second `docker-compose.test.yml` file which duplicates the web
services to slightly change the configuration, eg: to destroy the database on
down. It also includes the stripe-mock service, which emulates the Stripe API so
that calls aren't actually persisted, but created in memory instead.

This means that tests are encapsulated into separate ephemeral services that are
spun up/down and destroyed when the tests are complete. This also means that the
testing suite is portable, it creates everything it needs in the Github action
pipeline and shouldn't need to reach out to external resources to run.

When the test commands start:

- Generate a .env.test if it doesn't exist
- Boot the services in docker-compose.test.yml
- Boot the Django tests
- Spin down and destroy the test services

## Monitoring

This project has been setup to optionally use Sentry for application monitoring.
Once `SENTRY_ENABLED` has been set to `True` and `SENTRY_DSN` has been
configured, events will start to propagate to Sentry.
