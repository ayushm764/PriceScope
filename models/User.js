const mongoose = require('mongoose');
const bcrypt = require('bcrypt');

// Define the schema
const UserSchema = new mongoose.Schema({
  username: {
    type: String,
    required: true
  },
  phoneNumber: {
    type: String,
    required: true
  },
  password: {
    type: String,
    required: true
  },
  // 🔥 Store all searches by user
  searchHistory: {
    type: [String],
    default: []
  },
  // 🔥 Track user's most searched product
  mostSearchedItem: {
    type: String,
    default: ''
  }
});

// 🔐 Pre-save hook to hash the password
UserSchema.pre('save', async function (next) {
  if (!this.isModified('password')) return next();
  try {
    const salt = await bcrypt.genSalt(10);
    this.password = await bcrypt.hash(this.password, salt);
    next();
  } catch (err) {
    next(err);
  }
});

// 🔐 Method to compare password at login
UserSchema.methods.comparePassword = async function (candidatePassword) {
  return bcrypt.compare(candidatePassword, this.password);
};

// Export the model
module.exports = mongoose.model('User', UserSchema);
