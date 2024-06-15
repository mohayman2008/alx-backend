module.exports = {
  env: {
    browser: false,
    es6: true,
    jest: true,
  },
  extends: [
    'airbnb-base',
    'plugin:jest/all',
  ],
  globals: {
    Atomics: 'readonly',
    SharedArrayBuffer: 'readonly',
  },
  parserOptions: {
    ecmaVersion: 2018,
    sourceType: 'module',
  },
  plugins: ['jest'],
  rules: {
    'max-classes-per-file': 'off',
    'no-underscore-dangle': 'off',
    'no-console': 'off',
    'no-shadow': 'off',
    'prefer-arrow-callback': 'off',
    'func-names': 'off',
    'jest/prefer-expect-assertions': 'off',
    'jest/valid-expect': 'off',
    'jest/lowercase-name': 'off',
    'jest/no-hooks': 'off',
    'jest/no-test-callback': 'off',
    'curly': 'off',
    'nonblock-statement-body-position': 'off',
    'no-use-before-define': 'off',
    'no-restricted-syntax': [
      'error',
      'LabeledStatement',
      'WithStatement',
    ],
  },
  overrides:[
    {
      files: ['*.js'],
      excludedFiles: 'babel.config.js',
    }
  ]
};
