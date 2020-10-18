{ pkgs
, python
, lib
, sources ? import ./sources.nix
}:

let

  stdenv = pkgs.stdenv;

in

  with python.pkgs;

  rec {
    billiard = buildPythonPackage rec {
      pname = "billiard";
      version = "3.6.3.0";
      disabled = isPyPy;

      src = sources.billiard;

      checkInputs = [ pytest case psutil ];
      checkPhase = ''
        pytest
      '';

      meta = with stdenv.lib; {
        homepage = "https://github.com/celery/billiard";
        description = "Python multiprocessing fork with improvements and bugfixes";
        license = licenses.bsd3;
      };
    };

    vine = buildPythonPackage rec {
      pname = "vine";
      version = "5.0.0";

      disable = pythonOlder "2.7";

      src = fetchPypi {
        inherit pname version;
        hash = "sha256:0zk3pm0g7s4qfn0gk28lfmsyplvisaxi6826cgpq5njkm4j1cfvx";
      };

      buildInputs = [ case pytest ];

      meta = with stdenv.lib; {
        description = "Python promises";
        homepage = "https://github.com/celery/vine";
        license = licenses.bsd3;
      };
    };

    amqp = buildPythonPackage rec {
      pname = "amqp";
      version = "5.0.1";

      src = fetchPypi {
        inherit pname version;
        hash = "sha256:0pzspxsssb2ma2y640awp78y24q2742qrzbcmagxpqr3zvkgi0cq";
      };

      propagatedBuildInputs = [ vine ];

      checkInputs = [ pytestCheckHook case ];
      disabledTests = [
        "test_rmq.py" # requires network access
      ];

      meta = with stdenv.lib; {
        homepage = "https://github.com/celery/py-amqp";
        description = "Python client for the Advanced Message Queuing Procotol (AMQP). This is a fork of amqplib which is maintained by the Celery project";
        license = licenses.lgpl21;
      };
    };

    kombu = buildPythonPackage rec {
      pname = "kombu";
      version = "5.0.2";

      src = fetchPypi {
        inherit pname version;
        hash = "sha256:0g5c0lg2abva1d8nrc824jk5fcvf8kbbbvhb8xyx86271ax5z5pl";
      };

      propagatedBuildInputs = [ amqp ];

      checkInputs = [ botocore pytest case pytz Pyro4 sqlalchemy ];
      # test_redis requires fakeredis, which isn't trivial to package
      checkPhase = ''
        pytest --ignore t/unit/transport/test_redis.py
      '';

      meta = with stdenv.lib; {
        description = "Messaging library for Python";
        homepage = "https://github.com/celery/kombu";
        license = licenses.bsd3;
      };
    };

    celery = buildPythonPackage rec {
      pname = "celery";
      version = "5.0.0";

      src = fetchPypi {
        inherit pname version;
        hash = "sha256:0mgjw5cdkadcdpg5fg7nxqdd3722j6zh98r9f3ixh0z7vpyk0f9i";
      };

      postPatch = ''
        substituteInPlace requirements/default.txt \
          --replace "kombu>=4.6.10,<4.7" "kombu"
        substituteInPlace requirements/test.txt \
          --replace "moto==1.3.7" moto \
          --replace "pytest>=4.3.1,<4.4.0" pytest
      '';

      doCheck = false;

      propagatedBuildInputs = [ kombu click click-repl click-didyoumean cryptography billiard pytz vine ];

      meta = with stdenv.lib; {
        homepage = "https://github.com/celery/celery/";
        description = "Distributed task queue";
        license = licenses.bsd3;
      };
    };

    html5lib = buildPythonPackage rec {
      pname = "html5lib";
      version = "1.1";

      src = fetchPypi {
        inherit pname version;
        sha256 = "b2e5b40261e20f354d198eae92afc10d750afb487ed5e50f9c4eaf07c184146f";
      };

      propagatedBuildInputs = [
        six
        webencodings
      ];

      doCheck = false;

      meta = {
        homepage = "https://github.com/html5lib/html5lib-python";
        downloadPage = "https://github.com/html5lib/html5lib-python/releases";
        description = "HTML parser based on WHAT-WG HTML5 specification";
        longDescription = ''
          html5lib is a pure-python library for parsing HTML. It is designed to
          conform to the WHATWG HTML specification, as is implemented by all
          major web browsers.
        '';
        license = lib.licenses.mit;
        maintainers = with lib.maintainers; [ domenkozar prikhi ];
      };
    };

    bleach = buildPythonPackage rec {
      pname = "bleach";
      version = "3.2.1";

      src = fetchPypi {
        inherit pname version;
        hash = "sha256:1030qv12g0nasd3c61c96wp2z6k7575fbakf35a1haw4h6dr3daj";
      };

      propagatedBuildInputs = [ packaging six html5lib setuptools ];

      doCheck = false;

      meta = {
        description = "An easy, HTML5, whitelisting HTML sanitizer";
        longDescription = ''
          Bleach is an HTML sanitizing library that escapes or strips markup and
          attributes based on a white list. Bleach can also linkify text safely,
          applying filters that Django's urlize filter cannot, and optionally
          setting rel attributes, even on links already in the text.

          Bleach is intended for sanitizing text from untrusted sources. If you
          find yourself jumping through hoops to allow your site administrators
          to do lots of things, you're probably outside the use cases. Either
          trust those users, or don't.
        '';
        homepage = "https://github.com/mozilla/bleach";
        downloadPage = "https://github.com/mozilla/bleach/releases";
        license = lib.licenses.asl20;
        maintainers = with lib.maintainers; [ prikhi ];
      };
    };

    authlib = buildPythonPackage rec {
      version = "1.0.0-dev";
      pname = "authlib";

      src = pkgs.fetchFromGitHub {
        owner = "lepture";
        repo = "authlib";
        rev = "84ba75ab04606bbf5d7cc783b9b09f5b00291d9c";
        sha256 = "0ph97j94i40jj7nc5ya8pfq0ccx023zbqpcs5hrxmib53g64k5xy";
      };

      propagatedBuildInputs = [ cryptography requests ];

      checkInputs = [ mock pytest ];

      checkPhase = ''
        PYTHONPATH=$PWD:$PYTHONPATH pytest tests/{core,files}
      '';

      meta = with stdenv.lib; {
        homepage = "https://github.com/lepture/authlib";
        description = "The ultimate Python library in building OAuth and OpenID Connect servers. JWS,JWE,JWK,JWA,JWT included.";
        maintainers = with maintainers; [ flokli ];
        license = licenses.bsd3;
      };
    };

    django-webtest = buildPythonPackage rec {
      pname = "django-webtest";
      version = "1.9.7";

      src = fetchPypi {
        inherit pname version;
        sha256 = "c5a1e486a3d8d3623aa615b6db2f27de848aa7079303a84721e9a685f839796c";
      };

      doCheck = false;

      propagatedBuildInputs = [
        webtest
      ];

      meta = with stdenv.lib; {
        homepage = "https://github.com/django-webtest/django-webtest";
        license = licenses.mit;
        description = "Instant integration of Ian Bicking's WebTest (http://docs.pylonsproject.org/projects/webtest/) with django's testing framework.";
      };
    };
  }
