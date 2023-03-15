# math-discord

## Make LaTeX'ing easier in [Math Discord](https://discord.gg/math)
Do you like talking about math? Do you enjoying communicating with math symbols using the typesetting language LaTeX? Do you want Latex shortcuts in the math server? If you answered yes to all these questions, this repo is designed for you. You can produce compiled latex'd lessons ("factoids", denoted by its shortcut command `\.` before the factoid name) using a simple command of 

`,tex \.cts`

you get : 
<div align="center">
<img src="https://raw.githubusercontent.com/riemann-discord/math-discord/main/img/cts.png" alt="complete the square" height="400px"/>
</div>

<!-- ![complete the square](https://raw.githubusercontent.com/riemann-discord/math-discord/main/img/cts.png) -->

Or with 

`,tex \.double angle`

you get : 
<div align="center">
<img src="https://raw.githubusercontent.com/riemann-discord/math-discord/main/img/double-angle.png" alt="trig double angle identities" height="400px"/>
</div>

<!-- ![trig double angle identities](https://raw.githubusercontent.com/riemann-discord/math-discord/main/img/double-angle.png) -->

Here is a list of factoids:

`\.original`,
`\.algebra manipulation`,
`\.alg lesson`,
`\.alg manipulation`,
`\.alg manip`,
`\.algebra manip`,
`\.algebra lesson`,
`\.cross multiplication`,
`\.cross mult`,
`\.butterfly`,
`\.wrong reciprocal`,
`\.wrong recip`,
`\.wrong square root`,
`\.wrong root`,
`\.wrong fraction cancel`,
`\.wrong cancel`,
`\.wrong square`,
`\.freshman`,
`\.cts`,
`\.absolute value def`,
`\.absolute value`,
`\.abs def`,
`\.abs value`,
`\.quadratic formula`,
`\.exp rules`,
`\.log xp rule`,
`\.point slope`,
`\.law of sines`,
`\.law of sine`,
`\.sine law`,
`\.law of cosines`,
`\.law of cosine`,
`\.cosine law`,
`\.log rules`,
`\.sohcahtoa`,
`\.geom trig def`,
`\.double angle`,
`\.half angle`,
`\.sum diff trig`,
`\.recip trig`,
`\.reflect trig`,
`\.shift trig`,
`\.reflect shift trig`,
`\.sum2prod`,
`\.prod2sum`,
`\.rocket trig`,
`\.unit circle`,
`\.demoivre`,
`\.limit rules`,
`\.diff rules`,
`\.int rules`,
`\.FTC1`,
`\.FTC2`,
`\.integral area`,
`\.maclaurin`

### Use the preamble in [Math Discord](https://discord.gg/math):
1. Download [preamble.tex](https://github.com/riemann-discord/math-discord/blob/main/preamble.tex) to your local machine
2. Create your own server and invite [TeXit bot](https://top.gg/bot/510789298321096704) and go to any channel in your server
3. OR Go to [`#latex-testing`](https://discord.com/channels/268882317391429632/844681108473118750) or [`#latex-help`](https://discord.com/channels/268882317391429632/840667252793802752) channel in the Math Discord server
4. Upload `preamble.tex` that you downloaded in step 1. and type `,preamble --replace` in the same message.
5. Hit enter
6. Reply `y` to the message the bot sends to you to confirm your choice and wait
7. profit

The new factoids system is complete enough that it can probably be used now. Legacy interfaces have been provided so that it is still fully compatible with the old system. Currently, the list of all available factoids is not reported upon error; this is still WIP.

# A description of the new system

The new system works through the idea of "paths" under which factoids can be filed, much like a filesystem. Each factoid lives under a particular directory with a unique name within that directory.

## Factoid types

There are two types of factoids that can be created.

1. The first is a standard factoid which lives under a particular folder in the filesystem. It is associated with a unique name within the folder it lives in, and has a definition body which when the factoid is activated will be run by LaTeX.
2. The second is a factoid "bundle". It is a folder of bundle "entries" which are each individually a factoid that can be invoked. But the factoid bundle can also be invoked, which will display the entire bundle at once.

## The user interface

### Path specification

A path can be specified through a list of path components separated by the path separator `/`, where a path component can be any sequence of characters accepted by LaTeX (it would be best to keep this to characters with category code 10, 11, or 12). This can look like:

- `trig/pythag`
- `calc/diff/chain rule`
- etc.

A path can also optionally start with the component `.`, in which case `.` will be replaced by the current "default path prefix". This is empty to begin with, but can be set by the user using the following commands:

- `\PushDefaultFactoidPath{<path>}`: Sets the current default path prefix to `<path>`. To set the new default path prefix relative to the current one, prefix the `<path>` with `./`. Must be matched by a following `\PopDefaultFactoidPath`.
- `\PopDefaultFactoidPath`: Resets the default path prefix to what it was previously.

The intended usage looks something like

```latex
\PushDefaultFactoidPath{<path>}
  % do some stuff ...
\PopDefaultFactoidPath
```

### Factoid creation

Currently, the only type of factoid creation supported is creating new factoids which do not yet exist. Trying to create a factoid which already exists will result in an error.

The available commands are:

- `\NewFactoid{<path>}{<code>}`: Creates a new factoid located at `<path>` with code `<code>`.
- `\NewFactoidBundle{<bundle path>}{<bundle specification>}`: Creates a new factoid bundle located at `<path>` according to the `<bundle specification>`.

Within the bundle specification, the following commands are available:

- `\NewPreamble{<code>}`: Defines the "preamble" for the bundle, which gets inserted before the whole bundle code.
- `\NewInteramble{<code>}`: Defines the "interamble" for the bundle, which gets inserted between each bundle entry.
- `\NewPostamble{<code>}`: Defines the "postamble" for the bundle, which gets inserted after the whole bundle code.
- `\NewEntry{<relative entry path>}{<code>}`: Defines a bundle entry located at `<bundle path>/<relative entry path>` with code `<code>`.

An example of creating a factoid bundle looks like

```latex
\NewFactoidBundle{trig/reflect}{
  \NewPreamble{\begin{align*}}
  \NewInteramble{\\}
  \NewEntry{sin}
    {\sin(-\theta) & = -\sin\theta}
  \NewEntry{cos}
    {\cos(-\theta) & =  \cos\theta}
  \NewEntry{tan}
    {\tan(-\theta) & = -\tan\theta}
  \NewPostamble{\end{align*}}
}
```

which creates an `align*` environment of the trig reflection identities.

The entire bundle is accessed via the path `<bundle path>`. The individual entries of a bundle are accessed via the path `<bundle path>/<relative entry path>`.

### Factoid invocation

Factoids can be invoked by the following commands:

- `\Factoid{<path>}`: invokes the factoid at path `<path>`.
- `\FactoidFuzzy{<path>}`: tries to invoke a factoid at path `<path>`, and failing that, does a "fuzzy" search algorithm for factoids whose path has a suffix which matches the `<path>` provided. If a unique match is found, then that factoid will be invoked instead. But if multiple matches are found, then the invocation will fail (use a more specific suffix).
- `\. <path> <newline>`: alias to `\FactoidFuzzy`. This is a convenience macro and must be done on its own line, as it will try to capture everything up until the end of the line as its argument.

### Legacy interface

The following commands have been defined for compatibility reasons.

- `\DeclareFactoid{<path>}{<code>}`: alias to `\NewFactoid`.
- `\factoid{<path>}`: alias to `\Factoid`.


### Preamble Contributions:
1. Fork the repo
2. Open the repo from your account. The URL will be something like

    `https://github.com/<your_username>/math-discord/blob/main/preamble.tex`

3. Add your code to `preamble.tex` file from the GitHub user-interface.
4. Go back to 
    [https://github.com/riemann-discord/math-discord/edit/main/preamble.tex](https://github.com/riemann-discord/math-discord/blob/main/preamble.tex)
5. Click button that says "Make a Pull Request"
6. profit

Credit to
@snow (夢雪#2250), Mehdi_Moulati#1210, Toby#2275, RokettoJanpu#6002
for your contributions.
