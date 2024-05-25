{ pkgs, atomi, atomi_classic, pkgs-2305, pkgs-jan-17-24 }:
let
  pkgs = rec {
    atomipkgs_classic = (
      with atomi_classic;
      {
        inherit
          sg;
      }
    );
    atomipkgs = (
      with atomi;
      {
        inherit
          infisical
          pls
          mirrord;
      }
    );
    "nixos-23.05" = (
      with pkgs-2305;
      {
        inherit
          poetry;
      }
    );
    jan-17-24 = (
      with pkgs-jan-17-24;
      {
        inherit
          awscli2
          black
          coreutils
          docker
          findutils
          hadolint
          git
          gitlint
          gnugrep
          gnused
          jq
          kube3d
          kubectl
          mypy
          nixpkgs-fmt
          pre-commit
          ruff
          shellcheck
          watchexec
          helm-docs
          yq-go;
        flake8 = python310Packages.flake8;
        pnpm = nodePackages.pnpm;
        npm = nodePackages.npm;
        prettier = nodePackages.prettier;
        helm = kubernetes-helm;
      }
    );
  };
in
with pkgs;
atomipkgs //
atomipkgs_classic //
pkgs."nixos-23.05" //
jan-17-24
