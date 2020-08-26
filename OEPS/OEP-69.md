```
  OEP: X
  Title: Streaming Payment Standard
  Author: laizy <laizy@126.com>
  Type: Draft
  Status: XXX
  Created: 2020-04-16
```

## Abstract

This standard allows for the implementation of a standard API for streaming payment within smart contracts.

## Motivation

A standard interface which allows continuous token payment during a time range on the Ontology blockchain.

## Specification

### Structs
the Stream struct is defined as follows:

```go
type Stream struct {
  From      Address  // the payer
  To        Address  // the receiver
  Amount    uint128  // the total money to be streamed 
  Token     Address  // the token address to be streamed
  StartTime uint128  // the unix timestamp for when the stream starts
  StopTime  uint128  // the unix timestamp for when the stream stops
}
```

### Basic Methods

#### createStream
```go
func createStream(from, to Address, amount uint128, token Address, 
  startTime, stopTime uint128) (streamId uint128)
```

Create a new stream:
1. check witness of `from`;
2. check `to != zero && to != from && to != currentContractAddress`;
3. check `CurrentBlockTime <= startTime < stopTime`;
4. transfer token from `from` to this contract.

#### balanceOf

```go
func balanceOf(streamId uint128, addr Address) (balance uint128)
```
Returns the current balance of the `addr` account.

#### getStream

```go
func getStream(uint128 streamId) (
    from, to Address, amount uint128,
    token Address, startTime, stopTime uint128,
    uint128 remainingBalance, uint128 ratePerSecond
)
```

Returns the current active stream infomation.

#### withdrawFromStream

```go
func withdrawFromStream(streamId uint128) returns (uint128);
```

Transfer the streamed token to `To` address, can be called by `To` or `Proxy`, return amount transfered 

#### cancelStream

```go
func cancelStream(streamId uint128) (bool);
```

Cancel the stream, can be called by `From` or `To` address.

### Optional Methods

#### setProxy

```go
func setProxy(addr Address)
```

Set the proxy, which can be used to call the `withdrawFromStream`. this function should be called by contract Admin.

### Events

#### createStream

```
event createStream(streamId uint128, from, to Address, amount uint128,
  token Address, startTime, stopTime uint128);
```

Triggered when a stream is created.

#### withdrawFromStream

```
event withdrawFromStream(streamId uint128, to Address, amount uint128);
```
Triggered when a withdrawFromStream method is called successfully.

#### cancelStream

```
event cancelStream(streamId uint128, from, to Address, 
     fromBalance, toBalance uint128);
```

Triggered when a cancelStream method is called successfully.

### Implementation

