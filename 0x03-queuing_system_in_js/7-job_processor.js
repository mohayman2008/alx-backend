import { createQueue } from 'kue';

const Q_NAME = 'push_notification_code_2';
const CONCURRENT_JOBS_COUNT = 2;
const BLACKLIST = ['4153518780', '4153518781'];

const queue = createQueue();

function sendNotification(phoneNumber, message, job, done) {
  job.progress(0, 100);
  if (BLACKLIST.includes(phoneNumber)) {
    return done(new Error(`Phone number ${phoneNumber} is blacklisted`));
  }

  job.progress(50, 100);
  console.log(`Sending notification to ${phoneNumber}, with message: ${message}`);
  return done();
}

queue.process(Q_NAME, CONCURRENT_JOBS_COUNT, (job, done) => {
  sendNotification(job.data.phoneNumber, job.data.message, job, done);
});
