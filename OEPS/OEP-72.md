<pre>
  OEP: 72
  Title: DDXF DToken+Agent Standard
  Author: lucas7788<sishsh@163.com>
  Type: Standard
  Status: Accepted
  Created: 2018-07-03
</pre>

## Abstract

Sub-contract of DDXF series, a standard proposal to combine off-chain access-token (tokenization) with on-chain token (assertization). Provides support for data management, esp., the permission control. This contract is a basic version for DToken, which cannot be retransferred. For the rest DToken contracts, which support OEP4, OEP5, and OEP8.
Support the Agent to use tokens.

## Motivation

As an important component of DDXF, the authority management of data is managed in the form of on-chain tokens, including data authorization management and data operation authentication, supporting the management of data operation processes in the data life cycle, and using on-chain traceability And the ability to confirm rights enables data rights management to support cross-system interoperability.
According to different token characteristics, it can be further extended. This OEP is the basic data token + Agent. On top of the basic data token, the Agent is supported to use the token.

## Specification

### Methods

For methods related to the DToken standard, please refer to
[[https://github.com/ontio/OEPs/blob/master/OEPS/OEP-71.mediawiki|DToken]] and it's extensions.


#### useTokenByAgent

```rust
fn use_token_by_agent(account: &Address, agent: &Address, token_id: &[u8], n: U128) -> bool
```

Use token by agent, the agent of the token has the right to invoke this method.

|Parameter | Type |  Desc |
|----------|------|--------|
| account | &Address | buyer address
| agent | &Address | agent address
| token_id | &[u8] | the number of purchases
| n | U128 | the number of consuming token

Event

```
["useTokenByAgent", account,agent, token_id, n]
```

#### addTokenAgents

```rust
fn add_token_agents(
    account: &Address,
    token_id: &[u8],
    agents: &[Address],
    n: Vec<U128>,
) -> bool
```

This method only append agents for the specified token.

|Parameter | Type |  Desc |
|----------|------|--------|
| account | &Address | buyer address
| token_id | &[u8] | token id
| agents | &[Address] | the array of agent address
| n | Vec<U128> | number of authorizations per agent

Event

```
[ ["addTokenAgents", account, token_id, agent, n] ]
```

#### addAgents

```rust
fn add_agents(
    account: &Address,
    agents: Vec<Address>,
    n: Vec<U128>,
    token_ids: Vec<Vec<u8>>,
) -> bool
```

This method only append agents for the specified token.

|Parameter | Type |  Desc |
|----------|------|--------|
| account | &Address | buyer address
| agents | &[Address] | the array of agent address
| n | Vec<U128> | number of authorizations per agent
| token_id | Vec<Vec<u8>> | token ids

Event

```
[ ["addTokenAgents", account, token_id, agent, n] ]
```


#### removeTokenAgents

```rust
fn remove_token_agents(account: &Address, token_id: &[u8], agents: &[Address]) -> bool
```

This method only append agents for the specified token.

|Parameter | Type |  Desc |
|----------|------|--------|
| account | &Address | buyer address
| token_id | &[u8] | token id
| agents | &[Address] | the array of agent address

Event

```
[ ["removeTokenAgents", account, token_id] ]
```


### Implementation


Please refer to [[https://github.com/ontio/OEPs/blob/master/OEPS/OEP-73.mediawiki|OEP-73]],
[[https://github.com/ont-bizsuite/ddxf-contract-suite/tree/master/contracts/dtoken|DToken+Agent+Oep8]].
