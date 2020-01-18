# ansible-personal-infra
Automation of personal infrastructure

## Prepare
```bash
pip3 install --user ansible

# install required python packages
pip3 install --user requirements.txt

# install required role dependencies with ansible-galaxy
find -name "requirements.y*ml" -exec ansible-galaxy install -r '{}' \;
```

### Secrets
My encrypted secrets stored in another place. Symlink them to `environments/`, e.g. `ln -sr path/to/real/001_cross_env_secrets.yml environments/prod/host_vars/001_cross_env_secrets.yml`.
To decrypt these Ansible-encrypted secrets, point environment variable `$ANSIBLE_VAULT_PASSWORD_FILE` to the file containing the password used to encrypt them. This file will be automatically used by command `ansible-playbook` for decryption.

## Testing

### Role-level smoke tests
```bash
cd role/$ROLE_NAME
less README   # check out for additional instructions in role's README
molecule test
```

### End-to-end tests in a staging environment
```bash
vagrant up
```

## Deploy to prod
```bash
ansible-playbook -i environments/prod $PLAYBOOK_NAME
```
