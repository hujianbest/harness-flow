export interface HttpRequestInit {
  method: string;
  headers?: Record<string, string>;
  body?: string;
}

export interface HttpResponse {
  status: number;
  body: string;
}

export interface HttpClient {
  request(url: string, init: HttpRequestInit): Promise<HttpResponse>;
}

/**
 * Test double used by the walking-skeleton e2e test. Records every request
 * and never opens a socket — required by ADR-0003 + NFR-Testability-1.
 */
export interface RecordedRequest {
  url: string;
  method: string;
  headers: Record<string, string>;
  body: string;
}

export class RecordingHttpClient implements HttpClient {
  public readonly requests: RecordedRequest[] = [];

  async request(url: string, init: HttpRequestInit): Promise<HttpResponse> {
    this.requests.push({
      url,
      method: init.method,
      headers: init.headers ?? {},
      body: init.body ?? '',
    });
    return { status: 201, body: JSON.stringify({ id: 'recorded-id' }) };
  }
}

/**
 * Production HttpClient backed by Node 20+'s built-in fetch.
 *
 * Per ADR-0003, this client is NOT exercised by the walking-skeleton tests
 * (the e2e test injects RecordingHttpClient). It exists so a future real
 * Medium integration does not need to re-design the boundary.
 */
export class Node20FetchHttpClient implements HttpClient {
  async request(url: string, init: HttpRequestInit): Promise<HttpResponse> {
    const response = await fetch(url, {
      method: init.method,
      headers: init.headers,
      body: init.body,
    });
    const body = await response.text();
    return { status: response.status, body };
  }
}
