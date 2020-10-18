{ system ? (import <nixpkgs> {}).system }:
(import ./nix { inherit system; }).ci
