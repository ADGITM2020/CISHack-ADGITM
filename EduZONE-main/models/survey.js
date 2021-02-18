var mongoose = require("mongoose");



var surveySchema = new mongoose.Schema ({
    email:{
        type:String
    },
    surveyproblem:{
        type:String
    },
    username:{
        type: String
    }
})


module.exports = mongoose.model('Survey', surveySchema);
