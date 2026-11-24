# Lessons: AWS

Part of [lessons.md](../lessons.md), kept apart so it stays short. Read it before any AWS work; numbers are shared with the main file.

## AWS

9. An internal service on a public URL still needs auth: make service-to-service URLs IAM-only.
10. A new IAM role isn't usable for a few seconds: rerun the apply; don't change a trust policy that's right.
11. Cognito names allow only letters, digits, spaces and `+=,.@-`: keep apostrophes out of AWS names; descriptions are fine.
12. The base Python image's `pip` bundles old `urllib3`, `msgpack` and `setuptools`, and lags Debian's fixes, failing the image scan: runtime stages uninstall `pip` and run `apt-get upgrade`.
14. CloudFront's `web_acl_id` is optional and computed, so `null` leaves an attached web ACL in place: set `""` to detach, `null` only where Firewall Manager owns it.
28. A role is capped by the bootstrap's permissions boundary as well as its own policy, and a refused call can fail silently (an audit-bucket copy): add a new resource to the boundary in the same PR, and say the bootstrap needs redeploying.
