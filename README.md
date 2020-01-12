Tezos boilerplate : Pascal LiGo + PyTezos
===

> Boilerplate for developing Tezos smart contracts with Pascal Ligo and testing them with PyTezos

Prerequisites
---

### Ligo

```bash
curl https://gitlab.com/ligolang/ligo/raw/dev/scripts/installer.sh | bash -s "next"
```

### Python 3.6+

Create Python virtual environment
```
python3 -m venv ./venv
```
Activate Python virtual environment (remember to do this every time your open this project in a new terminal)
```
source ./venv/bin/activate
```

Quick Start
---

 - ``npm i`` Install Node dependencies
 - ``npm run init`` Initialize the project (will copy file, setup python, and install python dependencies)

Compile
---

 - ``npm run compile -- "src/contracts/<path to ligo file>"`` Compile a single Ligo smart contract
 - ``npm run compile:all`` Compile all Ligo smart contracts under ``src/contracts``
 - ``npm run compile:all:watch`` Compile all Ligo smart contracts under ``src/contracts`` whenever they change

Test
---

 - ``npm run test`` Run all tests
 - ``npm run test:watch`` Run all tests in watch mode

Suggested
---

Compile contracts on change in one terminal window:
```
npm run compile:all:watch
```
And run all tests in watch mode in another terminal window:
```
npm run test:watch
```
Then as you work on you contracts or tests everything (compilation and test re-running) will happen automatically

Additional Docs
---

 - [IDE Setup](docs/ide-intellij-python.md)
