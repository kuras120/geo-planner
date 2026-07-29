import { Injectable } from '@angular/core';

const CONFIG_VALIDATION_ORIGIN = 'https://runtime-config.invalid';

export interface RuntimeConfig {
  readonly apiBaseUrl: string;
}

export class RuntimeConfigError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'RuntimeConfigError';
  }
}

function isSameOriginAbsolutePath(value: string): boolean {
  try {
    return (
      value.startsWith('/') &&
      new URL(value, CONFIG_VALIDATION_ORIGIN).origin === CONFIG_VALIDATION_ORIGIN
    );
  } catch {
    return false;
  }
}

export function parseRuntimeConfig(value: unknown): RuntimeConfig {
  if (typeof value !== 'object' || value === null || !('apiBaseUrl' in value)) {
    throw new RuntimeConfigError('Runtime configuration must define apiBaseUrl.');
  }

  const { apiBaseUrl } = value;
  if (typeof apiBaseUrl !== 'string' || !isSameOriginAbsolutePath(apiBaseUrl)) {
    throw new RuntimeConfigError('apiBaseUrl must be a same-origin absolute path.');
  }

  return Object.freeze({ apiBaseUrl });
}

@Injectable({ providedIn: 'root' })
export class RuntimeConfigService {
  #config: RuntimeConfig | undefined;

  get value(): RuntimeConfig {
    if (!this.#config) {
      throw new RuntimeConfigError('Runtime configuration has not been loaded.');
    }

    return this.#config;
  }

  async load(): Promise<void> {
    const response = await fetch('/runtime-config.json', {
      cache: 'no-store',
      headers: { Accept: 'application/json' },
    });

    if (!response.ok) {
      throw new RuntimeConfigError(`Runtime configuration returned HTTP ${response.status}.`);
    }

    this.#config = parseRuntimeConfig(await response.json());
  }
}
