const express = require('express');
const router = express.Router();

// Dummy middleware to simulate user login
// Replace this with your real auth middleware
function isAuthenticated(req, res, next) {
    if (req.session && req.session.user) {
        return next();
    }
    res.redirect('/auth/login');
}

// GET /profile
router.get('/', isAuthenticated, (req, res) => {
    const user = req.session.user;
    res.render('profile', { user });
});

// GET /profile/history
router.get('/history', isAuthenticated, (req, res) => {
    const user = req.session.user;
    const history = req.session.searchHistory || [];
    res.render('searchhistory', { user, history });
});

// POST /profile/clear-history
router.post('/clear-history', isAuthenticated, (req, res) => {
    req.session.searchHistory = [];
    res.redirect('/profile/history');
});

module.exports = router;
