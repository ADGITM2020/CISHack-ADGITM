var mongoose = require("mongoose");
var passportLocalMongoose = require("passport-local-mongoose");


var UserSchema = new mongoose.Schema ({
    username: {
        type: String,
    },
    password:{
        type: String,       
    },
    Todo:[{
        todo:{
            type: mongoose.Schema.Types.ObjectId,
            ref:"Todo"
        },
        title:String, 
        completed: Boolean,
        status:Boolean
    }
    ]
})
UserSchema.plugin(passportLocalMongoose);

module.exports = mongoose.model('User', UserSchema);


