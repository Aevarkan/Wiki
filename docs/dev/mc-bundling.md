# Bundling

Made with reference from [Jayly's article](https://jaylydev.github.io/posts/bundle-minecraft-scripts-esbuild/).

This tutorial assumes you are familiar with the general process of making add-ons for Minecraft: Bedrock Edition. If you are not, have a look at the community [wiki](https://wiki.bedrock.dev/guide/introduction), especially the [Script API](https://wiki.bedrock.dev/scripting/scripting-intro) section.

Examples given for the command line assume you are using either Windows PowerShell, or command prompt.

I do not recommended following this tutorial on an Android device. You **will** struggle to follow this tutorial on a mobile device if you are not experienced.

## Minecraft's Scripting Sandbox

Minecraft: Bedrock Edition's Script API is sandboxed. This means you can only import from a select few modules.

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

    For a complete list, see [Microsoft's documentation](https://learn.microsoft.com/en-us/minecraft/creator/scriptapi/?view=minecraft-bedrock-experimental).

    Using experimental modules will require you to enable the `Beta APIs` experiment.

</details>

<details>
    <summary>Unsupported Modules</summary>

    There are few `@minecraft` modules that are not included in the sandbox:
    - `@minecraft/math`
    - `@minecraft/vanilla-data`

    The vast majority of packages are not in the `@minecraft` namespace, `command-wrapper` being one of them. These are not included in the sandbox either.

</details>

## Bundling Process

Bundling, as you might've guessed from the name, is the process of including outside modules into the final script file.

Say you have an `import` statement from `command-wrapper`.

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

There will no longer be an error for trying to import from `command-wrapper`, as its imports will become part of your add-on's code.

<details>
    <summary>All The Way Down</summary>


</details>

## ESBuild

Esbuild is one of many bundlers. As it's simple and fast, we'll use it for this tutorial.

---

We will need to tell the bundler a few things:
- Where to begin looking for files to bundle, the entry file
- Whether the bundle should be in a single file or many
- What format of JavaScript to output the bundle in
- Where to put the output
- What modules are already built-in

You should be familiar with what an entry file is, even if you haven't used a bundler before.

In your `manifest.json` file, you'll already have something like this:

```json
"entry": "scripts/main.js"
```

In a similar fashion, assuming your entry file is called `main.ts`, and is in a directory named `src`, you'll have

```js
entryPoints: "src/main.ts"
```

---

Let's put everything into one file, because why not.

```js
bundle: true
```

The Script API only supports a `format` called `esm`. So, we will need to tell esbuild to output in that format.

```js
format: "esm"
```

Let's put the output file in a directory called `scripts`, and call it `main.js`.

```js
outfile: "scripts/main.js"
```

Likely, this'll match the `entry` in your `manifest.json`.

---

Now, this one is a bit confusing. Modules *built into* the sandbox are *external*.

```js
external: [
    "@minecraft/server",
    "@minecraft/server-ui"
]
```

If you're using `@minecraft/server-admin`, `@minecraft/server-net`, or another built-in module, then you'd also include them here.

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

<details>
    <summary>The First Line</summary>
    
    You may have noticed I added `const { build } = require("esbuild");` without any explanation.

    Remember when I said the Script API only supports `esm` formatted code? That `require()` statement you're seeing there does the same thing as `import`, but in CommonJS syntax, the *other* major format[^1].

    Scripts made for Node.js, which you'll get to know in the next section, are mostly written in CommonJS.
</details>

[^1]: CommonJS and ECMAScript (shortened to `esm`) are the two major formats, but there are a few more apart from them. I'll leave you to explore them on your own.

In plain terms, you're telling esbuild to `build` your project according to a few specifications.

Esbuild is to `bundle` your project, starting from a file named `main.ts` in the `src` directory, using `esm` syntax, and then ouput it to a single file (`bundle`) called `main.js` in the `scripts` directory.

If it sees an import from `@minecraft/server`, or `@minecraft/server-ui`, then it must not change them.

If an error happens, `catch` it, and stop (`exit`) with code `1`[^2].

[^2]: In case you're curious, every time a process stops, it exits with a code. By convention, an exit code of `0` means the process stopped normally. An exit code of anything other than `0` means it did *not* stop normally.

### Installing Node

You might be wondering how to actually run esbuild. That's a good question.

NodeJS, and its package manager npm, is one way[^3].

[^3]: If you're so inclined, you can use a different package manager such as [Yarn](https://yarnpkg.com), [Bun](https://bun.com), or [pnpm](https://pnpm.io). However, there may be slight differences that prevent you from following this tutorial.

---

If you haven't already installed Node and npm, then do so by following the guide on the [Node.js website](https://nodejs.org/en/download).

In your command line, PowerShell on Windows, you should be able to type `npm -v`, and get a version number.

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

Your exact version numbers will very likely vary.

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

### Cruising The Command Line

[Earlier](#installing-node), you had a small taster of the command line, installing Node and npm.

From now on, we'll really have to get our hands dirty. The rest of this tutorial **exclusively** uses the command line.

---

Go to your project directory using the `cd` command.

For example, to navigate to a directory named `My Addon` inside of another directory called `Projects`, which is itself inside in the `D:` drive, you'd do the command

```ps1
cd /D "D:\Projects\My Addon"
```

This directory, `My Addon`, needs to contain `package.json`. If it doesn't, then you are not in the right place.

<details>
    <summary>Check With A Command</summary>

    Use the command `ls` to display the contents of your current directory. If you are not using PowerShell, then `dir` will do the same thing.

</details>    

---

Install the packages defined in `package.json` by running the command

```sh
npm install
```

You should see a directory named `node_modules` appear. Inside, you will find the modules you've defined in `dependencies` or `devDependencies`.

---

If you've copied [my configuration](#final-node-configuration), then you might want to run

```sh
npm update
```

As it's unlikely the versions shown in this tutorial are up to date.

<details>
    <summary>A Small Caveat</summary>

    Running `npm update` will not incremement major versions. For example, `typescript` version `5.8.2` will not update to `6.0.0`, but will update to `5.9.0`.

    You can install a specific version by adding `@x.y.z` at the end of the command. `x`, `y`, and `z` being placeholders for version numbers.

    For example, if you want to install version `2.1.0` of `@minecraft/server`, then run `npm install @minecraft/server@2.1.0`.

    See the [official npm documentation](https://docs.npmjs.com/cli/configuring-npm/package-json) for more detail.

</details>

### Running The Bundler

:::danger[STOP AND CHECK]

Before you run the next command. Ensure your `scripts` directory, or whichever directory you've set in `outfile`, is either empty, or not created.

Esbuild will **overwrite** files in that directory.

:::

At very last, we'll run esbuild with[^4]

[^4]: The astute among you will have spotted that `npm run build` simply runs `node esbuild.config.js`. Indeed, running either command will work.

```sh
npm run build
```

If your `outfile` and `bundle` parameters are the same as [mine](#final-configuration), then you'll find that a *single* file named `main.js` has appeared in the `scripts` directory.

---

Well done, you've now bundled an outside library into your add-on. If you've followed through and understood the process, then you should be able to take things from here.

This concludes the tutorial.

## Further Reading

This tutorial mainly covered the core process of bundling. You may find the following links useful:

- [Jayly's article](https://jaylydev.github.io/posts/bundle-minecraft-scripts-esbuild/) goes into more detail regarding edge cases

- Esbuild's [API documentation](https://esbuild.github.io/api/)

- Npm's `package.json` [documentation](https://docs.npmjs.com/cli/configuring-npm/package-json)

- [Semantic versioning](https://semver.org/), which is used by the vast majority of software projects
