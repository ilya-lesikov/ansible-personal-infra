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

To decrypt secrets in this repo, point environment variable `$ANSIBLE_VAULT_PASSWORD_FILE` to the file containing the password used to encrypt your secrets. This file will be automatically used by `ansible-playbook` command for secrets decryption.

## Role smoke testing

```bash
cd role/$ROLE_NAME
less README   # check out for additional instructions in role's README
molecule test
```

## Deploy to staging and execute end-to-end tests

```bash
vagrant up
```

## Deploy to prod

```bash
ansible-playbook -i environments/prod $PLAYBOOK_NAME
```
