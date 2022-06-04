# Metamorph

![IMG](/img/img.png)

First line is the input followed by colorized suggestions.

Doc: `metamorph --help`

(Work-in-progress: Doc: https://apn-pucky.github.io/metamorph/index.html )

[![PyPI version][pypi image]][pypi link]  ![downloads](https://img.shields.io/pypi/dm/metamorph.svg) 

| [Stable][doc release]        | [Dev][doc test]           |
| ------------- |:-------------:|
| [![workflow][a s image]][a s link]      | [![test][a t image]][a t link]     |

## Versions

### Stable

```sh
pip install metamorph [--user] [--upgrade]
```

### Dev

```sh
pip install --index-url https://test.pypi.org/simple/ metamorph [--user] [--upgrade]
```

## Configuration

For a list of parameters run `metamorph -h`.

The root node `flow` can have multiple different starting languages (given `start` is None).
```yml
translator: "GoogleTranslator"
start: "de"
goal: "de"

flow:
  de:
    fr:
      es:
        fr:
    de:
      es:
      fr:
        sv:
  fr:
    en:
  en:
  fi:
    de:
      fr:
        es:
          fr:
      de:
        es:
        fr:
          sv:
  sv:
```

This exemplary config.yml will produce following results (note `-sd` for diagrams and `-c` for config, while most command line parameters take precedence over config (`-gs` here)).

```sh
metamorph -sd -gs en -c config.yml
```

![DIAG](/img/diag.png)

(GoogleTranslate` gets abbreviated to `GT`)


[doc release]: https://apn-pucky.github.io/metamorph/index.html
[doc test]: https://apn-pucky.github.io/metamorph/test/index.html

[pypi image]: https://badge.fury.io/py/metamorph.svg
[pypi link]: https://pypi.org/project/metamorph/

[a s image]: https://github.com/APN-Pucky/metamorph/actions/workflows/release.yml/badge.svg
[a s link]: https://github.com/APN-Pucky/metamorph/actions/workflows/release.yml
[a t link]: https://github.com/APN-Pucky/metamorph/actions/workflows/test.yml
[a t image]: https://github.com/APN-Pucky/metamorph/actions/workflows/test.yml/badge.svg


