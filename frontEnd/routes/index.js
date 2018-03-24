var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next)
{
  res.render('index', { title: 'Express' });
});

/* GET user page. */
router.get('/userPage',function(req,res,next)
{
  //res.redirect('/userPage');
  res.render('userPage',{title: 'UserPage' });
});

/* GET timeOut page. */
router.get('/userPage/timeOut',function(req,res,next)
{
  res.render('timeOut',{title: 'timeOut' });
});

/* GET admin page. */
router.get('/admin',function(req,res,next)
{
  res.render('admin',{title: 'admin'});
});

/* GET adminCertainRoom page. */
router.get('/admin/adminCertainRoom',function(req,res,next)
{
  res.render('adminCertainRoom',{title: 'adminCertainRoom'});
});

module.exports = router;
