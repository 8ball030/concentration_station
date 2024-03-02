// @ts-nocheck
import base64url from 'base64url';
import { SiweMessage } from 'siwe';
import {
    getAddress,
    getContract,
    hashMessage,
    recoverMessageAddress,
    toHex,
} from 'viem';
import { signMessage } from 'wagmi/actions';

import { config } from '../wagmi';

/**
 * Convert the SiweMessage to a JWT
 * Unfortunately the SIWE standard only signs the message part instead of
 * allowing for the header to be included, but an improper header will also
 * cause the signature not to validate so that should not be a problem.
 *
 * @param message
 * @param signature
 * @returns jwt token string
 */
export async function createJwt(
    account,
    chainId,
    statement,
) {
    const message_ = new SiweMessage({
        domain: import.meta.env.VITE_APP_DOMAIN,
        uri: `https://localhost:5173/`,
        statement,
        address: account,
        issuedAt: new Date().toISOString(),
        version: '1',
        expirationTime: new Date(Date.now() + 10_000).toISOString(),
        chainId,
        resources: [
            `did:account:${account}`,
            `did:web:localhost:5173`,
        ],
    });
    const message = message_.prepareMessage();
    const signature = await signMessage({
        message,
    });
    const header = {
        alg: 'ES256K',
        typ: 'JWT',
    };
    return {
        jwt: [
            Buffer.from(JSON.stringify(header)),
            Buffer.from(message),
            Buffer.from(signature.slice(2), 'hex'),
        ]
            .map((d) => base64url(d, 'base64'))
            .join('.'),
        message: message_,
        signature,
    };
}

/**
 * Exchange a client side JWT to a server side JWT
 *
 * @param clientJwt
 * @returns {
 *  message: SiweMessage // new server side message
 *  originalMessage: SiweMessage // original client side message
 *  jwt: string // new server side JWT
 *  valid: boolean // is the client side JWT was valid (always true)
 *  account: `0x${string}` // user account address
 *  error?: string // error message
 *  error_description?: string // error description
 * }
 */
export async function exchangeToken(clientJwt) {
    return await fetch('/exchange', {
        headers: {
            Authorization: `Bearer ${clientJwt}`,
        },
    })
        .then((response) => response.json())
        .then(({ message, originalMessage, account, ...rest }) => {
            return {
                message: new SiweMessage(message),
                originalMessage: new SiweMessage(originalMessage),
                account: getAddress(account),
                ...rest,
            };
        });
}

/**
 * Simulate API call using the token as a bearer token
 *
 * @param jwt
 * @returns {
 *   message?: SiweMessage // the decoded and reencoded siwe message
 *   valid: boolean // if it was valid
 *   account?: `0x${string}` // the account address
 *   error?: string // error message
 *   error_description?: string // error description
 * }
 */
export async function verifyTokenOnServer(jwt) {
    return await fetch('/verify', {
        headers: {
            Authorization: `Bearer ${jwt}`,
        },
    })
        .then((response) => response.json())
        .then(({ message, account, ...rest }) => ({
            message: new SiweMessage(message),
            account: getAddress(account),
            ...rest,
        }));
}
