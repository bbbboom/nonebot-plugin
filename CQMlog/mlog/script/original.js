

const puppeteer = require('puppeteer-core');
const fs = require('fs');
const argv = process.argv.splice(2)
const url = argv[0]
const executablePath = argv[1]

if(!url || !executablePath) { process.exit(1); }

(async () => {
  const browser = await puppeteer.launch({
	  executablePath,
	  defaultViewport: {
		  width: 375,
		  height: 667
	  }
  });
  const page = await browser.newPage();
  
  page.waitForSelector('video').then((e) => {
	  const data = e.getProperty('src').then((a) => {a.jsonValue().then((b) => {
		  fs.writeFile('./mlog/script/out.json', JSON.stringify({'src': b}), (err) => {})
	  })})
	}).catch((err) => {fs.writeFile('./mlog/script/out.json', JSON.stringify({'src': 'null'}), (err) => {})})
    //await page.screenshot({path: 'example.png'});

	await page.goto(url);
	
    await browser.close();
})();