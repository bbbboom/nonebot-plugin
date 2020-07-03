"use strict";

require("core-js/modules/es.array.splice");

require("core-js/modules/es.object.to-string");

require("core-js/modules/es.promise");

require("regenerator-runtime/runtime");

function asyncGeneratorStep(gen, resolve, reject, _next, _throw, key, arg) { try { var info = gen[key](arg); var value = info.value; } catch (error) { reject(error); return; } if (info.done) { resolve(value); } else { Promise.resolve(value).then(_next, _throw); } }

function _asyncToGenerator(fn) { return function () { var self = this, args = arguments; return new Promise(function (resolve, reject) { var gen = fn.apply(self, args); function _next(value) { asyncGeneratorStep(gen, resolve, reject, _next, _throw, "next", value); } function _throw(err) { asyncGeneratorStep(gen, resolve, reject, _next, _throw, "throw", err); } _next(undefined); }); }; }

var puppeteer = require('puppeteer-core');

var fs = require('fs');

var argv = process.argv.splice(2);
var url = argv[0];
var executablePath = argv[1];

if (!url || !executablePath) {
  process.exit(1);
}

_asyncToGenerator( /*#__PURE__*/regeneratorRuntime.mark(function _callee() {
  var browser, page;
  return regeneratorRuntime.wrap(function _callee$(_context) {
    while (1) {
      switch (_context.prev = _context.next) {
        case 0:
          _context.next = 2;
          return puppeteer.launch({
            executablePath: executablePath,
            defaultViewport: {
              width: 375,
              height: 667
            }
          });

        case 2:
          browser = _context.sent;
          _context.next = 5;
          return browser.newPage();

        case 5:
          page = _context.sent;
          page.waitForSelector('video').then(function (e) {
            var data = e.getProperty('src').then(function (a) {
              a.jsonValue().then(function (b) {
                fs.writeFile('./mlog/script/out.json', JSON.stringify({
                  'src': b
                }), function (err) {});
              });
            });
          })["catch"](function (err) {
            fs.writeFile('./mlog/script/out.json', JSON.stringify({
              'src': 'null'
            }), function (err) {});
          }); //await page.screenshot({path: 'example.png'});

          _context.next = 9;
          return page["goto"](url);

        case 9:
          _context.next = 11;
          return browser.close();

        case 11:
        case "end":
          return _context.stop();
      }
    }
  }, _callee);
}))();
