# Contributing

If you would like to contribute to this projects, there are a few guidelines
that you'll want to review below.

## Code of Conduct

The Code of Conduct for this project is adapted from the Contributor Covenant,
version 3.0, permanently available at <https://www.contributor-covenant.org/version/3/0/>.

The adapted version with instructions on how to report possible violations are
available in the [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md) file in this repository.

## Branching

Although the default branch for this repository is `main`, all active
development needs to be branched off of the `develop` branch.

Once you have cloned this repository, you can create a new  branch off of
`develop` by using the following command:

    git checkout develop; git branch new-branch

Once development has been completed for the new feature or fix and local
testing has been completed, it can be pushed using the following command:

    git push -u origin new-branch

## Pull Requests

Once the new branch has been published to Github, the next step will be to
create a new pull request to merge the new branch with the `develop` branch.

After creating the pull request, it will go through a review and the request
will either be accepted or declined based on needs, code quality, testing
problems or any other reason that will be included in the commit message or
request declined message.

Pull requests from new branches to the `main` branch that do not go through
the `develop` branch via a pull request will be declined.

## License

This project is licensed under version 2.0 of the Apache License. A copy of
the license is available in this repository at [LICENSE](LICENSE).
