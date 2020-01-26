var mongoose = require('mongoose')

var ProcesShema = new mongoose.Schema({
    oid:String,
    name:String
})

var CpuSchema = new mongoose.Schema({
    usage:String,
    system:String,
    idle:String
})

var RamSchema = new mongoose.Schema({
    size:String,
    freeSpace:String,
    usedSpace:String,
    shared:String,
    buffer:String,
    cache:String

})

var DisckSchema = new mongoose.Schema({
    space:String,
    usedPerc:String,
    spaceused:String
})

var PacketsSchema = new mongoose.Schema({
    recvPackets:String,
    transPackets:String,
    recvPacketsIp:String,
    transPacketsIp:String 
})

var DataSchema = new mongoose.Schema({
    updateTime:String,
    upTime:String,
    computerName:String,
    networkIp:String,
    interfaces:String,
    packets: [PacketsSchema],
    disk:[DisckSchema],
    ram:[RamSchema],
    cpu:[CpuSchema],
    process:[ProcesShema]
})

var ConfigsSchema = new mongoose.Schema({
    ip:{type:String, required:true},
    port:{type:String, required:true},
    lastupdate:String,
    repTime:String,
    data:[DataSchema],
    active:{type:String, required:true, default:"true"}
})

module.exports=mongoose.model('configs',ConfigsSchema)