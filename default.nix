{ system ? builtins.currentSystem }:
(import ./nix { inherit system; }).ci
