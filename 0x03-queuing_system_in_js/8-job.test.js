import { expect } from 'chai';
import kue from 'kue';
import createPushNotificationsJobs from './8-job';

const Q_NAME = 'push_notification_code_3';
const queue = kue.createQueue();

/* eslint-disable no-undef */
describe('createPushNotificationsJobs', function () {
  before(function () {
    queue.testMode.enter();
  });

  afterEach(function () {
    queue.testMode.clear();
  });

  after(function () {
    queue.testMode.exit();
  });

  it('throws the right error when <jobs> is not an array', function (done) {
    const jobsData = { 0: { xyz: 'abc' }, 1: { num: 123 } };
    expect(() => createPushNotificationsJobs(jobsData, queue)).to.throw('Jobs is not an array');

    const { jobs } = queue.testMode;
    expect(jobs.length).to.be.equal(0);
    done();
  });

  it('creates jobs in the right queue with the right data', function (done) {
    const jobsData = [
      {
        phoneNumber: '4153518780',
        message: 'This is the code 1234 to verify your account',
      },
      {
        phoneNumber: '5153518780',
        message: 'This is the code 8844 to verify your account',
      },
    ];

    createPushNotificationsJobs(jobsData, queue);
    const { jobs } = queue.testMode;

    expect(jobs.length).to.be.equal(2);
    expect(jobs[0].id).not.to.be.equal(jobs[1].id);

    expect(jobs[0].type).to.be.equal(jobs[1].type).to.be.equal(Q_NAME);
    expect(jobs[0].data).to.be.equal(jobsData[0]);
    expect(jobs[1].data).to.be.equal(jobsData[1]);
    done();
  });
});
