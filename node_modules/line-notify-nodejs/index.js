'use strcit';

const axios = require('axios');
const qs = require('querystring');
const BASE_URL = 'https://notify-api.line.me';
const PATH = '/api/notify';

module.exports = (token) => {
  if (!token) {
    throw new Error('token is required');
  }

  return {
    notify: async (params) => {
      if (!params.message) {
        throw new Error('message is required');
      }

      const options = {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'Authorization': `Bearer ${token}`,
        },
      };

      await axios.post(`${BASE_URL}${PATH}`, qs.stringify(params), options);
    },
  };
};
