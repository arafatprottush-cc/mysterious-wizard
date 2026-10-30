# /preflight

Before starting any task:

1. Confirm the active workspace path.
2. Confirm sandbox/container status.
3. Report the active terminal and permission policy.
4. Verify the available terminal permission options in Settings.
5. Recommend the most restrictive usable policy.
6. Confirm the browser profile is separate, has no logins or wallet
   extensions, and has an appropriate domain allowlist.
7. Check for accidentally exposed secrets without printing their values.
8. Confirm .gitignore and security scanning configuration.
9. Check Git status and confirm existing work will be preserved.
10. Confirm CI status if a remote repository already exists.
11. Report anything missing, unsafe, or UNVERIFIED.
12. STOP if any critical safety check fails.
