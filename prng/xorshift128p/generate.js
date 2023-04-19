const arr = Array.from(Array(128 + 8), Math.random)
process.stdout.write("sequence = ")
console.dir(arr, {'maxArrayLength': null})
console.log("next =", Math.random())

//console.log(arr)
