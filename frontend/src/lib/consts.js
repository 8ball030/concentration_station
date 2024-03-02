// @ts-nocheck
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

export const SUPPORTED_LUKSO_NETWORKS = [
  {
    "name": "LUKSO Mainnet",
    "chainId": "42",
    "rpcUrl": "https://rpc.lukso.gateway.fm",
    "ipfsGateway": "https://api.universalprofile.cloud/ipfs",
    "token": "LYX"
  },
  {
    "name": "LUKSO Testnet",
    "chainId": "4201",
    "rpcUrl": "https://rpc.testnet.lukso.gateway.fm",
    "ipfsGateway": "https://api.universalprofile.cloud/ipfs",
    "token": "LYXt"
  }
]
export const CHAIN_NAME = {
  1: 'Ethereum',
  137: 'Matic',
  42220: 'Celo',
  42161: 'Arbitrum',
  8453: 'Base'
}

export const CHAIN_ID_TO_LEDGER_ID = {
    1: "ethereum",
    137: "matic",
    42220: "celo",
    42161: "arbitrum",
    8453: "base"
}

export const BASE_URL = 'http://192.168.222.31:5553'
export const SOCKET_URL = 'http://192.168.222.31:5554'
export const DEFAULT_CHAIN = CHAIN_MODE.ARBITRUM

export const STATUS_MSGS = {
  TX_SUCCESS: {
    message: `🤞🏼 Transaction submitted 🤞🏼`,
    timeout: 1000,
    max: 1
  },
  AGENT_SUCCESS: {
    message: 'Successfully connected to the agent!',
    timeout: 3000,
    background: 'variant-ghost-success',
    max: 1
  },
  AGENT_FAIL: {
    message: 'Disconnected from the agent!',
    timeout: 3000,
    background: 'variant-ghost-error',
    max: 1
  },
  AGENT_DATA: (row) => ({
    message: '🔮 ' + row + ' 🔮',
    timeout: 2500,
    background: 'variant-ghost-info',
    classes: 'info-toast',
    position: 't',
    max: 1
  }),
  API_ERROR: (endpoint, err) => ({
    message: ` =( ${err} ${endpoint}`,
    background: 'variant-filled-error',
    classes: 'error-toast'
  })
}