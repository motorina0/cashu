After requesting a mint (see #3 [TODO: Link]) and paying the invoice that was returned by the mint, a wallet proceeds with requesting tokens from the mint in return for paying the invoice. 

For that, a wallet sends a `POST /mint&payment_hash=<hash>` request with a JSON body to the mint. The body **MUST** include `BlindedMessages` that are worth a maximum of `<amount_sat>` [TODO: Refer to BlindedMessages]. If successful (i.e. the invoice has been previously paid and the `BlindedMessages` are valid), the mint responds with `Promises` [TODO: Link Promises].

## Example

Request of `Alice`:

```http
POST https://mint.host:3338/mint&payment_hash=67d1d9ea6ada225c115418671b64a
```

With the data being of the form `MintRequest`:

```json
{
	"blinded_messages": 
		[
			BlindedMessage,
			...
		]
}
```


With curl:

```bash
curl -X POST https://mint.host:3338/mint&payment_hash=67d1d9ea6ada225c115418671b64a -d \
{
	"blinded_messages": 
	[
		{
		"amount": 2, 
		"B_": "02634a2c2b34bec9e8a4aba4361f6bf202d7fa2365379b0840afe249a7a9d71239"
		},
		{
		"amount": 8, 
		"B_": "03b54ab451b15005f2c64d38fc512fca695914c8fd5094ee044e5724ad41fda247"
		
		}
	]
}
```

Response of `Bob`: 

If the invoice was successfully paid, `Bob` responds with a `PostMintResponse` which is essentially a list of `BlindedSignature`'s [TODO: Link PostMintResponse]

```json
{
"promises":
	[
		{
		"id": "DSAl9nvvyfva",
		"amount": 2,
		"C_": "03e61daa438fc7bcc53f6920ec6c8c357c24094fb04c1fc60e2606df4910b21ffb"
		},
		{
		"id": "DSAl9nvvyfva",
		"amount": 8,
		"C_": "03fd4ce5a16b65576145949e6f99f445f8249fee17c606b688b504a849cdc452de"
		},
	]
}

```

If the invoice was not paid yet, `Bob` responds with an error. In that case, `Alice` **CAN** repeat the same response until the Lightning invoice is settled.

## Unblinding signatures

Upon receiving the `PostMintResponse` with the list of `BlindedSignature`'s from the mint `Bob`, a wallet `Alice` **MUST** then unblind the `BlindedSignature`'s from `Bob` (see #0 Notation [TODO: Link to unblinding]) to generate a list of `Proof`'s. A `Proof` is effectively an ecash `Token` and can later be used to redeem the token. The wallet **MUST** store the `Proof` in its database.

A list multiple `Proof`'s is called `Proofs` and has the form:

```json
{
"proofs" : 
	[
		{
		"id": "DSAl9nvvyfva",
		"amount": 2,
		"secret": "S+tDfc1Lfsrb06zaRdVTed6Izg",
		"C": "0242b0fb43804d8ba9a64ceef249ad7a60f42c15fe6d4907238b05e857527832a3"
		},
		{
		...
		}
	]
}
```