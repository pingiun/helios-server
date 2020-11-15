{ project ? import ./nix { system = builtins.currentSystem; }
}:

project.pkgs.mkShell {
  buildInputs = project.devTools;
  shellHook = ''
    ${project.ci.pre-commit-check.shellHook}
  '';
}
