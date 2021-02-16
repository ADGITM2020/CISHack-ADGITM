const mongoose = require('mongoose');

const TodoTaskSchema = new mongoose.Schema({
content: {
    type: String,
    required: true
    },
    date: {
    type: Date,
    default: Date.now
    }
})
module.exports = mongoose.model('TodoTask',TodoTaskSchema);