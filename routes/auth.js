const express = require('express');
const router = express.Router();
const User = require('../models/User');

// GET signup page
router.get('/signup', (req, res) => {
  res.render('signup', { error: null });
});

// POST signup form
router.post('/signup', async (req, res) => {
  const { username, phoneNumber, password, confirmPassword } = req.body;
  
  if (!username || !phoneNumber || !password || !confirmPassword) {
    return res.render('signup', { error: 'All fields are required.' });
  }
  
  if (password !== confirmPassword) {
    return res.render('signup', { error: 'Passwords do not match.' });
  }
  
  try {
    // Check if a user exists with the same phone number
    const existingUser = await User.findOne({ phoneNumber });
    if (existingUser) {
      return res.render('signup', { error: 'User with that phone number already exists.' });
    }
    
    // Create and save the new user
    const newUser = new User({ username, phoneNumber, password });
    await newUser.save();
    
    // Set session and redirect to dashboard (or home)
    req.session.user = newUser;
    res.redirect('/');
  } catch (error) {
    console.error('Signup error:', error);
    res.render('signup', { error: 'An error occurred. Please try again.' });
  }
});

// GET login page
router.get('/login', (req, res) => {
  res.render('login', { error: null });
});

// POST login form updated to use phone number for login
router.post('/login', async (req, res) => {
  const { phoneNumber, password } = req.body;

  if (!phoneNumber || !password) {
    return res.render('login', { error: 'Both phone number and password are required.' });
  }

  try {
    // Look up the user by phone number instead of username
    const user = await User.findOne({ phoneNumber });
    if (!user) {
      return res.render('login', { error: 'Invalid phone number or password.' });
    }
    
    const isMatch = await user.comparePassword(password);
    if (!isMatch) {
      return res.render('login', { error: 'Invalid phone number or password.' });
    }
    
    req.session.user = user;
    res.redirect('/');
  } catch (error) {
    console.error('Login error:', error);
    res.render('login', { error: 'An error occurred. Please try again.' });
  }
});

router.get('/logout', (req, res) => {
  req.session.destroy(err => {
    if (err) {
      console.error('Logout error:', err);
      return res.redirect('/');
    }
    res.clearCookie('connect.sid');
    res.redirect('/');
  });
});

module.exports = router;
