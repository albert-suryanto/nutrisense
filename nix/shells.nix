{ pkgs, packages, env, addShellHook }:

with env;
{
  default = pkgs.mkShell rec {
    buildInputs = env.system ++ env.main ++ env.tools ++ env.dev ++ env.lint ++ [ pkgs.zlib ];
    shellHook = ''
      export LD_LIBRARY_PATH="${pkgs.lib.makeLibraryPath buildInputs}:$LD_LIBRARY_PATH"
      export LD_LIBRARY_PATH="${pkgs.stdenv.cc.cc.lib.outPath}/lib:$LD_LIBRARY_PATH"

      ${addShellHook}
    '';
  };
  ci = pkgs.mkShell rec {
    buildInputs = env.system ++ env.main ++ env.tools ++ env.lint ++ env.ci ++ [ pkgs.zlib ];
    shellHook = ''
      export LD_LIBRARY_PATH="${pkgs.lib.makeLibraryPath buildInputs}:$LD_LIBRARY_PATH"
      export LD_LIBRARY_PATH="${pkgs.stdenv.cc.cc.lib.outPath}/lib:$LD_LIBRARY_PATH"

      ${addShellHook}
    '';
  };
  cd = pkgs.mkShell rec {
    buildInputs = env.system ++ env.releaser ++ [ pkgs.zlib ];
    shellHook = ''
      export LD_LIBRARY_PATH="${pkgs.lib.makeLibraryPath buildInputs}:$LD_LIBRARY_PATH"
      export LD_LIBRARY_PATH="${pkgs.stdenv.cc.cc.lib.outPath}/lib:$LD_LIBRARY_PATH"

      ${addShellHook}
    '';
  };
}
