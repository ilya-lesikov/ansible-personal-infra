# ansible-personal-infra

Automation of personal infrastructure

## Usage

```bash
pip3 install --user ansible

# install required python packages
pip3 install --user requirements.txt

# install required role dependencies with ansible-galaxy
find roles/ -name "requirements.y*ml" -exec ansible-galaxy install -r '{}' \;
```

## Role smoke testing

```bash
cd role/role_name
# check out for additional instructions in role's README
less README
molecule test
```

## Staging env smoke testing

```bash
vagrant up
```
