// @ts-nocheck
import base64url from 'base64url';
import { SiweMessage } from 'siwe';

// TODO: update url
const VERIFY_URL = 'http://127.0.0.1:5000/verify'

/**
 * Convert the SiweMessage to a JWT
 * @param message
 * @param signature
 * @returns jwt token string
 */
export async function createJwt(
    account,
    chainId,
    statement,
    signer
) {
    const domain = window?.location.host;
    const message_ = new SiweMessage({
        domain,
        uri: window?.location.origin,
        statement,
        address: account,
        issuedAt: new Date().toISOString(),
        version: '1',
        chainId: String(chainId),
        resources: [
            `did:account:${account}`,
            `did:web:${domain}`,
        ],
    });

    const message = message_.prepareMessage();
    const signature = await signer.signMessage(
        message,
    );
    const header = {
        alg: 'ES256K',
        typ: 'JWT',
    };

    return {
        jwt: [
            Buffer.from(JSON.stringify(header)),
            Buffer.from(JSON.stringify({ message })),
            Buffer.from(signature.slice(2), 'hex'),
        ].map((d) => base64url(d, 'base64'))
            .join('.'),
        message: message_,
        signature,
    };
}


/**
 * Simulate API call using the token as a bearer token
 *
 * @param jwt
 * @returns {
 *   valid: boolean // if it was valid
 * }
 */
export async function verifyTokenOnServer(jwt) {
    return await fetch(VERIFY_URL, {
        headers: {
            Authorization: `Bearer ${jwt}`,
        },
    })
        .then((response) => {
            console.log('res', response)
            return response.json()
        }).catch((e) => {
            console.log(e)
        })
}
