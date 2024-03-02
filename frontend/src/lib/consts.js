export const APP_MODE = {
    NORMAL: 'normal',
    AGENT: 'agent',
    DEGEN: 'degen'
}

export const BASE_URL = 'http://192.168.222.31:5555'
export const SOCKET_URL = 'http://192.168.222.31:5556'
export const DEFAULT_CHAIN = 1;

export const INTENTION_DIRECTIONS = {
    DISLIKE: 'LEFT',
    LIKE: 'RIGHT'
}
export const MOVE_DIRECTION = {
    LEFT: -400,
    RIGHT: 400
}
export const CHAINS = {
    MAINNET: 1,
    GNOSIS: 100,
    POLYGON: 137
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