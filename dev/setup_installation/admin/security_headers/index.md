# Security Response Headers { #security-headers }

## Introduction

Hopsworks sets security response headers itself, in its application server, on the UI, its REST endpoints, its error pages and the services it proxies, so they apply whatever sits in front of the cluster: an ingress controller, a load balancer or an OpenShift route.
Each kind of response gets its own set:

| Response | Headers |
| --- | --- |
| The Hopsworks UI | `Content-Security-Policy`, `X-Content-Type-Options: nosniff`, `Strict-Transport-Security`, `Referrer-Policy: same-origin`, `Permissions-Policy`, `Cross-Origin-Opener-Policy: same-origin`, `Cross-Origin-Resource-Policy: same-origin`, `Cache-Control` |
| Hopsworks REST endpoints | `Content-Security-Policy: default-src 'none'; frame-ancestors 'none'`, `X-Content-Type-Options: nosniff`, `Strict-Transport-Security`, `Referrer-Policy: same-origin`, `Cross-Origin-Resource-Policy: same-origin`, `Cache-Control: no-store` unless an endpoint sets its own |
| Hopsworks error pages, such as the page that renews an expired session | The UI's headers, with `Cache-Control: no-store` |
| Services Hopsworks proxies, such as Jupyter, Grafana or Airflow | `X-Content-Type-Options: nosniff`, `Strict-Transport-Security`, `Referrer-Policy: same-origin`; the service's own `Content-Security-Policy` and `Cache-Control`, or the UI's `frame-ancestors` and `private, no-cache` when it sends none; a `304 Not Modified` gets neither fallback, so the browser keeps the headers it cached with the response |

The UI's Content-Security-Policy allows scripts and connections from the Hopsworks origin only, frames from the Hopsworks origin, `blob:` URLs and `https://www.youtube-nocookie.com`, and lets no other site frame the UI.
Other sites cannot embed the UI's files or the REST responses, and a page of another site that the UI opens in a new tab gets no handle to the UI's window.
Browsers check the UI's entry page with Hopsworks on every load, and keep its versioned assets for a year.
No response names the application server or its version.

Cookies set by Hopsworks or by a service it proxies carry `SameSite=Lax`, and `Secure` when the browser reached Hopsworks over HTTPS, also when TLS ends at the ingress.
Hopsworks' own cookies are also `HttpOnly`.
Cookies that the UI or a proxied service reads in the browser, such as Jupyter's `_xsrf`, keep the `HttpOnly` setting the service chose.

## Helm values { #security-headers-values }

The policy is set under `hopsworks.payara.securityHeaders`, listed in [Hopsworks values][helm-values-hopsworks]:

```yaml
hopsworks:
  payara:
    securityHeaders:
      cspMode: enforce
      extraSources:
        connect-src: []
        frame-ancestors: []
      hsts:
        maxAge: 31536000
        includeSubDomains: true
```

- `cspMode`: `enforce` blocks what the Content-Security-Policy forbids.
  `report-only` sends the same policy as `Content-Security-Policy-Report-Only`: the browser reports each violation in its console and blocks nothing.
  The page that shows a system health report keeps an enforced policy in both modes, because it isolates the report's scripts from the UI.
- `extraSources`: sources added to a directive of the UI's policy, one list per directive.
  The directives are `connect-src`, `frame-src`, `img-src`, `font-src`, `script-src`, `style-src`, `form-action` and `frame-ancestors`.
  A source is one CSP source expression, such as `https://serving.example.com:32443`, without spaces, `;` or `,`.
- `hsts.maxAge` and `hsts.includeSubDomains`: the `Strict-Transport-Security` header.
  The defaults match what ingress-nginx sends by default.

The values are rendered into the `<release>-security-headers` ConfigMap.
A `helm upgrade` that only changes these values needs no restart: once Kubernetes updates the mounted file in a pod, usually within one to two minutes, Hopsworks applies it within 30 seconds.

## Model deployments on another host or port { #security-headers-inference }

The UI calls model deployments, for example from the agent chat, at the inference endpoint.
When that endpoint is on another host or port than the Hopsworks UI, add it to `connect-src`:

```yaml
hopsworks:
  payara:
    securityHeaders:
      extraSources:
        connect-src:
          - https://serving.example.com:32443
```

## Embedding Hopsworks in another site { #security-headers-embedding }

The UI can only be framed by Hopsworks itself.
To let another site frame it, add that site to `frame-ancestors`:

```yaml
hopsworks:
  payara:
    securityHeaders:
      extraSources:
        frame-ancestors:
          - https://portal.example.com
```

Browsers check every ancestor of a frame, so the frames the UI opens allow the same sites: the page that shows a system health report, and the services Hopsworks proxies that send no `Content-Security-Policy` of their own.
A proxied service that sends its own policy keeps it.

## When a page does not work { #security-headers-troubleshooting }

A browser blocks what the policy forbids and logs a `Content-Security-Policy` error in its developer console.
To find what a page needs:

1. Set `cspMode: report-only` and run `helm upgrade`.
1. Reload the page until its response carries `Content-Security-Policy-Report-Only` instead of `Content-Security-Policy`, which can take up to two and a half minutes, then read the console: each violation names the directive and the blocked source.
1. Add the sources the page needs to `extraSources`, set `cspMode: enforce` again and run `helm upgrade`.

## Strict-Transport-Security { #security-headers-hsts }

With `Strict-Transport-Security`, a browser that has visited Hopsworks only uses HTTPS for its host, and with `includeSubDomains` for every subdomain of it, until `maxAge` runs out.
Every service on that host and those subdomains must then be served over HTTPS, the inference endpoint included, whatever its port.

To undo it, set `maxAge: 0` and run `helm upgrade`: a browser that receives the header over HTTPS forgets the host.
ingress-nginx adds a `Strict-Transport-Security` header of its own by default, so behind it the controller's `hsts` settings need the same change.
