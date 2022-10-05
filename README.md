# metamorph

![IMG](/img/img.png)

First line is the input followed by colorized suggestions.

Doc: `metamorph --help`

[![PyPI version][pypi image]][pypi link]  ![downloads](https://img.shields.io/pypi/dm/metamorph.svg) 

| [Stable][doc release]        | [Unstable][doc test]           |
| ------------- |:-------------:|
| [![workflow][a s image]][a s link]      | [![test][a t image]][a t link]     |
| [![Coverage Status][c s i]][c s l] | [![Coverage Status][c t i]][c t l] |
| [![Codacy Badge][cc s c i]][cc s c l]      |[![Codacy Badge][cc c i]][cc c l] | 
| [![Codacy Badge][cc s q i]][cc s q l]     |[![Codacy Badge][cc q i]][cc q l] | 
| [![Documentation][rtd s i]][rtd s l] | [![Documentation][rtd t i]][rtd t l]  | 

## Documentation

-   <https://metamorph-apn.readthedocs.io/en/stable/>
-   <https://apn-pucky.github.io/metamorph/index.html>

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
```yaml
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

This exemplary `configs/config.yaml` will produce following results (note `-sd` for diagrams and `-c` for config, while most command line parameters take precedence over config (`-gs` here)).
A list of translators can be found here <https://github.com/nidhaloff/deep-translator>.

```sh
metamorph -i -sd -gs en -c config.yaml
```

![DIAG](/img/diag.png)

(`GoogleTranslate` gets abbreviated to only capital letters `GT`)

[doc release]: https://apn-pucky.github.io/metamorph/index.html
[doc test]: https://apn-pucky.github.io/metamorph/test/index.html

[pypi image]: https://badge.fury.io/py/metamorph.svg
[pypi link]: https://pypi.org/project/metamorph/

[a s image]: https://github.com/APN-Pucky/metamorph/actions/workflows/stable.yml/badge.svg
[a s link]: https://github.com/APN-Pucky/metamorph/actions/workflows/stable.yml
[a t link]: https://github.com/APN-Pucky/metamorph/actions/workflows/unstable.yml
[a t image]: https://github.com/APN-Pucky/metamorph/actions/workflows/unstable.yml/badge.svg

[cc s q i]: https://app.codacy.com/project/badge/Grade/1acfcad112734b1ca875518cf1eeda34?branch=stable
[cc s q l]: https://www.codacy.com/gh/APN-Pucky/metamorph/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=APN-Pucky/metamorph&amp;utm_campaign=Badge_Grade?branch=stable
[cc s c i]: https://app.codacy.com/project/badge/Coverage/1acfcad112734b1ca875518cf1eeda34?branch=stable
[cc s c l]: https://www.codacy.com/gh/APN-Pucky/metamorph/dashboard?utm_source=github.com&utm_medium=referral&utm_content=APN-Pucky/HEPi&utm_campaign=Badge_Coverage?branch=stable

[cc q i]: https://app.codacy.com/project/badge/Grade/1acfcad112734b1ca875518cf1eeda34
[cc q l]: https://www.codacy.com/gh/APN-Pucky/metamorph/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=APN-Pucky/metamorph&amp;utm_campaign=Badge_Grade
[cc c i]: https://app.codacy.com/project/badge/Coverage/1acfcad112734b1ca875518cf1eeda34
[cc c l]: https://www.codacy.com/gh/APN-Pucky/metamorph/dashboard?utm_source=github.com&utm_medium=referral&utm_content=APN-Pucky/HEPi&utm_campaign=Badge_Coverage

[c s i]: https://coveralls.io/repos/github/APN-Pucky/metamorph/badge.svg?branch=stable
[c s l]: https://coveralls.io/github/APN-Pucky/metamorph?branch=stable
[c t l]: https://coveralls.io/github/APN-Pucky/metamorph?branch=master
[c t i]: https://coveralls.io/repos/github/APN-Pucky/metamorph/badge.svg?branch=master

[rtd s i]: https://readthedocs.org/projects/metamorph/badge/?version=stable
[rtd s l]: https://metamorph-apn.readthedocs.io/en/stable/?badge=stable
[rtd t i]: https://readthedocs.org/projects/metamorph/badge/?version=latest
[rtd t l]: https://metamorph-apn.readthedocs.io/en/latest/?badge=latest
