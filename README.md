pyroman2
========

[![Build Status](https://travis-ci.org/eblade/pyroman2.svg?branch=master)](https://travis-ci.org/eblade/pyroman2)

The way-too-ambitious project that I somehow can't let go the idea of


Dependencies
------------

* python3
* ubuntu: libfreetype6-dev libjpeg-dev zlib1g-dev libpng12-dev
* centos/fedora: freetype-devel libjpeg-devel libpng-devel
* via pip3: pillow or PIL

See http://stackoverflow.com/questions/4011705/python-the-imagingft-c-module-is-not-installed for help with pillow.


Features
--------

These features will have to be implemented before a beta release:

* Fonts
  * Base14 font support [DONE]
* Layout
  * Fully flexible per page [DONE]
  * Paragraph/heading templates
  * Nested lists with bullets or numbering
  * Inheritable parameters in document hierarchy [DONE]
* Text flow
  * Left, right, center and justify alignment
  * Automatic content flow from one page to another
* Figures
  * Using JPEG, PNG or BMP as figures
  * Figure labels
  * (optional) Resizing of images for appropriate DPI
* Parsing
  * Pyroman 1 support
  * (optional) support for other simlilar format such as Markdown or reStructuredText
* PDF rendering
  * Base14 font support [DONE]
  * Cross-references
  * Metadata
* Image rendering
  * Should look like the PDF output
  * Support the output formats PIL supports (at least JPEG and PNG)
* (optional) Tables
