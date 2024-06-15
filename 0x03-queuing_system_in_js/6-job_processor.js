import { createQueue } from 'kue';

const Q_NAME = 'push_notification_code';

const queue = createQueue();

function sendNotification(phoneNumber, message) {
  console.log(`Sending notification to ${phoneNumber}, with message: ${message}`);
}

queue.process(Q_NAME, ({ data }, done) => {
  sendNotification(data.phoneNumber, data.message);
  done();
});
