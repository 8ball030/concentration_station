export const APP_MODE = {
    NORMAL: 'Manual',
    AGENT: 'Augmented',
    DEGEN: 'Altra Degen'
}

export const INTENTION_DIRECTIONS = {
    DISLIKE: 'LEFT',
    LIKE: 'RIGHT'
}
export const MOVE_DIRECTION = {
    LEFT: -400,
    RIGHT: 400
}
export const CHAIN_MODE = {
    MAINNET: 1,
    MATIC: 137,
    CELO: 42220,
    ARBITRUM: 42161,
    BASE: 8453
}

export const CHAIN_NAME = {
    1: 'Ethereum',
    137: 'Matic',
    42220: 'Celo',
    42161: 'Arbitrum',
    8453: 'Base'
}

export const BASE_URL = 'http://192.168.222.31:5553'
export const SOCKET_URL = 'http://192.168.222.31:5554'
export const DEFAULT_CHAIN = CHAIN_MODE.ARBITRUM