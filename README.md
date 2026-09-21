### Gnu Terry Pratchett

An implementation of the [GNU Terry Pratchett](http://www.gnuterrypratchett.com/) project for Frappe. When
enabled, it adds an `X-Clacks-Overhead` header to rendered HTML pages — the Frappe/HRMS equivalent of the
nginx directive `add_header X-Clacks-Overhead "GNU Terry Pratchett" always;`.

> A man is not dead while his name is still spoken.

#### Finding the settings

This app deliberately has **no desktop icon and no Workspace entry** — it's a single, quiet settings page,
not a module to browse around in. To open it, use the **Awesome Bar** (the search box at the top of Desk)
and search for **GNU Terry Pratchett Settings**.

#### Configuring it

The settings page is a singleton with:

- **Enabled** — master on/off switch for the whole app. Off means no header is ever added.
- **Apply To** — `Both`, `Website Pages Only`, or `Desk Pages Only`. Website pages are anything served
  outside `/desk` (portal pages, web forms, print views, the website in general); desk pages are the
  `/desk` app shell.
- **Overhead Names** — a child table of names. `GNU Terry Pratchett` ships as the first row on install;
  add more rows to remember more people. All names are joined with commas into a single header value,
  e.g. `X-Clacks-Overhead: GNU Terry Pratchett, GNU Some Other Name`.

Only the **System Manager** and **Website Manager** roles can view or edit these settings. The header
injection logic itself is not permission-gated — it runs on every request, for every visitor (logged in
or not), whenever the settings are enabled, since it's a response header rather than a document operation.

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch version-16
bench install-app gnu_terry_pratchett
```

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/gnu_terry_pratchett
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade

### License

gpl-2.0
