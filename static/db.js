const { Client } = require('pg');

let connectionString = "postgres://qwovfbgagedxak:5b917a80a55b0f5dd22f2c9213a95a58b3c28c1b7e32de0444bd3d48112f0159@ec2-34-230-198-12.compute-1.amazonaws.com:5432/d9gn1i3p7mdrp5";
var pgClient = new Client(connectionString);
pgClient.connect();

var query = pgClient.query("SELECT * from Impuestos");

console.log(query)