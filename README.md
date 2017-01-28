# ScreenCloud - Caddy

This is a plugin that allow you to use [ScreenCloud](https://screencloud.net/) to upload directly to any  
website running [Caddy](https://caddyserver.com/) with the [upload extension](https://caddyserver.com/docs/upload).

It supports "Signature" (HMAC-SHA256) authentication (optional but recommended),  
and has a few other options up its sleeve.

### Installation

Preferences -> Online Services -> More services -> Install from URL:

- <https://github.com/p3lim/screencloud-caddy/releases/download/1.0.1/packaged.zip>

### Settings

![](https://cloud.githubusercontent.com/assets/26496/19211114/4be5cb94-8d35-11e6-8796-66b80044b834.png)


### Caddy configuration example

```
example.com {
	tls
	root /var/www
	browse /
	upload / {
		to "/var/www"
		hmac_keys_in john=c25vdw== # base64 encoded secret
	}
}

```
