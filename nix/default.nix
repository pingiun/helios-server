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

  helios-tests = pkgs.runCommand "helios-tests" { } ''
    cp -r ${src}/* .
    ${my-python}/bin/python manage.py test
    ${pkgs.black}/bin/black --check .
    touch $out
  '';

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
  devTools = [
    my-python
    pkgs.niv
    pre-commit-hooks.pre-commit
    pkgs.nixpkgs-fmt
    pkgs.black
  ];

  # to be built by github actions
  ci = {
    pre-commit-check = pre-commit-hooks.run {
      inherit src;
      hooks = {
        shellcheck.enable = true;
        nixpkgs-fmt.enable = true;
        nix-linter.enable = true;
      };
      # generated files
      excludes = [ "^nix/sources\.nix$" ];
    };
    inherit helios-tests helios-gunicorn helios-manage;
  };
}
