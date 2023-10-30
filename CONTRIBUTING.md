# Contributing to platechain

Thanks for contributing to open science! We welcome contributions from everyone. Please read the following guidelines before making a contribution.

## Submitting a contribution

To make a contribution, follow the following steps:

1. [Fork and clone this repository](https://docs.github.com/en/get-started/quickstart/fork-a-repo)
2. Make changes on your fork
3. [If needed] Please add tests for new features
4. Ensure that all tests pass and linting/formatting is consist
5. Submit a pull request

For more details about pull requests, please read [GitHub's guides](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request).

### Package management

We use `poetry` as our package manager. You can install poetry by following the instructions [here](https://python-poetry.org/docs/#installation).

DO NOT use pip or conda to install the dependencies. Instead, use poetry:

```bash
poetry install --all-extras
```

### Linting and formatting

We use `ruff` to lint and format our code. You can run the linter and formatter by running the following command:

```bash
poetry run ruff lint src/
poetry run ruff format src/
```

Please ensure that the linter does not report any errors or warnings before submitting a pull request.

### Testing

We use `pytest` to test our code. You can run tests by running the following command:

```bash
poetry run pytest
```

Please ensure that all tests pass before submitting a pull request.

## Release Process

We manually cut releases. Please reach out to the maintainers if you would like to cut a release.

Inspired by [PandasAI's contribution guide](https://raw.githubusercontent.com/gventuri/pandas-ai/main/CONTRIBUTING.md)
