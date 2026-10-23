# Hello, World! Static Web Page

A minimalist static web page that displays a standard 'Hello, World!' greeting to unauthenticated public visitors with responsive layout and instantaneous load times.

## Prerequisites & Tooling
- **Runtime:** Node.js (v16+ recommended) and npm.
- **Browser:** Any modern web browser (Chrome, Firefox, Safari, Edge).

## 1. Clone & Install Dependencies
Open a terminal, clone the repository (or navigate to the project root directory), and install dependencies:
```bash
npm install --no-package-lock
```

## 2. Environment Setup
No external environment variables or backend secrets are required.
A sample `.env.example` file is provided for reference:
```bash
cp .env.example .env
```
* `PORT`: Default local port for serving static files (safely defaults to `3000`).

## 3. Database / External Services
- None required (Stateless static HTML/CSS application).

## 4. Running the Application
Start the local development server:
```bash
npm start
```
* Open 1 terminal window.
* Open your web browser and navigate to `http://localhost:3000`.
* Verify that the page loads instantly and displays the centered heading **"Hello, World!"**.

## 5. Testing & Building
Execute the automated test suite:
```bash
npm test
```
Build command (no-op for static assets):
```bash
npm run build
```

## 6. Troubleshooting
- **Port 3000 occupied:** If another application is using port 3000, start the server on a different port using `npx serve . -l 4000`.
- **Missing dependencies:** Run `npm install --no-package-lock` to ensure local static serving utilities are installed.