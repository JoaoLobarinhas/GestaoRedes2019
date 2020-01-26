var express = require('express');
var axios = require('axios')
var lhost = require('../configs/env').hostApi
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  axios.get('http://localhost:3000/api/')
    .then(data=>{
      res.render('index', {data:data.data});
    })
    .catch(erro=>res.render('error', { error:erro }))
});

router.get('/:id', function(req, res, next) {
  if(req.query.name){
    axios.get('http://localhost:3000/api/'+req.params.id+"?name="+req.query.name)
      .then(data=>{
        console.log(data.data)
        res.render('detailProcess', {data:data.data, dataId: data.data[0]._id})
      })
      .catch(erro=>res.render('error', { error:erro }))
  }
  else{
    axios.get('http://localhost:3000/api/'+req.params.id)
    .then(data=>{
      let datas = data.data[0]
      axios.get('http://localhost:3000/api/'+req.params.id+"?unique=true")
        .then(dataUnique=>{
          let dataU = dataUnique.data
          res.render('detail', {data:datas, dataU:dataU})
        })
        .catch(erro=>res.render('error', { error:erro }))
    })
    .catch(erro=>{
      if(erro.response.status == 500){
        res.render('error', { message:"Id not found", error:erro })
      }
      else{
        res.render('error', { error:erro })
      }
    })
  }
});

module.exports = router;
