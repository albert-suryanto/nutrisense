{
  inputs = {
    # util
    flake-utils.url = "github:numtide/flake-utils";
    treefmt-nix.url = "github:numtide/treefmt-nix";
    pre-commit-hooks.url = "github:cachix/pre-commit-hooks.nix";

    # registry
    nixpkgs.url = "nixpkgs/9418167277f665de6f4a29f414d438cf39c55b9e";
    nixpkgs-2305.url = "nixpkgs/nixos-23.05"; # don't pin
    nixpkgs-jan-17-24.url = "nixpkgs/c3e128f3c0ecc1fb04aef9f72b3dcc2f6cecf370";

    atomipkgs.url = "github:kirinnee/test-nix-repo/v20.0.0";
    atomipkgs_classic.url = "github:kirinnee/test-nix-repo/classic"; # sg
  };
  outputs =
    { self

      # utils
    , flake-utils
    , treefmt-nix
    , pre-commit-hooks

      # registries
    , atomipkgs
    , atomipkgs_classic
    , nixpkgs
    , nixpkgs-2305
    , nixpkgs-jan-17-24
    } @inputs:
    flake-utils.lib.eachDefaultSystem
      (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        pkgs-2305 = nixpkgs-2305.legacyPackages.${system};
        pkgs-jan-17-24 = nixpkgs-jan-17-24.legacyPackages.${system};

        atomi = atomipkgs.packages.${system};
        atomi_classic = atomipkgs_classic.packages.${system};
        pre-commit-lib = pre-commit-hooks.lib.${system};
      in
      let
        out = rec {
          pre-commit = import ./nix/pre-commit.nix {
            inherit pre-commit-lib formatter packages;
          };
          formatter = import ./nix/fmt.nix {
            inherit treefmt-nix pkgs;
          };
          packages = import ./nix/packages.nix {
            inherit
              pkgs
              atomi
              atomi_classic
              pkgs-2305
              pkgs-jan-17-24;
          };
          env = import ./nix/env.nix {
            inherit pkgs packages;
          };
          devShells = import ./nix/shells.nix {
            inherit pkgs env packages;
            addShellHook = checks.pre-commit-check.shellHook;
          };
          checks = {
            pre-commit-check = pre-commit;
            format = formatter;
          };
        };
      in
      with out;
      {
        inherit checks formatter packages devShells;
      }
      );
}
