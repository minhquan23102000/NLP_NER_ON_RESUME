email-scramble
==============

> Universal JavaScript helper to encode/decode email addresses and phone numbers with ROT-18 to hide them from bots. This library can be used server-side with Node or on the front-end (CommonJS, AMD, global variable).

[![npm](https://img.shields.io/npm/v/email-scramble.svg?style=flat-square)](https://www.npmjs.com/package/email-scramble) [![Build Status](https://img.shields.io/travis/ThibWeb/email-scramble.svg?style=flat-square)](https://travis-ci.org/ThibWeb/email-scramble) [![devDependency Status](https://img.shields.io/david/dev/ThibWeb/email-scramble.svg?style=flat-square)](https://david-dm.org/ThibWeb/email-scramble#info=devDependencies) [![Code Climate](https://img.shields.io/codeclimate/github/ThibWeb/email-scramble.svg?style=flat-square)](https://codeclimate.com/github/ThibWeb/email-scramble) [![Test Coverage](https://img.shields.io/codeclimate/coverage/github/ThibWeb/email-scramble.svg?style=flat-square)](https://codeclimate.com/github/ThibWeb/email-scramble)

> Have a look at [the examples](https://rawgit.com/ThibWeb/email-scramble/master/examples/index.html).
> If you'd like to know more about obfuscation techniques and their success ratio, [here's a great blog post on the subject](http://techblog.tilllate.com/2008/07/20/ten-methods-to-obfuscate-e-mail-addresses-compared/).

## Getting Started

email-scramble uses a simple ROT transformation. The default rotation is ROT-18, which means that letters will be rotated by 13 and numbers by 5.

```js
var encodedEmail = emailScramble.encode('mail@example.com');
var decodedMail = emailScramble.decode(encodedMail);

// You can also pick any other flavor of ROT:
function myROT(str) {
  // Here letters are obfuscated with ROT-13 and numbers are kept clear.
  return emailScramble.rot(13, 0, str);
}

// Functional-programming partial application style:
var myRot = emailScramble.rot.bind(emailScramble, 13, 0);
```

Here's a real-world example:

```js
// <a href="znvygb:znvy@rknzcyr.pbz" data-email-scramble>Send me an email!</a>
var links = document.querySelectorAll('[data-email-scramble]');

links.forEach(function decodeLink(link) {
  link.href = emailScramble.decode(link.href);
});
```

### Download & import

`email-scramble` is available on [npm](https://www.npmjs.com/package/email-scramble), or you can [download a ZIP](https://github.com/ThibWeb/email-scramble/releases)

```
npm install --save email-scramble
```

This library can be used as an ES6 module, Node/Browserify CommonJS-like module, a RequireJS AMD module or a global:

```js
// ES6
import emailScramble from 'email-scramble';

// The CommonJS way.
var emailScramble = require('email-scramble');

// Global variable.
var emailScramble = window.emailScramble;
```

## Contributing

```bash
# Install deps
npm install
# Test
npm test
npm run lint
# Install git hooks
./.githooks/deploy
```

## Built with

- https://github.com/mathiasbynens/rot
- https://github.com/umdjs/umd

## LICENSE (ISC)

Copyright (c) 2016, Thibaud Colas

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
