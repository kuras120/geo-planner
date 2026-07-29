import { ApplicationErrorHandler } from './application-error-handler';

describe('ApplicationErrorHandler', () => {
  it('exposes an unhandled error state', () => {
    const consoleError = vi.spyOn(console, 'error').mockImplementation(() => undefined);
    const handler = new ApplicationErrorHandler();

    handler.handleError(new Error('test'));

    expect(handler.hasUnhandledError()).toBe(true);
    expect(consoleError).toHaveBeenCalledOnce();
    consoleError.mockRestore();
  });
});
