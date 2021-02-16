var express=require("express"),
    app = express(),
    mongoose=require("mongoose"), 
    nodemailer = require("nodemailer"),  
    bodyParser = require("body-parser"),
    passport = require("passport"),
    LocalStrategy = require("passport-local"),
    methodOverride=require("method-override"),
    TodoTask = require('./models/Todo.js'),
    Survey=require("./models/survey.js"),
    User = require("./models/user.js");


mongoose.connect("mongodb+srv://hackathon:hackathon@hackathon.skd4q.mongodb.net/hackathon?retryWrites=true&w=majority",{useNewUrlParser: true,useUnifiedTopology: true,useFindAndModify:false});

app.use(bodyParser.urlencoded({extended:true}));

process.env.NODE_TLS_REJECT_UNAUTHORIZED = "0";

app.set("view engine","ejs");

app.use(express.static(__dirname+"/public"));

app.use(methodOverride("_method"));

app.use(require("express-session")({
    secret:"this is secret content",
    resave:false,
    saveUninitialized:false
  }));

app.use(passport.initialize());
app.use(passport.session());
passport.use(new LocalStrategy(User.authenticate()));
passport.serializeUser(User.serializeUser());
passport.deserializeUser(User.deserializeUser());

app.use(function(req,res,next){
    res.locals.currentUser=req.user; 
    next();   
  });


app.get("/",function(req,res){
    res.render("home");
});



app.get("/music",isLoggedIn,function(req,res){
    res.render("music");
});

app.get("/register", function(req, res){
    res.render("register");
});

app.post("/register", function(req,res){
    var newUser = ({username: req.body.username});
    console.log("in body");
    User.register(newUser, req.body.password, function(err, user){
      if(err){

          console.log(err);
          return res.render("register");
      }
      passport.authenticate("local")(req,res, function(){
          console.log("registration successfullllllllll");
          console.log(user);

        res.redirect("/");
      });
    });
  });



app.get("/login", function(req, res){
    res.render("login");
});


app.post("/login",passport.authenticate("local",
{
  successRedirect:"/",
  failureredirect:"/login"
}),function(req,res){
  if(err){
    console.log(err);
  }
  
});

app.get("/logout",function(req,res){
    req.logout();

    res.redirect("/");
  });

  function isLoggedIn(req,res,next){
    if(req.isAuthenticated()){
      return next();
    }

    res.redirect("/login");
  }

app.get("/todo",isLoggedIn, function(req, res){
    TodoTask.find({}, function(err, tasks) {
    res.render("todo", { TodoTask: tasks });
    })
  });

app.post("/todo", isLoggedIn, function(req, res){
  var todoTask = new TodoTask({
    content: req.body.content
  })
    todoTask.save();
    res.redirect("/todo");
});

app.delete("/remove/:id",isLoggedIn,function(req,res){
  TodoTask.findByIdAndRemove(req.params.id,function(err){
    if(err){
      res.redirect("/todo");
      console.log(err);
    }
    else{
      console.log("todo deleted");
      res.redirect("/todo");
    }
  });
});

app.get("/survey",isLoggedIn, function(req, res){
  res.render("survey");
});

const transporter = nodemailer.createTransport({
  service: 'gmail',
  auth: {
    user: 'eduzonepvtltd@gmail.com',
    pass: 'eduzone12345' 
  }
});

app.post("/survey",isLoggedIn,function(req,res){
  var currentusername=req.body.username;
  console.log("----------------------------------------------");
  console.log(currentusername);
  console.log("-------------------------------------");
  var surveyproblem=req.body.surveyproblem;
  var email= req.body.email;
  console.log(email);
  var newsurvey = new Survey({
    email: req.body.email,
    surveyproblem:req.body.surveyproblem
  })
    newsurvey.save();
    console.log("new survey created");
    console.log(email);
    console.log(surveyproblem);
    if(surveyproblem!==null){ 
      var mailOptions = {
            to: email,
            from: "faustino1@ethereal.email",
            subject: "thanks for giving a feedback for eduzone",
            text:
              "Hello,"+currentusername+"\n\n" + 
              "This is to notify you that we have recieved your review for eduzone and would try our very best to stand up to your expectations\n"+
              "we value your review and would start working towards making eduZone an overall better experience for our valuable users \n \n regards, \n Team EduZone",
          };
          transporter.sendMail(mailOptions, (error, info) => {
            if (error) {
                console.log('Error occurred');
                console.log(error);
                return process.exit(1);
            }
    
            console.log('Message sent successfully!');
            console.log(nodemailer.getTestMessageUrl(info));
            transporter.close();
        });
        }
  
    
    else{
      var mailOptions = {
        to: email,
        from: "faustino1@ethereal.email",
        subject: "eduzone's review",
        text:
          "Hello,\n\n" +
          "This is a confirmation that the password for your account " +
          currentusername +
          " has just been changed.\n",
      };        var mailOptions = {
            to: currentusername,
            from: "faustino1@ethereal.email",
            subject: "thanks for giving a feedback for eduzone",
            text:
              "Hello,"+currentusername+"\n\n" + 
              "This is to notify you that we appreciate your kind gesture of giving us a positive review and we're glad that our appication is being accepted and enjoyed by the users.We would keep bringing more and more features to enhance the overall experience soon \n \n regards, \n Team EduZone",
          };
          transporter.sendMail(mailOptions, (error, info) => {
            if (error) {
                console.log('Error occurred');
                console.log(error.mailOptions);
                return process.exit(1);
            }
    
            console.log('Message sent successfully!');
            console.log(nodemailer.getTestMessageUrl(info));
            transporter.close();
        });
        }
    

    res.redirect("/");
})

app.get("/blog", isLoggedIn, function(req, res){
  res.render("blog");
});


app.get("*",function(req,res){
    res.send("sorry page not found.....");
  });



app.listen(3000,function(){
    console.log("now serving your app");
});