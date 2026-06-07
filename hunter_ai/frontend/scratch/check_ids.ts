import { chromium } from 'playwright';

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('https://wyszukiwarka.gunb.gov.pl/');
  
  console.log('Checking radio buttons...');
  const radios = await page.evaluate(() => {
    return Array.from(document.querySelectorAll('input[type="radio"]')).map(r => ({
      name: (r as HTMLInputElement).name,
      value: (r as HTMLInputElement).value,
      label: (r.parentElement?.innerText || '').trim()
    }));
  });
  console.log('Radios:', JSON.stringify(radios, null, 2));

  console.log('Checking selects...');
  const selects = await page.evaluate(() => {
    return Array.from(document.querySelectorAll('select')).map(s => ({
      id: s.id,
      name: s.name,
      options: Array.from(s.options).slice(0, 5).map(o => ({ text: o.text, value: o.value }))
    }));
  });
  console.log('Selects:', JSON.stringify(selects, null, 2));

  await browser.close();
})();
