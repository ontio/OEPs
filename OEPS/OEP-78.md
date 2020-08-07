```
  OEP: 78
  Title: DDXF SplitPolicy Standard
  Author: lucas7788<sishsh@163.com>
  Type: Standard
  Status: Accepted
  Created: 2020-08-03
```

## Abstract


The contract is used to determine the profit distribution strategy of multiple owners of DToken.


## Motivation

There may be multiple owners of DToken on the chain, and each owner's share of profit distribution is different. The specific allocation can be set in this contract.

## Specification

### Methods

#### register

```rust
pub fn register(key: &[u8], param_bytes: &[u8]) -> bool{}
```

Register the dividend distribution strategy on the chain.

The RegisterParam is defined as follow:
```rust
#[derive(Encoder, Decoder)]
pub struct RegisterParam {
    addr_amt: Vec<AddrAmt>,  //Address and share for agreed profit distribution
    token_type: TokenType,   //The currency used for the agreed fee. Ont, ong and oep4 are currently supported
    contract_addr: Option<Address>,//If it is an oep4 token, the address where the oep4 contract needs to be executed
}
#[derive(Encoder, Decoder, Clone)]
pub struct AddrAmt {
    to: Address,
    weight: u32,
    has_withdraw: bool,
}
```


The parameters are of the following type:

| Parameter | Type | Description|
|-----------|-------|-----------|
| key | &[u8] | also called resource_id in the other contract, used to mark the uniqueness of dividend strategy
| param_bytes | &[u8] | the serialization result of FeeSplitModel

Event

This method will launch the following events:
```
["register", key, param_bytes]
```


#### getRegisterParam

```rust
pub fn get_register_param(key: &[u8]) -> RegisterParam{}
```

Query RegisterParam by key.

The parameters are of the following type:

| Parameter | Type | Description|
|-----------|-------|-----------|
| key | &[u8] | key is also called resource_id in the other contract, used to mark the uniqueness of dividend strategy


#### transfer

```rust
pub fn transfer(from: &Address, key: &[u8], amt: U128) -> bool{}
```

Transfer token assets to current contract address.

The parameters are of the following type:

| Parameter | Type | Description|
|-----------|-------|-----------|
| from | &Address | buyer address
| key | &[u8] | Commodity ID
| amt | U128 | Fees paid by the buyer

Event

```
["transfer", from, key, amt]
```

#### getBalance

```rust
pub fn get_balance(key: &[u8]) -> U128{}
```

Query balance by commodity ID

| Parameter | Type | Description|
|-----------|-------|-----------|
| key | &[u8] | commodity ID


#### withdraw

```rust
pub fn withdraw(key: &[u8], addr: &Address) -> bool{}
```

The data owner withdraw token from the contract.

| Parameter | Type | Description|
|-----------|-------|-----------|
| key | &[u8] | commodity ID
| addr | &Address | the address who withdraw token, need the address signature

Event

```
["withdraw", key, addr]
```

#### transferWithdraw

```rust
pub fn transfer_withdraw(from: &Address, key: &[u8], amt: U128) -> bool{}
```

The buyer pays the fee and sends the fee directly to the data owner.

| Parameter | Type | Description|
|-----------|-------|-----------|
| from | &Address | buyer address
| key | &[u8] | commodity ID
| amt | U128 | Fees paid by the buyer

Event

```
["transferWithdraw", from, key, amt]
```

### Implementation

[OEP-78](https://github.com/ont-bizsuite/ddxf-contract-suite/tree/master/contracts/split_policy)