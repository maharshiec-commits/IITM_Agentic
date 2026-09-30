# KB-VPN-001 — VPN Authentication Failed (Windows)

## Symptoms
- VPN shows "Authentication failed"
- Often happens after password change or cached credentials

## Steps
1. Confirm username format: corp\username
2. Sync system time (important for auth)
3. Clear cached credentials
4. Re-import VPN profile if needed

## Notes
If repeated failures occur, escalate to L2 with event logs and VPN client version.
