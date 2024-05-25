{ pkgs, packages }:
with packages;
{
  ci = [
    awscli2
    git
  ];

  dev = [
    watchexec
  ];

  lint = [
    black
    flake8
    hadolint
    gitlint
    mypy
    ruff
    sg
    shellcheck
  ];

  main = [
    pls
    poetry
  ];

  releaser = [
    sg
  ];

  system = [
    coreutils
    findutils
    gnugrep
    gnused
    jq
    yq-go
  ];

  tools = [
    # docker    # The nix docker version is not compatible with the one of CI jobs. docker buildx build ....--cache-from "type=s3,region=${AWS_REGION},bucket=${AWS_BUCKET},name=${CACHE_COMMIT}" \
    kube3d
    helm
    kubectl
    pnpm
    npm
  ];
}
