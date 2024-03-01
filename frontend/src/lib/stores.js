import { writable } from "svelte/store";
import {APP_MODE} from './consts'
import {CHAIN_MODE} from './consts'

export const state = writable([0]);
export const likedState = writable(new Set());

export const currentCoinIndex = writable(0);
export const transactionLink = writable("https://etherscan.io/tx/0x20d0fda3b4bfbac76ed7d9fe9f6b669b50ad3e94d6a1bacc047584afe9f7ef53");
export const mode = writable(APP_MODE.NORMAL)
export const chain = writable(CHAIN_MODE.MAINNET)