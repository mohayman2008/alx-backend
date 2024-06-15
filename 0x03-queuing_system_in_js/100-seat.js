import { promisify } from 'util';
import express from 'express';
import { createQueue } from 'kue';
import { createClient } from 'redis';

/* eslint-disable no-unused-vars */
const Q_NAME = 'reserve_seat';
// let available = 50;
let reservationEnabled = true;

const redis = createClient()
  .on('error', (err) => console.log('Redis client not connected to the server:', err.message))
  .on('connect', () => console.log('Redis client connected to the server'));
const redisGetAsync = promisify(redis.get).bind(redis);

redis.set('available_seats', 50);

const queue = createQueue();

const app = express();
const PORT = 1245;

app.listen(PORT, () => {
  console.log(`Express app started on port ${PORT}`);
});

app.get('/available_seats', async (req, res) => {
  const result = {
    numberOfAvailableSeats: await getCurrentAvailableSeats(),
  };
  res.json(result);
});

app.get('/reserve_seat', async (req, res) => {
  res.type('application/json');
  res.send(await reserveSeatHandler());
});

app.get('/process', async (req, res) => {
  res.type('application/json');
  res.send('{ "status": "Queue processing" }');
  await queue.process(Q_NAME, queueProcessor);
});

async function getCurrentAvailableSeats() {
  const value = await redisGetAsync('available_seats');
  return value;
}

function reserveSeat(number) {
  redis.set('available_seats', number);
}

async function reserveSeatHandler() {
  if (!reservationEnabled)
    return '{ "status": "Reservation are blocked" }';

  const job = queue.createJob(Q_NAME, 1);
  const saveJob = promisify(job.save).bind(job);

  const err = await saveJob();
  if (err)
    return '{ "status": "Reservation failed" }';

  job
    .on('complete', (result) => {
      console.log(`Seat reservation job ${job.id} completed`);
    })
    .on('failed', (errorMessage) => {
      console.log(`Seat reservation job ${job.id} failed: ${errorMessage}`);
    });

  return '{"status":"Reservation in process"}';
}

async function queueProcessor(job, done) {
  let available = Number(await getCurrentAvailableSeats());

  if (available <= 0) {
    reservationEnabled = false;
    done(new Error('Not enough seats available'));
  }
  available -= 1;
  if (available === 0) reservationEnabled = false;

  reserveSeat(available);
  done();
}
