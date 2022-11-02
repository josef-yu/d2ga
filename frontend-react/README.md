This is a [Next.js](https://nextjs.org/) project bootstrapped with [`create-next-app`](https://github.com/vercel/next.js/tree/canary/packages/create-next-app).

---

## Setup

To set up and run the project you will need to have [node](https://nodejs.org/en/) version 18.6.0.

### `Node installation via NVM`

If you want to change between node versions easily, you can install NVM command in your machine (for [windows](https://github.com/coreybutler/nvm-windows), for [POSIX systems](https://github.com/nvm-sh/nvm)); otherwise, you can use the installer from [node](https://nodejs.org/en/) directly and skip to [`Run npm install`](#run-npm-install).

#### `Run nvm install versionNumber`

To install node with nvm, run `nvm install versionNumber`.

#### `Run nvm use versionNumber`

To view if the node version is properly installed, run `nvm list` to view the list of all installed node versions. Afterwards, you can now run `nvm use versionNumber`.


---

### `Run npm install`

While in the project directory in a terminal of your choice, run `npm install` to install the node modules needed for the project to run.

---

### `Run npm run dev`

After installation of the node modules of the project, run `npm run dev` to run the react web app in development mode.

If in case an error of port is already in use, edit the `.env` file in the root directory of the project. Insert a new line of code as follows: `export PORT=portNumber`. Then re run the project with the command mentioned.

---

### Linting

The project uses `prettier` and `eslint` for the linting and formatting of the code. You can install the extensions in vscode. 

Make sure to setup `prettier` to use tabs for spacing and quotes to single quotes. You can do this via `File > Preferences > Settings > Search prettier` and do the said necessary changes. You can also run the linting command `npm run lint` to check the whole codebase right away.

---
## Project Structure

The web app uses reactjs. There is a `components` folder for anything that isn't supposed to show up on the actual website.

Use the `assets` folder for images, assets and mockup data.

The project mainly uses [material-ui](https://material-ui.com/) library for the UI components. The styling for components made by `material-ui` is made with [`makeStyles`](https://material-ui.com/styles/basics/) function with the base implementation of the theme located at `frontend-react/styles/theme.js`

#### Folder Structure
```
├───frontend-react
    ├───api
    ├───components
    ├───constants
    ├───pages
    ├───public
    ├───styles
    ├───utilities
```

Folders and files explanation:

- `frontend-react` => stores all frontend files
- `api` => stores all api calls separated by controllers
- `components` => stores all reusable react components
- `constants` => stores all project constants paired with the context provider located at `src/context` folder
- `pages` => stores all the pages and sub pages of the app
- `public` => stores all the static assets of the app. You can reference this directly as the starting directory of the source
- `styles` => stores all styling in JSS (CSS in JS)
- `utilities` => stores all the [custom hooks](https://reactjs.org/docs/hooks-custom.html) and [theme](https://material-ui.com/customization/theming/) of the project

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js/) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/deployment) for more details.
