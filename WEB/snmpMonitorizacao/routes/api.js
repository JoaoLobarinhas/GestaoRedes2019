var express = require('express');
var router = express.Router();
var Configs = require('../controllers/configs')
var mongoose = require('mongoose')

/* GET users listing. */
router.get('/', function(req, res, next) {
  Configs.listar()
    .then(dados=>res.jsonp(dados))
    .catch(erro=>res.status(500).jsonp(erro))
});

router.get('/:id', function(req, res, next) {
  if(req.query.unique){
    Configs.getProcessUnique(mongoose.Types.ObjectId(req.params.id))
      .then(dados=>res.jsonp(dados))
      .catch(erro=>res.status(500).jsonp(erro))
  }
  else if(req.query.name){
    Configs.getProcess(mongoose.Types.ObjectId(req.params.id),req.query.name)
      .then(dados=>res.jsonp(dados))
      .catch(erro=>res.status(500).jsonp(erro))
  }
  else{
    Configs.getId(req.params.id)
      .then(dados=>res.jsonp(dados))
      .catch(erro=>res.status(500).jsonp(erro))
  }
});


module.exports = router;
