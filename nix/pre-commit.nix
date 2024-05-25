{ formatter, pre-commit-lib, packages }:
pre-commit-lib.run {
  src = ./.;

  # hooks
  hooks = {
    # formatter
    treefmt = {
      enable = true;
      excludes = [ ".*scaffold/templates/.*" ".*infra/.*" "pnpm-lock.yaml" "Changelog.md" "CommitConventions.md" ".*schema.json" ];
    };
    # linters From https://github.com/cachix/pre-commit-hooks.nix
    shellcheck = {
      enable = false;
    };

    a-helm-lint-chart = {
      enable = true;
      name = "Helm Lint Chart";
      description = "Lints helm charts";
      entry = "${packages.helm}/bin/helm lint -f infra/chart/values.yaml infra/chart";
      files = "infra/chart/.*";
      language = "system";
      pass_filenames = false;
    };

    a-gitlint = {
      enable = true;
      name = "Gitlint";
      description = "Lints git commit message";
      entry = "${packages.gitlint}/bin/gitlint --staged --msg-filename .git/COMMIT_EDITMSG";
      language = "system";
      pass_filenames = false;
      stages = [ "commit-msg" ];
    };

    a-shellcheck = {
      enable = true;
      name = "Shell Check";
      entry = "${packages.shellcheck}/bin/shellcheck";
      files = ".*sh$";
      language = "system";
      pass_filenames = true;
    };

    a-enforce-exec = {
      enable = true;
      name = "Enforce Shell Script executable";
      entry = "${packages.coreutils}/bin/chmod +x";
      files = ".*sh$";
      language = "system";
      pass_filenames = true;
    };

    a-hadolint = {
      enable = true;
      name = "Docker Linter";
      entry = "${packages.hadolint}/bin/hadolint";
      files = ".*Dockerfile$";
      language = "system";
      pass_filenames = true;
    };

    a-helm-docs = {
      enable = true;
      name = "Helm Docs";
      entry = "${packages.helm-docs}/bin/helm-docs";
      files = ".*";
      language = "system";
      pass_filenames = false;
    };

    a-ruff = {
      enable = true;
      name = "Lint Python files with Ruff";
      entry = "${packages.ruff}/bin/ruff check --force-exclude --fix";
      language = "python";
      files = ".*py";
    };
  };

  settings = {
    treefmt = {
      package = formatter;
    };
  };
}
