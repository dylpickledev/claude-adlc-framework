Execute the following actions to clear the 1Password secrets cache and reload fresh values:

1. Remove the cache file: `rm -f $HOME/.da-agent-hub-secrets-cache`
2. Reload secrets from 1Password: `bash ~/dotfiles/load-secrets-from-1password.sh`
3. Verify the new values are loaded (check output)
4. Confirm that the cache has been refreshed with new values from 1Password

This forces an immediate refresh rather than waiting for the 24-hour cache to expire.
