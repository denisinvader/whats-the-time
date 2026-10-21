# Contributing

Thanks for working on What's the Date? A good change makes the clock easier to trust or the skill easier to use. Before opening a PR, describe the question or failure you saw, the platform and Python version, and what you changed.

## Set up

Use Python 3.9 or newer. The runtime has no required packages. Install Ruff for local style checks with `python -m pip install "ruff>=0.14,<1"`.

```sh
python -m unittest discover -s tests -v
ruff check .
ruff format --check .
```

On Windows, `py -3` can replace `python`. Add tests for behavior that can break across platforms or at date boundaries. Keep the skill instructions short: the model needs to know when to read the clock, which command to run, and how to handle time zones. Put implementation details in the script or this repository's docs.

## Pull requests

Open a focused PR against the default branch. Explain the user-visible behavior, list the checks you ran, and call out any platform you could not test. If you change the JSON fields or an installation path, update the README in the same PR. Maintainers review changes for correctness, portability, and whether the instructions still let agents answer naturally.

Please report suspected vulnerabilities privately as described in [SECURITY.md](SECURITY.md).
