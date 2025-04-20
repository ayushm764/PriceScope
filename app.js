// app.js
const express = require('express');
const dotenv = require('dotenv');
const path = require('path');
const mongoose = require('mongoose');
const session = require('express-session');
const MongoStore = require('connect-mongo');

dotenv.config();
const app = express();

// MongoDB connection
mongoose.connect(process.env.MONGO_URI, {
  useNewUrlParser: true,
  useUnifiedTopology: true
})
.then(() => console.log('MongoDB connected'))
.catch((err) => console.error('MongoDB connection error:', err));

// View engine setup
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Static files & form parser
app.use(express.static(path.join(__dirname, 'public')));
app.use(express.urlencoded({ extended: true }));

// Session config
app.use(session({
  secret: process.env.SESSION_SECRET || 'yourSecretKey',
  resave: false,
  saveUninitialized: false,
  store: MongoStore.create({ mongoUrl: process.env.MONGO_URI }),
  cookie: { maxAge: 1000 * 60 * 60 * 24 } // 1 day
}));

// 🔥 Pass user object to all views
app.use((req, res, next) => {
  res.locals.user = req.session.user || null;
  next();
});

// Mount routes
const indexRoutes = require('./routes/index');
const dealsRoutes = require('./routes/deals');
const authRoutes = require('./routes/auth');
const profileRoutes = require('./routes/profile'); // 🔥 New profile route

app.use('/', indexRoutes);
app.use('/deals', dealsRoutes);
app.use('/auth', authRoutes);
app.use('/profile', profileRoutes); // 🔥 Mounting profile routes

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});
