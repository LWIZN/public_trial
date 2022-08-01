describe('line-notify-nodejs', () => {
  const mockAxios = require('axios');
  jest.mock('axios');

  test('Notify should be sent', async () => {
    const target = require('./index')('token');

    await target.notify({
      message: 'message',
    });

    expect(mockAxios.post.mock.calls.length).toBe(1);
  });

  test('Token required error', () => {
    const target = require('./index');
    try {
      target(null);
      expect(1).toBe(2);
    } catch (e) {
      expect(e.message).toEqual('token is required');
    }
  });

  test('Message required error', async () => {
    const target = require('./index')('token');
    try {
      await target.notify({
        message: null,
      });
      expect(1).toBe(2);
    } catch (e) {
      expect(e.message).toEqual('message is required');
    }
  });
});
