const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');
const express = require('express');
const router = express.Router();

// 🏠 Home
router.get('/', (req, res) => {
  res.render('index', { title: 'PriceScope - Find Best Prices' }); // 🔁 user is now in res.locals.user
});

// 📜 Privacy Policy
router.get('/privacy', (req, res) => {
  res.render('privacy');
});

// 📃 Terms & Conditions
router.get('/terms', (req, res) => {
  res.render('terms');
});

// 🧪 Test Flipkart Scraper
router.get('/test-flipkart', (req, res) => {
  const searchQuery = req.query.search || 'iphone';
  const scraperFlipkart = path.join(__dirname, '../scraper2.py');

  const flipkartProcess = spawn('python', [scraperFlipkart, searchQuery], {
    cwd: process.cwd(),
  });

  flipkartProcess.stderr.on('data', (data) => {
    console.error(`Flipkart scraper stderr: ${data.toString()}`);
  });

  flipkartProcess.on('close', (flipkartCode) => {
    console.log(`Flipkart scraper exited with code ${flipkartCode}`);
    const flipkartJsonPath = path.join(process.cwd(), 'deals2.json');

    if (!fs.existsSync(flipkartJsonPath)) {
      return res.status(500).send('Flipkart data file not found.');
    }

    fs.readFile(flipkartJsonPath, 'utf-8', (err, flipkartData) => {
      if (err) return res.status(500).send('Failed to read Flipkart file.');

      let flipkartDeals;
      try {
        flipkartDeals = JSON.parse(flipkartData);
      } catch (parseErr) {
        return res.status(500).send('Failed to parse Flipkart data.');
      }

      return res.json({ flipkartDeals });
    });
  });
});

// 📱 Static S23 Ultra Page
router.get('/s23', (req, res) => {
  res.render('s23ultra');
});

module.exports = router;
