import { createClient, print as redisPrint } from 'redis';
import { promisify } from 'util';

const client = createClient()
  .on('error', (err) => console.log('Redis client not connected to the server:', err.message))
  .on('connect', () => console.log('Redis client connected to the server'));
const getAsync = promisify(client.get).bind(client);

function setNewSchool(schoolName, value) {
  client.set(schoolName, value, redisPrint);
}

async function displaySchoolValue(schoolName) {
  console.log(await getAsync(schoolName).catch((err) => { console.log(err); }));
}

async function asyncMain() {
  await displaySchoolValue('Holberton');
  setNewSchool('HolbertonSanFrancisco', '100');
  await displaySchoolValue('HolbertonSanFrancisco');
}

asyncMain();
