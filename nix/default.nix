{ sources ? import ./sources.nix
, system
}:
let
  # default nixpkgs
  pkgs = import sources.nixpkgs { localSystem.system = system; };

  # gitignore.nix
  gitignoreSource = (import sources."gitignore.nix" { inherit (pkgs) lib; }).gitignoreSource;

  pre-commit-hooks = (import sources."pre-commit-hooks.nix");

  src = gitignoreSource ./..;

  requirements = (import ./requirements.nix { python = pkgs.python39; lib = pkgs.lib; inherit pkgs; });

  my-python = pkgs.python39.withPackages (ps: with ps; [
    django
    requirements.authlib
    psycopg2
    pycryptodome
    gunicorn
    requirements.celery
    requirements.bleach
    requirements.django-webtest
  ]);

  helios-server = pkgs.python39.pkgs.buildPythonApplication {
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

  manage-py = "${src}/manage.py";
  wsgi = "helios_server.wsgi:application";

  helios-manage = pkgs.writeScriptBin "helios-manage" ''
    ${my-python}/bin/python ${manage-py} $@
  '';

  helios-gunicorn = pkgs.writeScriptBin "helios-gunicorn" ''
    ${my-python}/bin/python ${manage-py} migrate
    ${my-python}/bin/gunicorn ${wsgi} \
            --pythonpath ${src} $@
  '';

in
{
  inherit pkgs src;

  # provided by shell.nix
  devTools = {
    inherit (pkgs) niv;
    inherit (pre-commit-hooks) pre-commit;
    inherit helios-manage;
    inherit helios-gunicorn;
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
    inherit helios-gunicorn;
  };
}
