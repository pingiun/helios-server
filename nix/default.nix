{ sources ? import ./sources.nix
}:
let
  # default nixpkgs
  pkgs = import sources.nixpkgs {};

  # gitignore.nix
  gitignoreSource = (import sources."gitignore.nix" { inherit (pkgs) lib; }).gitignoreSource;

  pre-commit-hooks = (import sources."pre-commit-hooks.nix");

  pypi2nix = (import sources."pypi2nix" {});

  src = gitignoreSource ./..;

  requirements = (import ./requirements.nix { python = my-python; lib = pkgs.lib; inherit pkgs; });

  my-python = pkgs.python39;

  helios-server = pkgs.python39.pkgs.buildPythonPackage {
    pname = "helios-server";
    version = "4.0.0";

    doCheck = true;

    checkPhase = ''
      python manage.py test
    '';

    propagatedBuildInputs = with pkgs.python39Packages; [
      django
      requirements.authlib
      psycopg2
      pycryptodome
      requirements.celery
      requirements.bleach
      requirements.django-webtest
    ];

    inherit src;
  };

in
{
  inherit pkgs src;

  # provided by shell.nix
  devTools = {
    inherit (pkgs) niv;
    inherit (pre-commit-hooks) pre-commit;
    inherit pypi2nix;
    inherit my-python;
  };

  # to be built by github actions
  ci = {
    pre-commit-check = pre-commit-hooks.run {
      inherit src;
      hooks = {
        shellcheck.enable = true;
        nixpkgs-fmt.enable = false;
        nix-linter.enable = false;
      };
      # generated files
      excludes = [ "^nix/sources\.nix$" ];
    };
    inherit helios-server;
  };
}
