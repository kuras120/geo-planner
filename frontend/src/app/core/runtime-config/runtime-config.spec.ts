import { RuntimeConfigError, parseRuntimeConfig } from './runtime-config';

describe('parseRuntimeConfig', () => {
  it('accepts a same-origin API path', () => {
    expect(parseRuntimeConfig({ apiBaseUrl: '/api' })).toEqual({ apiBaseUrl: '/api' });
  });

  it.each([undefined, {}, { apiBaseUrl: 'https://provider.example' }, { apiBaseUrl: '//host' }])(
    'rejects unsafe or incomplete input: %s',
    (value) => {
      expect(() => parseRuntimeConfig(value)).toThrow(RuntimeConfigError);
    },
  );
});
