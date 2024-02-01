{
  description = "dev-syncer";

  inputs.nixpkgs.url = "github:nixOs/nixpkgs";

  outputs = { self, nixpkgs }: 
  let
    pkgs = (import nixpkgs {system = "x86_64-linux";});

    python = pkgs.python3;

    pythonWithPackages = python.withPackages (ps: with ps; [
      asn1crypto
      bcrypt
      cffi
      cryptography
      inotify
      nose
      paramiko
      pyasn1
      pycparser
      #nacl
      six
    ]);

    dev-syncer = pkgs.stdenv.mkDerivation {
      pname = "dev-syncer";
      version = "0.1";

      installPhase = ''
        mkdir -p $out/bin
        echo '#!${pythonWithPackages}/bin/python3' > $out/bin/dev-sync
        cat ${./daemon.py} >> $out/bin/dev-sync
        chmod +x $out/bin/dev-sync
      '';

      phases = [ "installPhase" ];
    };

  in {
    packages.x86_64-linux = {
      inherit dev-syncer;
    };
  };
}
