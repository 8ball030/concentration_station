<script>
	// @ts-nocheck
	import { ethers } from 'ethers';
	import { Avatar } from '@skeletonlabs/skeleton';
	import { fetchProfile } from '$lib/actions/fetchProfile';
	import { accountStore } from '$lib/stores';
	import { luksoStore } from '$lib/stores';
	import { createJwt, verifyTokenOnServer } from '$lib/actions/sign';
	import { SUPPORTED_LUKSO_NETWORKS } from '$lib/consts';

	let network = {};
	let luksoProfile = {};
	let provider = {};
	let accounts = [];

	accountStore.subscribe((value) => {
		accounts = value;
	});
	luksoStore.subscribe((value) => {
		luksoProfile = value;
	});

	async function connectToLukso() {
		if (!accounts.length || !luksoProfile.value) {
			provider = new ethers.BrowserProvider(window?.lukso);
			accounts = await provider.send('eth_requestAccounts', []);
			accountStore.set(accounts);

			network = await provider.getNetwork();
			luksoProfile = fetchProfile(network?.name || 'LUKSO Testnet', accounts[0]);
			luksoStore.set(luksoProfile);

			const signer = await provider.getSigner();
			const token = await createJwt(
				accounts[0],
				SUPPORTED_LUKSO_NETWORKS[1].chainId,
				'By logging in, you confirm the terms and conditions',
				signer
			);

			if (token) {
				const verify = await verifyTokenOnServer(token.jwt);
			}
		}
	}

	function disconnect() {
		accounts = [];
		accountStore.set(accounts);
	}
</script>

<button
	class="m-2 btn variant-ghost-primary font-bold py-2 px-4 rounded"
	on:click={accounts[0] ? disconnect : connectToLukso}
>
	{accounts[0] ? 'Disconnect' : 'Connect with Lukso'}
</button>
{#if accounts[0]}
	<Avatar
		src={luksoProfile?.value?.LSP3Profile?.profileImage}
		width="w-20"
		rounded="rounded-full"
	/>
{/if}
