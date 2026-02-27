# AtMLA Email Digest Converter

Python utilities for converting ListServ email digests into HTML files.

## Requirement

* Python 3.12 or later

## Input File Format

The input files consist of monthly email digests from the AtMLA mailing list.

The digests were sent in email to the list maintainer, because of this have
the following structure:

```text
<Email header of email sent to the list maintainer>
=========================================================================
<Listserv email 1>
=========================================================================
<Listserv email 2>
=========================================================================
...
```

The `=========================================================================`
string separates each of the emails, which are then valid ".eml files.

## email_splitter.py

Processes each of the monthly email digest input files (assumed to have a ".eml"
extension), splitting each email container in the file into an "outputs"
subdirectory, with an indexed filename related to the original input filename.

```bash
$ python email_splitter.py <INPUT_DIR> <OUTPUT_DIR>
```

## email_convert.py

This code was largely taken from
<https://www.tutorialpedia.org/blog/a-tool-to-convert-email-to-html>
with a few small tweaks.

Processes each ".eml" file in the "outputs" subdirectory, creating an HTML
file with the same name (with an ".html" extension) in an "html" subdirectory.

Attachments are placed in an "attachments" subdirectory.

```bash
$ python email_convert.py <INPUT_DIR> <OUTPUT_DIR>
```

## Tests

Tests are written using the "unittest" library provided by Python to keep this
application free of external dependencies.

To run the tests:

```bash
$ python -m unittest
```

## License

See the [LICENSE](LICENSE.md) file for license rights and limitations
(Apache 2.0).
