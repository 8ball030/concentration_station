// @ts-nocheck
import { browser } from '$app/environment';

export class LikedCoins {
    likedCoinsList = new Set()

	constructor() {
		if (!browser) {
			return;
		}
		
        if (localStorage.getItem('likedCoinsList') !== null) {
            this.likedCoinsList = new Set(JSON.parse(localStorage.getItem('likedCoinsList')));
        }
	}

	set value(v) {
		this.likedState = v;
	}

	get value() {
		return this.likedState;
	}

	add(coin) {
		this.likedCoinsList = this.likedCoinsList.add(coin);

		if (browser) {
			localStorage.setItem('likedCoinsList', JSON.stringify(Array.from(this.likedCoinsList)));
		}
	}

	remove(coin) {
		this.likedCoinsList.delete(coin);

		this.likedCoinsList = this.likedCoinsList;
		if (browser) {
			localStorage.setItem('likedCoinsList', JSON.stringify(Array.from(this.likedCoinsList)));
		}
	}
}
