# CNCH App

Everything you need to build a Svelte project, powered by [`sv`](https://github.com/sveltejs/cli).

## Prerequisites

This project uses [pnpm](https://pnpm.io/) as the package manager. Make sure you have it installed:

```sh
npm install -g pnpm
```

## Environment Configuration

This project requires the following environment variable:

### `PUBLIC_API_BASE_URL`

The base URL for the backend API.

- **Default**: `http://127.0.0.1:8000/user`
- **Required**: No (uses default if not set)

#### Local Development Setup

Create a `.env` file in the project root:

```env
PUBLIC_API_BASE_URL=http://127.0.0.1:8000/user
```

#### Production Setup

For production deployments, set the environment variable to your API server:

```env
PUBLIC_API_BASE_URL=https://api.yourserver.com/user
```

## Creating a project

If you're seeing this, you've probably already done this step. Congrats!

```sh
# create a new project
pnpm dlx sv create my-app
```

To recreate this project with the same configuration:

```sh
# recreate this project
pnpm dlx sv create --template minimal --no-types --add prettier mcp="ide:vscode+setup:remote" tailwindcss="plugins:forms" --install pnpm cnch-app
```

## Developing

Once you've created a project and installed dependencies with `pnpm install`, start a development server:

```sh
pnpm run dev

# or start the server and open the app in a new browser tab
pnpm run dev -- --open
```

## Building

To create a production version of your app:

```sh
pnpm run build
```

You can preview the production build with `pnpm run preview`.

## Docker

This project includes a Dockerfile for containerized deployment.

### Building the Docker image

```sh
docker build -t cnch-app .
```

### Running the container

```sh
# Basic run (uses default API URL)
docker run -p 3000:3000 cnch-app

# With environment variables from .env file
docker run -p 3000:3000 --env-file .env cnch-app

# With inline environment variable
docker run -p 3000:3000 -e PUBLIC_API_BASE_URL=https://api.yourserver.com/user cnch-app

# With custom port
docker run -p 8080:3000 -e PUBLIC_API_BASE_URL=https://api.yourserver.com/user cnch-app
```

### Using Docker Compose

```sh
docker-compose up -d
```

> The app uses [@sveltejs/adapter-node](https://svelte.dev/docs/kit/adapter-node) for Node.js deployment.
