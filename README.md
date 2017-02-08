# ScreenCloud - Caddy

This is a plugin that allow you to use [ScreenCloud](https://screencloud.net/) to upload directly to any  
website running [Caddy](https://caddyserver.com/) with the [upload extension](https://caddyserver.com/docs/upload).

It supports "Signature" (HMAC-SHA256) authentication (optional but recommended),  
and has a few other options up its sleeve.

### Installation

Preferences -> Online Services -> More services -> Install from URL:

- <https://github.com/p3lim/screencloud-caddy/releases/download/1.0.2/packaged.zip>

### Settings

![](https://cloud.githubusercontent.com/assets/26496/22751861/7be1912c-ee36-11e6-8b1c-3dd3803d08dd.png)


### Caddy configuration example

```
example.com {
	tls
	root /var/www
	browse /
	upload / {
		to "/var/www"
		hmac_keys_in jon=c25vdw== # base64 encoded secret
	}
}

```
