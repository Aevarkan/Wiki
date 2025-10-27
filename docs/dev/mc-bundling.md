# Bundling

Made with reference from [Jayly's article](https://jaylydev.github.io/posts/bundle-minecraft-scripts-esbuild/).

This tutorial assumes you are familiar with the general process of making add-ons for Minecraft: Bedrock Edition. If you are not, have a look at the community [wiki](https://wiki.bedrock.dev/guide/introduction), especially the [Script API](https://wiki.bedrock.dev/scripting/scripting-intro) section.

## The Script Sandbox

Minecraft: Bedrock Edition's Script API is sandboxed. This means you can only import from a small number of modules.

For example, you can import from `@minecraft/server`, but not from `command-wrapper`.

```typescript
import { system } from "@minecraft/server";
import { defineCommand } from "command-wrapper";
```

If you try importing from a module like `command-wrapper` without bundling, you will get an error when loading your add-on pack.

<details>
    <summary>Supported Modules</summary>

    These modules are built-in to the sandbox:
    - `@minecraft/server`
    - `@minecraft/server-ui`
    - `@minecraft/server-admin` (experimental)
    - `@minecraft/server-net` (experimental)

    For a complete list, see [Microsoft's documentation](https://learn.microsoft.com/en-us/minecraft/creator/scriptapi/minecraft/server/minecraft-server?view=minecraft-bedrock-experimental).

    Using experimental modules will require you to enable the `Beta APIs` experiment.

</details>

<details>
    <summary>Unsupported Modules</summary>

    There are also a few `@minecraft` modules that are not included in the sandbox:
    - `@minecraft/math`
    - `@minecraft/vanilla-data`

    Of course, packages without `@minecraft` in their name, such as `command-wrapper`, are not included.

</details>

## Bundling Process

Bundling, as you might've guessed from the name, is the process of including outside modules into the final script file.

For example, see what happens to an import from `command-wrapper`.

```typescript
import { defineCommand } from "command-wrapper";

const smiteCommand = defineCommand({
    // not relevant
})
```

Bundling will result in something like this.

```typescript
function defineCommand(command) {
    return command;
}

const smiteCommand = defineCommand({
    // not relevant
})
```

## ESBuild

Esbuild is one of many bundlers. As it's simple and fast, we'll use it for this tutorial.

---

We will need to tell the bundler a few things:
- What format to output our code in
- Whether the bundle should be in a single file or many
- Where to put the output
- What modules are already built-in

The Script API only supports a format called `esm`. So, we will need to tell esbuild to output in that format.

```js
format: "esm"
```

Let's put everything into one file, because why not.

```js
bundle: true
```

Let's put the output file in a directory called `scripts`, and call it `main.js`.

```js
outfile: "scripts/main.js"
```

---

You should be familiar with what an entry file is, even if you haven't used a bundler before.

You likely already have something like this in your `manifest.json` file:

```json
"entry": "scripts/main.js"
```

In a similar fashion, assuming your entry file is called `main.ts`, and is in a directory named `src`, you'll have

```js
entryPoints: "src/main.ts"
```

---

Now, this one is a bit confusing. Modules *built into* the sandbox are *external*.

```js
external: [
    "@minecraft/server",
    "@minecraft/server-ui"
]
```

If you were using them, you'd also put `@minecraft/server-admin` and `@minecraft/server-net` here.

### Final Configuration

The final configuration is something like this, although yours will vary slightly depending on how your project is set up.

Name this file `esbuild.config.js` for later.

```js
const { build } = require("esbuild");

build({
    entryPoints: "src/main.ts",
    bundle: true,
    format: "esm",
    outfile: "scripts/main.js",
    external: [
        "@minecraft/server",
        "@minecraft/server-ui"
    ],
}).catch(() => process.exit(1));
```

You may have noticed I added `const { build } = require("esbuild");` without an explanation.

Remember when I said the Script API only supports `esm` formatted code? That `require()` statement you're seeing there does the same thing as `import`, but in CommonJS syntax, the *other* major format[^1].

[^1]: CommonJS and ECMAScript (shortened to `esm`) are the two major formats, but there are a few more apart from them. I'll leave you to explore them on your own.

Scripts made for Node.js, which you'll get to know in the next section, are commonly written in CommonJS.

---

In plain terms, you're telling esbuild to `build` your project according to a few specifications.

Esbuild is to `bundle` your project, starting from a file named `main.ts` in the `src` directory, format it in `esm`, and put it in a single file (`bundle`) called `main.js` in the `scripts` directory.

If it sees an import from `@minecraft/server`, or `@minecraft/server-ui`, then it must not change them.

If an error happens, `catch` it, and stop (`exit`) with code `1`[^2].

[^2]: In case you're curious, every time a process stops, it exits with a code. By convention, an exit code `0` means the process stopped normally. An exit code of anything other than `0` it did *not* stop normally.

### Installing Node

You might be wondering how to actually run esbuild. That's a good question.

NodeJS, and its package manager npm, is one way to do it[^3].

[^3]: If you're so inclined, you can use a different package manager such as [Yarn](https://yarnpkg.com), [Bun](https://bun.com), or [pnpm](https://pnpm.io), but I won't be responsible for any errors you get there.

---

If you haven't already, install them from the [Node.js website](https://nodejs.org/en/download).

In your commandline, you should be able to type `npm -v`, and get a version number.

```sh
node -v
v22.14.0

npm -v
11.6.1
```

If you get something like the above, then you've installed Node.js and npm successfully.

### Configuring Node

This next section may feel like we're doing steps backwards. As we're using npm just to *install* packages, and not *publishing* them, this is expected.

---

Npm uses a file called `package.json` to store data for a project. 

Now, our built-in modules are `@minecraft/server` and `@minecraft/server-ui`.

```json
"dependencies": {
    "@minecraft/server": "^2.2.0",
    "@minecraft/server-ui": "^2.0.0"
}
```

We're using the outside module `command-wrapper`, and are using `esbuild` to bundle it. The project, hopefully, is in `typescript`.

```json
"devDependencies": {
    "command-wrapper": "^0.1.1",
    "esbuild": "^0.25.11",
    "typescript": "^5.8.2"
}
```

Your exact version numbers will likely vary.

---

To `build` the project, we need `node` to run `esbuild.config.js`, the configuration file from [before](#final-configuration).

```json
"scripts": {
    "build": "node esbuild.config.js"
}
```

#### Final Node Configuration

You'll end up with a `package.json` file that looks like the one below.

```json
{
  "scripts": {
    "build": "node esbuild.config.js"
  },
  "dependencies": {
    "@minecraft/server": "^2.2.0",
    "@minecraft/server-ui": "^2.0.0"
  },
  "devDependencies": {
    "command-wrapper": "^0.1.1",
    "esbuild": "^0.25.11",
    "typescript": "^5.8.2"
  }
}
```

### The Commandline

To go any further, we'll need to use the commandline. In Windows, this is Powershell, or cmd.

---

Go to your project directory using the `cd` command.

As an example, to navigate to a a directory named `My Addon` that's inside of `Projects`, which is in the `D:` drive, you'd do the command

```ps1
cd /D "D:\Projects\My Addon"
```

This directory, `My Addon`, needs to contain `package.json`. If it doesn't, then you are not in the right place.

---

Install the packages defined in `package.json` by running the command `npm install`. You should see a directory named `node_modules` appear.

If you've copied my configuration, then you might want to run `npm update`, as it's unlikely the versions shown in this tutorial are the latest ones.

If you, for example, want to specifically install version `2.1.0` of `@minecraft/server`, then run the command `npm install @minecraft/server@2.1.0`.

### Running The Bundler

At very last, you can run esbuild using the command[^4]

[^4]: The observant ones among you will have spotted that `npm run build` simply runs the command `node esbuild.config.js`. Running either command will work.

```sh
npm run build
```

If your `outfile` and `bundle` parameters are the same as [mine](#final-configuration), then you'll find that a file named `main.js` has appeared in the `scripts` directory.

---

Well done, you've now bundled an outside library into your add-on. If you've followed through and understood the process, then you should be able to take things from here.

This concludes the tutorial.
