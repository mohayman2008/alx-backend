import { createClient, print as redisPrint } from 'redis';

const client = createClient()
  .on('error', (err) => console.log('Redis client not connected to the server:', err.message))
  .on('connect', () => console.log('Redis client connected to the server'));

function setNewSchool(schoolName, value) {
  client.set(schoolName, value, redisPrint);
}

function displaySchoolValue(schoolName) {
  client.get(schoolName, (err, reply) => { console.log(reply); });
}

displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');
