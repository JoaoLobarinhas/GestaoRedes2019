var Configs = require('../models/configs')

module.exports.listar=()=>{
    return Configs.find().exec()
}

module.exports.getId=id=>{
    return Configs.find({_id:id}).exec()
}

module.exports.getProcess=(id,process)=>{
    return (Configs.aggregate([ {"$match":{"_id":id}},  
    {"$project":{"data.process":1,"data.updateTime":1}}, 
    {"$unwind":"$data"}, 
    {"$unwind":"$data.process"}, 
    {"$match":{"data.process.name":process}}]))
}

module.exports.getProcessUnique=(id)=>{
    return (Configs.aggregate([ {"$match":{"_id":id}},  
    {"$project":{"data.process":1}}, 
    {"$unwind":"$data"}, 
    {"$unwind":"$data.process"},
    {"$group": {_id: null, uniqueValues: {$addToSet: "$data.process.name"}}},
    ]))
}
