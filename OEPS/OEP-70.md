```
  OEP: 70
  Title: DDXF Marketplace Standard
  Author: lucas7788<sishsh@163.com>
  Type: Standard
  Status: Accepted
  Created: 2020-08-03
```

## Abstract

The contract is used to publish, update and delete the goods on the chain, and users can purchase them.

## Motivation

Sub-contract of DDXF series, provides a place for token/DToken owner to manage their published items, and enable token exchange between token owner and token acquiers.As an important component of DDXF, it provides a matching and transaction environment for assetized data, including the release and management of assetized data, and supports data transmission and exchange in the data life cycleData auditing, arbitration challenge and other services can be extended. This OEP is the basic Marketplace and only supports the release, update, deletion, and trading of data assets.

## Specification
### Methods
#### init

```
fn init(dtoken: Address, split_policy: Address) -> bool
```

This method will store the default [dtoken contract address](https://github.com/ontio/OEPs/blob/master/OEPS/OEP-73.mediawiki) and [split_policy contract address](https://github.com/ontio/OEPs/blob/master/OEPS/OEP-78.md),only the admin has the right to invoke this method.

The parameters are of the following type:

| Parameter    | Type    |   Desc                        |
| ------------ | ------- | ----------------------------- |
| dtoken       | Address | dtoken contract address       |
| split_policy | Address | split_policy contract address |

#### dtokenSellerPublish

```
pub fn dtoken_seller_publish(
    resource_id: &[u8],
    resource_ddo_bytes: &[u8],
    item_bytes: &[u8],
    split_policy_param_bytes: &[u8],
) -> bool
```

The seller publishes goods on the chain by calling this method.

ResourceDDO struct defined as follow:

```
#[derive(Clone, Encoder, Decoder)]
pub struct ResourceDDO {
    pub manager: Address,  // data owner
    pub item_meta_hash: H256,
    pub dtoken_contract_address: Vec<Address>, // can be empty
    pub accountant_contract_address: Option<Address>, // can be empty
    pub split_policy_contract_address: Option<Address>, //can be empty
}
```

This ResourceDDO contains three optional fields, [dtoken contract address](https://github.com/ontio/OEPs/blob/master/OEPS/OEP-73.mediawiki), [accountant contract address](https://github.com/ontio/OEPs/blob/master/OEPS/OEP-77.md) and [split_policy contract address](https://github.com/ontio/OEPs/blob/master/OEPS/OEP-78.md).

If dtoken_contract_address is not set, the default dtoken contract address will be used.If accountant_contract_address is not set, the MP will not be charged for the purchase.If split_policy_contract_address is not set, the default split policy contract address will be used.

DTokenItem struct defined as follow:

```
#[derive(Clone, Encoder, Decoder)]
pub struct DTokenItem {
    pub fee: Fee, //Commodity charge information, token type, token contract address and commodity unit price.
    pub expired_date: u64, //Commodity expiration time.
    pub stocks: u64, //Commodity stocks.
    pub sold: u64,// The number of items sold.
    pub token_template_ids: Vec<Vec<u8>>,// token_template_id array,token_template_id is used to mark the uniqueness of the TokenTemplate in the DToken contract.
}
```

Fee struct defined as follow:

```
#[derive(Encoder, Decoder, Clone)]
pub struct Fee {
    pub contract_addr: Address,//Token contract address.
    pub contract_type: TokenType,//contract type, support ont, ong, oep4.
    pub count: u64, //unit price.
}
#[derive(Clone)]
pub enum TokenType {
    ONT,
    ONG,
    OEP4,
}
```

RegisterParam struct defined as follows:

```
#[derive(Encoder, Decoder, Clone)]
pub struct AddrAmt {
    to: Address,
    weight: u32,
    has_withdraw: bool,
}
#[derive(Encoder, Decoder)]
pub struct RegisterParam {
    addr_amt: Vec<AddrAmt>,
    token_type: TokenType,
    contract_addr: Option<Address>,
}
```

The parameters are of the following type:

| Parameter                | Type  | Desc                                             |
| ------------------------ | ----- | ------------------------------------------------ |
| resource_id              | &[u8] | used to mark the only commodity in the chain     |
| resource_ddo_bytes       | &[u8] | the result of ResourceDDO struct serialization   |
| item_bytes               | &[u8] | the result of DTokenItem struct serialization    |
| split_policy_param_bytes | &[u8] | the result of RegisterParam struct serialization |

Event

```
["dtokenSellerPublish", resource_id, resource_ddo_bytes, item_bytes, split_policy_param_bytes]
```

#### update

```
fn update(
    resource_id: &[u8],
    resource_ddo_bytes: &[u8],
    item_bytes: &[u8],
    split_policy_param_bytes: &[u8],
) -> bool
```

The seller calls this method to update the information of the goods on the chain.

| Parameter                | Type  | Desc                                             |
| ------------------------ | ----- | ------------------------------------------------ |
| resource_id              | &[u8] | used to mark the only commodity in the chain     |
| resource_ddo_bytes       | &[u8] | the result of ResourceDDO struct serialization   |
| item_bytes               | &[u8] | the result of DTokenItem struct serialization    |
| split_policy_param_bytes | &[u8] | the result of RegisterParam struct serialization |

Event

```
["update", resource_id, resource_ddo_bytes, item_bytes, split_policy_param_bytes]
```

#### delete

```
pub fn delete(resource_id: &[u8]) -> bool
```

Sellers delete items on the chain

| Parameter   | Type  | Desc                                         |
| ----------- | ----- | -------------------------------------------- |
| resource_id | &[u8] | used to mark the only commodity in the chain |

Event

```
["delete", resource_id]
```

#### buyDToken

```
pub fn buy_dtoken(resource_id: &[u8], n: U128, buyer_account: &Address, payer: &Address) -> bool
```

The buyer calls this method to purchase the goods on the chain.

| Parameter     | Type     | Desc                                         |
| ------------- | -------- | -------------------------------------------- |
| resource_id   | &[u8]    | used to mark the only commodity in the chain |
| n             | U128     | the number of purchases                      |
| buyer_account | &Address | buyer's address                              |
| payer         | &Address | Address to pay for the purchase              |

Event

```
["buyDToken", resource_id, n, buyer_account, payer]
```

#### buyDTokens

```
pub fn buy_dtokens(
    resource_ids: Vec<Vec<u8>>,
    ns: Vec<U128>,
    buyer_account: &Address,
    payer: &Address,
) -> bool
```

Buy more than one dtoken at a time.

| Parameter     | Type         | Desc                                                         |
| ------------- | ------------ | ------------------------------------------------------------ |
| resource_ids  | Vec<Vec<u8>> | array of resource_id which used to mark the only commodity in the chain |
| ns            | Vec<U128>    | array of n which is the number of purchases. the length of resource_ids must be the same with the length of ns. |
| buyer_account | &Address     | buyer's address                                              |
| payer         | &Address     | Address to pay for the purchase                              |

Event

```
["buyDToken", resource_id, n, buyer_account, payer]
```

#### buyDTokenReward

```
pub fn buy_dtoken_reward(
    resource_id:&[u8],
    n:U128,
    buyer_account:&Address,
    payer:&Address,
    unit_price:U128,
) -> bool
```

This method can only be called for items that the fee.count is 0. The buyer can reward the seller with any number of tokens.

| Parameter     | Type     | Desc                                         |
| ------------- | -------- | -------------------------------------------- |
| resource_id   | &[u8]    | used to mark the only commodity in the chain |
| n             | U128     | the number of purchases                      |
| buyer_account | &Address | buyer's address                              |
| payer         | &Address | Address to pay for the purchase              |
| unit_price    | U128     | unit price the buyer is willing to pay       |

Event

```
["buyDToken", resource_id, n, buyer_account, payer, unit_price]
```

### Implementation

[OEP-70 contract](https://github.com/ont-bizsuite/ddxf-contract-suite/tree/master/contracts/marketplace)